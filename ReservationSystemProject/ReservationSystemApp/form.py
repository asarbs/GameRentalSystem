from django.forms import TextInput
from django.forms import DateInput
from django.forms import ModelForm
from django.forms import CharField
from django.forms import inlineformset_factory
from django.forms import PasswordInput
from django.contrib.auth.models import User

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


class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        exclude = ('user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'groups')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user