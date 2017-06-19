import django_tables2 as tables
from django_tables2.utils import A
from models import Game


class GameTable(tables.Table):
    edit = tables.LinkColumn('GameDetails', args=[A('pk')], text="Details", attrs={'a':{'class': "button"}})

    class Meta:
        model = Game
        attrs = {"class": "paleblue"}
