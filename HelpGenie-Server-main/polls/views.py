from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

import os
import cv2
import numpy as np

class Home(TemplateView):
    template_name = 'Home.html'

#유효한 문장인지 확인하는 함수. 명령어가 없는 문장, 명령어가 2개이상 포함된 문장을 걸러줌.
#ex. 이번 요금 -> 명령어가 없는 문장 -> false
#ex. 이번 가입 조회 -> 명령어가 두개인 문장 -> false

def isCorrectSentence(translated_words):
    command_list = [ "변경","조회", "가입", "납부", "대리점" ] # CRUD
    numOfDetectedCommand = 0

    for i in range(len(translated_words)):
            for j in range(0, len(command_list)):
                    if translated_words[i] == command_list[j]:
                            numOfDetectedCommand += 1

    if numOfDetectedCommand == 1:   #input string에 명령어가 1개 포함 되어 있다면, True return
            return True
    else:                           #input string에 명령어가 0개 혹은 2개이상 포함되어 있다면, False return
            return False

#비디오에서 탐지한 모든 객체를 담아놓은 리스트에, 사전(Dictionary)에 등록된 단어가 포함되어 있으면, 그 단어를 translated_words 리스트에 담는 함수.
#ex. detected_object_list에 [change_1,fee_2,check_1,check_2,fee_1,join]가 담겨있다면, 이 리스트에서 사전에 등록된 라벨조합이 있는지 없는 지를 확인함.
#   저 리스트를 argument로 넣고 translate_list를 호출하면, check_1check_2를 찾아내 "변경"이라는 문자열로 변환하고 join을 "가입"이라는
#   문자열로 변환한 뒤, translated_words에 넣음

def translate_list(detected_object_list):
    if detected_object_list == []:
            return []

    # key : 구분동작의 라벨을 공백없이 이어붙인 string
    # value : key에 매핑되는 value값
    sign_language_dictionary = {"change_1change_2":"변경", "check_1check_2":"조회", "pay":"납부",
                                "service_1service_2":"서비스", "fee_1fee_2":"요금",
                                "this":"이번달","join":"가입","office":"대리점"}
    translated_words = [] #detected_object_list에서 찾은 단어(학습된 단어)를 넣는 리스트.

    MAX_LEN = 3 #학습한 수어의 구분동작의 max값. MAX_LEN이 3이면 학습한 수어는 최대 3개의 구분동작을 갖고 있다는 것을 의미함.
                # 즉, withdrawal_1withdrawal_2withdrawal_3withdrawal_4 이런식으로 구분동작 4개이상으로 이뤄진 수어가 없다는 뜻.

    for i in range(1,MAX_LEN + 1): #i : detected_object_list(DOL)의 element들과 딕셔너리의 키값과 비교하며 구분 동작 i(1,2,3)개로 구성된 단어를 찾음.
        for j in range(0, len(detected_object_list)):
            #print("i:",i,", j:",j)
            current_key=""#DOL에서 검출한 후보키.(현재 보고 있는 키)
                            #ex. 현재 i(cur_len) 값이 2라면, DOL의 원소들을 2개씩 이어붙여서 딕셔너리 검색키를 만든 다음에 current_key에 저장함.

            x_flag = 0 #딕셔너리와 매핑 된 라벨들은 그 값을 x로 바꾸는데, 현재 보고 있는 key를 구성하는 label에 x가 포함되어 있다면, garbage key이므로 딕셔너리 검색을 하지 않음.
            for k in range(0, i):
                if j + k >= len(detected_object_list):
                    #print("out of range 3")
                    break
                else:
                    if detected_object_list[j + k] == "x":
                        x_flag = True
                        break
                    current_key += detected_object_list[j + k];
            if x_flag:
                continue
            print("current_key",current_key)

            if sign_language_dictionary.get(current_key): #DOL에서 검출한 후보KEY가 딕셔너리에 등록되어 있다면,
                translated_words.append(sign_language_dictionary[current_key]) #translated_words에 key에 매핑된 value를 추가함.
                print("translate:",translated_words)
                print("detected:",detected_object_list)

                for k in range(j, j + i):#찾은 단어의 key를 구성하는 label 값을 x로 변경.
                    detected_object_list[k] = "x"

                #print("print detected_object after j")

                #print("result:",detected_object_list)
    
    if isCorrectSentence(translated_words):
        translated_str = " ".join(translated_words) #translated_words에 포함된 단어들을 공백으로 연결하여 str으로 저장
    else:
        translated_str = "Error" #유효한 문장이 아니라면 Error를 저장
    
    return translated_str
        
def upload(request):
    if request.method == 'POST':

        file = './media/sign.avi'

        # 이미 sign.avi 파일이 media 파일에 존재 할 경우 삭제
        if os.path.isfile(file):
            print("Delete Success")
            os.remove(file)

        print("If out")
        
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)

        print("This is Sentence")


        # 비디오 신호 받기
        VideoSignal = cv2.VideoCapture(r"C:\Users\Administrator\Desktop\yolo\mytestsite\media\sign.avi")
        # YOLO 가중치 파일과 CFG 파일 로드
        YOLO_net = cv2.dnn.readNet(r"C:\Users\Administrator\Downloads\video_capture_test\number\yolov4-tiny_last.weights",r"C:\Users\Administrator\Downloads\video_capture_test\number\yolov4-tiny.cfg")

        # YOLO NETWORK 재구성
        classes = []
        with open(r"C:\Users\Administrator\Downloads\video_capture_test\number\obj.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = YOLO_net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]
        count = 0
        detectedObjectList = []

        while True:
            # 비디오 프레임을 하나씩 읽음
            ret, frame = VideoSignal.read()
            if frame is None:
                break

            h, w, c = frame.shape
            count += 1

            # 10프레임마다 한 번씩 출력
            if(count % 10   == 0):

                # YOLO 입력
                blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
                True, crop=False)
                YOLO_net.setInput(blob)
                outs = YOLO_net.forward(output_layers)

                class_ids = []
                confidences = []
                boxes = []

                for out in outs:

                    for detection in out:

                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]

                        if confidence > 0.5:
                            # 중앙좌표와 w, h 값을 구함
                            center_x = int(detection[0] * w)
                            center_y = int(detection[1] * h)
                            dw = int(detection[2] * w)
                            dh = int(detection[3] * h)
                            # Rectangle coordinate
                            x = int(center_x - dw / 2)
                            y = int(center_y - dh / 2)
                            boxes.append([x, y, dw, dh])
                            confidences.append(float(confidence))
                            class_ids.append(class_id)
                            #print(class_id)

                indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)


                for i in range(len(boxes)):
                    if i in indexes:
                        x, y, w, h = boxes[i]

                        label = str(classes[class_ids[i]])


                        if len(detectedObjectList)==0:
                            detectedObjectList.append(str(classes[class_ids[i]]))

                        print("len : ",len(detectedObjectList))

                        # 새로 들어온 라벨과 detectedObjectList를 비교하여 중복되지 않은 값만 detectedObjectList에 삽입
                        duplicate_object = False
                        for j in range(len(detectedObjectList)) :
                            print("list : ",detectedObjectList[j])
                            print("dected : ", str(classes[class_ids[i]]))
                            if(detectedObjectList[j]== str(classes[class_ids[i]])):
                                duplicate_object = True

                        if duplicate_object ==False:
                            detectedObjectList.append(str(classes[class_ids[i]]))



                        #if(detectedObjectList[len(detectedObjectList)-1] != str(classes[class_ids[i]])) :
                        #   detectedObjectList.append(str(classes[class_ids[i]]))


                        score = confidences[i]

                        # 경계상자와 클래스 정보 이미지에 입력
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                        cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5,
                        (255, 255, 255), 1)

            # OpenCV에 프레임 그리기
            cv2.imshow("YOLOv3", frame)

            if cv2.waitKey(100) > 0:
                break

        # 종료 후 비디오와 opencv 해제
        VideoSignal.release()
        cv2.destroyAllWindows()
        
        print("\n\nresult")
        for word in detectedObjectList :
                print(word)
        print()

        returnValue = translate_list(detectedObjectList)
        
        return HttpResponse(returnValue)
        
# Create your views here.
