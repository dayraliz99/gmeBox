# Generated by Django 3.0.7 on 2020-10-23 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_producto_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='impuesto_iva',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Iva'),
        ),
    ]