from django.urls import path
from . import views

app_name = 'user'

urlpatterns =[
  path('signup', views.member_register, name='signup'),
  path('member_idcheck', views.member_idcheck, name="member_idcheck"),
  path('member_insert', views.member_insert, name="member_insert"),
  path('member_login', views.member_login, name="member_login"),
  path('login', views.login_view, name='login'),
  path('logout', views.logout_view, name='logout'),
]