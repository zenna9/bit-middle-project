from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from eat.models import diet, login, imgs
from django.db.models import Sum, F, Count, Case, When
import pandas as pd
import pymysql
import numpy as np
from whateat.mysql import oursql  # mysql 계정정보
from datetime import datetime # 경준-0607 건강정보 페이지에서 Footer 이동하려고 만든거
from eat.recommend import recommend_food

# 채은 : 페이지 접속 시 최초화면
def index(request) :
    return render(request, 'login.html')

# 채은 : 로그인한 메인화면 ==(if 데이터 있는 경우 , 없는경우)===================
def logindone(request,date):
        idx = request.session['idx']
        # dietlist = get_list_or_404(diet, user_id=idx, date=date)
        dietlist = diet.objects.filter(user_id=idx, date=date)
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

# 경준
def team_index(request):
    return render(request, 'introduce.html')

# 경준
#  날짜별 나의 사진을 볼 수 있는 링크
def mypage_index(request, date):
    try : # 사진이 있으면서 날짜를 선택하지 않았을경우
        idx = request.session['idx']
        username = get_object_or_404(login, user_id=idx).user_name  # USER_NAME
        dietlist = get_list_or_404(diet, user_id=idx, date=date)
        context = {'idx': idx, 'date': date, 'dietlist': dietlist,'name':username}
        return render(request, "myprofile.html", context)
    except : # 사진이 없을경우
        context = {'idx':idx,'date':date, 'name':username}
        return render(request, 'myprofile_null.html', context)

#경준
# 전체 사진 보기/ 내 모든 사진을 볼 수 있는 링크/ 내가 올린사진이 없으면 except
def profile_allphoto(request):
    try:
        idx = request.session['idx'] #UESR_ID
        dietlist = get_list_or_404(diet, user_id=idx)
        username= get_object_or_404(login, user_id=idx).user_name #USER_NAME
        context = {'idx': idx, 'dietlist': dietlist, 'date': '나의 모든 사진','name':username}
        return render(request, "myprofile_all.html", context)
    except:
        context = {'idx': idx,'name':username}
        return render(request, 'myprofile_null.html', context)

def tutorial_page(request):
    return render(request, 'tutorial.html')


def helthinfo(request):
    date = datetime.today().strftime("%Y-%m-%d")
    idx = request.session['idx']
    chart_data = get_list_or_404(diet, user_id=idx)[:5]
    username = get_object_or_404(login, user_id=idx).user_name  # USER_NAME
    # 1. 어떤 아이디의 모든 영양 정보값 추출
    # -------------1번까지 데이터 차트 적용 확인--------------------
    # 2. 어떤 날짜에 해당하는 영양 정보값 더하기
    # 3. 어떤 아이디에 해당되는 날짜데이터와 영양정보데이터 list 생성하기
    # 4. 가장 최신의 날짜 3개의 데이터에 해당하는 결과값을 chart에 반영
    # --------------------여기까지 완료 -----------------------------
    # 5. 가장 최신의 날짜에 해당하는 탄단지 비율 데이터 찾기
    # print(chart_data)
    food_labels= [] #날짜 데이터
    food_kcal= [] #kcal 데이터
    food_salt= [] #salt 데이터
    all_data= [] #모든 데이터(테스트용)

    #  연습1. 특정 아이디의 최근 입력한 데이터의 data, kcal, salt
    for foodinfo in chart_data:
        # 데이터 전처리
        # 날짜 데이터의 date타입을 str으로 변환
        after_date = (foodinfo.date).strftime('%m-%d')

        # kcal, salt 데이터 1의 자리 숫자 반올림
        food_data2 = round(foodinfo.kcal, -1)
        food_data3 = round(foodinfo.salt, -1)

        # 테스트용 차트에 띄울 data
        food_labels.append(after_date)
        food_kcal.append(food_data2)
        food_salt.append(food_data3)

        # alldata = 특정 아이디의 최근 식단 입력값
        all_data.append({
            "id": idx,
           "date": after_date,
           "s_kcal": food_data2,
           "s_salt": food_data3,
        })

    # 경준 MySQL 쿼리문으로 특정 아이디의 최근날짜 3일간 소금, 칼로리합
    # conn = pymysql.connect(host='192.168.0.29', port=3306, user='user1', passwd='1111', db='bitteam2', charset='utf8')
    # MySQL 데이터 가져오기
    conn = pymysql.connect(host=oursql.s_host, port=3306, user=oursql.s_user, passwd=oursql.s_passwd, db='bitteam2', charset='utf8')
    curs = conn.cursor()
    # 첫번째 쿼리문 : 그날 하루 먹었던 음식의 총 칼로리, 소금양
    sql = "SELECT `user_id`, date_format(`date`,'%m-%d') as `date`, TRUNCATE(SUM(`kcal`),-1) AS 'daily_kcal', TRUNCATE(SUM(`salt`),-1) AS 'daily_salt'  FROM eat_diet WHERE `user_id` = '" + idx + "' GROUP BY `date` ORDER BY -`date`;"
    curs.execute(sql)
    # 실행결과 모두 조회해서 dailyinfo에 저장
    dailyinfo = curs.fetchall()
    # tuple => list 변환
    data_list = [list(row) for row in dailyinfo]
    # list => array 변환
    data_list_np = np.array(data_list)  # ARRAY 자료구조


    # 두번째 쿼리문 : 특정 아이디의 이름값
    sql1 = "SELECT `user_name` FROM eat_login WHERE `user_id` = '" + idx + "';"
    curs.execute(sql1)
    # 이름데이터 name test로 저장
    name_test = curs.fetchone()
    # 이름데이터 tuple => str 변환
    name_list = ''.join(name_test)


    # 특정 아이디의 영양정보(칼로리, 염분섭취량) 와 이름 합치기
    daily_data = []
    a = len(data_list_np)
    b = range(a)

    # 특정아이디의 가장 최근 3일의 영양데이터
    for i in b : # range(len(data_list_np)
        if i > 2 :
            break # 최대 3개까지 반복
        daily_data.append({
            "id:": data_list_np[i][0],
            "name": name_list,
            "date": data_list_np[i][1],
            "d_kcal": data_list_np[i][2],
            "d_salt": data_list_np[i][3],
        })
    print('daily_data: ',daily_data, type(daily_data))

    # 차트에 반영할 데이터 따로 뽑기위한 코드
    df = pd.DataFrame(daily_data)
    # 날짜데이터
    date_list = df['date'].values.tolist()
    # kcal 데이터
    kcal_list = df['d_kcal'].values.tolist()
    # salt 데이터
    salt_list = df['d_salt'].values.tolist()

    # 세번째 쿼리문 : 특정 날짜의 탄단지 음식의 비율
    conn = pymysql.connect(host=oursql.s_host, port=3306, user=oursql.s_user, passwd=oursql.s_passwd, db='bitteam2', charset='utf8')
    curs = conn.cursor()
    sql2 = "SELECT *,ROUND((t1.dt/t4.alld)*100) AS 't%',ROUND((t2.dd/t4.alld)*100) AS 'd%',ROUND((t3.dj/t4.alld)*100) AS 'j%'\
        FROM (SELECT `user_id`, date_format(`date`,'%Y-%m-%d') as `date`,ROUND(SUM(`tan`)) AS dt FROM bitteam2.eat_diet \
        WHERE `user_id`='rhrudwnszoq'  AND `date`='2022-05-10') AS t1,\
        (SELECT ROUND(SUM(`dan`)) AS dd FROM bitteam2.eat_diet WHERE `user_id`='rhrudwnszoq'  AND `date`='2022-05-10') AS t2,\
        (SELECT ROUND(SUM(`ji`)) AS dj FROM bitteam2.eat_diet WHERE `user_id`='rhrudwnszoq'  AND `date`='2022-05-10') AS t3,\
        (SELECT ROUND(SUM(`tan`)+SUM(`dan`)+SUM(`ji`))  AS alld FROM bitteam2.eat_diet WHERE `user_id`='rhrudwnszoq'  AND `date`='2022-05-10') AS t4;"
    curs.execute(sql2)
    food_data4 = curs.fetchall()
    curs.close()
    conn.close()
    food_data4_np = np.array(food_data4)
    food_percent = []
    # 연습용으로 만든 2개의 리스트
    food_percent_data =[]
    # food_percent_labels =[]
    for i in range(len(food_data4_np)):
        food_percent.append({
            "id:": food_data4_np[0][0],
            "name": name_list,
            "date": food_data4_np[0][1],
            "d_tan": food_data4_np[0][2],
            "d_dan": food_data4_np[0][3],
            "d_ji": food_data4_np[0][4],
            "alld": food_data4_np[0][5],
            "percnet_t": food_data4_np[0][6],
            "percnet_d": food_data4_np[0][7],
            "percnet_j": food_data4_np[0][8],
        });
        # 탄단지비율 데이터
        food_percent_data.append({
            "percnet_t": food_data4_np[0][6],
            "percnet_d": food_data4_np[0][7],
            "percnet_j": food_data4_np[0][8],
        });
    print('food_percent_data:', food_percent_data[0] , type(food_percent_data[0]))
    percent_label = list(food_percent_data[0].keys())
    percent_data =list(food_percent_data[0].values())
    print('percent_label', percent_label, type(percent_label))
    print('percent_data',percent_data, type(percent_data))
    percent_data = [round(float(percent_data[i])) for i in range(len(percent_data))]
    lack_percent = [round(100-(percent_data[i])) for i in range(len(percent_data))]
    
    # 성균 : 음식추천 모듈 가져와서 리턴값에 업데이트
    rcfoodsinfo=recommend_food()
    # 리턴값: {영양성분 이름 / 권장량대비 섭취영양 / 권장량대비 부족영양 / 부족영양소 (2종) / 부족영양소 별 추천읍식 (2종)}
    # 리턴값구성 - recommend_data= {'nameAndEatNf': nameAndEatNf, 'nameAndLackNf': nameAndLackNf, \
    #      'lackNf_dec':[r1,r2], 'recommend_p': [r1_recommend.index[0],r2_recommend.index[0]]}
    
    # 추천음식 데이터 recommend_data={{ key값 }}
    # context = {'idx':idx, 'labels':food_labels,'kcal_data':food_kcal, 'salt_data':food_salt}
    #  기존에 임시로 띄어놓은 차트에 해당하는 데이터 가져오기
    context = {'mydata': daily_data, 'date':date,'idx': idx, 'name': name_list, 'labels':date_list, 'kcal_data':kcal_list,
               'salt_data':salt_list, 'chart_data':f'탄({percent_data[0]}), 단({percent_data[1]}), 지({percent_data[2]})',
               'chart_label':percent_label,'name':username, 'lack_data': f'탄({lack_percent[0]}), 단({lack_percent[1]}), 지({lack_percent[2]})'}
    context.update(rcfoodsinfo)
    return render(request, 'helth.html', context)