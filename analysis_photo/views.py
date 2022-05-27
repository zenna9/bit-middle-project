from distutils.command.upload import upload
from django.shortcuts import get_list_or_404, render, get_object_or_404, redirect
from eat import models
from eat.models import imgs, diet
from analysis_photo.models import menu
from django.http import HttpResponseRedirect
from django.urls import reverse


# zenna : 메인 페이지에서 사진 업로드 버튼을 눌렀을 경우, 
#   sql photo 테이블에 사진 정보 저장 
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
    # b_foodlist = menu.objects.all()
    b_hc_id = b_hc.id
    request.session['idx']=idx
    return HttpResponseRedirect(reverse('analysis_photo:f_hp', args=(b_hc_id,)))


# zenna : 사진 인덱스를 받아와 인식결과, 추가등록을 할 수 있는 페이지로 이동
def f_hp(request, b_hc_id):
    b_hc = get_object_or_404(imgs, id=b_hc_id)
    context = {'k_hc': b_hc, 'idx':request.session['idx']}
    return render(request, 'your_photo.html', context)

# zenna : 
# def f_uploading_photo (request):
#     idx = request.POST['idx']
#     return redirect('이동할 url')

# zenna : AI 인식 결과, 사용자가 추가한 메뉴 계산하여 sql 저장 -> 완료 후 메인 페이지로 이동
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
        
    # print('=-=-===-=-=-=-=-=-=-=',menulist)

    diets = diet()
    diets.user_id = request.POST['idx']
    diets.date=request.POST['date']
    diets.time = request.POST['time']
    diets.foodimage = request.POST['file_location']
    
    nutrlist = {'kcal':0,'tan':0,'dang':0,'ji':0,'dan':0,'kalsum':0,'inn':0,'salt':0,'kalum':0, 'magnesum':0, 'chul':0,'ayeon':0,'kolest':0,'transfat':0} #빈 딕트 선언

    for i in range(0, len(menulist)) :
        # print('menulist',menulist[i][0])
        datalist = get_object_or_404(menu, food_name=menulist[i][0])
        nutrlist['kcal'] = nutrlist['kcal'] + (datalist.kcal / datalist.basic_g * menulist[i][1])
        nutrlist['tan'] = nutrlist['tan'] + (datalist.tan / datalist.basic_g * menulist[i][1])
        nutrlist['dang'] = nutrlist['dang'] + (datalist.dang / datalist.basic_g * menulist[i][1])
        nutrlist['ji'] = nutrlist['ji'] + (datalist.ji / datalist.basic_g * menulist[i][1])
        nutrlist['dan'] = nutrlist['dan'] + (datalist.dan / datalist.basic_g * menulist[i][1])
        nutrlist['kalsum'] = nutrlist['kalsum'] + (datalist.kalsum / datalist.basic_g * menulist[i][1])
        nutrlist['inn'] = nutrlist['inn'] + (datalist.inn / datalist.basic_g * menulist[i][1])
        nutrlist['salt'] = nutrlist['salt'] + (datalist.salt / datalist.basic_g * menulist[i][1])
        nutrlist['kalum'] = nutrlist['kalum'] + (datalist.kalum / datalist.basic_g * menulist[i][1])
        nutrlist['magnesum'] = nutrlist['magnesum'] + (datalist.magnesum / datalist.basic_g * menulist[i][1])
        nutrlist['chul'] = nutrlist['chul'] + (datalist.chul / datalist.basic_g * menulist[i][1])
        nutrlist['ayeon'] = nutrlist['ayeon'] + (datalist.ayeon / datalist.basic_g * menulist[i][1])
        nutrlist['kolest'] = nutrlist['kolest'] + (datalist.kolest / datalist.basic_g * menulist[i][1])
        nutrlist['transfat'] = nutrlist['transfat'] + (datalist.transfat / datalist.basic_g * menulist[i][1])

    
    diets.kcal = nutrlist['kcal']
    diets.tan = nutrlist['tan']
    diets.dang =nutrlist['dang'] 
    diets.ji =nutrlist['ji']
    diets.dan =nutrlist['dan']
    diets.kalsum =nutrlist['kalsum']
    diets.inn =nutrlist['inn']
    diets.salt =nutrlist['salt'] 
    diets.kalum =nutrlist['kalum']
    diets.magnesum =nutrlist['magnesum']
    diets.chul =nutrlist['chul'] 
    diets.ayeon =nutrlist['ayeon'] 
    diets.kolest =nutrlist['kolest'] 
    diets.transfat =nutrlist['transfat']

    diets.save()
    request.session['idx']=idx
    return redirect('/m/ain/'+date)