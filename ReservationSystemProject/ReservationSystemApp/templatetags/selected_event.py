from django import template
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

from ReservationSystemApp.models import Event

register = template.Library()

@register.simple_tag(takes_context=True)
def selected_event(context, request, user):
    if user.is_anonymous():
        return ""
    try:
        event = Event.objects.get(id=request.session['event_id'])
    except KeyError:
        return mark_safe(u'<a href="{0}" class="button">Select Event</a>'.format(reverse("SelectEvent", args=())))
    return mark_safe(u'<b>Selected Event:</b> {}'.format(event))


@register.simple_tag(takes_context=True)
def login(context, user):
    if user.is_anonymous():
        return mark_safe(u'<a href="{0}" class="button">Login</a>'.format(reverse("login", args=())))
    return mark_safe(u'User: {} <a href="{}" class="button">Logout</a><a href="{}" class="button">Change password</a>'.
                     format(user, reverse("logout"), reverse("changePassword") ))


@register.simple_tag(takes_context=True)
def make_menu(context, user):
    if user.is_anonymous():
        return ""

    menu_data = []

    if user.is_superuser:
        menu_data.append([reverse("operatorList"), "Operator List"])
        menu_data.append([reverse("ListEvent"), "Event List"])
        menu_data.append([reverse("GamesList"), "Game List"])

    menu_data.append([reverse("Rental"), "New Rental"])
    menu_data.append([reverse("Return"), "Return"])
    menu_data.append([reverse("RentalList"), "Rental List"])
    menu_data.append([reverse("NewClient"), "New client"])
    menu_data.append([reverse("ClientList"), "Client list"])

    menu_data.append([reverse("SelectEvent"), "Select Event"])

    if user.is_superuser:
        menu_data.append([reverse("statistics"), "Statistics"])

    menu = [u'<a href="{0}"  class="button">{1}</a>'.format(url[0], url[1]) for url in menu_data]

    return mark_safe(' '.join(menu))


@register.simple_tag(takes_context=True)
def make_menu2(context, user):
    menu_data = []
    menu2_Operator(context, menu_data)
    menu2_Event(context, menu_data)
    menu2_Game(context, menu_data)

    menu = [u'<a href="{0}"  class="button">{1}</a>'.format(url[0], url[1]) for url in menu_data]
    return mark_safe(' '.join(menu))


def menu2_Game(context, menu_data):
    path = context.request.get_full_path()
    urls_list = [reverse("GamesList"),
                 reverse("NewGame"),
                 reverse("NewGameCopy"),
                 "/GameUpdate/",
                 "/GameDetails/",
                 "/DeleterGameCopy/",
                 "/DeleteGame/",
                 "/GameCopyDetails/"]
    if any(s in path for s in urls_list):
        menu_data.append([reverse("NewGame"), "New Game"])


def menu2_Operator(context, menu_data):
    if context.request.get_full_path() == reverse("operatorList"):
        menu_data.append([reverse("addOperator"), "New Operator"])


def menu2_Event(context, menu_data):
    path = context.request.get_full_path()
    urls_list = [reverse("ListEvent"), reverse("NewEvent"), "/EventUpdate/", "/EventDetails/"]
    if any(s in path for s in urls_list):
        menu_data.append([reverse("NewEvent"), "New Event"])


