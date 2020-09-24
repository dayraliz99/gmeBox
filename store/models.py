from django.db import models
from people.models import Persona


class Empresa(models.Model):
    nombre = models.CharField(
        max_length=250, verbose_name='Nombre')
    nombre_contacto = models.CharField(
        max_length=250, verbose_name='Contacto')
    email = models.EmailField(
        unique=True, verbose_name='Correo electrónico')
    telefono = models.CharField(
        max_length=250, verbose_name='Teléfono', null=True, blank=True)
    celular = models.CharField(
        max_length=250, verbose_name='Celular', null=True, blank=True)
    direccion = models.CharField(
        max_length=250, verbose_name='Dirección', null=True, blank=True)


class Proveedor(models.Model):
    nombre = models.CharField(
        max_length=250, verbose_name='Nombre')
    email = models.EmailField(
        unique=True, verbose_name='Correo electrónico')
    telefono = models.CharField(
        max_length=250, verbose_name='Teléfono', null=True, blank=True)
    celular = models.CharField(
        max_length=250, verbose_name='Celular', null=True, blank=True)
    direccion = models.CharField(
        max_length=250, verbose_name='Dirección', null=True, blank=True)


class Tecnico(Persona):
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso")


class Cliente(Persona):
    def __str__(self):
        return self.numero_identificacion


class OrdenMantenimiento(models.Model):
    ESTADO = (
        ('NUEVO', 'Nuevo'),
        ('EN_REVISION', 'EN revisión'),
        ('REVISADO', 'Revisado'),
        ('FINALIZADO', 'Finalizado'),
    )
    fecha_registro = models.DateField(
        verbose_name="Fecha de registro", auto_now_add=True)
    descripcion = models.CharField(
        max_length=250, verbose_name='Descripción', null=True, blank=True)
    estado = models.CharField(
        max_length=50,
        choices=ESTADO,
        default='NUEVO',
        verbose_name='Estado'
    )
    monto_servicio = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Monto', default=0.00)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='ordenes')


class DetalleOrden(models.Model):
    ESTADO = (
        ('NUEVO', 'Nuevo'),
        ('EN_REVISION', 'EN revisión'),
        ('REVISADO', 'Revisado'),
        ('CONFIRMADO', 'Confirmado'),
        ('Arregado', 'Arreglado'),
        ('FINALIZADO', 'Finalizado'),
    )
    nombre_equipo = models.CharField(
        max_length=250, verbose_name='Nombre de equipo')
    observacion = models.CharField(
        max_length=250, verbose_name='Observación')

    estado = models.CharField(
        max_length=50,
        choices=ESTADO,
        default='NUEVO',
        verbose_name='Estado'
    )
    precio_servicio = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio de servicio', default=0.00)
    orden_mantenimiento = models.ForeignKey(
        OrdenMantenimiento, on_delete=models.CASCADE, related_name='detalles')


class RevisionTecnica(models.Model):
    fecha_revision = models.DateField(
        verbose_name="Fecha de revisión")
    descripcion = models.CharField(
        max_length=250, verbose_name='Descripción')
    tecnico = models.ForeignKey(
        Tecnico, on_delete=models.CASCADE, related_name='revisiones')
    detalle_orden = models.ForeignKey(
        DetalleOrden, on_delete=models.CASCADE, related_name='revisiones')
