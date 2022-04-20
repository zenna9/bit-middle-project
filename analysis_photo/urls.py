from django.urls import path
from analysis_photo import views
from django.conf import settings
from django.conf.urls.static import static

# url/ph/

app_name = 'analysis_photo'

urlpatterns = [
    path('', views.uploadFile, name='uploadFile'),
    path('<int:document_id>/', views.upload2, name='upload2')
]

if settings.DEBUG : 
    urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
    )
