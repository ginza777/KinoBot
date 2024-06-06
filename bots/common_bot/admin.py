from django.contrib import admin

from .main_bot.admin import *  # noqa
from .models import Movie, MovieChannel, Unnecessary_word_filter, MovieTrailer


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', "view_count", 'file_unique_id', "code", "caption", "has_trailer"]
    search_fields = ('code', 'caption')


@admin.register(MovieTrailer)
class MovieTrailerAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_unique_id']
    search_fields = ('file_unique_id',)


@admin.register(MovieChannel)
class MovieChannelAdmin(admin.ModelAdmin):
    list_display = ['id', 'channel_id', 'channel_username']
    search_fields = ('channel_id', 'channel_username')


@admin.register(Unnecessary_word_filter)
class UnnecessaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'word']
    search_fields = ('word',)
