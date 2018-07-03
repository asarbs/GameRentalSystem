# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Client(models.Model):
    GENDER = (("Men", "Men"),
             ("Woman", "Women"))
    name = models.CharField(max_length=256, verbose_name="Name")
    surname = models.CharField(max_length=256, verbose_name="Surname")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField(max_length=5, choices=GENDER, verbose_name="Gender", default="Men")
    barcode = models.IntegerField(verbose_name="Barcode", default="0", unique=True)

    def __str__(self):
        return u'{0} {1}'.format(self.name, self.surname)

    def __unicode__(self):
        return u'{0} {1}'.format(self.name, self.surname)


class Game(models.Model):
    name = models.CharField(max_length=256, verbose_name="Nazwa")
    number = models.IntegerField(verbose_name="Pozycja na liście", default="0")

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class GameCopy(models.Model):
    STATE = (("Loaned", "Loaned"), ("Free", "Free"))
    barcode = models.IntegerField(verbose_name="Barcode", default="0", unique=True)
    weight = models.IntegerField(verbose_name="Weight", default="0")
    comments = models.TextField(blank=True, verbose_name="Comments")
    state = models.CharField(max_length=6, choices=STATE, default="Free", verbose_name="State")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name="Client", blank=True, null=True)
    rentalDateTime = models.DateTimeField(blank=True, editable=True, null=True)
    returnDateTime = models.DateTimeField(blank=True, editable=True, null=True)


class Event(models.Model):
    name = models.CharField(max_length=256, verbose_name="Name")
    date = models.DateField()

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class GameCopyHistory(models.Model):
    gameCopy = models.ForeignKey(GameCopy, verbose_name="Game Copy")
    game = models.ForeignKey(Game, verbose_name="Game", blank=True, null=True)
    state = models.CharField(max_length=6, choices=GameCopy.STATE, default="Free", verbose_name="State")
    user = models.ForeignKey(User, verbose_name="Operator")
    client = models.ForeignKey(Client, verbose_name="Client")
    event = models.ForeignKey(Event, verbose_name="Event")
    dateTime = models.DateTimeField(auto_now_add=True, blank=True, editable=True)


class PaymentCategories(models.Model):
    name = models.CharField(max_length=256, verbose_name="Nazwa")
    cost = models.IntegerField(verbose_name="Cena za dzień")