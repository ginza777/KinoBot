from .main_bot.urls import *  # noqa   import urlpatterns
from .api import  UserApi,LocationApi,ChannelApi,MovieTrailerApi,MovieApi,MovieChannelApi,UnnecessaryWordFilterApi
from django.urls import path
from .apps import BotConfig

urlpatterns = urlpatterns + [
    path(f'api/v1/bot/{BotConfig.app_url}/user/', UserApi.as_view(), name='user_to_json'),
    path(f'api/v1/bot/{BotConfig.app_url}/location/', LocationApi.as_view(), name='location_to_json'),
    path(f'api/v1/bot/{BotConfig.app_url}/channel/', ChannelApi.as_view(), name='channel_to_json'),
    path(f'api/v1/bot/{BotConfig.app_url}/movie_trailer/', MovieTrailerApi.as_view(), name='movie_trailer_to_json'),
    path(f'api/v1/bot/{BotConfig.app_url}/movie/', MovieApi.as_view(), name='movie_to_json'),
    path(f'api/v1/bot/{BotConfig.app_url}/movie_channel/', MovieChannelApi.as_view(), name='movie_channel_to_json'),
    path(f'api/v1/bot/{BotConfig.app_url}/unnecessary_word_filter/', UnnecessaryWordFilterApi.as_view(), name='unnecessary_word_filter_to_json'),

]