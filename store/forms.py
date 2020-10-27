from django import forms
from store.models import Tecnico, OrdenMantenimiento, Cliente, DetalleOrden, RevisionTecnica, Factura, DetalleFactura, PagoFactura
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
        fields = ('cliente', 'descripcion',)
        widgets = dict(
            cliente=forms.Select(attrs={'class': 'form-control'}),
            descripcion=forms.TextInput(attrs={'class': 'form-control'}),
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


class OrdenMantenimientoConfirmarForm(ModelForm):
    """
    Formulario personalizado para crear y editar una orden de mantenimiento.
    """
    class Meta:
        model = OrdenMantenimiento
        fields = ('id',)


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


class RevisionTecnicaForm(ModelForm):
    """
    Formulario personalizado para asignar un técnico a un detalle de orden de mantenimiento.
     **Context**
    ``RevisionTecnica``
        An instance of :model:`store.RevisionTecnica`.
    """
    class Meta:
        model = RevisionTecnica
        fields = ('tecnico', )
        widgets = dict(
            tecnico=forms.Select(
                attrs={'class': 'form-control'}),
        )


class GestionarRevisionTecnicaForm(ModelForm):
    """
    Formulario para listar y editar una revisión de un equipo.
     **Context**
    ``RevisionTecnica``
        An instance of :model:`store.RevisionTecnica`.
    """
    ESTADO = (
        ('EN_REVISION', 'En revisión'),
        ('REVISADO', 'Revisado'),
        ('Arregado', 'Arreglado'),
    )
    estado = forms.ChoiceField(
        choices=ESTADO,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = RevisionTecnica
        fields = ('fecha_revision', 'descripcion',)
        widgets = dict(
            fecha_revision=forms.DateInput(
                attrs={'class': 'form-control', "type": "date"}),
            descripcion=forms.Textarea(
                attrs={'class': 'form-control'}),
        )


class FacturaForm(ModelForm):
    """
    Formulario personalizado para crear y editar una factura.
    """
    class Meta:
        model = Factura
        fields = ('cliente', 'fecha_venta', 'empresa',)
        widgets = dict(
            cliente=forms.Select(
                attrs={'class': 'form-control'}),
            empresa=forms.Select(
                attrs={'class': 'form-control'}),
            fecha_venta=forms.TextInput(
                attrs={'class': 'form-control', "type": "date"}),
        )


class DetalleFacturaForm(ModelForm):
    """
    Formulario personalizado para crear y editar un detalle de factura.
     **Context**
    ``DetalleFactura``
        An instance of :model:`store.DetalleFactura`.
    """
    class Meta:
        model = DetalleFactura
        fields = ('cantidad', 'producto', 'precio_unitario',)
        widgets = dict(
            cantidad=forms.TextInput(
                attrs={'class': 'form-control', "type": "number"}),
            precio_unitario=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', "step":"0.01"}),
            producto=forms.Select(attrs={'class': 'form-control'}),
        )


class PagoFacturaForm(ModelForm):
    """
    Formulario personalizado para crear y editar un pago de factura.
     **Context**
    ``PagoFactura``
        An instance of :model:`store.PagoFactura`.
    """
    class Meta:
        model = PagoFactura
        fields = ('fecha_pago', 'monto', 'descripcion')
        widgets = dict(
            fecha_pago=forms.DateInput(
                attrs={'class': 'form-control', "type": "date"}),
            monto=forms.TextInput(
                attrs={'class': 'form-control', 'type': 'number', "step":"0.01"}),
            descripcion=forms.Textarea(attrs={'class': 'form-control'}),
        )
