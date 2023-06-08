from ultralytics import YOLO
import cv2
import cvzone
import math
import PokerHandFunction
import ultralytics
#cap = cv2.VideoCapture(1)  # For Webcam
#cap.set(3, 1280)
#cap.set(4, 720)

model = YOLO("D:\CV\Project 4 - Poker Hand Detector\\large_14000_0951.pt")
#54
#classNames= ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Joker', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs', 'backcard']
#52
classNames=  ['10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s', '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s', '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s', 'Ac', 'Ad', 'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks', 'Qc', 'Qd', 'Qh', 'Qs']
#classNames= ['10C', '10D', '10H', '10S', '2C', '2D', '2H', '2S', '3C', '3D', '3H', '3S', '4C', '4D', '4H', '4S', '5C', '5D', '5H', '5S', '6C', '6D', '6H', '6S', '7C', '7D', '7H', '7S', '8C', '8D', '8H', '8S', '9C', '9D', '9H', '9S', 'AC', 'AD', 'AH', 'AS', 'JC', 'JD', 'JH', 'JS', 'KC', 'KD', 'KH', 'KS', 'QC', 'QD', 'QH', 'QS']


#src= cv2.imread("D:\CV\Project 4 - Poker Hand Detector\\fig2.jpg",cv2.IMREAD_COLOR)
#src = cv2.resize(src, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)
#cv2.imwrite('temp.jpg', src)
cap = cv2.imread("D:\CV\Project 4 - Poker Hand Detector\p5.jpg", cv2.IMREAD_COLOR)
#cap = model('temp.jpg', show=True ,augment=True)

source = cv2.imread("D:\CV\Project 4 - Poker Hand Detector\p5.jpg", cv2.IMREAD_COLOR)
source = cv2.resize(source, (0, 0), fx=0.15, fy=0.15, interpolation=cv2.INTER_AREA)
h, w, c = source.shape
model = YOLO('D:\CV\Project 4 - Poker Hand Detector\large_14000_0903.pt')
#model = YOLO('D:\CV\Project 4 - Poker Hand Detector\large_10584_0859.pt')


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
"""
for i in yourcards:
  temp.append(str(i).upper)
yourcards=temp
temp=[]
for i in mycards:
  temp.append(str(i).upper)
mycards=temp
temp=[]
"""

yourcards=PokerHandFunction.listitem_touppercase(yourcards)
mycards=PokerHandFunction.listitem_touppercase(mycards)
print(f"opponent card list - {yourcards} ")
print(f"my card list - {mycards} ")


PokerHandFunction.madecalc(mycards,yourcards)
#while True:
 #   success, img = cap.read()
  #  results = model(img, stream=True )
   # hand = []
    #for r in results:
     #   boxes = r.boxes
      #  for box in boxes:
            # Bounding Box
           # x1, y1, x2, y2 = box.xyxy[0]
          #  x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
           # w, h = x2 - x1, y2 - y1
          #  cvzone.cornerRect(img, (x1, y1, w, h))
            # Confidence
          #  conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
         #   cls = int(box.cls[0])

           # cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

          #  if conf > 0.5:
             #   hand.append(classNames[cls])

                
                
                
                
#print(hand)
#hand = list(set(hand))
#print(hand)
#if len(hand) == 5:
#    results = PokerHandFunction.findPokerHand(hand)
#    print(results)
#    cvzone.putTextRect(source, f'Your Hand: {results}', (300, 75), scale=3, thickness=5)

    #img=cv2.resize(img, dsize=(0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)

