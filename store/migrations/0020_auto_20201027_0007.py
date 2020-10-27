# Generated by Django 3.0.7 on 2020-10-27 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20201026_0242'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='servicio',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Servicio'),
        ),
        migrations.AddField(
            model_name='empresa',
            name='valores',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Valores'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='descripcion',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='mision',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Misión'),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='vision',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Visión'),
        ),
    ]
