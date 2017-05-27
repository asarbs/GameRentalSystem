# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Client(models.Model):
    GENDER = (("Men", "Men"),
             ("Woman", "Women"))
    name = models.CharField(max_length=256, verbose_name="Name")
    surname = models.CharField(max_length=256, verbose_name="Surname")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=5, choices=GENDER, verbose_name="Gender", default="Men")
    barcode = models.IntegerField(verbose_name="Barcode", default="0")

    def __str__(self):
        return u'{0} {1}'.format(self.name, self.surname)

    def __unicode__(self):
        return u'{0} {1}'.format(self.name, self.surname)


class Game(models.Model):
    name = models.CharField(max_length=256, verbose_name="Name")
    number = models.IntegerField(verbose_name="Number on list", default="0")

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class GameCopy(models.Model):
    STATE = (("Loaned", "Loaned"), ("Free", "Free"))
    barcode = models.IntegerField(verbose_name="Barcode", default="0")
    weight = models.IntegerField(verbose_name="Weight", default="0")
    comments = models.TextField(blank=True, verbose_name="Comments")
    state = models.CharField(max_length=6, choices=STATE, default="Free", verbose_name="State")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=256, verbose_name="Name")
    date = models.DateField()

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)