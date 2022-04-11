from django.shortcuts import render
from eat.models import diet

def index(request):
    dietlist = diet.objects.all()
    context = {'dietlist':dietlist}
    return render(request, 'index.html', context)

def upload_p(request):
    return render(request, 'your_photo.html')
