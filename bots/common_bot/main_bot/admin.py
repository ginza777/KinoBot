from django.conf import settings
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from  ..logsender.models import * #
from .models import Location, User, Channel, BotToken
from ..default_handlers.broadcast_message.utils import send_one_message
from ..forms import BroadcastForm
from ..tasks import broadcast_message


@admin.register(BotToken)
class BotTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'username']


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'channel_username', 'channel_id']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id",
        'user_id', 'username', 'first_name', 'last_name',
        'language_code', 'deep_link', "is_blocked_bot","created_at","updated_at"
    ]
    list_filter = ["is_blocked_bot", ]
    search_fields = ('username', 'user_id')

    actions = ['broadcast']

    def broadcast(self, request, queryset):
        """ Select users via check mark in django-admin panel, then select "Broadcast" to send message"""
        user_ids = queryset.values_list('user_id', flat=True).distinct().iterator()
        if 'apply' in request.POST:
            broadcast_message_text = request.POST["broadcast_text"]

            if settings.DEBUG:  # for test / debug purposes - run in same thread
                for user_id in user_ids:
                    send_one_message(
                        user_id=user_id,
                        text=broadcast_message_text,
                    )
                self.message_user(request, f"Just broadcasted to {len(queryset)} users")
            else:
                broadcast_message.delay(text=broadcast_message_text, user_ids=list(user_ids))
                self.message_user(request, f"Broadcasting of {len(queryset)} messages has been started")

            return HttpResponseRedirect(request.get_full_path())
        else:
            form = BroadcastForm(initial={'_selected_action': user_ids})
            return render(
                request, "admin/broadcast_message.html", {'form': form, 'title': u'Broadcast message'}
            )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id']


@admin.register(LogSenderBot)
class LogSenderBotAdmin(admin.ModelAdmin):
    list_display = ("id","name", "token", "bot_username", "channel_name", "channel_id", "created_at", "updated_at",)

@admin.register(BackupDbBot)
class BackupDbBotAdmin(admin.ModelAdmin):
    list_display = ("id","name", "token", "bot_username", "channel_name", "channel_id", "created_at", "updated_at",)



__all__ = ['UserAdmin', 'LocationAdmin', 'ChannelAdmin','LogSenderBotAdmin','BackupDbBotAdmin',]
