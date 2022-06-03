from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView


urlpatterns = [
    path('ph/', include('analysis_photo.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='tutorial.html'), name='tutorial'),
    path('lg/', include ('login.urls')),
    path('m/', include('eat.urls')),
    # path('accounts/', include('allauth.urls')), #채은 : 구글 로그인기능

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
