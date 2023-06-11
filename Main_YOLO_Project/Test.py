# 필요 라이브러리 임포트
from flask import Flask, render_template # 플라스크 라이브러리
from ultralytics import YOLO # 욜로 라이브러리
import cv2
import PokerHandFunction
import os

app = Flask(__name__)

# 턴제 증가를 위한 변수, start_analysis 함수에서 사용
count = 0

# app.route('/') 시 index.html로 이동
# root <- index.html임
@app.route('/')
def home():
    return render_template('index.html')

# html 파일을 불러오기 위한 매개 라우터
@app.route('/main')
def main():
    return render_template('index.html')

# 분석 시작 버튼을 클릭 시 해당 라우터를 실행함. 이 로직 가장 하단 리턴값을 확인해보면 main.html 렌더 템플릿을 하고 있음.
# main.html에 최종적으로 변수를 담아서 리턴해준다. 즉 함수 종료 시점에 알아서 main.html이 열린다
@app.route('/start_analysis')
def start_analysis():

    # 위에서 전역 변수로 선언한 count를 글로벌 타입으로 설정
    global count 
    
    if count == 12:
        # 함수 종료
        return render_template('index.html', end = count)
        
    else:
        # 파일 path 확인 로직
        file_path = "./Main_YOLO_Project/static/images/p"+str(count)+".jpg" # 첫jpg 파일 0 다음분석 클릭시 1씩 증가
        model_path= "./Main_YOLO_Project/static/images/large_14000_0951.pt"
        print("파일경로 : ", file_path)
        count += 1 # < 1씩 증가로직
        print("모델경로 : ", model_path)

        # 파일이 경로 내에 있는지 없는지 체크
        if os.path.exists(file_path):
            print("파일 존재")
        else:
            print("파일을 찾을 수 없음")
        # 모델이 경로 내에 있는지 없는지 체크
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

        # 상대카드 ----------------------------------------------------------------------------------------
        # add detected card sign here from opponent's cards.  
        yourcards = model(yourcard, show=False)
        cv2.waitKey(0)
        for i, yourcard in enumerate(yourcards):
            boxes = yourcard.boxes.cpu().numpy()
            for box in boxes:
                r = box.xyxy[0].astype(int)
                temp.append(yourcard.names[int(box.cls[0])])

                # 초록색 rgb코드로 바운딩박스를 그려준다.
                cv2.rectangle(yourcard.orig_img, (r[0], r[1]), (r[2], r[3]), (0, 255, 0), 2) 

        # 실행 이미지 파일마다 변수에 경로 설정
        img_path = f"./Main_YOLO_Project/static/images/yourcard.jpg"
        cv2.imwrite(img_path, yourcard.orig_img)  # 이미지 파일 저장       
        
        # update detected images into yourcards without duplicates
        yourcards = list(set(temp))

        # set temporary list empty1
        temp = []

        # 내 카드 ----------------------------------------------------------------------------------------
        # add detected card sign here from my cards.
        mycards = model(mycard, show=False)
        cv2.waitKey(0)
        for i, mycard in enumerate(mycards):
            boxes = mycard.boxes.cpu().numpy()
            for box in boxes:
                r = box.xyxy[0].astype(int)
                temp.append(mycard.names[int(box.cls[0])])
                
                # 분홍색 rgb코드로 바운딩박스를 그려준다.
                cv2.rectangle(mycard.orig_img, (r[0], r[1]), (r[2], r[3]), (255, 0, 255), 2)

        # 실행 이미지 파일마다 변수에 경로 설정
        img_path = f"./Main_YOLO_Project/static/images/mycard.jpg"
        cv2.imwrite(img_path, mycard.orig_img)  # 이미지 파일 저장

        # update detected images into mycards without duplicates
        mycards = list(set(temp))

        # set temporary list empty
        temp = []

        # change alphabet into uppercase from item list.
        yourcards = PokerHandFunction.listitem_touppercase(yourcards)
        mycards = PokerHandFunction.listitem_touppercase(mycards)

        # x 값에 고정 족보 셋팅
        x1 = ["로얄 스트레이트 플러시", "스트레이트 플러시", "포카드",
            "풀 하우스", "플러시", "마운틴", "백 스트레이트", "스트레이트",
            "트리플", "투페어", "원페어"]
        # y 값에 madecalc 함수에서 리턴한 값 반환(내카드랑 상대카드를 해당 함수에 넣는다.)
        y1 =PokerHandFunction.madecalc(mycards,yourcards)

        # xy값에 x1값 y1값을 인덱스별로 합친다. ex-> x1 = aa, y1 = bb => xy = aabb
        xy = []
        for i in range(len(x1)):
            xy.append(str(x1[i]) + "(" + str(y1[i]) + "%)")
            print(xy)

        # main.html에 리턴한다. x1,y1값을 셋팅하여 리턴한다.
        # xy에 x(족보) + y(확률) 확률값을 더하여 같이 리턴한다.
        return render_template('main.html', x1=x1, y1=y1, xy = xy)


if __name__ == '__main__':
    app.run()
