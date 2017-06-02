from django.forms import TextInput
from django.forms import DateInput
from django.forms import ModelForm
from django.forms import Form
from django.forms import CharField
from django.forms import Select
from django.forms import inlineformset_factory

from models import Game
from models import GameCopy
from models import Event


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


class DateInput(DateInput):
    input_type = 'date'


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'date']
    widgets = {
        'name': TextInput(),
        'date': DateInput()
    }
