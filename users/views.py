from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from users.models import Member
from .models import User
from datetime import datetime
# 인증에 성공했을때 user 오브젝트 실패했을때 None
# Create your views here.

def login_view(request):
  if request.method == 'POST':
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
      print('로그인 인증 성공')
      login(request, user) # 로그인 성공됬을때 나오는 메세지를 따로 만들어야한다.
    else:
      print('로그인 인증 실패')
  return render (request,"users/login.html")

def logout_view(request):
  logout(request)
  return redirect ("user:login")

def signup_view(request):

  if request.method == 'POST':
    print(request.POST)
    username = request.POST["username"]
    password = request.POST["password"]
    firstname = request.POST["firstname"]
    lastname = request.POST["lastname"]
    email = request.POST["email"]
    student_id = request.POST["student_id"]

    user = User.objects.create(username, email, password)
    user.last_name = lastname
    user.first_name = firstname
    user.student_id = student_id
    user.save()

    # 회원가입 했을때 로그인 페이지로 전달하기
    return redirect("user:login")

  return render(request, "users/signup.html")

def member_register(request):
  return render (request, 'users/signup.html', {})

@csrf_exempt
def member_idcheck(request):
  context = {}

  memberid = request.GET['member_id']

  rs = Member.objects.filter(member_id = memberid)
  if (len(rs)) > 0:
    context['flag'] = '1'
    context['result_msg'] = '이미 존재하는 아이디 입니다.'
  else:
    context['flag'] = '0'
    context['result_msg'] = '사용 가능한 아이디 입니다.'

  return JsonResponse (context, content_type='application/json')


@csrf_exempt
def member_insert(request):
  context = {}

  memberid = request.GET['member_id']
  memberpwd = request.GET['member_pwd']
  membername = request.GET['member_name']
  memberemail = request.GET['member_email']

  rs = Member.objects.create(member_id=memberid,
                             member_pwd=memberpwd,
                             member_name=membername,
                             member_email=memberemail,
                             usage_flag='1',
                             register_date=datetime.now()
                             )

  context['result_msg'] = '회원 가입 하였습니다. Home 에서 로그인 하세요.'

  return JsonResponse (context, content_type='application/json')


@csrf_exempt
def member_login(request):
  context = {}

  memberid = request.GET['member_id']
  memberpwd = request.GET['member_pwd']


  # 이미 로그인 되어있는 상태 체크
  if 'member_no' in request.session:
    context['flag'] = "1"
    context['result_msg'] = '이미 로그인 되어 있습니다.'
  else:
    rs = Member.objects.filter(member_id=memberid, member_pwd=memberpwd)

    # User 정보 존재여부 체크
    if(len(rs)) == 0: # User 정보가 없을때
      context['flag'] = "1"
      context['result_msg'] = '로그인 정보가 잘못되었습니다.'
    else: # 로그인 ID/PW 를 Session에 저장
      rsMember = Member.objects.get(member_id=memberid, member_pwd=memberpwd)
      print(rsMember)
      memberno = rsMember.member_no
      membername = rsMember.member_name
      rsMember.access_latest= datetime.now()
      rsMember.save()

      print('membername:',membername)

      request.session['member_no'] = memberno
      request.session['member_name'] = membername

      context['flag'] = '0'
      context['result_msg'] = '로그인에 성공하였습니다.'

  return JsonResponse (context, content_type='application/json')

