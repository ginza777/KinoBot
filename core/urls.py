import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bots.common_bot.urls import urlpatterns as bot_urlpatterns

from . import views
from .swagger.schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path('rosetta/', include('rosetta.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', views.index, name="index"),
]

# bots
urlpatterns += bot_urlpatterns

# swagger
urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
