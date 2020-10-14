from django import forms
from store.models import Tecnico, OrdenMantenimiento, Cliente
from django.forms import ModelForm


class TecnicoForm(ModelForm):
    class Meta:
        model = Tecnico
        fields = '__all__'


class OrdenMantenimientoForm(ModelForm):
    """
    Formulario personalizado para crear y editar una orden de mantenimiento.
    """
    class Meta:
        model = OrdenMantenimiento
        fields = ('empresa', 'cliente', 'descripcion', 'estado', )
        widgets = dict(
            estado=forms.Select(attrs={'class': 'form-control'}),
            cliente=forms.Select(attrs={'class': 'form-control'}),
            empresa=forms.Select(attrs={'class': 'form-control'}),
            descripcion=forms.TextInput(attrs={'class': 'form-control'}),
        )


class ClienteForm(ModelForm):
    """
    Formulario personalizado para crear y editar un cliente.
    """
    class Meta:
        model = Cliente
        fields = ('tipo_documento_identificacion', 'nombre',
                  'apellido', 'numero_identificacion', )
        widgets = dict(
            tipo_documento_identificacion=forms.Select(
                attrs={'class': 'form-control'}),
            nombre=forms.TextInput(attrs={'class': 'form-control'}),
            apellido=forms.TextInput(attrs={'class': 'form-control'}),
            numero_identificacion=forms.TextInput(
                attrs={'class': 'form-control'}),
        )
