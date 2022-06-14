from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

import eat.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', eat.views.tutorial_page, name='tutorial'),
    path('lg/', include ('login.urls')),
    path('m/', include('eat.urls')),
    path('ph/', include('analysis_photo.urls')),
    path('auth/', include('users.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
