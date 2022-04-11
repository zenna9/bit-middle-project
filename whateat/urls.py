
from django.contrib import admin
from django.urls import path
from eat import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload_p', views.upload_p, name='upload_p'),

]
