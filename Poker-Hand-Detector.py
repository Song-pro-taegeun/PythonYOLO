from ultralytics import YOLO
import cv2
import PokerHandFunction

#load pre-train file
model = YOLO("D:\CV\Project 4 - Poker Hand Detector\\large_14000_0951.pt")
#load input image here
source = cv2.imread("D:\CV\Project 4 - Poker Hand Detector\p4.jpg", cv2.IMREAD_COLOR)
#resize image 
source = cv2.resize(source, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
#image shape info
h, w, c = source.shape
#set image's half point
halfh=int(h/2)

#enable if you want to put entire image
#dummy=model(source,show=False)

#from top to center is opponent's card.
yourcard = source[0:halfh,:]
#from center to bottom is my card.
mycard = source[halfh:,:]
#set temporary list empty 
temp=[]

#add detected card sign here from opponent's cards.
yourcards = model(yourcard,show=True)
cv2.waitKey(0)
for yourcard in yourcards:
  boxes=yourcard.boxes.cpu().numpy()
  for box in boxes:
    r=box.xyxy[0].astype(int)
    temp.append(yourcard.names[int(box.cls[0])])
#update detected images into yourcards without duplicates
yourcards=list(set(temp))

#set temporary list empty
temp=[]

#add detected card sign here from my cards.
mycards = model(mycard,show=True)
cv2.waitKey(0)
for mycard in mycards:
  boxes=mycard.boxes.cpu().numpy()
  for box in boxes:
    r=box.xyxy[0].astype(int)
    temp.append(mycard.names[int(box.cls[0])])
#update detected images into yourcards without duplicates
mycards=list(set(temp))

#set temporary list empty
temp=[]

#change alphabet into uppercase from item list.
yourcards=PokerHandFunction.listitem_touppercase(yourcards)
mycards=PokerHandFunction.listitem_touppercase(mycards)

#print list items to terminal
print(f"opponent card list - {yourcards} ")
print(f"my card list - {mycards} ")

#call madecalc from PokerHandFunction.
result =PokerHandFunction.madecalc(mycards,yourcards)
print(result)

     
