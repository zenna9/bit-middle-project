from django.urls import path
from analysis_photo import views

# url/ph/

app_name = 'analysis'

urlpatterns = [
    path('your_photo/', views.your_photo, name='your_photo'),
]
