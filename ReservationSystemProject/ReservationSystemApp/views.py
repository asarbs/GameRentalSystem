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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django_tables2 import RequestConfig
from django_filters.views import FilterView

import operator
import datetime

from form import GameForm
from form import GameCopyItemFormset
from form import EventForm
from form import UserForm
from form import ChangePasswordForm
from models import Client
from models import Game
from models import GameCopy
from models import Event
from models import GameCopyHistory
from tables import GameTable
from tables import GameCopyTable
from filters import GameFilter
from filters import GameCopyFilter


# Create your views here.

@login_required(login_url='/login/')
def main(request):
    return render(request, 'main.html', {})


class NewClientView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Client
    fields = ['name', 'surname', 'age', 'gender', 'barcode']

    def get_success_url(self):
        return reverse("ClientDetails", args=(self.object.id,))


class ClientDetails(LoginRequiredMixin,DetailView):
    model = Client


class ClientList(LoginRequiredMixin,ListView):
    model = Client

@login_required(login_url='/login/')
def DeleteClient(request, pk):
    Client(id=pk).delete()
    return HttpResponseRedirect(reverse("ClientList"))


class ClientEdit(LoginRequiredMixin,UpdateView):
    model = Client
    fields = ['name', 'surname', 'age', 'gender', 'barcode']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("ClientDetails", args=(self.object.id,))


class NewGameView(LoginRequiredMixin,CreateView):
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
        Called if all forms are valid. Creates a Game instance along with
        associated GameCopy and then redirects to a
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


class GameDetails(LoginRequiredMixin, DetailView):
    model = Game

    def get_object(self, queryset=None):
        object = super(GameDetails,self).get_object()
        gameCopy = GameCopy.objects.filter(game=object)
        object.gameCopy = gameCopy
        object.gameCopyItemFormset = GameCopyItemFormset()
        return object


class GameList(LoginRequiredMixin, ListView):
    model = Game
    filter_class = GameFilter

    def get_queryset(self, **kwargs):
        return Game.objects.all()

    def get_context_data(self, **kwargs):
        context = super(GameList, self).get_context_data(**kwargs)
        filter = GameFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        table = GameTable(filter.qs)
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['filter'] = filter
        context['table2Render'] = table
        return context


class GameEdit(LoginRequiredMixin, UpdateView):
    model = Game
    fields = ['name', 'number']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse("GameDetails", args=(self.object.id,))


@login_required(login_url='/login/')
def NewGameCopy(request):
    game = Game.objects.get(id=request.GET['game_id'])
    GameCopy(barcode=request.POST['gamecopy_set-0-barcode'],
                        weight=request.POST['gamecopy_set-0-weight'],
                        comments=request.POST['gamecopy_set-0-comments'],
                        state=request.POST['gamecopy_set-0-state'],
                        game=game).save()
    return HttpResponseRedirect(reverse("GameDetails", args=(request.GET['game_id'],)))


class GameCopyDetails(LoginRequiredMixin, DetailView):
    model = GameCopy

    def get_object(self, queryset=None):
        object = super(GameCopyDetails,self).get_object()
        gameCopyHistory = GameCopyHistory.objects.filter(gameCopy=object)
        object.gameCopyHistory = gameCopyHistory
        return object


@login_required(login_url='/login/')
def DeleteGamesCopy(request, pk):
    GameCopy(id=pk).delete()
    return HttpResponseRedirect(reverse("GameDetails", args=(request.GET['game_id'],)))


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def Rental(request):
    if request.method == 'POST':
        values = {"gameCopyBarcode_val": request.POST['gameCopyBarcode'],
                  "clientBarcode_val": request.POST['clientBarcode'],
                  "comment_val": request.POST['comment'],
                  "gameCopyWeight_val":  request.POST['gameCopyWeight'],
                  "numberOfRentalDays_val": request.POST['numberOfRentalDays']}
        errors = {"gameCopyBarcode_errors": [],
                  "clientBarcode_errors": [],
                  "gameCopyWeight_errors": [],
                  "numberOfRentalDays_errors": []}

        if checkIfBarcodesAreEmpty(errors, request):
            values.update(errors)
            return render(request, "ReservationSystemApp/Rental_form.html",
                          values)
        try:
            gameCopy = GameCopy.objects.get(barcode=request.POST['gameCopyBarcode'])
        except ObjectDoesNotExist as x:
            errors['gameCopyBarcode_errors'].append("Copy not found") #TODO: translation
        try:
            clinet = Client.objects.get(barcode=request.POST['clientBarcode'])
        except ObjectDoesNotExist as x:
            errors['clientBarcode_errors'].append("Client not found") #TODO: translation

        if gameCopy.state == GameCopy.STATE[0][0]:
            errors['gameCopyBarcode_errors'].append("Game rented") #TODO: translation

        if(int(request.POST['numberOfRentalDays']) < 1 or int(request.POST['numberOfRentalDays']) > 50):
            errors['numberOfRentalDays_errors'].append(u'Nie prawidłowa liczba dni wyporzyczenia')


        if len(errors['gameCopyBarcode_errors']) > 0 or len(errors['clientBarcode_errors']) > 0 or len(errors['gameCopyWeight_errors']) > 0:
            values.update(errors)
            return render(request, "ReservationSystemApp/Rental_form.html", values)

        try:
            event = Event.objects.get(id=request.session['event_id'])
        except KeyError:
            return HttpResponseRedirect(reverse("SelectEvent"))

        now = datetime.datetime.now()
        gameCopy.weight = request.POST['gameCopyWeight']
        gameCopy.comments = request.POST['comment']
        gameCopy.state = GameCopy.STATE[0][0]
        gameCopy.client = clinet
        gameCopy.rentalDateTime = now
        gameCopy.returnDateTime = now + datetime.timedelta(days=int(request.POST['numberOfRentalDays']))
        gameCopy.save()



        gameCopyHistory = GameCopyHistory(gameCopy=gameCopy, state=GameCopy.STATE[0][0], user=request.user,
                                          client=clinet, event=event, game=gameCopy.game)
        gameCopyHistory.save()

        return HttpResponseRedirect(reverse("GameDetails", args=(gameCopy.game.id,)))

    return render(request, "ReservationSystemApp/Rental_form.html", {'numberOfRentalDays_val': None})


@login_required(login_url='/login/')
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


def GameCopyReturn(request, pk):
    values = {"gameCopyBarcode_errors": [],
              "gameCopyBarcode_val": [],
              "gameCopy": None}
    try:
        gameCopy = GameCopy.objects.get(id=pk)
    except ObjectDoesNotExist as x:
        values['gameCopyBarcode_errors'].append("Game copy not found")
        return render(request, "ReservationSystemApp/Return_form.html", values)
    if gameCopy.state == GameCopy.STATE[1][0]:
        values['gameCopyBarcode_errors'].append("Game not rented")
        return render(request, "ReservationSystemApp/Return_form.html",values)

    values['gameCopy'] = gameCopy
    return render(request, "ReservationSystemApp/Return_form.html", values)

@login_required(login_url='/login/')
def makeReturn(request, pk):

    gameCopy = GameCopy.objects.get(id=pk)

    try:
        event = Event.objects.get(id=request.session['event_id'])
    except KeyError:
        return HttpResponseRedirect(reverse("SelectEvent"))
    gameCopyHistory = GameCopyHistory(gameCopy=gameCopy, state=GameCopy.STATE[1][0], user=request.user, client=gameCopy.client,
                                      event=event, game=gameCopy.game)
    gameCopyHistory.save()


    gameCopy.weight = 0
    gameCopy.comments = ""
    gameCopy.state = GameCopy.STATE[1][0]
    gameCopy.client = None
    gameCopy.rentalDateTime = None
    gameCopy.returnDateTime = None
    gameCopy.save()



    return HttpResponseRedirect(reverse("GameDetails", args=(gameCopy.game.id,)))


class NewEvent(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'ReservationSystemApp/event_form.html'

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("EventDetails", args=(self.object.id,))


class EventDetails(LoginRequiredMixin, DetailView):
    model = Event

    def get_object(self, queryset=None):
        object = super(EventDetails, self).get_object()
        games = Game.objects.all()
        data = []
        for game in games:
            count_loan = GameCopyHistory.objects.filter(event=object, game=game, state=GameCopy.STATE[0][0]).count()
            count_return = GameCopyHistory.objects.filter(event=object, game=game, state=GameCopy.STATE[1][0]).count()
            data.append({"game": game, "count_loan": count_loan, "count_return": count_return})

        data.sort(key=operator.itemgetter('count_loan'))

        object.statistics = data
        return object


class ListEvent(LoginRequiredMixin, ListView):
    model = Event


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'ReservationSystemApp/event_update_form.html'

    def get_success_url(self):
        return reverse("EventDetails", args=(self.object.id,))


@login_required(login_url='/login/')
def SelectEvent(request):
    if request.method == 'POST':
        request.session['event_id'] = request.POST['slected_event']
    events = Event.objects.all()
    return render(request, "ReservationSystemApp/select_event_form.html", {"events": events})


@login_required(login_url='/login/')
def addUser(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        if uf.is_valid():
            user = uf.save()
            return HttpResponseRedirect("/")
    else:
        uf = UserForm(prefix='user')
    return render(request, 'ReservationSystemApp/addUser.html', {"form": uf})


@login_required(login_url='/login/')
def changePassword(request):
    if request.method == 'POST':
        changePasswordForm = ChangePasswordForm(data=request.POST, user=request.user)
        if changePasswordForm.is_valid():
            changePasswordForm.save()
            return HttpResponseRedirect("/logout/")
    else:
        changePasswordForm = ChangePasswordForm(user=request.user)
    return render(request, "ReservationSystemApp/changePassword.html", {"form": changePasswordForm})


class OperatorList(ListView):
    model = User


@login_required(login_url='/login')
def DeactivateOperator(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('operatorList'))


@login_required(login_url='/login')
def ActivateOperator(request, pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('operatorList'))


def statistics(request):
    games = Game.objects.all()
    data = []
    for game in games:
        count_loan = GameCopyHistory.objects.filter(game=game, state=GameCopy.STATE[0][0]).count()
        count_return = GameCopyHistory.objects.filter(game=game, state=GameCopy.STATE[1][0]).count()
        data.append({"game": game, "count_loan": count_loan, "count_return": count_return})

    data.sort(key=operator.itemgetter('count_loan'))
    return render(request, "ReservationSystemApp/statistics.html", {"data": data})


class RentalList(LoginRequiredMixin, ListView):
    model = GameCopy
    filter_class = GameCopyFilter

    def get_queryset(self, **kwargs):
        qs = GameCopy.objects.filter(state=GameCopy.STATE[0][0])
        return qs

    def get_context_data(self, **kwargs):
        context = super(RentalList, self).get_context_data(**kwargs)
        myFilter = GameCopyFilter(self.request.GET, queryset=self.get_queryset(**kwargs))
        table = GameCopyTable(myFilter.qs)
        RequestConfig(self.request, paginate={'per_page': 30}).configure(table)
        context['filter'] = myFilter
        context['table2Render'] = table
        return context
