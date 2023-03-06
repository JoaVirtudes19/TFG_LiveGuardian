from django.shortcuts import render
from web.camera import camCache
from django.http import StreamingHttpResponse, HttpResponseRedirect
from web.models import Cam,Detection,Detector,User,Group
from web.forms import CrearCamara,CrearDetector, CrearUsuario, CrearGrupo
from django import forms
from django.forms import ModelForm
import cv2
from datetime import datetime
import base64
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import numpy as np
from io import BytesIO
# Create your views here.


def inicio(request):
    cameras = Cam.objects.all()
    return render(request,'inicio.html',{'titulo':"Dashboard",'cameras':cameras}) ### Vista provisional

def telegram(request):
    titulo = "Telegram"
    usuarios = User.objects.all().order_by('-id')
    grupos = Group.objects.all().order_by('-id')
    return render(request,'telegram.html',{'titulo':titulo,'users':usuarios,'groups':grupos}) ### Vista provisional

def detecciones(request):
    titulo = "Detecciones"
    detecciones = Detection.objects.all().order_by('-id')
    return render(request,'detecciones.html',{'titulo':titulo,'detections':detecciones}) ### Vista provisional

def detectores(request):
    titulo = "Detectores"
    detectores = Detector.objects.all().order_by('-id')
    return render(request,'detectores.html',{'titulo':titulo,'detectors':detectores}) ### Vista provisional

def ayuda(request):
    return render(request,'ayuda.html',{'titulo':"Ayuda"}) ### Vista provisional

def configuracion(request):
    titulo = "Configuración"
    return render(request,'configuracion.html',{'titulo':titulo}) ### Vista provisional

def crearCamara(request):
    titulo = "Crear cámara"
    if request.method == 'POST':
        form = CrearCamara(request.POST)
        if form.is_valid():
            camara = form.save()
            camCache.add(camara)
            return HttpResponseRedirect('/')
        else:
            return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearCamara/'}) ### Vista provisional

    else:
        form = CrearCamara()
        return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearCamara/'}) ### Vista provisional


def crearDetector(request):
    titulo = "Crear detector"
    if request.method == 'POST':
        form = CrearDetector(request.POST, request.FILES)
        if form.is_valid():
            detector = form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearDetector/'}) ### Vista provisional

    else:
        form = CrearDetector()
        return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearDetector/'}) ### Vista provisional
    

def crearUsuario(request):
    titulo = "Crear usuario"
    if request.method == 'POST':
        form = CrearUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            return HttpResponseRedirect('/Telegram')
        else:
            return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearUsuario/'}) ### Vista provisional

    else:
        form = CrearUsuario()
        return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearUsuario/'}) ### Vista provisional
    

def crearGrupo(request):
    titulo = "Crear grupo"
    if request.method == 'POST':
        form = CrearGrupo(request.POST)
        if form.is_valid():
            grupo = form.save()
            return HttpResponseRedirect('/Telegram')
        else:
            return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearGrupo/'}) ### Vista provisional

    else:
        form = CrearGrupo()
        return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearGrupo/'}) ### Vista provisional


def deleteCam(request,id_cam):
    try:
        Cam.objects.get(id=id_cam).delete() ### Intentamos borrar la cámara
        camCache.delete(id_cam)
        return HttpResponseRedirect('/')
    except:
        ### Añadir template para error
         return HttpResponseRedirect('/')

def deleteDetection(request,id_detection):
        Detection.objects.get(id=id_detection).delete()
        return HttpResponseRedirect('/Detecciones')

def deleteDetector(request,id_detector):
        Detector.objects.get(id=id_detector).delete()
        return HttpResponseRedirect('/Detectores')

def deleteUser(request,id_user):
        User.objects.get(id=id_user).delete()
        return HttpResponseRedirect('/Telegram')

def deleteGroup(request,id_group):
        Group.objects.get(id=id_group).delete()
        return HttpResponseRedirect('/Telegram')
    
def detailCam(request,id_cam):
    ### Este Bloque de código se puede separar en una función aparte
    if request.method == 'POST':
        cam = Cam.objects.all().get(id=id_cam)
        frame = camCache.get(id_cam).frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) ### Posible eliminación
        img_pil = Image.fromarray(frame)
        buffer = BytesIO()
        img_pil.save(buffer, format='JPEG')
        image_file = SimpleUploadedFile('detection-cam-'+str(id_cam) + '.jpg', buffer.getvalue())
        fecha = datetime.now()
        Detection.objects.create(cam=cam,date=fecha,img=image_file,items='',pred='',detector=None)

    titulo = "Vista detallada"
    cam = Cam.objects.all().get(id=id_cam)
    return render(request,'detail.html',{'titulo':titulo,'cam':cam}) ### Vista provisional


def detailDetection(request,id_detection):
    titulo = "Vista detallada"
    detection = Detection.objects.all().get(id=id_detection)
    return render(request,'detailDetection.html',{'titulo':titulo,'detection':detection}) ### Vista provisional

### Función temporal para probar las cámaras
def video(request,id_cam):
    CAMERA_INPUT = camCache.get(id_cam)
    try:
        return StreamingHttpResponse(gen(CAMERA_INPUT),content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        render(request,'inicio.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
