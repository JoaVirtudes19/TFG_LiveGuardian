from web.models import Cam
import cv2
import threading
from icevision.all import *
from icevision.models import *
from PIL import Image
import numpy as np
import time
from io import BytesIO
from web.models import Detection
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import telebot
from telebot import types

TOKEN = "5282233910:AAG_mddkn8zdw_Iip-n1zQX_gSURiBLomC0" ###Este toquen se saca desde la configuración
class VideoCamera(object):
    def __init__(self,instance):
        self.instance  = instance
        self.live = True
        self.fps = 0
        self.recent = []
        self.video = cv2.VideoCapture(instance.url)
        (self.grabbed,self.frame) = self.video.read()
        self.thread = threading.Thread(target=self.update,args=())
        self.thread.start()
        self.firstFrame = self.frame
        self.history = [0] * 40

    def __del__(self):
        ### Crear un logger
        print("-----------------EVENT-----------------")
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
            if self.grabbed:
                self.frame = frame
            else:
                self.frame = self.firstFrame
                self.video = cv2.VideoCapture(self.instance.url)

    def make_detection(self,frame,labels,scores):
        print("DETECCIÓN GUARDADA")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ### Posible eliminación
        img_pil = Image.fromarray(frame)
        buffer = BytesIO()
        img_pil.save(buffer, format='JPEG')
        image_file = SimpleUploadedFile('detection-cam-'+str(self.instance.id) + '.jpg', buffer.getvalue())
        fecha = datetime.now()
        Detection.objects.create(cam=self.instance,date=fecha,img=image_file,items=str(labels),pred=str(scores),detector=self.instance.detector)
        ### Enviar mensaje de telegram
        bot = telebot.TeleBot(TOKEN)
        for grupo in self.instance.groups.all():
            for user in grupo.user_set.all():
                bot.send_message(user.chat_id,"📸Detección:\nCámara: {}\nFecha: {}\nItems: {}\n%: {}".format(self.instance.name,datetime.now(),labels,scores))
                bot.send_photo(user.chat_id, img_pil)




    def detection(self):
        checkpoint_and_model = model_from_checkpoint(self.instance.detector.model.path)
        model_type = checkpoint_and_model["model_type"]
        backbone = checkpoint_and_model["backbone"]
        class_map = checkpoint_and_model["class_map"]
        img_size = checkpoint_and_model["img_size"]
        model_type, backbone, class_map, img_size
        model = checkpoint_and_model["model"]
        valid_tfms = tfms.A.Adapter([*tfms.A.resize_and_pad(img_size), tfms.A.Normalize()])
        while self.live:
            (self.grabbed, frame) = self.video.read()
            if not self.grabbed:
                self.frame = self.firstFrame
                self.video = cv2.VideoCapture(self.instance.url)
                continue
            if self.fps % 3 == 0: ### Futuro parámetro ajustable desde la configuración en la interfaz
                self.recent = []
                self.labels = []
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ### Posible eliminación
                img_conv = Image.fromarray(img)
                pred_dict  = model_type.end2end_detect(img_conv, valid_tfms, model, class_map=class_map, detection_threshold=0.5,return_img=False)
                ### Cambiar el detection_threshold como un parametro de entrada al crear el detector
                if pred_dict['detection']['label_ids']:
                    self.recent = pred_dict['detection']['bboxes']
                    self.labels = pred_dict['detection']['labels']
                self.fps +=1          
            else:
                for i in range(len(self.recent)):
                    box = self.recent[i]
                    label = self.labels[i]
                    cv2.rectangle(frame, (box.xmin, box.ymin), (box.xmax, box.ymax), (255,0,0), 2)
                    cv2.putText(frame, label, (box.xmin, box.ymin-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
                self.frame = frame
                
                if pred_dict['detection']['label_ids']:
                    self.history = self.history[1:] + [1]
                    if sum(self.history) == 10:
                        self.make_detection(frame,pred_dict['detection']['labels'],pred_dict['detection']['scores'])
                else:
                    self.history = self.history[1:] + [0]
                self.fps +=1  

            


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



    def delete(self,id):
        cam = self.cache.pop(id,None)
        cam.live = False
        del(cam)

    def get(self,id):
        return self.cache[id]


camCache = CamCache()
