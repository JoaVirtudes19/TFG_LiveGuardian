from django.shortcuts import render
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
