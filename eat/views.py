from django.shortcuts import render, get_object_or_404
from eat.models import diet, login

def index(request, user_idx):
    dietlist = get_object_or_404(diet, user_idx=user_idx)
    context = {'dietlist': dietlist}
    return render(request, 'index.html', context)

def upload_p(request):
    dietlist = diet.objects.all()
    context = {'dietlist':dietlist}
    return render(request, 'your_photo.html', context)

# def get_post(request):
#     if request.method =='GET':
#         id = request.GET['id']
#         data = {
#             'data' : id,
#         }
#         return render(request, 'your_photo.html', data)
#     elif request.method =='POST' :
#         id = request.POST['id']
#         name = request.POST['name']
#         data = {
#             'data' : id,
#             'name' : name,
#         }
#         return render(request, 'your_photo.html', data)