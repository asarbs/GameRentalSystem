# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Game
from models import GameCopy
from models import Event
from models import Client
from models import GameCopyHistory

# Register your models here.


class GameCopyInline(admin.StackedInline):
    model = GameCopy
    extra = 0


class GameAdmin(admin.ModelAdmin):
    inlines = [GameCopyInline]


class EventAdmin(admin.ModelAdmin):
    pass


class ClientAdmin(admin.ModelAdmin):
    pass


class GameCopyHistoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Game,GameAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(GameCopyHistory, GameCopyHistoryAdmin)
