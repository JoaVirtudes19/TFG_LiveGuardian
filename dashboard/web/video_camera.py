import threading
import time
from datetime import datetime
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from icevision.all import *
from icevision.models import *

from web.config import global_config
from web.models import Detection
from web.telegram import telegram_component


class VideoCamera(object):
    def __init__(self, instance):
        self.instance = instance
        self.live = True
        self.fps = 0
        self.recent = []
        self.frames_to_detector = global_config.get_config('framesToDetector')
        self.history_size_to_detect = global_config.get_config('historySizeToDetect')
        self.video = cv2.VideoCapture(instance.url)
        (self.grabbed, self.frame) = self.video.read()
        self.first_frame = cv2.imread('static/error.jpeg')

        self.history = [0] * global_config.get_config('historySize')
        self.retry = 0
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.start()

    def __del__(self):
        print("-----------------EVENT-----------------")
        print("Camera: " + str(self.instance.name) + " has been deleted.")
        self.video.release()

    def set_error_frame(self):
        self.frame = self.first_frame.copy()
        alto, ancho, canales = self.frame.shape
        texto = '{:04d}s'.format(self.retry)
        posicion = (int(ancho / 2) - 250, int(alto - 50))
        cv2.putText(self.frame, texto, posicion, cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 255, 255), 20)

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    ### Streaming
    def update(self):
        if self.instance.detector is not None:
            self.detection()
        else:
            self.noDetection()

    def noDetection(self):
        while self.live:
            (self.grabbed, frame) = self.video.read()
            if self.grabbed:
                self.retry = 0
                self.frame = frame
            else:
                self.retry += 1
                self.set_error_frame()
                self.video = cv2.VideoCapture(self.instance.url)
                time.sleep(1)

    def make_detection(self, frame, labels, scores):
        print("DETECTION SAVED")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(frame)
        buffer = BytesIO()
        img_pil.save(buffer, format='JPEG')
        image_file = SimpleUploadedFile('detection-cam-' + str(self.instance.id) + '.jpg', buffer.getvalue())
        fecha = datetime.now()
        Detection.objects.create(cam=self.instance.name, date=fecha, img=image_file, items=str(labels),
                                 pred=str(scores),
                                 detector=self.instance.detector.name)
        telegram_component.send_detection(self.instance, labels, scores, img_pil)

    def detection(self):
        checkpoint_and_model = model_from_checkpoint(self.instance.detector.model.path)
        model_type = checkpoint_and_model["model_type"]
        class_map = checkpoint_and_model["class_map"]
        img_size = checkpoint_and_model["img_size"]
        model = checkpoint_and_model["model"]

        valid_transforms = tfms.A.Adapter([*tfms.A.resize_and_pad(img_size), tfms.A.Normalize()])

        while self.live:
            (self.grabbed, frame) = self.video.read()

            if not self.grabbed:
                self.retry += 1
                self.set_error_frame()
                self.video = cv2.VideoCapture(self.instance.url)
                time.sleep(1)
                continue
            self.retry = 0
            if self.fps % self.frames_to_detector == 0:
                self.recent_bboxes = []
                self.recent_labels = []

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_conv = Image.fromarray(img)

                pred_dict = model_type.end2end_detect(img_conv, valid_transforms, model, class_map=class_map,
                                                      detection_threshold=0.5, return_img=False)

                if pred_dict['detection']['label_ids']:
                    self.recent_bboxes = pred_dict['detection']['bboxes']
                    self.recent_labels = pred_dict['detection']['labels']


            for i in range(len(self.recent_bboxes)):
                bbox = self.recent_bboxes[i]
                label = self.recent_labels[i]
                cv2.rectangle(frame, (bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymax), (255, 0, 0), 2)
                cv2.putText(frame, label, (bbox.xmin, bbox.ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

            self.frame = frame

            if pred_dict['detection']['label_ids']:
                self.history = self.history[1:] + [1]
                if sum(self.history) == self.history_size_to_detect and self.fps % self.frames_to_detector == 0:
                        self.make_detection(frame, pred_dict['detection']['labels'], pred_dict['detection']['scores'])
            else:
                self.history = self.history[1:] + [0]

            self.fps += 1
