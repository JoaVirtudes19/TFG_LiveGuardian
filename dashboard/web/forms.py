from django import forms
from django.forms import ModelForm
from web.models import Cam


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


    #nombreCamara = forms.CharField(label="Nombre de la cámara", widget=forms.TextInput(attrs={'size':'10','class':'form-control'}), required=True)
    #url = forms.CharField(label="Url de la cámara", widget=forms.TextInput(attrs={'size': '40','class':'form-control'}), required=True)
    #detector = forms.ModelChoiceField(required=False,label="Seleccione un detector", queryset=Detector.objects.all().order_by("name"),widget=forms.Select(attrs={'class':'form-control'}))
    #grupos = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'form-control'}),required=False,label="Selecciona grupos de Telegram", queryset=Group.objects.all().order_by("name"))