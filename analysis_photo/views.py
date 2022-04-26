from distutils.command.upload import upload
from django.shortcuts import render, get_object_or_404
from eat import models
from eat.models import imgs
from django.http import HttpResponseRedirect
from django.urls import reverse

# def uploadFile(request):
def f_fu(request):

    if request.method =="POST":
        #폼에서 데이터 받아오기, 변수화
        # uploadedFile = request.FILES["uploadedFile"]
        b_uf = request.FILES["i_fu"]


        #폴더에 저장
        b_fj = models.imgs(
            uploadedFile = b_uf
        )
        b_fj.save()

        b_fuw =  b_fj.uploadedFile
    b_hc= get_object_or_404(imgs, uploadedFile=b_fuw)
    b_hc_id = b_hc.id
    return HttpResponseRedirect(reverse('analysis_photo:f_hp', args=(b_hc_id,)))

def f_hp(request, b_hc_id):
    b_hc = get_object_or_404(imgs, id=b_hc_id)
    context = {'k_hc': b_hc}
    return render(request, 'your_photo.html', context)