"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from web.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('Dashboard/', inicio),
    path('Configuracion/', configuracion),
    path('Telegram/', telegram),
    path('Detecciones/', detecciones),
    path('Detectores/', detectores),
    path('Ayuda/', ayuda),
    path('video/<int:id_cam>', video),
    path('CrearCamara/', crearCamara),
    path('deleteCam/<int:id_cam>', deleteCam),
    path('deleteDetection/<int:id_detection>', deleteDetection),
    path('deleteDetector/<int:id_detector>', deleteDetector),
    path('deleteUser/<int:id_user>', deleteUser),
    path('deleteGroup/<int:id_group>', deleteGroup),
    path('CrearDetector/', crearDetector),
    path('CrearUsuario/', crearUsuario),
    path('CrearGrupo/', crearGrupo),
    path('camara/<int:id_cam>', detailCam),
    path('detection/<int:id_detection>', detailDetection),

]
