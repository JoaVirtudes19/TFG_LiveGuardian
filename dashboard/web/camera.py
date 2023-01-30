from web.models import Cam
import cv2
import threading
from icevision.all import *
from icevision.models import *
from PIL import Image
import numpy as np

class VideoCamera(object):
    def __init__(self,instance):
        self.instance  = instance
        self.video = cv2.VideoCapture(instance.url)
        (self.grabbed,self.frame) = self.video.read()
        threading.Thread(target=self.update,args=()).start() ### Hilos para mantener la camara encendida

    def __del__(self):
        ### Tenemos que matar el hilo primero
        print("Camera: "+str(self.instance.name)+ " has been deleted.")
        self.video.release()

    def get_frame(self):
        image = self.frame
        _,jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    ### Streaming
    def update(self):
        if self.instance.detector != None:
            self.detection()
        else:
            self.noDetection()

    def noDetection(self):
        while True:
            (self.grabbed, frame) = self.video.read()
            self.frame = frame

    def detection(self):
        checkpoint_and_model = model_from_checkpoint(self.instance.detector.model.path)
        model_type = checkpoint_and_model["model_type"]
        backbone = checkpoint_and_model["backbone"]
        class_map = checkpoint_and_model["class_map"]
        img_size = checkpoint_and_model["img_size"]
        model_type, backbone, class_map, img_size
        model = checkpoint_and_model["model"]
        img_size = checkpoint_and_model["img_size"]
        valid_tfms = tfms.A.Adapter([*tfms.A.resize_and_pad(img_size), tfms.A.Normalize()])
        while True:
            (self.grabbed, frame) = self.video.read()
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_conv = Image.fromarray(img)
            pred_dict  = model_type.end2end_detect(img_conv, valid_tfms, model, class_map=class_map, detection_threshold=0.5)
            nimg = np.array(pred_dict['img'])
            ocvim = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
            self.frame = ocvim


class CamCache():
    def __init__(self) -> None:
        self.cache = dict()
        ### Start cache
        for camInstance in Cam.objects.all():
            print(str(camInstance.id))
            self.add(camInstance)
    

    def add(self,instance):
        self.cache[instance.id] = VideoCamera(instance)
        print(self.cache)



    def delete(self,instance):
        self.cache.pop(instance.id,None)

    def get(self,id):
        return self.cache[id]


camCache = CamCache()
