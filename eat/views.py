from django.shortcuts import render, get_object_or_404, redirect
from eat.models import diet, login, imgs
from django.db.models import Sum

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<str:idx>/<slug:date>', views.logindone, name='index_login'),
# ]

def index(request):
    return render(request, 'login.html')

# 로그인한 메인화면 ======================
def logindone(request, idx, date):
    dietlist = get_object_or_404(diet, user_idx=idx, date=date)
    sum_tan = diet.objects.filter(date=date).aggregate(Sum('tan'))
    print("*****여깄다~=================================******",sum_tan)
    sum_tan_percent = str(sum_tan['tan__sum']/10000*100)+'%'
    print("*****sum tan percent~=================================******",sum_tan_percent)
    context = {'dietlist': dietlist, 'tan': sum_tan_percent}

    return render(request, 'index.html', context)

def your_photo(request):
    return render(request, '../analysis_photo/templates/your_photo.html')



