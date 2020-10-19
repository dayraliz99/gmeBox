from django import forms
from store.models import Tecnico, OrdenMantenimiento, Cliente, DetalleOrden, RevisionTecnica
from django.forms import ModelForm


class TecnicoForm(ModelForm):
    correo_electronico = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Tecnico
        fields = ('tipo_documento_identificacion', 'nombre',
                  'apellido', 'numero_identificacion', 'fecha_ingreso')
        widgets = dict(
            tipo_documento_identificacion=forms.Select(
                attrs={'class': 'form-control'}),
            nombre=forms.TextInput(attrs={'class': 'form-control'}),
            apellido=forms.TextInput(attrs={'class': 'form-control'}),
            numero_identificacion=forms.TextInput(
                attrs={'class': 'form-control'}),
            fecha_ingreso=forms.DateInput(
                attrs={'class': 'form-control', "type": "date"})
        )


class OrdenMantenimientoForm(ModelForm):
    """
    Formulario personalizado para crear y editar una orden de mantenimiento.
    """
    class Meta:
        model = OrdenMantenimiento
        fields = ('cliente', 'descripcion', 'estado', )
        widgets = dict(
            estado=forms.Select(attrs={'class': 'form-control'}),
            cliente=forms.Select(attrs={'class': 'form-control'}),
            descripcion=forms.TextInput(attrs={'class': 'form-control'}),
        )


class ClienteForm(ModelForm):
    """
    Formulario personalizado para crear y editar un cliente.
    """
    correo_electronico = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Cliente
        fields = ('tipo_documento_identificacion', 'nombre',
                  'apellido', 'numero_identificacion',)
        widgets = dict(
            tipo_documento_identificacion=forms.Select(
                attrs={'class': 'form-control'}),
            nombre=forms.TextInput(attrs={'class': 'form-control'}),
            apellido=forms.TextInput(attrs={'class': 'form-control'}),
            numero_identificacion=forms.TextInput(
                attrs={'class': 'form-control'})
        )


class DetalleOrdenForm(ModelForm):
    """
    Formulario personalizado para crear y editar un detalle de orden de mantenimiento.
     **Context**
    ``DetalleOrden``
        An instance of :model:`store.DetalleOrden`.
    """
    class Meta:
        model = DetalleOrden
        fields = ('nombre_equipo', 'precio_servicio',
                  'observacion', 'estado', )
        widgets = dict(
            nombre_equipo=forms.TextInput(attrs={'class': 'form-control'}),
            precio_servicio=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number'}),
            observacion=forms.TextInput(attrs={'class': 'form-control'}),
            estado=forms.Select(attrs={'class': 'form-control'}),
        )


class RevisionTecnicaForm(ModelForm):
    """
    Formulario personalizado para crear y editar una revisión técnica.
     **Context**
    ``RevisionTecnica``
        An instance of :model:`store.RevisionTecnica`.
    """
    class Meta:
        model = RevisionTecnica
        fields = ('tecnico', 'descripcion')
        widgets = dict(
            tecnico=forms.Select(attrs={'class': 'form-control'}),
            descripcion=forms.TextInput(
                attrs={'class': 'form-control'}),
        )
