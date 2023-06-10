import base64
import io
from flask import Flask, render_template
from ultralytics import YOLO
import cv2
import cvzone
import math
import PokerHandFunction
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
    count += 1
    
    # 파일이 있는지 없는지 체크
    if os.path.exists(file_path):
        print("File exists.")
    else:
        print("File does not exist.")

    img = cv2.imread(file_path)
    model = YOLO("./Project_4_Taegeun/static/images/playingCards.pt")
    classNames = ['10C', '10D', '10H', '10S',
                  '2C', '2D', '2H', '2S',
                  '3C', '3D', '3H', '3S',
                  '4C', '4D', '4H', '4S',
                  '5C', '5D', '5H', '5S',
                  '6C', '6D', '6H', '6S',
                  '7C', '7D', '7H', '7S',
                  '8C', '8D', '8H', '8S',
                  '9C', '9D', '9H', '9S',
                  'AC', 'AD', 'AH', 'AS',
                  'JC', 'JD', 'JH', 'JS',
                  'KC', 'KD', 'KH', 'KS',
                  'QC', 'QD', 'QH', 'QS']

    results = model(img, stream=True)
    hand = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

            if conf > 0.5:
                hand.append(classNames[cls])

    print("hand 1: ")
    print(hand)
    hand = list(set(hand))
    print("hand 2: ")
    print(hand)
    if len(hand) == 5:
        results = PokerHandFunction.findPokerHand(hand)
        print(results)

    _, img_encoded = cv2.imencode('.jpg', img)
    image_data = base64.b64encode(img_encoded).decode('utf-8')

    x1 = ["투페어", "원페어", "3", "4", "5", "6", "7"]
    y1 = [36.43, 22.55, 80, 50, 10, 20, 30]

    return render_template('main.html', x1=x1, y1=y1, image_data=image_data)

if __name__ == '__main__':
    app.run()
