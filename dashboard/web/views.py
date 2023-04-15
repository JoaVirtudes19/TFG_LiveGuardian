from datetime import datetime
from io import BytesIO

import cv2
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render

from web.camera import cam_cache
from web.config import global_config
from web.forms import CrearCamara, CrearDetector, CrearUsuario, CrearGrupo
from web.models import Cam, Detection, Detector, User, Group


# Create your views here.


def inicio(request):
    cameras = Cam.objects.all()
    return render(request, 'inicio.html', {'titulo': "LiveGuardian", 'cameras': cameras})  ### Vista provisional


def telegram(request):
    titulo = "LG/Telegram"
    usuarios = User.objects.all().order_by('-id')
    grupos = Group.objects.all().order_by('-id')
    return render(request, 'telegram.html',
                  {'titulo': titulo, 'users': usuarios, 'groups': grupos})  ### Vista provisional


def detecciones(request):
    titulo = "LG/Detecciones"
    detecciones = Detection.objects.all().order_by('-id')
    return render(request, 'detecciones.html', {'titulo': titulo, 'detections': detecciones})  ### Vista provisional


def detectores(request):
    titulo = "LG/Detectores"
    detectores = Detector.objects.all().order_by('-id')
    return render(request, 'detectores.html', {'titulo': titulo, 'detectors': detectores})  ### Vista provisional


def ayuda(request):
    return render(request, 'ayuda.html', {'titulo': "LG/Ayuda"})  ### Vista provisional


def configuracion(request):
    titulo = "LG/Configuración"
    framesToDetector = global_config.get_config('framesToDetector')
    historySize = global_config.get_config('historySize')
    historySizeToDetect = global_config.get_config('historySizeToDetect')
    token = global_config.get_config('token')
    if request.method == 'POST':
        global_config.set_config(request.POST)
        for instance in Cam.objects.all():
            ### Update cams config
            cam = cam_cache.get(instance.id)
            cam.history = [0] * global_config.get_config('historySize')
            cam.frames_to_detector = global_config.get_config('framesToDetector')
            cam.history_size_to_detect = global_config.get_config('historySizeToDetect')
            cam.token = global_config.get_config('token')
        return HttpResponseRedirect('/')
    return render(request, 'configuracion.html',
                  {'titulo': titulo, 'framesToDetector': framesToDetector, 'historySize': historySize,
                   'historySizeToDetect': historySizeToDetect, 'token': token})  ### Vista provisional


def crear_camara(request):
    titulo = "LG/Crear cámara"
    if request.method == 'POST':
        form = CrearCamara(request.POST)
        if form.is_valid():
            camara = form.save()
            cam_cache.add(camara)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'formulario.html',
                          {'titulo': titulo, 'form': form, 'ruta': '/CrearCamara/'})  ### Vista provisional

    else:
        form = CrearCamara()
        return render(request, 'formulario.html',
                      {'titulo': titulo, 'form': form, 'ruta': '/CrearCamara/'})  ### Vista provisional


def crear_detector(request):
    titulo = "LG/Crear detector"
    if request.method == 'POST':
        form = CrearDetector(request.POST, request.FILES)
        if form.is_valid():
            detector = form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'formulario.html',
                          {'titulo': titulo, 'form': form, 'ruta': '/CrearDetector/'})  ### Vista provisional

    else:
        form = CrearDetector()
        return render(request, 'formulario.html',
                      {'titulo': titulo, 'form': form, 'ruta': '/CrearDetector/'})  ### Vista provisional


def crear_usuario(request):
    titulo = "LG/Crear usuario"
    if request.method == 'POST':
        form = CrearUsuario(request.POST)
        if form.is_valid():
            usuario = form.save()
            return HttpResponseRedirect('/Telegram')
        else:
            return render(request, 'formulario.html',
                          {'titulo': titulo, 'form': form, 'ruta': '/CrearUsuario/'})  ### Vista provisional

    else:
        form = CrearUsuario()
        return render(request, 'formulario.html',
                      {'titulo': titulo, 'form': form, 'ruta': '/CrearUsuario/'})  ### Vista provisional


def crear_grupo(request):
    titulo = "LG/Crear grupo"
    if request.method == 'POST':
        form = CrearGrupo(request.POST)
        if form.is_valid():
            grupo = form.save()
            return HttpResponseRedirect('/Telegram')
        else:
            return render(request, 'formulario.html',
                          {'titulo': titulo, 'form': form, 'ruta': '/CrearGrupo/'})  ### Vista provisional

    else:
        form = CrearGrupo()
        return render(request, 'formulario.html',
                      {'titulo': titulo, 'form': form, 'ruta': '/CrearGrupo/'})  ### Vista provisional


def eliminar_camara(request, id_cam):
    try:
        Cam.objects.get(id=id_cam).delete()  ### Intentamos borrar la cámara
        cam_cache.delete(id_cam)
        return HttpResponseRedirect('/')
    except:
        ### Añadir template para error
        return HttpResponseRedirect('/')


def eliminar_deteccion(request, id_detection):
    Detection.objects.get(id=id_detection).delete()
    return HttpResponseRedirect('/Detecciones')


def eliminar_detector(request, id_detector):
    Detector.objects.get(id=id_detector).delete()
    return HttpResponseRedirect('/Detectores')


def eliminar_usuario(request, id_user):
    User.objects.get(id=id_user).delete()
    return HttpResponseRedirect('/Telegram')


def eliminar_grupo(request, id_group):
    Group.objects.get(id=id_group).delete()
    return HttpResponseRedirect('/Telegram')


def detalles_camara(request, id_cam):
    ### Este Bloque de código se puede separar en una función aparte
    if request.method == 'POST':
        cam = Cam.objects.all().get(id=id_cam)
        frame = cam_cache.get(id_cam).frame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  ### Posible eliminación
        img_pil = Image.fromarray(frame)
        buffer = BytesIO()
        img_pil.save(buffer, format='JPEG')
        image_file = SimpleUploadedFile('detection-cam-' + str(id_cam) + '.jpg', buffer.getvalue())
        fecha = datetime.now()
        Detection.objects.create(cam=cam, date=fecha, img=image_file, items='', pred='', detector=None)

    titulo = "LG/Vista detallada"
    cam = Cam.objects.all().get(id=id_cam)
    return render(request, 'detail.html', {'titulo': titulo, 'cam': cam})  ### Vista provisional


def detalles_deteccion(request, id_detection):
    titulo = "LG/Vista detallada"
    detection = Detection.objects.all().get(id=id_detection)
    return render(request, 'detailDetection.html', {'titulo': titulo, 'detection': detection})  ### Vista provisional


### Función temporal para probar las cámaras
def video(request, id_cam):
    CAMERA_INPUT = cam_cache.get(id_cam)
    try:
        return StreamingHttpResponse(gen(CAMERA_INPUT), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        render(request, 'inicio.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
