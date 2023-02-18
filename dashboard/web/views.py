from django.shortcuts import render
from web.camera import camCache
from django.http import StreamingHttpResponse, HttpResponseRedirect
from web.models import Cam
from web.forms import CrearCamara,CrearDetector
from django import forms
from django.forms import ModelForm

# Create your views here.



def inicio(request):
    cameras = Cam.objects.all()
    return render(request,'inicio.html',{'title':"Dashboard",'cameras':cameras}) ### Vista provisional

def telegram(request):
    return render(request,'telegram.html',{'title':"Telegram"}) ### Vista provisional

def detecciones(request):
    return render(request,'detecciones.html',{'title':"Detecciones"}) ### Vista provisional

def ayuda(request):
    return render(request,'ayuda.html',{'title':"Ayuda"}) ### Vista provisional

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
        print("POSTSTTTTTTTTTTTTTTTTTT")
        form = CrearDetector(request.POST, request.FILES)
        if form.is_valid():
            print("ES VALIDOOOOOOOOOOOOOOOOOO")
            detector = form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearDetector/'}) ### Vista provisional

    else:
        form = CrearDetector()
        return render(request,'formulario.html',{'titulo':titulo,'form':form,'ruta':'/CrearDetector/'}) ### Vista provisional


def deleteCam(request,id_cam):
    try:
        Cam.objects.get(id=id_cam).delete() ### Intentamos borrar la cámara
        camCache.delete(id_cam)
        return HttpResponseRedirect('/')
    except:
        ### Añadir template para error
         return HttpResponseRedirect('/')


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
