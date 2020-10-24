from django.db import models
from people.models import Persona
from django.urls import reverse
from datetime import datetime


class Empresa(models.Model):
    """
    Institución donde se implementa el sistema, se ingresa los datos básico de la institución
    """
    nombre = models.CharField(
        max_length=250, verbose_name='Nombre')
    contacto = models.CharField(
        max_length=250, verbose_name='Contacto')
    email = models.EmailField(
        unique=True, verbose_name='Correo electrónico')
    telefono = models.CharField(
        max_length=250, verbose_name='Teléfono', null=True, blank=True)
    celular = models.CharField(
        max_length=250, verbose_name='Celular', null=True, blank=True)
    direccion = models.CharField(
        max_length=250, verbose_name='Dirección', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    """
    Contiene los datos de un proveedor.
    """
    nombre = models.CharField(
        max_length=250, verbose_name='Nombre')
    contacto = models.CharField(
        max_length=250, verbose_name='Contacto')
    email = models.EmailField(
        unique=True, verbose_name='Correo electrónico')
    telefono = models.CharField(
        max_length=250, verbose_name='Teléfono', null=True, blank=True)
    celular = models.CharField(
        max_length=250, verbose_name='Celular', null=True, blank=True)
    direccion = models.CharField(
        max_length=250, verbose_name='Dirección', null=True, blank=True)

    def __str__(self):
        return self.nombre


class Tecnico(Persona):
    """
    Persona que se encarga de registrar una revisión técnica de un equipo
    """
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso")


class Cliente(Persona):
    def __str__(self):
        return '{} {} {}'.format(self.nombre, self.apellido, self.numero_identificacion)


class OrdenMantenimiento(models.Model):
    """
    Contiene los datos del registro de una orden de mantenimientos de uno o muchos equipos y los datos del cliente
    """
    ESTADO = (
        ('NUEVO', 'Nuevo'),
        ('EN_REVISION', 'En revisión'),
        ('REVISADO', 'Revisado'),
        ('CONFIRMADO', 'Confirmado'),
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
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='ordenes')

    def get_absolute_url(self):
        return reverse('order-update', kwargs={'pk': self.pk})

    def verificar_estado_detalles(self, estado):
        """
        Permite verificar el estado actual de todos los detalles de la orden.
        """
        if self.detalles.count() == 0:
            return False

        for detalle in self.detalles.all():
            if detalle.estado != estado:
                return False
        return True

    def calcular_monto(self):
        self.monto_servicio = sum(
            map(lambda detalle: detalle.precio_servicio, self.detalles.all()))

    def confirmar(self):
        factura = Factura.objects.create(fecha_venta=datetime.now(), cliente=self.cliente, empresa=self.empresa, subtotal=0.0, impuesto=0.0,
                                         total=0.0)

        for detalle in self.detalles.all():

            detalle.estado = "CONFIRMADO"
            detalle.save()
            detalle_factura = DetalleFactura(
                precio_unitario=detalle.precio_servicio, cantidad=1, impuesto=0.0)
            detalle_factura.calcular_total()
            factura.detalles.add(detalle_factura, bulk=False)
        factura.calcular_subtotal()
        factura.calcular_impuesto()
        factura.calcular_total()
        factura.save()


class DetalleOrden(models.Model):
    """
    Contiene los datos de un equipo a reparar
    """
    ESTADO = (
        ('NUEVO', 'Nuevo'),
        ('EN_REVISION', 'En revisión'),
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
    """
    Detalle que ingresa un técnico sobre un equipo
    """
    fecha_revision = models.DateField(
        verbose_name="Fecha de revisión", blank=True, null=True)
    descripcion = models.CharField(
        max_length=250, verbose_name='Descripción')
    tecnico = models.ForeignKey(
        Tecnico, on_delete=models.CASCADE, related_name='revisiones')
    detalle_orden = models.ForeignKey(
        DetalleOrden, on_delete=models.CASCADE, related_name='revisiones')


class Categoria(models.Model):
    """
    IPermite categorizar los productos.
    """
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    descripcion = models.TextField(
        verbose_name='Descripción', null=True, blank=True)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """
    Contiene los datos de un producto que se manejan dentro de una empresa
    """
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio', default=0.0)
    impuesto_iva = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Iva', default=0.0)
    descripcion = models.TextField(
        verbose_name='Descripción', null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return '{} Precio: {}'.format(self.nombre, self.precio)

    def calcular_cantidad(self):
        self.cantidad = sum(
            map(lambda detalle: detalle.cantidad, self.compras.all())) - sum(
            map(lambda detalle: detalle.cantidad, self.ventas.all()))


class Precio (models.Model):
    """
    Contiene los costos de un producto
    """
    valor = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio')
    nombre = models.CharField(max_length=255)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='precios')


class Impuesto (models.Model):
    """
    Contiene los valores de impuesto de un producto
    """
    porcentaje = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name='Porcentaje')
    nombre = models.CharField(max_length=255)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='impuestos')


class Compra (models.Model):
    """
    Contiene el registro de una compra de uno o muchos productos que ingresan a la empresa y contiene los
    datos del proveedo a quien se realiza la compra.
    """
    ESTADO = (
        ('POR_PAGAR', 'Por pagar'),
        ('PAGADO', 'Pagado'),
    )
    fecha_compra = models.DateField(
        verbose_name="Fecha de compra")
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='SubTotal', default=0.0)
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto', default=0.0)
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total', default=0.0)
    estado = models.CharField(
        max_length=50,
        choices=ESTADO,
        default='POR_PAGAR',
        verbose_name='Estado'
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name='compras')

    def calcular_subtotal(self):
        self.subtotal = sum(
            map(lambda detalle: detalle.total, self.detalles.all()))

    def calcular_total(self):
        self.total = self.subtotal + self.impuesto

    def calcular_impuesto(self):
        self.impuesto = sum(
            map(lambda detalle: detalle.impuesto, self.detalles.all()))


class DetalleCompra (models.Model):
    """
    Contiene el detalle de compra, se relaciona con un producto.
    """
    detalle = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio Unitario')
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto', default=0.0)
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total', default=0.0)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='compras')
    compra = models.ForeignKey(
        Compra, on_delete=models.CASCADE, related_name='detalles')

    def calcular_total(self):
        print('pasa')
        self.total = self.cantidad * self.precio_unitario


class Factura (models.Model):
    """
    Contiene los datos de una factura como productos a vender, cliente y valores como subtotal, total e impuestos.
    """
    ESTADO = (
        ('POR_PAGAR', 'Por pagar'),
        ('PAGADO', 'Pagado'),
    )
    fecha_venta = models.DateField(
        verbose_name="Fecha de compra")
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='SubTotal', default=0.0)
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto', default=0.0)
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total', default=0.0)
    monto_pagado = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total', default=0.0)
    estado = models.CharField(
        max_length=50,
        choices=ESTADO,
        default='POR_PAGAR',
        verbose_name='Estado'
    )
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='facturas')
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name='facturas')

    def get_absolute_url(self):
        return reverse('invoice-update', kwargs={'pk': self.pk})

    def calcular_subtotal(self):
        self.subtotal = sum(
            map(lambda detalle: detalle.total, self.detalles.all()))

    def calcular_impuesto(self):
        self.impuesto = sum(
            map(lambda detalle: detalle.impuesto, self.detalles.all()))

    def calcular_total(self):
        self.total = self.subtotal+self.impuesto

    def calcular_pagos(self):
        self.monto_pagado = sum(
            map(lambda pago: pago.monto, self.pagos.all()))
        if self.monto_pagado == self.total:
            self.estado = "PAGADO"
        else:
            self.estado = "POR_PAGAR"


class DetalleFactura (models.Model):
    """
    Contiene los datos del producto a vender.
    """
    detalle = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio Unitario', default=0.0)
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto', default=0.0)
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total', default=0.0)
    producto = models.ForeignKey(
        Producto, null=True, blank=True, on_delete=models.CASCADE, related_name='ventas')
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name='detalles')

    def calcular_total(self):
        self.total = self.precio_unitario * self.cantidad


class PagoFactura (models.Model):
    """
    Pagos de Factura.
    """
    fecha_pago = models.DateField(verbose_name="Fecha de compra")
    monto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio Unitario', default=0.0)
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name='pagos')
    descripcion = models.CharField(max_length=255, null=True, blank=True)
