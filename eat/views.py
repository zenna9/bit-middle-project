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
    # --------------------여기까지 완료 -----------------------------
    # 5. 가장 최신의 날짜에 해당하는 탄단지 비율 데이터 찾기
    # print(chart_data)
    food_labels= [] #날짜 데이터
    food_kcal= [] #kcal 데이터
    food_salt= [] #salt 데이터
    all_data= [] #모든 데이터(테스트용)

    for foodinfo in chart_data:
        # 데이터 전처리
        # 날짜 데이터의 date타입을 str으로 변환
        # after_date = (foodinfo.date).strftime('%Y-%m-%d')
        after_date = (foodinfo.date).strftime('%m-%d')
        print(after_date, type(after_date))

        # kcal, salt 데이터 1의 자리 숫자 반올림
        food_data2 = round(foodinfo.kcal, -1)
        food_data3 = round(foodinfo.salt, -1)

        # list append
        food_labels.append(after_date)
        food_kcal.append(food_data2)
        food_salt.append(food_data3)

        # alldata = 해당 아이디에 해당하는 최근 입력값
        all_data.append({
            "id": idx,
           "date": after_date,
           "s_kcal": food_data2,
           "s_salt": food_data3,
        });


        # MySQL 데이터 가져오기
        conn = pymysql.connect(host='192.168.0.29', port=3306, user='user1', passwd='1111', db='bitteam2', charset='utf8')
        curs = conn.cursor()
        # 첫번째 쿼리문 : 그날 하루 먹었던 음식의 총 칼로리, 소금양
        sql = "SELECT `user_id`, date_format(`date`,'%m-%d') as `date`, TRUNCATE(SUM(`kcal`),-1) AS 'daily_kcal', TRUNCATE(SUM(`salt`),-1) AS 'daily_salt'  FROM eat_diet WHERE `user_id` = '" + idx + "' GROUP BY `date` ORDER BY -`date`;"
        curs.execute(sql)
        # 실행결과 모두 읽어보기 fetch all
        dailyinfo = curs.fetchall()

        # 두번째 쿼리문 : 그날 하루 먹었던 음식의 총 칼로리, 소금양
        sql1 = "SELECT `user_name` FROM eat_login WHERE `user_id` = '" + idx + "';"
        curs.execute(sql1)
        # 이름데이터 저장 네임테스트로 이름 저장
        name_test = curs.fetchone()
        curs.close()
        conn.close()
        # 이름데이터 tuple 에서 str 변환
        name_list = ''.join(name_test)
        # tuple 형태 데이터 list 변환
        data_list=[list(row) for row in dailyinfo]
        # list를 array 로 변환
        data_list_np = np.array(data_list)

        # 특정 아이디의 그날 먹은 총 칼로리와 염분섭취량
        daily_data = []
        a = len(data_list_np)
        b = range(a)

        for i in b : # range(len(data_list_np) 데이터의 갯수
            if i > 2 :
                break # 3개까지만 반복하고 나오기
            daily_data.append({
                "id:": data_list_np[i][0],
                "name": name_list,
                "date": data_list_np[i][1],
                "d_kcal": data_list_np[i][2],
                "d_salt": data_list_np[i][3],
            }) # 하루총 칼로리 소금 Dict형 데이터
        print(daily_data, type(daily_data))

        # 차트에 반영할 데이터 따로 뽑기위한 코드
        df=pd.DataFrame(daily_data)
        # 날짜데이터
        date_list = df['date'].values.tolist()
        # kcal 데이터
        kcal_list = df['d_kcal'].values.tolist()
        # salt 데이터
        salt_list = df['d_salt'].values.tolist()

#         # 한날짜의 데이터리스트
#         어떤 한날짜의 총 염분, 칼로리 합친양을 보여주고싶으니까
#         label을 날짜 하루로하고,
#         data를 염분 칼로리로 해야되는데,
#         첫번째 인덱스의 두번째 행을 찾고자 할때
#         1. 특정 행의 데이터 찾기
#         list[0],
#
#         2. 딕셔너리 리스트에서 특정 값 찾기 반복문
#         for chartdata in  daily_data[0].values():
#             print('차트데이터: ', chartdata)
#
#             3. 날짜 리스트를 만들어놓고 데이터 추가하기
#             list = ["","",""]
#  내가 찾으려는 키값을 리스트로 만들어놓고
# 그거에 해당하는 dict를 만들수 있다.
#
# lista=["date","kcal","salt"]
# values=[dict[a] for a in lista]

    # context = {'idx':idx, 'labels':food_labels,'kcal_data':food_kcal, 'salt_data':food_salt}
    context = {'mydata': daily_data, 'idx': idx, 'name': name_list, 'labels':date_list, 'kcal_data':kcal_list, 'salt_data':salt_list}
    print(context, type(context))
    return render(request, 'helth.html', context)