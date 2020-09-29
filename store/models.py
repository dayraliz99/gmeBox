from django.db import models
from people.models import Persona


class Empresa(models.Model):
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
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='ordenes')


class DetalleOrden(models.Model):
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
    fecha_revision = models.DateField(
        verbose_name="Fecha de revisión")
    descripcion = models.CharField(
        max_length=250, verbose_name='Descripción')
    tecnico = models.ForeignKey(
        Tecnico, on_delete=models.CASCADE, related_name='revisiones')
    detalle_orden = models.ForeignKey(
        DetalleOrden, on_delete=models.CASCADE, related_name='revisiones')


class Categoria(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    empresa = models.ForeignKey(
        Empresa, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre')
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    descripcion = models.TextField(verbose_name='Descripción', null=True, blank=True)
    categoria = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name='productos')


class Precio (models.Model):
    valor = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio')
    nombre = models.CharField(max_length=255)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='precios')


class Impuesto (models.Model):
    porcentaje = models.DecimalField(
        max_digits=4, decimal_places=2, verbose_name='Porcentaje')
    nombre = models.CharField(max_length=255)
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='impuestos')


class Compra (models.Model):
    ESTADO = (
        ('POR_PAGAR', 'Por pagar'),
        ('PAGADO', 'Pagado'),
    )
    fechaCompra = models.DateField(
        verbose_name="Fecha de compra")
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='SubTotal')
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
    estado = models.CharField(
        max_length=50,
        choices=ESTADO,
        default='POR_PAGAR',
        verbose_name='Estado'
    )
    proveedor = models.ForeignKey(
        Proveedor, on_delete=models.CASCADE, related_name='compras')


class DetalleCompra (models.Model):
    detalle = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precioUnitario = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio Unitario')
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='compras')
    compra = models.ForeignKey(
        Compra, on_delete=models.CASCADE, related_name='detalles')


class Factura (models.Model):
    ESTADO = (
        ('POR_PAGAR', 'Por pagar'),
        ('PAGADO', 'Pagado'),
    )
    fechaVenta = models.DateField(
        verbose_name="Fecha de compra")
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='SubTotal')
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
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


class DetalleFactura (models.Model):
    detalle = models.CharField(max_length=255, null=True, blank=True)
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad')
    precioUnitario = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Precio Unitario')
    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Impuesto')
    total = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name='Total')
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name='ventas')
    factura = models.ForeignKey(
        Factura, on_delete=models.CASCADE, related_name='detalles')
