from django.shortcuts import render, get_object_or_404, get_list_or_404
from eat.models import diet, login
from django.db.models import Sum
import pandas as pd
import pymysql
import numpy as np
from whateat.mysql import oursql  # mysql 계정정보
from datetime import datetime, timedelta # 경준-0607 건강정보 페이지에서 Footer 이동하려고 만든거
from eat.recommend import recommend_food # 0616 성균이형 추가확인

# 채은 : 페이지 접속 시 최초화면
def index(request) :
    return render(request, 'eat/login.html')

# 채은 : 로그인한 메인화면 ==(if 데이터 있는 경우 , 없는경우)===================
def logindone(request,date):
        idx = request.session['idx']
        # dietlist = get_list_or_404(diet, user_id=idx, date=date)
        dietlist = diet.objects.filter(user_id=idx, date=date)
        if dietlist.exists():
            loginn = get_object_or_404(login, user_id=idx)
            sums = diet.objects.filter(date=date,user_id=idx).aggregate(Sum('tan'))
            need_list = ['dang', 'kcal', 'ji', 'dan'] 

            for i in need_list :
                    sums.update(diet.objects.filter(date=date, user_id=idx).aggregate(Sum(i)))
            # 당, 칼로리, 지방, 단백질 총계 리스트 = sums
            # ============================================================================

            dict_percent = {'per_tan': '{}%'.format(round(sums['tan__sum'] / loginn.recommend_tan*100,1))}
            dict_percent.update({'per_kcal': '{}%'.format(round(sums['kcal__sum'] / loginn.recommend_kcal*100,1))})
            dict_percent.update({'per_ji': '{}%'.format(round(sums['ji__sum'] / loginn.recommend_ji*100,1))})
            dict_percent.update({'per_dan': '{}%'.format(round(sums['dan__sum'] / loginn.recommend_dan*100,1))})

            context = {'dietlist': dietlist, 'idx':idx, 'date':date,'sums':sums, 'logininfo': loginn, 'percent': dict_percent}
            return render(request, 'eat/index.html', context)
        else : 
            context = {'idx':idx,'date':date}
            return render(request, 'eat/index_null.html', context)

# 경준
def team_index(request):
    return render(request, 'eat/introduce.html')

# 경준
#  날짜별 나의 사진을 볼 수 있는 링크
def mypage_index(request, date):
    try : # 사진이 있으면서 날짜를 선택하지 않았을경우
        idx = request.session['idx']
        username = get_object_or_404(login, user_id=idx).user_name  # USER_NAME
        dietlist = get_list_or_404(diet, user_id=idx, date=date)
        context = {'idx': idx, 'date': date, 'dietlist': dietlist,'name':username}
        return render(request, "eat/myprofile.html", context)
    except : # 사진이 없을경우
        context = {'idx':idx,'date':date, 'name':username}
        return render(request, 'eat/myprofile_null.html', context)

#경준
# 전체 사진 보기/ 내 모든 사진을 볼 수 있는 링크/ 내가 올린사진이 없으면 except
def profile_allphoto(request):
    try:
        idx = request.session['idx'] #UESR_ID
        date = datetime.today().strftime("%Y-%m-%d")
        dietlist = get_list_or_404(diet, user_id=idx)
        username= get_object_or_404(login, user_id=idx).user_name #USER_NAME
        context = {'idx': idx, 'dietlist': dietlist,'date':date,'name':username}
        return render(request, "eat/myprofile_all.html", context)
    except:
        context = {'idx': idx,'name':username,'date':date}
        return render(request, 'eat/myprofile_null.html', context)

def tutorial_page(request):
    return render(request, 'eat/tutorial.html')


def helthinfo(request):
    date = datetime.today().strftime("%Y-%m-%d")
    idx = request.session['idx']
    username = get_object_or_404(login, user_id=idx).user_name  # USER_NAME

    # 주간 염분, 칼로리 섭취량 리스트
    month_salt = []
    month_kcal = []

    # 지난 1주간 염분 섭취량 데이터
    start = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d")
    end = datetime.today().strftime("%Y-%m-%d")
    week1_data = diet.objects.filter(date__range=[start, end], user_id=idx).aggregate(Sum('kcal'), Sum('salt'))
    month_kcal.append(round(week1_data.get('kcal__sum')))  # 지난 1주간 칼로리 섭취량 총합
    month_salt.append(round(week1_data.get('salt__sum')))  # 지난 1주간 염분 섭취량 총합

    # 2주전 염분 섭취량 데이터
    start2 = (datetime.now() - timedelta(weeks=2)).strftime("%Y-%m-%d")
    week2_data = diet.objects.filter(date__range=[start2, start], user_id=idx).aggregate(Sum('kcal'), Sum('salt'))
    month_kcal.append(round(week2_data.get('kcal__sum')))  # 2주전 1주간 칼로리 섭취량 총합
    month_salt.append(round(week2_data.get('salt__sum')))  # 2주전 1주간 염분 섭취량 총합

    # 3주전 염분 섭취량 데이터
    start3 = (datetime.now() - timedelta(weeks=3)).strftime("%Y-%m-%d")
    week3_data = diet.objects.filter(date__range=[start3, start2], user_id=idx).aggregate(Sum('kcal'), Sum('salt'))
    month_kcal.append(round(week3_data.get('kcal__sum')))  # 3주전 1주간 칼로리 섭취량 총합
    month_salt.append(round(week3_data.get('salt__sum')))  # 3주전 1주간 소금 섭취량 총합

    # 주간 탄단지 비율데이터
    conn = pymysql.connect(host=oursql.s_host, port=3306, user=oursql.s_user, passwd=oursql.s_passwd, db='bitteam2',
                           charset='utf8')
    curs = conn.cursor()
    sql4 = "SELECT ROUND((t1.wt/t4.alld)*100) AS 't%',	ROUND((t2.wd/t4.alld)*100) AS 'd%', ROUND((t3.wj/t4.alld)*100) AS 'j%' FROM\
        (SELECT ROUND(SUM(`tan`),-1) AS wt FROM bitteam2.eat_diet WHERE date BETWEEN '" + start + "' AND '" + end + "' AND user_id = '" + idx + "' GROUP BY user_id ) AS t1,\
        (SELECT ROUND(SUM(`dan`),-1) AS wd FROM bitteam2.eat_diet WHERE date BETWEEN '" + start + "' AND '" + end + "' AND user_id = '" + idx + "' GROUP BY user_id ) AS t2,\
        (SELECT ROUND(SUM( `ji`),-1) AS wj FROM bitteam2.eat_diet WHERE date BETWEEN '" + start + "' AND '" + end + "' AND user_id = '" + idx + "' GROUP BY user_id ) AS t3,\
        (SELECT ROUND(SUM(`tan`)+SUM(`dan`)+SUM(`ji`)) AS alld FROM bitteam2.eat_diet WHERE date BETWEEN '" + start + "' AND '" + end + "' AND user_id = '" + idx + "' GROUP BY user_id ) AS t4;"
    curs.execute(sql4)
    chart5_data = curs.fetchall()
    chart5_data = [list(row) for row in chart5_data]  # tuple => list 변환
    chart5_data = [round(float(chart5_data[0][i])) for i in range(len(chart5_data[0]))]  # float => int


    # 최근식단 3일간 소금, 칼로리량
    sql = "SELECT `user_id`, date_format(`date`,'%m-%d') as `date`," \
          "ROUND(SUM(`kcal`),-1) AS 'daily_kcal'," \
          "ROUND(SUM(`salt`),-1) AS 'daily_salt' " \
          "FROM eat_diet WHERE `user_id` = '" + idx + "' GROUP BY `date` ORDER BY -`date`;"
    curs.execute(sql)
    dailyinfo = curs.fetchall() # tuple 자료구조
    data_list = [list(row) for row in dailyinfo]  # tuple => list
    data_list = np.array(data_list)  # list => numpy_array


    # 최근식단 3일간 소금, 칼로리량 키값부여
    daily_data = []
    for i in range(len(data_list)):
        if i > 2:
            break  # 최대 3개까지 반복
        daily_data.append({
            "id:": data_list[i][0],
            "date": data_list[i][1],
            "d_kcal": data_list[i][2],
            "d_salt": data_list[i][3]
        })

    # 차트에 반영할 데이터 따로 뽑기위한 코드
    df = pd.DataFrame(daily_data)
    date_list = df['date'].values.tolist()  # 차트 라벨데이터 :날짜 데이터
    kcal_list = df['d_kcal'].values.tolist()  # 차트 데이터 : 3일간 kcal 합
    salt_list = df['d_salt'].values.tolist()  # 차트 데이터 : 3일간 salt 합

    # 최근 날짜의 탄단지 음식의 비율
    sql2 =  "SELECT ROUND((t1.dt/t4.alld)*100) AS 't%',ROUND((t2.dd/t4.alld)*100) AS 'd%',ROUND((t3.dj/t4.alld)*100) AS 'j%' FROM" \
            "(SELECT ROUND(SUM(`tan`)) AS dt FROM bitteam2.eat_diet WHERE `user_id`='" + idx + "' AND `date`='" + date + "') AS t1," \
            "(SELECT ROUND(SUM(`dan`)) AS dd FROM bitteam2.eat_diet WHERE `user_id`='" + idx + "'  AND `date`='" + date + "') AS t2," \
            "(SELECT ROUND(SUM(`ji` )) AS dj FROM bitteam2.eat_diet WHERE `user_id`='" + idx + "'  AND `date`='" + date + "') AS t3," \
            "(SELECT ROUND(SUM(`tan`)+SUM(`dan`)+SUM(`ji`)) AS alld FROM bitteam2.eat_diet WHERE `user_id`='" + idx + "'  AND `date`='" + date + "') AS t4;"
    curs.execute(sql2)
    curs.close()
    conn.close()

    daily_percent = curs.fetchall()          # tuple 자료구조
    daily_percent = np.array(daily_percent)  # array 자료구조
    daily_percent_data = []                  # dict형 list (key값 부여)
    for i in range(len(daily_percent)):
        daily_percent_data.append({ "t%": daily_percent[i][i], "d%": daily_percent[i][i+1], "j%": daily_percent[i][i+2] });

    percent_label = list(daily_percent_data[0].keys())  # 하루 탄단지 라벨
    percent_data = list(daily_percent_data[0].values())  # 하루 탄단지 데이터
    # percent_data = [round(float(percent_data)) for i in range(len(percent_data))]  # float => int 성균ver
    percent_data = [ int(i) for i in percent_data ]  # float => int 경준ver

    # 성균 : 음식추천 모듈 가져와서 리턴값에 업데이트
    lack_percent = [round(100-(percent_data[i])) for i in range(len(percent_data))]
    rcfoodsinfo=recommend_food(request,date)
    # 리턴값: {부족영양소 코멘트 / 부족영양소1 / 부족영양소2 / 추천음식 (2종) / 추천음식명1 / 추천음식명2 / 탄단지외 영양소 일일권장량 대비 퍼센트값 리스트 (for 경준)}
    # 리턴값구성 - recommend_data= {'rComments': comment, 'lackN1':r1, 'lackN2':r2, 'recommendFoods': f'{r1_recommend.index[0]}({r1}:{r1_recommend_p}%), {r2_recommend.index[0]}({r2}:{r2_recommend_p}%)',/
    #                   'r1': r1_recommend.index[0], 'r2': r2_recommend.index[0], 'N_percent': eat_lst[3:]}

    # 추천음식 데이터 recommend_data={{ key값 }}
    # context = {'idx':idx, 'labels':food_labels,'kcal_data':food_kcal, 'salt_data':food_salt}
    #  기존에 임시로 띄어놓은 차트에 해당하는 데이터 가져오기



    # context = {'mydata': daily_data, 'date':date,'idx': idx, 'name': name_list, 'labels':date_list, 'kcal_data':kcal_list,
    #            'salt_data':salt_list,'chart_data1':percent_data, 'chart_data':f'탄({percent_data[0]}), 단({percent_data[1]}), 지({percent_data[2]})',
    #            'chart_label':percent_label,'name':username, 'lack_data': f'탄({lack_percent[0]}), 단({lack_percent[1]}), 지({lack_percent[2]})'}

    context = {'date': date, 'idx': idx, 'name': username,
               'chart_data1': percent_data, 'chart_label': percent_label,
               'labels': date_list, 'salt_data': salt_list, 'kcal_data': kcal_list,
               'chart_data': f'탄({percent_data[0]}), 단({percent_data[1]}), 지({percent_data[2]})',
               'lack_data': f'탄({lack_percent[0]}), 단({lack_percent[1]}), 지({lack_percent[2]})'}

    # 경준
    context['weekpercent'] = chart5_data  # 0616 주간 탄단지 비율
    context['mon_kcal'] = month_kcal  # 0617 주간 칼로리 섭취량
    context['mon_salt'] = month_salt  # 0617 주간 염분 섭취량
    context['month_label'] = ['최근1주', '1주전', '2주전']  # 0617 주간 염분,칼로리 label
    # 성균
    context.update(rcfoodsinfo)
    return render(request, 'eat/helth.html', context)