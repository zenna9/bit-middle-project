from django.shortcuts import render, get_object_or_404
from eat import models
from eat.models import imgs
from django.http import HttpResponseRedirect
from django.urls import reverse

def uploadFile(request):

    if request.method =="POST":
        #폼에서 데이터 받아오기
        uploadedFile = request.FILES["uploadedFile"]
        zenna_url = ""
        #폴더에 저장
        document = models.imgs(
            uploadedFile = uploadedFile
        )
        document.save()
        zenna_url =  document.uploadedFile
        print("zenna 이거야", zenna_url)
    document = get_object_or_404(imgs, uploadedFile=zenna_url)
    document_id = document.id
    return HttpResponseRedirect(reverse('analysis_photo:upload2', args=(document_id,)))

def upload2(request, document_id):
    one_image_all_info = get_object_or_404(imgs, id=document_id)
    context = {'oiai': one_image_all_info}
    return render(request, 'your_photo.html', context)