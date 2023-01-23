from web.models import Cam
import cv2
import threading

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
        pass


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
