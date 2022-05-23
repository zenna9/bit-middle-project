from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from eat.models import diet, login, imgs
from django.db.models import Sum, F, Count, Case, When

# zenna. 페이지 접속 시 최초화면
def index(request) :
    return render(request, 'login.html')

# zenna : 로그인한 메인화면 ==(데이터 있는 경우 try, 없는 경우 except)====================
def logindone(request, idx, date):
    try :
        dietlist = get_list_or_404(diet, user_id=idx, date=date)
        # dietlist.kcal = round(dietlist.kcal,1)
        loginn = get_object_or_404(login, user_id=idx)
        sums = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('tan'))
        need_list = ['dang', 'kcal', 'ji', 'dan']

        for i in need_list :
                sums.update(diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum(i)))
        # 당, 칼로리, 지방, 단백질 총계 리스트 = sums
        # ============================================================================

        dict_percent = {'per_tan': '{}%'.format(round(sums['tan__sum'] / loginn.recommend_tan*100,1))}
        dict_percent.update({'per_kcal': '{}%'.format(round(sums['kcal__sum'] / loginn.recommend_kcal*100,1))})
        dict_percent.update({'per_ji': '{}%'.format(round(sums['ji__sum'] / loginn.recommend_ji*100,1))})
        dict_percent.update({'per_dan': '{}%'.format(round(sums['dan__sum'] / loginn.recommend_dan*100,1))})

        context = {'dietlist': dietlist, 'idx':idx, 'date':date,'sums':sums, 'logininfo': loginn, 'percent': dict_percent}
        # print("==============================",dict_percent)
        return render(request, 'index.html', context)
    except :
        context = {'idx':idx,'date':date}
        return render(request, 'index_null.html', context)


def team_index(request):
    return render(request, 'introduce.html')

#  날짜별 나의 사진을 선택할수 있는 링크
def mypage_index(request, idx, date):
    try : # 사진이 있으면서 날짜를 선택하지 않았을경우
        dietlist = get_list_or_404(diet, user_id=idx, date=date)
        context = {'idx': idx, 'date': date, 'dietlist': dietlist}
        return render(request, "myprofile.html", context)
    except : # 사진이 없을경우
        context = {'idx':idx,'date':date}
        return render(request, 'myprofile_null.html', context)

# 전체 사진 보기 /내 모든 사진을 볼수있는 링크 / 내가 올린사진이 없으면 except
def profile_allphoto(request, idx):
    try:
        dietlist = get_list_or_404(diet, user_id=idx)
        context = {'idx': idx, 'dietlist': dietlist}
        return render(request, "myprofile_all.html", context)
    except:
        context = {'idx': idx}
        return render(request, 'myprofile_null.html', context)

def tutorial_page(request):
    return render(request, 'tutorial.html')

def helthinfo(request, idx):
    try:
        dietlist = get_list_or_404(diet, user_id=idx)
        context = {'idx': idx, 'dietlist': dietlist}
        return render(request, 'helth.html', context)
    except:
        context = {'idx': idx}
        return render(request, 'helth.html', context)


# def helthinfo_chart(request):
#
#
#
#     import pymysql
#     dbCon = pymysql.connect(host='localhost', port='3306', user='user1', passwd='1111', db='bitteam2')
#     cursor = dbCon.cursor()
#     cursor.execute("SELECT*FROM table")
#     dailyinfo = cursor.fetchall()
#     cursor.close()
#     dbCon.close()
#
#     return render(request,'helth.html',{
#         'title':'하루 총 칼로리량',
#         'dtitle1' : '아침',
#         'dtitle2' : '점심',
#         'dtitle3' : '저녁',
#         'dailyinfo' : dailyinfo
#     })
#
#
# # 템플레이트 코드
# title:{
#     display:true,
#     text:'{{title}}'
# }
#
# label: '{{dtitle1}}',
# label: '{{dtitle1}}',
# labels: [{% for i in dailyinfo %}}'{{i.O}}',{% endfor %}],
#
# data: [{% for i in dailyinfo %}}'{{i.2}}',{% endfor %}],
# data: [{% for i in dailyinfo %}}'{{i.2}}',{% endfor %}],
#
#
# var color = Cart.helpers.color;
# var barChartData = (
#     labels : [{% for i in daily_info %}]'{{i.0}}',{{% endfor %}},
#     datasets:[(
#         label : '{{dtitle1}}';
#         backgrountColor : color (window.chartColor.red).alpha(0,5).rgbstring(),
#         borderWidth: 1;
#         data : [{% for i in dbinfo %}]'{{i.}}',(% endfor %)
# ),(     label : '{{dtitle1}}',
# ),(     label : '{{dtitle2}}',
# ),(     label : '{{dtitle3}}',
#
#
#
# )]
# )