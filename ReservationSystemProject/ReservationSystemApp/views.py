# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from form import GameForm
from form import GameCopyItemFormset
from models import Client
from models import Game


# Create your views here.

def main(request):
    return render(request, 'main.html', {})


class NewClientView(CreateView):
    model = Client
    fields = ['name', 'surname', 'age', 'gender', 'barcode']

    def get_success_url(self):
        return reverse("/", args=())


class NewGameView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'ReservationSystemApp/game_form.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        gameCopyItemFormset = GameCopyItemFormset()
        return self.render_to_response(self.get_context_data(form=form, gameCopyItemFormset=gameCopyItemFormset))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        gameCopyItemFormset = GameCopyItemFormset(self.request.POST)
        print(gameCopyItemFormset.is_valid(), gameCopyItemFormset.total_error_count())
        for error in gameCopyItemFormset.errors:
            print("A", error)

        if form.is_valid() and gameCopyItemFormset.is_valid():
            return self.form_valid(form, gameCopyItemFormset)
        else:
            return self.form_invalid(form, gameCopyItemFormset)

    def form_valid(self, form, gameCopyItemFormset):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        gameCopyItemFormset.instance = self.object
        gameCopyItemFormset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, gameCopyItemFormset):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, gameCopyItemFormset=gameCopyItemFormset))

    def get_success_url(self):
        return reverse("/", args=())
