from django.urls import path
from eat import views
from django.conf import settings
from django.conf.urls.static import static

# path('m/', include('eat.urls')),
app_name = 'eat'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:idx>/<str:date>', views.logindone, name='index_login'),
    path('<str:idx>/<str:date>/mypage', views.mypage_index, name='mypage_profile'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
