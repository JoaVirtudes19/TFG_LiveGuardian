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
    path('CrearCamara/', crear_camara),
    path('deleteCam/<int:id_cam>', eliminar_camara),
    path('deleteDetection/<int:id_detection>', eliminar_deteccion),
    path('deleteDetector/<int:id_detector>', eliminar_detector),
    path('deleteUser/<int:id_user>', eliminar_usuario),
    path('deleteGroup/<int:id_group>', eliminar_grupo),
    path('CrearDetector/', crear_detector),
    path('CrearUsuario/', crear_usuario),
    path('CrearGrupo/', crear_grupo),
    path('Camara/<int:id_cam>', detalles_camara),
    path('Deteccion/<int:id_detection>', detalles_deteccion),

]
