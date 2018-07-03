# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A
from models import Game
from models import GameCopy


class GameTable(tables.Table):
    edit = tables.LinkColumn('GameDetails', args=[A('pk')], text=u'Szczegóły', attrs={'a':{'class': "button"}}, verbose_name="Akcje")
    name = tables.Column(verbose_name='Nazwa')
    number = tables.Column(verbose_name=u'Pozycja na liście')

    class Meta:
        model = Game
        attrs = {"class": "paleblue"}


class GameCopyTable(tables.Table):
    edit = tables.LinkColumn('GameCopyReturn', args=[A('pk')], text="Zwrot", attrs={'a': {'class': "button"}})
    game = tables.Column("Gra")
    barcode = tables.Column("Kod kreskowy egzemparza gry")
    client = tables.Column("Klient")
    rentalDateTime = tables.Column("Data wypożyczenia")
    returnDateTime = tables.Column("Data zwrotu")

    class Meta:
        model = GameCopy
        attrs = {"class": "paleblue"}
        fields = ['game', 'barcode', 'client', "rentalDateTime", "returnDateTime"]  # fields to display

