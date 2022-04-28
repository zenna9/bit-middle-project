from django.urls import path
from analysis_photo import views
from django.conf import settings
from django.conf.urls.static import static

# url/ph/

app_name = 'analysis_photo'

urlpatterns = [
    path('', views.f_fu, name='f_fu'),
    path('<int:b_hc_id>/', views.f_hp, name='f_hp')
]

if settings.DEBUG : 
    urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
    )
