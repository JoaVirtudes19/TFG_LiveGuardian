from django import forms
from django.forms import ModelForm
from web.models import Cam, Detector


class CrearCamara(ModelForm):
    class Meta:
        model = Cam
        fields = '__all__'
        labels = {
            'name': 'Nombre de la cámara',
            'url': 'Url de la cámara',
            'detector':'Seleccione un detector',
            'groups': 'Seleccione varios grupos'
        }
        widgets = {
            'name': forms.TextInput(attrs={'size':'10','class':'form-control'}),
            'url': forms.TextInput(attrs={'size': '40','class':'form-control'}),
            'detector': forms.Select(attrs={'class':'form-control'}),
            'groups': forms.SelectMultiple(attrs={'class':'form-control'})
        }



class CrearDetector(ModelForm):
    class Meta:
        model = Detector
        fields = '__all__'
        labels = {
            'name':'Nombre del detector',
            'model': 'Elija un modelo'

        }
        widgets = {
            'name': forms.TextInput(attrs={'size':'10','class':'form-control'}),
            'model': forms.FileInput(attrs={'class':'form-control'})
        }
