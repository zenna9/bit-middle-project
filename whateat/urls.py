
from django.contrib import admin
from django.urls import path, include
from eat import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('<str:user_idx>/<slug:date>', views.index, name='index_login'),

    path('<str:user_idx>/upload_p/', views.upload_p, name='upload_p'),
    # path('parameter/', views.get_post),
    # path('parameter/', views.get_post),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
