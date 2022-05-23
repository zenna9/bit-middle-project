from datetime import date
from sre_constants import SUCCESS

from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
# from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import pymysql
from datetime import datetime
from eat.models import login

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt




# zenna : 로그인, Mysql과 데이터 비교
@csrf_exempt
def logining(request):
    user_id = request.POST.get('user_id')
    password = request.POST.get('password')
    con = pymysql.connect(host='192.168.0.29', port=3306, user='user1', passwd='1111', db='bitteam2', charset='utf8')
    cursor = con.cursor(pymysql.cursors.DictCursor)

    stmt = "SELECT user_id FROM eat_login WHERE user_id='{}' and password='{}'"
    stmt = stmt.format(user_id, password)
    cursor.execute(stmt)
    data = cursor.fetchall()  #
    date = datetime.today().strftime("%Y-%m-%d") # 날짜데이터 전처리

    if not data:  # 데이터가 없으면 로그인 실패 페이지
        return render(request, 'login_fail.html')
    else:
        return redirect ('/m/'+user_id+'/'+date)

        # return redirect('my_photos') 0517 경준 연습 (지울예정)
        # return redirect('/m/'+user_id+'/mypage') 0517 경준 연습 (지울예정)




# zenna : 최초 접속 로그인 페이지
def index(request):
    return render(request, 'index.html')

# zenna : 회원가입 버튼 눌렀을 경우
def register(request):
    return render(request, 'register.html')

# zenna : 회원가입 폼 제출 시 , sql에 정보 저장
def register_submit(request):
    logins = login()
    logins.user_id = request.POST['user_id']
    logins.password = request.POST['password']
    logins.user_name = request.POST['user_name']
    logins.user_sex = request.POST['user_sex']
    logins.user_height = request.POST['user_height']
    logins.user_weight = request.POST['user_weight']
    logins.user_age = request.POST['user_age']
    logins.wanted_weight = request.POST['wanted_weight']
    logins.momentum = request.POST['momentum']

    if logins.momentum == 1 :
        momen = 25
    elif logins.momentum == 2 :
        momen = 30
    elif logins.momentum == 3 : 
        momen = 35
    elif logins.momentum == 4 : 
        momen = 40
    else : momen =30
    logins.recommend_kcal = (float(logins.user_height)-100)*0.9*momen
    logins.save()

    return redirect('/lg/success')
