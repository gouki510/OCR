import torch
import torch.nn as nn
from torchvision import models
import torchvision.transforms as transforms
import cv2
from PIL import Image, ImageOps
import numpy as np
import warnings
import sys

warnings.simplefilter('ignore')


dic = {0:'あ', 1:'い', 2:'う', 3:'え', 4:'お', 5:'か', 6:'き', 7:'く', 8:'け', 9:'こ',10:'さ',11:'し',12:'す',13:'せ',
      14:'そ',15:'た',16:'ち',17:'つ',18:'て',19:'と',20:'な',21:'に',22:'ぬ',23:'ね',24:'の',25:'は',26:'ひ',27:'ふ',28:'へ',29:'ほ',
      30:'ま',31:'み',32:'む',33:'め',34:'も',35:'や',36:'ゆ',37:'よ',38:'ら',39:'り',40:'る',41:'れ',42:'ろ',43:'わ',44:'を',45:'ん',46:'゜',47:'゛'}
import os

def save_frame_camera_key(device_num, dir_path, basename, ext='jpg', delay=1, window_name='frame'):
    cap = cv2.VideoCapture(device_num)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    n = 0
    while True:
        ret, frame = cap.read()
        cv2.imshow(window_name, frame)
        key = cv2.waitKey(delay) & 0xFF
        if key == ord('c'):
            cv2.imwrite('{}_{}.{}'.format(base_path, n, ext), frame)
            n += 1
        elif key == ord('q'):
            break

    cv2.destroyWindow(window_name)

def threshold(img_path,store_path):
    img = cv2.imread(img_path)
    threshold = 150
    ret, img_thresh = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    cv2.imwrite(store_path,img_thresh)

def invert(img_path,store_path):
    im = Image.open(img_path)
    im_invert = ImageOps.invert(im)
    im_invert.save(store_path, quality=95)
    
def predict(data_path):
    
    transform = transforms.Compose(
        [   
            transforms.Resize((63,64)),
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            
        ]
    )

    img = cv2.imread(data_path)
    img = Image.fromarray(img)
    data = transform(img)
    data = data.unsqueeze(0)
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(512,48)
    model_path = 'ocr_th.pth'
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    output = model(data.float())
    result = output.max(1)[1].item()
    print(dic[int(result)])

if __name__ == '__main__':
    #save_frame_camera_key(1, '/home/mech-user/Desktop/3S/keisannki/product/handwritten', 'test')
    img_path = sys.argv[1]
    store_path = img_path[:-4] + '_threshold' + img_path[-4:]
    data_path = store_path[:-4] + '_invert' + img_path[-4:]
    threshold(img_path,store_path)
    invert(store_path,data_path)
    predict(data_path)