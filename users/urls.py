from django.urls import path
from . import views

app_name = 'user'

urlpatterns =[
  path('signup', views.member_register, name='signup'),
  path('member_idcheck', views.member_idcheck, name="member_idcheck"),
  path('member_insert', views.member_insert, name="member_insert"),
  path('member_login', views.member_login, name="member_login"),
  path('member_logout', views.member_logout, name="member_logout"),
  path('edit', views.member_edit, name="member_edit"),
  path('member_update', views.member_update, name="member_update"),
  path('login', views.login_view, name='login'),
  path('logout', views.logout_view, name='logout'),
]