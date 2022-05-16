from django.urls import path
from analysis_photo import views
from django.conf import settings
from django.conf.urls.static import static

# url/ph/

app_name = 'analysis_photo'

urlpatterns = [
    path('', views.f_fu, name='f_fu'), # zenna
    path('f_uploading', views.f_upload_at_sql, name='f_uas'), # zenna
    path('<int:b_hc_id>/<str:idx>', views.f_hp, name='f_hp') # zenna
]

# zenna : 사진 업로드를 위한 media폴더 설정 구문 
if settings.DEBUG : 
    urlpatterns += static(
    settings.MEDIA_URL,
    document_root = settings.MEDIA_ROOT
    )
