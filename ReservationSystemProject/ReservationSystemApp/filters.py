import django_filters

from models import Game
from models import GameCopy


class GameFilter(django_filters.FilterSet):
    class Meta:
        model = Game
        fields = {'name': ['contains']}


class GameCopyFilter(django_filters.FilterSet):
    class Meta:
        model = GameCopy
        fields = ['barcode']
