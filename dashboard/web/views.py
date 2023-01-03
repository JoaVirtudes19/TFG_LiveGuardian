from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request,'inicio.html',{'title':"Dashboard"}) ### Vista provisional

def telegram(request):
    return render(request,'telegram.html',{'title':"Telegram"}) ### Vista provisional

def detecciones(request):
    return render(request,'detecciones.html',{'title':"Detecciones"}) ### Vista provisional

def ayuda(request):
    return render(request,'ayuda.html',{'title':"Ayuda"}) ### Vista provisional
