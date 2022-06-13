from __future__ import print_function, division

import torch
import numpy as np
from torchvision import datasets, transforms
import os
from PIL import Image
import torch
from torch.autograd import Variable
import torch.nn.functional as F
import platform, psutil
from pathlib import Path

RN_DIR= Path(__file__).resolve().parent.parent.parent

# print(os.getcwd())
# print('Session START :', time.strftime('%Y-%m-%d %Z %H:%M:%S', time.localtime(time.time())))
# print('===============================================================')
def printOsInfo():

    print('GPU                  :\t', torch.cuda.get_device_name(0)) 

    print('OS                   :\t', platform.system())


if __name__ == '__main__':

    printOsInfo()

def printSystemInfor():

    print('Process information  :\t', platform.processor())
    
    print('Process Architecture :\t', platform.machine())
    
    print('RAM Size             :\t',str(round(psutil.virtual_memory().total / (1024.0 **3)))+"(GB)")
    
    print('===============================================================')
      

if __name__ == '__main__':

    printSystemInfor()  


# print('Pytorch')
# print('torch ' + torch.__version__)
# print('numpy ' + np.__version__)
# print('torchvision ' + torch.__version__)
# print('matplotlib ' + matplotlib.__version__)
# print('pillow ' + PIL.__version__)
# print('pandas ' + pd.__version__)
# print('seaborn ' + sns.__version__)   
# print('psutil ' + psutil.__version__) 
# print('===============================================================')
    

data_transforms = {
        'Uploaded Files': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])}

data_dir = 'media'

path = {x: os.path.join(os.path.dirname(os.path.abspath("./media/")),data_dir,x)
                for x in ['Uploaded Files']}


image_datasets = {x: datasets.ImageFolder(path[x],
                                          data_transforms[x])
                  for x in ['Uploaded Files']}

dataloaders = { 'Uploaded Files' : torch.utils.data.DataLoader(image_datasets['Uploaded Files'], batch_size=84,
                                             shuffle=True, num_workers=4)  }

dataset_sizes = {x: len(image_datasets[x]) for x in ['Uploaded Files']}

class_names = image_datasets['Uploaded Files'].classes

filepath = RN_DIR / 'media/Uploaded Files'
# print(filenames)


def load_checkpoint(filepath):
    checkpoint = torch.load(filepath, map_location='cpu')
    model = checkpoint['model_ft']
    model.load_state_dict(checkpoint['state_dict'], strict=False)
    model.class_to_idx = checkpoint['class_to_idx']
    optimizer_ft = checkpoint['optimizer_ft']
    epochs = checkpoint['epochs']

    for param in model.parameters():
        param.requires_grad = False

    return model, checkpoint['class_to_idx']

ckpt = torch.load("./analysis_photo/resnet/weights/new_opencv_ckpt_b84_e200.pth", map_location='cpu')
ckpt.keys()

model, class_to_idx = load_checkpoint("./analysis_photo/resnet/weights/new_opencv_ckpt_b84_e200.pth")

# 기본적인 ResNet 18과 동일한 동작을 위하여 정규화 레이어 추가
image_size = 224
norm_mean = [0.485, 0.456, 0.406]
norm_std = [0.229, 0.224, 0.225]

map_location=torch.device('cpu')

strict = False

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        

def predict2(image_path, model, topk=5):
    img = Image.open(image_path)
    img = process_image(img)

    img = np.expand_dims(img, 0)

    img = torch.from_numpy(img)

    model.eval()
    inputs = Variable(img).to(device)
    logits = model.forward(inputs)

    ps = F.softmax(logits, dim=1)
    topk = ps.cpu().topk(topk)

    return (e.data.numpy().squeeze().tolist() for e in topk)
    
def process_image(image):
    preprocess = transforms.Compose([
        transforms.Resize(256), #이미지의 크기를 변경
        transforms.CenterCrop(224), #이미지의 중앙 부분을 잘라서 크기 조절
        transforms.ToTensor(), #torch.Tensor 형식으로 변경
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])])
    image = preprocess(image)
    return image

def classPred(path):
    filename, Classes, Probs = [], [], []
    im = path
    probs, classes = predict2(im, model.to(device))
    filename.append(im)
    output = [filename]
    output.append(classes)
    output.append(probs)
    Classes.append(classes)
    Probs.append(probs)
    return Classes
    # return filename , Classes, Probs
# Classes = classPred(length, path)
