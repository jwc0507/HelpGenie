from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse

import cv2
import numpy as np

class Home(TemplateView):
    template_name = 'Home.html'

def isCorrectSentence(translated_words):
    command_list = [ "7","8" ] # CRUD
    numOfDetectedCommand = 0

    for i in range(len(translated_words)):
            for j in range(0, len(command_list)):
                    if translated_words[i] == command_list[j]:
                            numOfDetectedCommand += 1

    if numOfDetectedCommand == 1:
            return False
    else: 
            return True

def translate_list(detected_object_list):
    if detected_object_list == []:
            return []
    sign_language_dictionary = {"0":"0","1":"1","2":"2","3":"3","4":"4","5":"5","6":"6","7":"7","8":"8","9":"9"}
    translated_words = []
    MAX_LEN = 3
    for i in range(1,MAX_LEN + 1):
        for j in range(0, len(detected_object_list)):
            #print("i:",i,", j:",j)
            current_key=""

            x_flag = 0
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

            if sign_language_dictionary.get(current_key):
                translated_words.append(sign_language_dictionary[current_key])
                print("translate:",translated_words)
                print("detected:",detected_object_list)

                for k in range(j, j + i):
                    detected_object_list[k] = "x"

                #print("print detected_object after j")

                #print("result:",detected_object_list)
    
    if isCorrectSentence(translated_words):
        translated_str = "Error"
    else:
        translated_str = " ".join(translated_words)
    
    return translated_str
        
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)

        '''

        # 웹캠 신호 받기
        VideoSignal = cv2.VideoCapture(r"C:\Users\Administrator\Desktop\yolo\mytestsite\media\test2.avi")
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
            # 웹캠 프레임
            print("read?")
            ret, frame = VideoSignal.read()
            if frame is None:
                break

            h, w, c = frame.shape
            count += 1

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
                            # Object detected
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

            cv2.imshow("YOLOv3", frame)

            if cv2.waitKey(100) > 0:
                break

        print("\n\nresult")
        for word in detectedObjectList :
                print(word)
        print()

        returnValue = translate_list(detectedObjectList)
        '''
        return HttpResponse(returnValue)
        
# Create your views here.
