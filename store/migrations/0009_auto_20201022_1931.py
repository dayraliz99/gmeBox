# Generated by Django 3.0.7 on 2020-10-22 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_auto_20201022_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='compra',
            old_name='fechaCompra',
            new_name='fecha_compra',
        ),
    ]