from datetime import date
from sre_constants import SUCCESS
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from eat.models import login
import eat
from eat import views
# from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import pymysql
from datetime import datetime

def logining(request):
    user_id = request.POST.get('user_id')
    password = request.POST.get('password')
    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='000000', db='bitteam2', charset='utf8')
    cursor = con.cursor(pymysql.cursors.DictCursor)
    stmt = "SELECT user_id FROM eat_login WHERE user_id='{}' and password='{}'"
    stmt = stmt.format(user_id, password)
    cursor.execute(stmt) #
    data = cursor.fetchall() #

    date = datetime.today().strftime("%Y-%m-%d")


    if not data: #데이터가 없으면
        # context = 
        return render(request, 'login_fail.html')
    else:
        return redirect('/m/'+user_id+'/'+date)

def index(request):
    return render(request, 'index.html')

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


def register(request):
    return render(request, 'register.html')


# def create_process(request):
#     new_user = request.POST.get('username')
#     con = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='bit123', db='dogstagram_db', charset='utf8')
#     cursor = con.cursor(pymysql.cursors.DictCursor)
#     stmt = "SELECT username FROM dogbook_users WHERE username='{}'"
#     stmt = stmt.format(new_user)
#     cursor.execute(stmt)
#     data = cursor.fetchall()

#     if not data:
#         user = users()
#         user.username = request.POST.get('username')
#         user.full_name = request.POST.get('full_name')
#         user.email = request.POST.get('email')
#         user.passwd = request.POST.get('passwd')
#         user.phoneno = request.POST.get('phoneno')
#         user.save()
#         return render(request, 'dogbook/success.html')

#     else:
#         return render(request, 'dogbook/login_fail.html')

    # if 'id_check_btn' in request.POST:
    #     user = request.POST.get('username')
    #     return render(request, 'dogbook/popup.html')


# def id_check(request):
#     user = request.POST.get('username')
#     con = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='wlgus7921', db='dogstagram_db', charset='utf8')
#     cursor = con.cursor(pymysql.cursors.DictCursor)
#     stmt = "SELECT username FROM dogbook_users WHERE username='{}'"
#     stmt = stmt.format(user)
#     cursor.execute(stmt)
#     data = cursor.fetchall()
#     # user = users.objects.get(username=username)
#     if not data:
#         # context = {'form': form, 'error': '이 아이디는 사용중입니다. 다른 아이디를 입력하세요.'}
#         messages.success(request, f'This username can be used')
#         return render(request, 'dogbook/id_success.html')
#     else:
#         messages.info(request, f'This username is already in use')
#         return render(request, 'dogbook/id_fail.html')


# def open_popup(request):
#     return render(request, 'dogbook/popup.html')

# def open_popup2(request, username):
#     context = {'usr': username}
#     return render(request, 'dogbook/popup.html', context)




# def profile(request, username):
#     usr = get_object_or_404(users, username=username)
#     imgs = Uploads.objects.filter(author=username)
#     context = {'thisuser': usr, 'usrimgs': imgs}
#     return render(request, 'dogbook/profile.html', context)


# def pet_register(request):
#     return render(request, 'dogbook/pet_register.html')


# def missing(request):
#     return render(request, 'dogbook/practice.html')


# def upload_page(request, username):
#     usr = get_object_or_404(users, username=username)
#     context = {'thisuser': usr}
#     return render(request, 'dogbook/upload_page.html', context)


# def upload(request, username):
#     if request.method == "POST":
#         # Fetching the form data
#         content = request.POST["content"]
#         upload_image = request.FILES["upload_image"].name
#         author = request.POST['author']

#         # Saving the information in the database
#         document = Uploads(
#             content = content,
#             imagefile = upload_image,
#             author = author
#         )

#         document.save()

#     return HttpResponseRedirect(reverse('dogbook:profile', args=(username,)))