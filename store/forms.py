from django import forms
from store.models import Tecnico, OrdenMantenimiento
from django.forms import ModelForm


class TecnicoForm(ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'


class OrdenMantenimientoForm(ModelForm):

    class Meta:
        model = OrdenMantenimiento
        fields = ('descripcion', 'estado', 'cliente')
        widgets = dict(
            estado=forms.Select(attrs={'class': 'form-control'}),
            cliente=forms.Select(attrs={'class': 'form-control'}),
            descripcion=forms.TextInput(attrs={'class': 'form-control'}),
        )
