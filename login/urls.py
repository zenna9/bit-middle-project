from django.urls import path
from login import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

# path('m/', include('eat.urls')),
app_name = 'login'

urlpatterns = [
    # path('<str:idx>/<str:date>', views.logindone, name='index_login'),
        # 로그인과 로그아웃 회원가입
    path('', TemplateView.as_view(template_name='login.html'), name='loginindex'),
    path('logining/', views.logining, name='logining'),
    path('register/', views.register, name='register'),
]
