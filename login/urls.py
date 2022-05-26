from django.urls import path
from login import views
# from django.conf import settings
# from django.conf.urls.static import static
from django.views.generic.base import TemplateView

# path('lg/', include('eat.urls')),
app_name = 'login'

urlpatterns = [
    # path('<str:idx>/<str:date>', views.logindone, name='index_login'),
        # 로그인과 로그아웃 회원가입
    path('', TemplateView.as_view(template_name='login.html'), name='loginindex'),
    path('logining/', views.logining, name='logining'),
    path('register/', views.register, name='register'),
    path('register/submit', views.register_submit, name='register_submit'),
    path('success/', TemplateView.as_view(template_name='register_succ.html'), name='mmm'),
    path('newlg/', TemplateView.as_view(template_name='login2.html'), name='lg2')

]
