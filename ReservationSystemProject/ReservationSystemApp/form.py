from django.forms import ModelForm
from django.forms import inlineformset_factory

from models import Game
from models import GameCopy


class GameForm(ModelForm):
  class Meta:
    model = Game
    fields = ['name', 'number']

GameCopyItemFormset = inlineformset_factory(Game,
                                            GameCopy,
                                            form=GameForm,
                                            fields=('barcode', 'weight', 'comments', 'state'),
                                            can_delete=False,
                                            extra=1)