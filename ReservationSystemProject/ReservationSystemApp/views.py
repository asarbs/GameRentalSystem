# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from form import GameForm
from form import GameCopyItemFormset
from models import Client
from models import Game
from models import GameCopy


# Create your views here.

def main(request):
    return render(request, 'main.html', {})


class NewClientView(CreateView):
    model = Client
    fields = ['name', 'surname', 'age', 'gender', 'barcode']

    def get_success_url(self):
        return reverse("ClientDetails", args=(self.object.id,))


class ClientDetails(DetailView):
    model = Client


class ClientList(ListView):
    model = Client


def DeleteClient(request, pk):
    Client(id=pk).delete()
    return HttpResponseRedirect(reverse("ClientList"))


class ClientEdit(UpdateView):
    model = Client
    fields = ['name', 'surname', 'age', 'gender', 'barcode']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("ClientDetails", args=(self.object.id,))


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
        return reverse("GameDetails", args=(self.object.id,))


class GameDetails(DetailView):
    model = Game

    def get_object(self, queryset=None):
        object = super(GameDetails,self).get_object()
        gameCopy = GameCopy.objects.filter(game=object)
        object.gameCopy = gameCopy
        object.gameCopyItemFormset = GameCopyItemFormset()
        return object


class GameList(ListView):
    queryset = Game.objects.order_by("number")
    model = Game


class GameEdit(UpdateView):
    model = Game
    fields = ['name', 'number']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("GameDetails", args=(self.object.id,))


def NewGameCopy(request):
    game = Game.objects.get(id=request.GET['game_id'])
    GameCopy(barcode=request.POST['gamecopy_set-0-barcode'],
                        weight=request.POST['gamecopy_set-0-weight'],
                        comments=request.POST['gamecopy_set-0-comments'],
                        state=request.POST['gamecopy_set-0-state'],
                        game=game).save()
    return HttpResponseRedirect(reverse("GameDetails", args=(request.GET['game_id'],)))


def DeleteGamesCopy(request, pk):
    GameCopy(id=pk).delete()
    return HttpResponseRedirect(reverse("GameDetails", args=(request.GET['game_id'],)))


def GameDelete(request, pk):
    Game(id=pk).delete()
    return HttpResponseRedirect(reverse("GamesList"))


def checkIfBarcodesAreEmpty(errors, request):
    result = False
    result = checkIfGameBarcodeAreEmpty(errors, request)
    if len(request.POST['clientBarcode']) == 0:
        errors['clientBarcode_errors'].append("This field can't be empty")
        result = True
    if len(request.POST['gameCopyWeight']) == 0:
        errors['gameCopyWeight_errors'].append("This field can't be empty")
        result = True
    return result


def checkIfGameBarcodeAreEmpty(errors, request):
    if len(request.POST['gameCopyBarcode']) == 0:
        errors['gameCopyBarcode_errors'].append("This field can't be empty")
        return True
    return False


def Rental(request):
    if request.method == 'POST':
        values = {"gameCopyBarcode_val": request.POST['gameCopyBarcode'],
                  "clientBarcode_val": request.POST['clientBarcode'],
                  "comment_val": request.POST['comment'],
                  "gameCopyWeight_val":  request.POST['gameCopyWeight']}
        errors = {"gameCopyBarcode_errors": [],
                  "clientBarcode_errors": [],
                  "gameCopyWeight_errors": []}

        if checkIfBarcodesAreEmpty(errors, request):
            values.update(errors)
            return render(request, "ReservationSystemApp/Rental_form.html",
                          values)
        try:
            gameCopy = GameCopy.objects.get(barcode=request.POST['gameCopyBarcode'])
        except ObjectDoesNotExist as x:
            errors['gameCopyBarcode_errors'].append("Copy not found")
        try:
            clinet = Client.objects.get(barcode=request.POST['clientBarcode'])
        except ObjectDoesNotExist as x:
            errors['clientBarcode_errors'].append("Client not found")

        if gameCopy.state == GameCopy.STATE[0][0]:
            errors['gameCopyBarcode_errors'].append("Game rented")

        print()
        if len(errors['gameCopyBarcode_errors']) > 0 or len(errors['clientBarcode_errors']) > 0 or len(errors['gameCopyWeight_errors']) > 0:
            values.update(errors)
            return render(request, "ReservationSystemApp/Rental_form.html", values)

        gameCopy.weight = request.POST['gameCopyWeight']
        gameCopy.comments = request.POST['comment']
        gameCopy.state = GameCopy.STATE[0][0]
        gameCopy.client = clinet
        gameCopy.save()

        return HttpResponseRedirect(reverse("GameDetails", args=(gameCopy.game.id,)))
    return render(request, "ReservationSystemApp/Rental_form.html", {})


def Return(request):
    if request.method == 'POST':
        values = {"gameCopyBarcode_errors": [],
                  "gameCopyBarcode_val": request.POST['gameCopyBarcode'],
                  "gameCopy": None}
        if checkIfGameBarcodeAreEmpty(values, request):
            return render(request, "ReservationSystemApp/Return_form.html",
                          values)
        try:
            gameCopy = GameCopy.objects.get(barcode=request.POST['gameCopyBarcode'])
        except ObjectDoesNotExist as x:
            values['gameCopyBarcode_errors'].append("Game copy not found")
            return render(request, "ReservationSystemApp/Return_form.html",
                          values)
        if gameCopy.state == GameCopy.STATE[1][0]:
            values['gameCopyBarcode_errors'].append("Game not rented")
            return render(request, "ReservationSystemApp/Return_form.html",
                          values)

        values['gameCopy'] = gameCopy
        return render(request, "ReservationSystemApp/Return_form.html", values)
    return render(request, "ReservationSystemApp/Return_form.html", {})


def makeReturn(request, pk):
    print("makeReturn")
    gameCopy = GameCopy.objects.get(id=pk)
    gameCopy.weight = 0
    gameCopy.comments = ""
    gameCopy.state = GameCopy.STATE[1][0]
    gameCopy.client = None
    gameCopy.save()
    return HttpResponseRedirect(reverse("GameDetails", args=(gameCopy.game.id,)))