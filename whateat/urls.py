from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from eat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.logining, name="login"),
    path('ph/', include('analysis_photo.urls')),
    path('m/', include('eat.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
