from django.db import models
from django.dispatch import receiver
import os
# Create your models here.


class Detector(models.Model):
    name = models.CharField(max_length=255,unique=True)
    model = models.FileField(upload_to='models')
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