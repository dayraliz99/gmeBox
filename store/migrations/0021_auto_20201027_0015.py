# Generated by Django 3.0.7 on 2020-10-27 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_auto_20201027_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empresa',
            name='servicio',
        ),
        migrations.RemoveField(
            model_name='empresa',
            name='valores',
        ),
    ]
