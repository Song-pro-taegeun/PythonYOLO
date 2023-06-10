from flask import Flask, render_template
from ultralytics import YOLO
import cv2
import cvzone
import math

import PokerHandFunction
import numpy
import os
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
    print("파일경로 : ", file_path)
    print("모델경로 : ", model_path)

    count += 1

    # 파일이 있는지 없는지 체크
    if os.path.exists(file_path):
        print("파일 존재")
    else:
        print("파일을 찾을 수 없음")
    # 모델이 있는지 없는지 체크
    if os.path.exists(model_path):
        print("모델 존재")
    else:
        print("모델을 찾을 수 없음")

    # load pre-trained file
    model = YOLO(model_path)
    source = cv2.imread(file_path, cv2.IMREAD_COLOR) # load input image

    # resize image
    source = cv2.resize(source, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    h, w, c = source.shape # image shape info
    halfh = int(h / 2) # set image's half point

    # from top to center is opponent's card.
    yourcard = source[0:halfh, :]
    # from center to bottom is my card.
    mycard = source[halfh:, :]

    # set temporary list empty
    temp = []

    # add detected card sign here from opponent's cards.  
    ImgYourcards = []  
    yourcards = model(yourcard, show=False)
    cv2.waitKey(0)
    for i, yourcard in enumerate(yourcards):
        boxes = yourcard.boxes.cpu().numpy()
        for box in boxes:
            r = box.xyxy[0].astype(int)
            temp.append(yourcard.names[int(box.cls[0])])
            cv2.rectangle(yourcard.orig_img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 2)  # Green bounding box

    img_path = f"./Project_4_Taegeun/static/images/yourcard.jpg"  # 이미지 파일 경로 설정
    cv2.imwrite(img_path, yourcard.orig_img)  # 이미지 파일 저장
    ImgYourcards.append(img_path)  # 이미지 파일 경로를 리스트에 추가          
    
    # update detected images into yourcards without duplicates
    yourcards = list(set(temp))

    # set temporary list empty1
    temp = []

    # add detected card sign here from my cards.
    ImgMycards = [] 
    mycards = model(mycard, show=False)
    cv2.waitKey(0)
    for i, mycard in enumerate(mycards):
        boxes = mycard.boxes.cpu().numpy()
        for box in boxes:
            r = box.xyxy[0].astype(int)
            temp.append(mycard.names[int(box.cls[0])])
            cv2.rectangle(mycard.orig_img, (r[0], r[1]), (r[2], r[3]), (255, 0, 255), 2)  # Pink bounding box

    img_path = f"./Project_4_Taegeun/static/images/mycard.jpg"  # 이미지 파일 경로 설정
    cv2.imwrite(img_path, mycard.orig_img)  # 이미지 파일 저장
    ImgMycards.append(img_path)  # 이미지 파일 경로를 리스트에 추가

    # update detected images into mycards without duplicates
    mycards = list(set(temp))

    # set temporary list empty
    temp = []

    # change alphabet into uppercase from item list.
    yourcards = PokerHandFunction.listitem_touppercase(yourcards)
    mycards = PokerHandFunction.listitem_touppercase(mycards)

    # call madecalc from PokerHandFunction.
    x1 = ["로얄 스트레이트 플러시", "스트레이트 플러시", "포카드",
          "풀 하우스", "플러시", "마운틴", "백 스트레이트", "스트레이트",
          "트리플", "투페어", "원페어"]
    # y1 =PokerHandFunction.madecalc(mycards,yourcards)
    y1 =PokerHandFunction.madecalc(mycards,yourcards)

    print("족보확률이용 : ", y1)
    print("내카드", mycards)
    print("너카드", yourcards)

    return render_template('main.html', yourcards=ImgYourcards, mycards=ImgMycards, x1=x1, y1=y1)


if __name__ == '__main__':
    app.run()
