from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from eat.models import diet, login, imgs
from django.db.models import Sum, F, Count, Case, When

def index(request) :
    return render(request, 'login.html')

# 로그인한 메인화면 ======================
def logindone(request, idx, date):
    try : 
        dietlist = get_list_or_404(diet, user_idx=idx, date=date)
        loginn = get_object_or_404(login, user_id=idx)

        
        sums = diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum('tan'))

        need_list = ['dang', 'kcal', 'ji', 'dan']

        for i in need_list :
                sums.update(diet.objects.filter(date=date).filter(user_idx=idx).aggregate(Sum(i)))
        # 당, 칼로리, 지방, 단백질 총계 리스트 = sums
        # ============================================================================

        dict_percent = {'per_tan': '{}%'.format(round(sums['tan__sum'] / loginn.recommend_tan*100,1))}
        dict_percent.update({'per_kcal': '{}%'.format(round(sums['kcal__sum'] / loginn.recommend_kcal*100,1))})
        dict_percent.update({'per_ji': '{}%'.format(round(sums['ji__sum'] / loginn.recommend_ji*100,1))})
        dict_percent.update({'per_dan': '{}%'.format(round(sums['dan__sum'] / loginn.recommend_dan*100,1))})

        context = {'dietlist': dietlist, 'idx':idx, 'date':date,'sums':sums, 'logininfo': loginn, 'percent': dict_percent}
        return render(request, 'index.html', context)
    except :
        return render(request, 'no_data.html')


