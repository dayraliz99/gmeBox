# Generated by Django 3.0.7 on 2020-09-24 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, verbose_name='Nombres')),
                ('apellido', models.CharField(max_length=250, verbose_name='Apellidos')),
                ('numero_identificacion', models.CharField(max_length=100, verbose_name='Número de Identificación')),
                ('tipo_documento_identificacion', models.CharField(choices=[('DNI', 'DNI'), ('RUC', 'Ruc'), ('PASAPORTE', 'Pasaporte')], default='CEDULA', max_length=50, verbose_name='Tipo de Identificación')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calle_principal', models.CharField(max_length=250, verbose_name='Calle Principal')),
                ('calle_secundaria', models.CharField(blank=True, max_length=250, null=True, verbose_name='Calle Secundaria')),
                ('telefono', models.CharField(max_length=250, verbose_name='Teléfono')),
                ('referencia', models.TextField(blank=True, null=True, verbose_name='Referencia')),
                ('tipo_direccion', models.CharField(choices=[('TRABAJO', 'Trabajo'), ('CASA', 'Domicilio')], default='CASA', max_length=50, verbose_name='Tipo de Dirección')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direcciones', to='people.Persona')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('correo_electronico', models.EmailField(blank=True, max_length=254, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=True)),
                ('nombre_de_usuario', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('persona', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='people.Persona')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['persona', 'nombre_de_usuario'],
            },
        ),
    ]
