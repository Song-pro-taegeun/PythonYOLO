import base64
import io
from flask import Flask, render_template
from ultralytics import YOLO
import cv2
import cvzone
import math
import PokerHandFunction
import APokerHandFunction
import numpy
import os
import time
from flask import send_file

app = Flask(__name__)
count = 1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/start_analysis')
def start_analysis():
    global count 
    file_path = "./Project_4_Taegeun/static/images/p"+str(count)+".jpg"
    model_path= "./Project_4_Taegeun/static/images/large_14000_0951.pt"
    count += 1
    print("FilePath" + file_path)
    print("model_path@@@@" + model_path)
    
    # 파일이 있는지 없는지 체크
    if os.path.exists(file_path):
        print("File exists.")
    else:
        print("File does not exist.")

    # 파일이 있는지 없는지 체크
    if os.path.exists(model_path):
        print("@@@@ exists.")
    else:
        print("@@@@ does not exist.")

    model = YOLO(model_path)

    #54
    classNames=  ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
    source = cv2.imread("./Project_4_Taegeun/static/images/p5.jpg", cv2.IMREAD_COLOR)
    source = cv2.resize(source, (0, 0), fx=0.15, fy=0.15, interpolation=cv2.INTER_AREA)
    h, w, c = source.shape

    halfh=int(h/2)
    dummy=model(source,show=False)
    yourcard = source[0:halfh,:]#슬라이싱
    mycard = source[halfh:,:]#슬라이싱
    temp=[]

    yourcards = model(yourcard,show=True)
    cv2.waitKey(0)
    for yourcard in yourcards:
        boxes=yourcard.boxes.cpu().numpy()
        for box in boxes:
            r=box.xyxy[0].astype(int)
            #print(r)
            temp.append(yourcard.names[int(box.cls[0])])

    yourcards=list(set(temp))
    temp=[]
    mycards = model(mycard,show=True)
    cv2.waitKey(0)
    for mycard in mycards:
        boxes=mycard.boxes.cpu().numpy()
        for box in boxes:
            r=box.xyxy[0].astype(int)
            #print(r)
            temp.append(mycard.names[int(box.cls[0])])
    mycards=list(set(temp))
    temp=[]


    yourcards=APokerHandFunction.listitem_touppercase(yourcards)
    mycards=APokerHandFunction.listitem_touppercase(mycards)
    print(f"opponent card list - {yourcards} ")
    print(f"my card list - {mycards} ")

    x1 = ["로얄 스트레이트 플러시", "스트레이트 플러시", "포카드", 
          "풀 하우스", "플러시", "마운틴", "백 스트레이트", "스트레이트", 
          "트리플", "투페어", "원페어"]
    y1 = APokerHandFunction.madecalc(mycards,yourcards)

    _, img_encoded = cv2.imencode('.jpg', source)
    image_data = base64.b64encode(img_encoded).decode('utf-8')
    
    return render_template('main.html', x1=x1, y1=y1, image_data=image_data)

if __name__ == '__main__':
    app.run()
