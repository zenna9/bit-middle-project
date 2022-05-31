from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404

import eat.models
from eat.models import diet, login, imgs
from django.db.models import Sum, F, Count, Case, When
from django.http import Http404
import urllib.request
import pandas as pd
import pymysql

# 채은 : 페이지 접속 시 최초화면
def index(request) :
    return render(request, 'login.html')

# 채은 : 로그인한 메인화면 ==(데이터 있는 경우 try, 없는 경우 except)====================

def logindone(request,date):
    # try :
        idx = request.session['idx']
        # dietlist = get_list_or_404(diet, user_id=idx, date=date)
        dietlist = diet.objects.filter(user_id=idx, date=date)
        print("this is dietlist : =========", dietlist)
        if dietlist.exists():
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
            return render(request, 'index.html', context)
        else : 
            context = {'idx':idx,'date':date}
            return render(request, 'index_null.html', context)
    # except :
    # except diet.objects.filter(user_id=idx, date=date).DoesNotExist:

# 경준
def team_index(request):
    return render(request, 'introduce.html')

# 경준
#  날짜별 나의 사진을 선택할수 있는 링크
def mypage_index(request, idx, date):
    try : # 사진이 있으면서 날짜를 선택하지 않았을경우
        dietlist = get_list_or_404(diet, user_id=idx, date=date)
        context = {'idx': idx, 'date': date, 'dietlist': dietlist}
        return render(request, "myprofile.html", context)
    except : # 사진이 없을경우
        context = {'idx':idx,'date':date}
        return render(request, 'myprofile_null.html', context)

#경준
# 전체 사진 보기/ 내 모든 사진을 볼수있는 링크/ 내가 올린사진이 없으면 except
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
        chart_data = get_list_or_404(diet, user_id=idx)[:5]
        # 1. 어떤 아이디의 모든 영양 정보값 추출
        # -------------1번까지 데이터 차트 적용 확인--------------------
        # 2. 어떤 날짜에 해당하는 영양 정보값 더하기
        # 3. 어떤 아이디에 해당되는 날짜데이터와 영양정보데이터 list 생성하기

        # 4. 가장 최신의 날짜 3개의 데이터에 해당하는 결과값을 chart에 반영
        # 5. 가장 최신의 날짜에 해당하는 탄단지 비율 데이터 찾기
        print(chart_data)
        food_labels= [] #날짜 데이터
        food_kcal= [] #kcal 데이터
        food_salt= [] #salt 데이터
        all_data= [] #모든 데이터(테스트용)

        for foodinfo in chart_data:
            # 데이터 전처리
            # 날짜 데이터의 date타입을 str으로 변환
            after_date = (foodinfo.date).strftime('%Y-%m-%d')
            # kcal, salt 데이터 1의 자리 숫자 반올림
            food_data2 = round(foodinfo.kcal, -1)
            food_data3 = round(foodinfo.salt, -1)

            # list append
            food_labels.append(after_date)
            food_kcal.append(food_data2)
            food_salt.append(food_data3)

            # 아이디의 날짜별 데이터
            # MySQL Connectrion 연결
            conn = pymysql.connect(host='192.168.0.29', port=3306, user='user1', passwd='1111', db='bitteam2', charset='utf8')
            # conn = pymysql.connect(host='ec2-43-200-16-33.ap-northeast-2.compute.amazonaws.com', port=3306, user='user1', passwd='1111', db='bitteam2', charset='utf8')
            # Connection 으로부터 결과를 얻어올때 사용할 cursor 생성
            curs = conn.cursor()
            # 쿼리문 작성
            sql = "SELECT `user_id`, date_format(`date`,'%Y-%m-%d') as `date`, TRUNCATE(SUM(`kcal`),-1) AS 'daily_kcal', TRUNCATE(SUM(`salt`),-1) AS 'daily_salt'  FROM eat_diet WHERE `user_id` = '" + idx + "' GROUP BY `date`;"
            # 쿼리문 실행(execute)
            curs.execute(sql)
            # 실행결과 모두 읽어보기 fetch all
            dailyinfo = curs.fetchall()
            # 변수 닫아주기
            curs.close()
            conn.close()


            # tuple 형태 데이터 list 변환
            print(dailyinfo, type(dailyinfo))
            data_list=[list(row) for row in dailyinfo]
            print(data_list, type(data_list))




            # 총 데이터를 한 변수에 담기위해서 dict
            all_data.append({"id": idx,
                             "date": after_date,
                             "s_kcal": food_data2,
                             "s_salt": food_data3,
                            });
        context = {'idx':idx, 'labels':food_labels,'kcal_data':food_kcal, 'salt_data':food_salt}

        return render(request, 'helth.html', context)



# def chart(request,idx):
#     labels=[]
#     data=[]
#     # (round(Sum('kcal'), -1) groupby(date=date) agg(Sum('kcal')
#     chart_data = diet.objects.filter(user_id=idx)[:5]
#     for data in chart_data:
#         labels.append(data.date)
#         data.append(data.kcal)
#     return render (request, 'helth.html',{
#         'labels' : labels,
#         'data' : data
#     })

    # html
    # sums = diet.objects.filter(date=date).filter(user_id=idx).aggregate(Sum('tan'))
# def helthinfo_chart(request):
#
    # dbCon = pymysql.connect(host='localhost', port='3306', user='user1', passwd='1111', db='bitteam2')
    # cursor = dbCon.cursor()
    # cursor.execute("SELECT `user_id`, `date`, TRUNCATE(SUM(`kcal`),-1) AS "daily_kcal", TRUNCATE(SUM(`salt`),-1) AS "daily_salt"  FROM eat_diet WHERE `user_id` = 'rhrudwnszoq' GROUP BY `date`;")
    # dailyinfo = cursor.fetchall()
    # cursor.close()
    # dbCon.close()
    # print(dailyinfo,type(dailyinfo))
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