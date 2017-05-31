# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-29 18:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReservationSystemApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='barcode',
            field=models.IntegerField(default='0', unique=True, verbose_name='Barcode'),
        ),
        migrations.AlterField(
            model_name='gamecopy',
            name='barcode',
            field=models.IntegerField(default='0', unique=True, verbose_name='Barcode'),
        ),
    ]
