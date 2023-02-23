from django.db import models
from django.dispatch import receiver
import os
# Create your models here.


### TELEGRAM

class Group(models.Model):
    name = models.CharField(max_length=100,unique=True)
    def __str__(self) -> str:
        return str(self.name)


class User(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=100,unique=True)
    group = models.ForeignKey(Group,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self) -> str:
        return str(self.name)


### DETECTOR
class Detector(models.Model):
    name = models.CharField(max_length=255,unique=True)
    model = models.FileField(upload_to='models')
    def __str__(self) -> str:
        return str(self.name)
    

class Detection(models.Model):
    cam = models.ForeignKey("Cam",on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(null=False,blank=False)
    img = models.ImageField(upload_to='detections')
    items = models.CharField(max_length=100,null=True,blank=True)
    pred = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self) -> str:
        if self.cam != None:
            return str(self.cam.name) + ": " + str(self.date)
        else:
            return "NoCam: " + str(self.date)


### CÁMARAS

class Cam(models.Model):
    name = models.CharField(max_length=100,unique=True)
    detector = models.ForeignKey(Detector,on_delete=models.SET_NULL,null=True,blank=True)
    url = models.CharField(max_length=2048)
    groups = models.ManyToManyField(Group,blank=True)
    def __str__(self) -> str:
        return str(self.name)



### Función que elimina el archivo en caso de ser eliminado su objeto
@receiver(models.signals.post_delete, sender=Detector)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    try:
        if instance.model:
            if os.path.isfile(instance.model.path):
                os.remove(instance.model.path)
                print("Archivo "+str(instance.model.name)+" eliminado")
            else:
                print("Archivo "+str(instance.model.name)+" no existe")
    except:
        ### Añadir a un log
        print("Archivo "+str(instance.model.name)+" no ha podido ser eliminado")

### Función que elimina el archivo en caso de ser eliminado su objeto
@receiver(models.signals.post_delete, sender=Detection)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    try:
        if instance.img:
            if os.path.isfile(instance.img.path):
                os.remove(instance.img.path)
                print("Archivo "+str(instance.img.path)+" eliminado")
            else:
                print("Archivo "+str(instance.img.path)+" no existe")
    except:
        ### Añadir a un log
        print("Archivo "+str(instance.img.path)+" no ha podido ser eliminado")




