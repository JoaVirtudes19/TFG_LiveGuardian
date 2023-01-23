from django.shortcuts import render
from web.camera import camCache
from django.http import StreamingHttpResponse
from web.models import Cam

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
