from distutils.command.upload import upload
from django.shortcuts import get_list_or_404, render, get_object_or_404, redirect
from eat import models
from eat.models import imgs, diet
from analysis_photo.models import menu
from django.http import HttpResponseRedirect
from django.urls import reverse

# def uploadFile(request):
def f_fu(request):

    if request.method =="POST":
        #폼에서 데이터 받아오기, 변수화
        # uploadedFile = request.FILES["uploadedFile"]
        b_uf = request.FILES["i_fu"]
        idx = request.POST['idx']
        # print(type(idx),"==================",b_uf)
        #폴더에 저장

        b_fj = models.imgs(
            uploadedFile = b_uf
        )
        b_fj.save()

        b_fuw =  b_fj.uploadedFile
    b_hc= get_object_or_404(imgs, uploadedFile=b_fuw)
    b_hc_id = b_hc.id
    return HttpResponseRedirect(reverse('analysis_photo:f_hp', args=(b_hc_id,idx,)))

def f_hp(request, b_hc_id,idx):
    b_hc = get_object_or_404(imgs, id=b_hc_id)
    context = {'k_hc': b_hc, 'idx':idx}
    return render(request, 'your_photo.html', context)


def f_uploading_photo (request):
    # ?file_location=&date=2022-05-04&time=2&menu1=ㅇㄹㅇㄹ&g1=33&menu2=ㅇㄹㅇㄹ&g2=33
    idx = request.POST['idx']
    return redirect('이동할 url')

def f_upload_at_sql(request):
    idx = request.POST['idx']
    date=request.POST['date']

    menulist = []
    for i in range(1, 2):
        try:
            if (request.POST['ai_{}'.format(i)] != ''):
                # print(request.POST['ai_{}'.format(i)])            
                menulist.append([(request.POST['ai_{}'.format(i)]),int(request.POST['ai_g{}'.format(i)])])
        except : print('첫번째가 이;상해')
    for i in range(1, 5):
        try:
            if (request.POST['sl_{}'.format(i)] != ''):
                # print(request.POST['sl_{}'.format(i)])            
                menulist.append([(request.POST['sl_{}'.format(i)]),int(request.POST['sl_g{}'.format(i)])])
        except : print('2번째가 이상하대')
        
    print('=-=-===-=-=-=-=-=-=-=',menulist)

    diets = diet()
    diets.user_id = request.POST['idx']
    diets.date=request.POST['date']
    diets.time = request.POST['time']
    diets.foodimage = request.POST['file_location']
    
    nut_list = {} #빈 딕트 선언
    for i in range(0, len(menulist)) :
        print('menulist',menulist[i][0])
        newlist = get_object_or_404(menu, food_name=menulist[i][0])
        print('newlist',newlist.kcal)


    # menu1
    # g1
    # menu2
    # g2


    # 음식 정보 인식.. 계산...

    diets.save()


    #음식값 구한 내용  sql..
    
    return redirect('/m/'+idx+'/'+date)