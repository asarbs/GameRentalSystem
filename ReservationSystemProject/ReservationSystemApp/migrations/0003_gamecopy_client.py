# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 19:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ReservationSystemApp', '0002_auto_20170529_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamecopy',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ReservationSystemApp.Client', verbose_name='Client'),
        ),
    ]
