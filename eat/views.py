from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from eat.models import diet, login, imgs
from django.db.models import Sum, F, Count, Case, When

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<str:idx>/<slug:date>', views.logindone, name='index_login'),
# ]

def index(request):
    return render(request, 'login.html')

# 로그인한 메인화면 ======================
def logindone(request, idx, date):
    dietlist = get_list_or_404(diet, user_idx=idx, date=date)
    # sum_tan = diet.objects.filter(date=date).aggregate(Sum('tan'))
    # print("*****여깄다~=================================******",sum_tan)
    # sum_tan_percent = str(sum_tan['tan__sum']/10000*100)+'%'
    # print("*****sum tan percent~=================================******",sum_tan_percent)
    # 
    # sumlist = diet.objects.values('date').annotate(tansuSum=Sum('tan'))
    # print("====날짜별로 그룹화한 탄수화물 총계=============",sumlist)
    sumlist2 = diet.objects.filter(date=date).annotate(Sum('kcal')).annotate(Sum('tan')).annotate(Sum('dang')).annotate(Sum('ji')).annotate(Sum('dan')).annotate(Sum('kalsum')).annotate(Sum('inn')).annotate(Sum('salt')).annotate(Sum('kalum')).annotate(Sum('magnesum')).annotate(Sum('chul')).annotate(Sum('ayeon')).annotate(Sum('kolest')).annotate(Sum('transfat'))
    sumlist3 = list(sumlist2.values())
    for i in range(0,14) :
        sum_to_percent = dict()
    context = {'dietlist': dietlist, 'tan': sumlist3}
    return render(request, 'index.html', context)


