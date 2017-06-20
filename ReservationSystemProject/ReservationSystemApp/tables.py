import django_tables2 as tables
from django_tables2.utils import A
from models import Game
from models import GameCopy


class GameTable(tables.Table):
    edit = tables.LinkColumn('GameDetails', args=[A('pk')], text="Details", attrs={'a':{'class': "button"}})

    class Meta:
        model = Game
        attrs = {"class": "paleblue"}


class GameCopyTable(tables.Table):
    edit = tables.LinkColumn('GameCopyReturn', args=[A('pk')], text="Return", attrs={'a': {'class': "button"}})
    class Meta:
        model = GameCopy
        attrs = {"class": "paleblue"}
        fields = ['game', 'barcode', 'client']  # fields to display

