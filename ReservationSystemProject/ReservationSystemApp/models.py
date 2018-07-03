# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PaymentCategories(models.Model):
    name = models.CharField(max_length=256, verbose_name="Nazwa")
    cost = models.IntegerField(verbose_name="Cena za dzień")

    def __str__(self):
        return u'{0}'.format(self.name)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Client(models.Model):
    GENDER = (("Men", "Men"),
             ("Woman", "Women"))
    name = models.CharField(max_length=256, verbose_name="Imię")
    surname = models.CharField(max_length=256, verbose_name="Nazwisko")
    age = models.IntegerField(verbose_name="wiek", null=True, default="0")
    gender = models.CharField(max_length=5, choices=GENDER, verbose_name=u'Płeć', default="Men", null=True)
    barcode = models.IntegerField(verbose_name="kod kreskowy", default="0", unique=True)

    def __str__(self):
        return u'{0} {1}'.format(self.name, self.surname)

    def __unicode__(self):
        return u'{0} {1}'.format(self.name, self.surname)


class Game(models.Model):
    name = models.CharField(max_length=256, verbose_name="Nazwa")
    number = models.IntegerField(verbose_name="Pozycja na liście", default="0")
    paymentCategory = models.ForeignKey(PaymentCategories, verbose_name="Kategoria cenowa", default='1')

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
    cost = models.IntegerField(verbose_name="Cena", default="0")

    def calculatePrice(self):
        if self.returnDateTime == None and self.rentalDateTime == None:
            return None
        else:
            timeDiff = self.returnDateTime - self.rentalDateTime
            price = timeDiff.days * self.cost
            return str(timeDiff.days) + "dni * " + str(self.cost) + u'zł = ' + str(price) + u'zł'



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
