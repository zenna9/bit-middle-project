from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from eat.models import diet, login, imgs
from django.db.models import Sum, F, Count, Case, When

# urlpatterns = [
#     path('', views.index, name='index'),
#     path('<str:idx>/<slug:date>', views.logindone, name='index_login'),
# ]

# 로그인하라는 1번 화면
def login(request):
    return render(request, 'login.html')

def index(request):
    return render(request, 'login.html')

# 로그인한 메인화면 ======================
def logindone(request, idx, date):
    dietlist = get_list_or_404(diet, user_idx=idx, date=date)

    sums = diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('tan'))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('dang')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('ji')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('dan')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('kalsum')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('inn')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('salt')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('kalum')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('magnesum')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('chul')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('ayeon')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('kolest')))
    sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('transfat')))

    # sums = [sum_tan,sum_dang, sum_ji, sum_dan, sum_kalsum, sum_inn, sum_salt, sum_kalum, sum_magnesum, sum_chul, sum_ayeon, sum_kolest, sum_transfat]
    print("*****여깄다~=================================******",sums)
    # sum_tan_percent = str(sum_tan['tan__sum']/10000*100)+'%'
    # print("*****sum tan percent~=================================******",sum_tan_percent)
    #
    # sumlist = diet.objects.values('date').annotate(tansuSum=Sum('tan'))
    # print("====날짜별로 그룹화한 탄수화물 총계=============",sumlist)
    # sumlist2 = diet.objects.filter(date=date).aggregate(Sum('kcal')).aggregate(Sum('tan')).aggregate(Sum('dang')).aggregate(Sum('ji')).aggregate(Sum('dan')).aggregate(Sum('kalsum')).aggregate(Sum('inn')).aggregate(Sum('salt')).aggregate(Sum('kalum')).aggregate(Sum('magnesum')).aggregate(Sum('chul')).aggregate(Sum('ayeon')).aggregate(Sum('kolest')).aggregate(Sum('transfat'))
    # sumlist3 = list(sumlist2.values())
    # for i in range(0,14) :
        # sum_to_percent = dict()
    context = {'dietlist': dietlist, 'idx':idx, 'date':date,'sums':sums}
    return render(request, 'index.html', context)


