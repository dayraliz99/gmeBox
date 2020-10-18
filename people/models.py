from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin


class Persona(models.Model):
    TIPO_DOCUMENTO = (
        ('DNI', 'DNI'),
        ('RUC', 'Ruc'),
        ('PASAPORTE', 'Pasaporte'),
    )
    nombre = models.CharField(
        max_length=250, verbose_name='Nombres')
    apellido = models.CharField(
        max_length=250, verbose_name='Apellidos')
    numero_identificacion = models.CharField(
        max_length=100, verbose_name='Número de Identificación')
    tipo_documento_identificacion = models.CharField(
        max_length=50,
        choices=TIPO_DOCUMENTO,
        default='CEDULA',
        verbose_name='Tipo de Identificación'
    )

    def __str__(self):
        return '{} {}'.format(self.nombre, self.apellido)


class Direccion(models.Model):
    TIPO_DIRECCION = (
        ('TRABAJO', 'Trabajo'),
        ('CASA', 'Domicilio'),
    )
    calle_principal = models.CharField(
        max_length=250, verbose_name='Calle Principal')
    calle_secundaria = models.CharField(
        max_length=250, null=True, blank=True, verbose_name='Calle Secundaria')
    telefono = models.CharField(max_length=250, verbose_name='Teléfono')
    referencia = models.TextField(
        verbose_name='Referencia', null=True, blank=True,)
    tipo_direccion = models.CharField(
        max_length=50,
        choices=TIPO_DIRECCION,
        default='CASA',
        verbose_name='Tipo de Dirección'
    )
    persona = models.ForeignKey(
        Persona, on_delete=models.CASCADE, related_name='direcciones')


class ManejadorUsuarios(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Usuario debe tener un correo valido.')

        if not kwargs.get('username'):
            raise ValueError('El usuario debe tener un nombre valido.')

        usuario = self.model(correo_electronico=self.normalize_email(email),
                             nombre_de_usuario=kwargs.get('username')
                             )

        usuario.set_password(password)
        usuario.save()

        return usuario

    def create_superuser(self, email, password, **kwargs):
        usuario = self.create_user(email, password, **kwargs)
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    correo_electronico = models.EmailField(
        unique=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    nombre_de_usuario = models.CharField(max_length=50, unique=True)
    persona = models.OneToOneField(
        Persona, null=True, on_delete=models.CASCADE, related_name="usuario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = [correo_electronico]

    objects = ManejadorUsuarios()

    class Meta:
        ordering = ['persona', 'nombre_de_usuario']

    def __str__(self):
        return self.nombre_de_usuario
