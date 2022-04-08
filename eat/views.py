from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def upload_p(request):
    return render(request, 'your_photo.html')
