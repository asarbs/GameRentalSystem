# -*- coding: utf-8 -*-
from django.forms import TextInput
from django.forms import DateInput
from django.forms import ModelForm
from django.forms import CharField
from django.forms import inlineformset_factory
from django.forms import PasswordInput
from django.forms import Form
from django.contrib.auth.models import User

from models import Game
from models import GameCopy
from models import Event


class GameForm(ModelForm):
  class Meta:
    model = Game
    fields = ['name', 'number', 'paymentCategory']
    labels = {
        'name': 'Nazwa',
        'number': u'Pozycja na liście',
        'paymentCategory': u'Kategoria cenowa',
    }

GameCopyItemFormset = inlineformset_factory(Game,
                                            GameCopy,
                                            form=GameForm,
                                            fields=('barcode', 'weight', 'comments', 'state'),
                                            labels={'barcode': u'Kod kreskowy', 'weight': u'Waga', 'comments': u'Komenatrz', 'state': u'Status'},
                                            can_delete=False,
                                            extra=1)


class DateInput(DateInput):
    input_type = 'date'


class EventForm(ModelForm):
  class Meta:
    model = Event
    fields = ['name', 'date']
    labels = {
        'name': 'Nazwa',
        'date': 'Data',
    }
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

class ChangePasswordForm(Form):
    new_password = CharField(widget=PasswordInput(), label=u'Nowe hasło')
    new_password_confirm = CharField(widget=PasswordInput(), label="Zapisz")

    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        if not self.cleaned_data.get('new_password') == self.cleaned_data.get('new_password_confirm'):
            self.add_error('new_password_confirm', "Passwords do not match")

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["new_password"])
        if commit:
            self.user.save()
        return self.user