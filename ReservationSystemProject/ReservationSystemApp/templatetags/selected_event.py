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
    return mark_safe(u'<a href="{0}" class="button">Logout</a>'.format(reverse("logout", args=())))