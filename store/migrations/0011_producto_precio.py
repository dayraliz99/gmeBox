# Generated by Django 3.0.7 on 2020-10-23 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20201023_0131'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12, verbose_name='Precio'),
        ),
    ]
