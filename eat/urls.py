from django.urls import path
from eat import views
from django.conf import settings
from django.conf.urls.static import static

# path('m/', include('eat.urls')),
app_name = 'eat'

urlpatterns = [
    path('', views.index, name='index'),
    path('tutorial', views.tutorial_page, name='tutorial'),
    path('teampage', views.team_index, name='teampage'),
    path('<str:idx>/mypage', views.profile_allphoto, name='my_photos'),
    path('<str:idx>/helthinfo', views.helthinfo, name='helthinfo'),
    path('<str:idx>/<str:date>', views.logindone, name='index_login'),
    path('<str:idx>/<str:date>/mypage', views.mypage_index, name='myprofile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
