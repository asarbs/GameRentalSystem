# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-03 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReservationSystemApp', '0009_gamecopy_returndatetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='age',
            field=models.IntegerField(default='0', null=True, verbose_name='wiek'),
        ),
        migrations.AlterField(
            model_name='client',
            name='barcode',
            field=models.IntegerField(default='0', unique=True, verbose_name='kod kreskowy'),
        ),
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(choices=[('Men', 'Men'), ('Woman', 'Women')], default='Men', max_length=5, null=True, verbose_name='P\u0142e\u0107'),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Imi\u0119'),
        ),
        migrations.AlterField(
            model_name='client',
            name='surname',
            field=models.CharField(max_length=256, verbose_name='Nazwisko'),
        ),
        migrations.AlterField(
            model_name='paymentcategories',
            name='cost',
            field=models.IntegerField(verbose_name='Cena za dzie\u0144'),
        ),
    ]