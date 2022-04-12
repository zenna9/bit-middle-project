from django.contrib import admin
from django.urls import path, include
from eat import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('<str:idx>/<slug:date>', views.logindone, name='index_login'),

    path('upload_p/', views.upload_p, name='upload_p'),
    path('your_photo/', views.your_photo, name='your_photo'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
