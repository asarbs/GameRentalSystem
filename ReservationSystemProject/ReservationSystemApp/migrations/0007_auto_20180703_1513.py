# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-07-03 13:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReservationSystemApp', '0006_gamecopyhistory_game'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Nazwa')),
                ('cost', models.IntegerField(max_length=256, verbose_name='Cena za dzie\u0144')),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Nazwa'),
        ),
        migrations.AlterField(
            model_name='game',
            name='number',
            field=models.IntegerField(default='0', verbose_name='Pozycja na li\u015bcie'),
        ),
    ]