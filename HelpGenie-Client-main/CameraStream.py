import cv2
import time
from PyQt5 import QtGui, QtCore
import threading
import signal
import restApi
import dialogFlow
import geoMaster as GM


class Camera(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        self.signal_ob = signal.Signal() # 시그널 객체
        self.file_name = 'sign.avi' # 녹화하여 서버에 전송할 파일

    # UI 쪽에서 자기자신 객체를 sinal에 넘겨 메소드를 등록하는 함수
    def setSignal(self, class_ob):
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)

    # 스레드 실행시 호출되는 함수
    def run(self):
        # 이 클래스 내 메소드를 동적으로 호출하여 처리
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))

    # 청각장애인 고객 서비스 상담 시작 함수
    def counsel(self):
        self.genieTalk("이 서비스는 청각장애인분들을 위한 화면이에요. 원하시는 서비스를 수어로 입력해주세요.")
        
        while self.is_on:
            time.sleep(4)
            # 수어 영상 녹화
            self.recordVideo(12)

            # 서버로 녹화 영상을 파일로 전송 및 수어 해석 문자열 받기
            result_data = restApi.uploadVideo(self.file_name, "upload")
            self.customTalk(result_data)
            # 받은 문자열을 자연어 처리하여 핵심 키워드 추출
            keyword = dialogFlow.detect_intent_texts(result_data)
            print("keyword: {}".format(keyword))

            # 핵심 키워드를 바탕으로 서비스 분기
            if (keyword == "가입"):
                self.serviceJoin()
            elif (keyword == "조회"):
                self.serviceCheck(False)
            elif (keyword == "이번달 조회"):
                self.serviceCheck(True)
            elif (keyword == "서비스 조회"):
                self.serviceService()
            elif (keyword == "변경"):
                self.serviceChange()
            elif (keyword == "납부"):
                self.servicePay()
            elif (keyword == "대리점"):
                self.serviceOffice()
            else:
                self.genieTalk("죄송해요. 다시 한 번 말씀해주세요.")
                continue
            
            time.sleep(6)
            self.genieTalk("상담을 계속 진행하고 싶으시면 원하시는 서비스를 수어로 입력해주시고, 종료하시고 싶으시면 종료버튼을 눌러주세요.")

    # 신규 가입 기능 메소드
    def serviceJoin(self):
        self.genieTalk("가입절차를 시작하겠습니다. 가입정보를 입력해주세요. (숫자 두 번)")
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        
        self.genieTalk("어떤 요금제를 이용하시겠어요? 수어 번호로 입력해주세요.\n1. 55 요금제\n2. 시즌 초이스 요금제\n3. 슈퍼 플랜 요금제")
        time.sleep(5)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        choice_num = result_data
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}
        
        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 가입이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))

    # 휴대폰 요금제 조회 기능 메소드
    def serviceCheck(self, have_this):
        if (not have_this): # "이번 달 조회" 와 구분하기 위해 사용
            self.genieTalk("몇 월 요금제를 조회하시겠어요? (숫자 두 번)")
            month = list()
            time.sleep(4)
            self.recordVideo(5)
            result_data = restApi.uploadVideo(self.file_name, "num")
            self.customTalk(result_data)
            month.append(result_data)
            self.recordVideo(5)
            result_data = restApi.uploadVideo(self.file_name, "num")
            self.customTalk(result_data)
            month.append(result_data)
            month_result = month[0]+month[1]
            self.genieTalk("고객님께서 {}월 납부하실 금액은 65,000원 입니다.".format(month_result))
        else:
            self.genieTalk("고객님께서 7월 납부하실 금액은 65,000원 입니다.")

    # 서비스 조회 기능 메소드
    def serviceService(self):
        self.genieTalk("고객님이 가입하신 서비스는 다음과 같습니다.")
        self.genieTalk("1. KT Seezn 서비스")
        self.genieTalk("2. 링투유 서비스")
        self.genieTalk("3. 지니 뮤직 서비스")

    # 요금제 변경 기능 메소드
    def serviceChange(self):
        self.genieTalk("변경하실 요금제를 수어 번호로 입력해주세요. (숫자 한 번)")
        self.genieTalk("1. 55 요금제")
        self.genieTalk("2. 시즌 초이스 요금제")
        self.genieTalk("3. 슈퍼 플랜 요금제")
        time.sleep(5)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        choice_num = result_data
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}
        
        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 요금제 변경이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))

    # 요금제 납부 기능 메소드
    def servicePay(self):
        self.genieTalk("등록하신 카드 비밀번호 두 자리를 입력해주세요. (숫자 두 번)")
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        time.sleep(2)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        self.customTalk(result_data)
        
        self.genieTalk("이번 달 납부하실 금액은 65,000원입니다. 등록하신 카드로 결제 완료되었습니다. 감사합니다.")

    # 대리점 위치 조회 기능 메소드 (Geomaster)
    def serviceOffice(self):
        self.genieTalk("어떤 대리점의 위치를 확인하시겠어요?\n1번 인천 지점\n2번 대전 지점\n3번 광주 지점\n확인하시고 싶은 대리점 위치를 번호로 입력해주세요.")
        time.sleep(5)
        self.recordVideo(5)
        result_data = restApi.uploadVideo(self.file_name, "num")
        office_dict = {'1': 'incheon', '2': 'daejeon', '3': 'kwangju'}
        
        if (result_data not in office_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        
        GM.openMap(office_dict[result_data])
            
        self.genieTalk("해당 대리점의 위치를 인터넷 창으로 띄워드렸어요.")
        
    # 헬프지니(상담사) 대화창 텍스트 추가
    def genieTalk(self, text: str):
        self.signal_ob.emit("appendTextDeaf", "헬프지니: "+text)

    # 고객 대화창 텍스트 추가
    def customTalk(self, text: str):
        self.signal_ob.emit("appendTextDeaf2", "고객님: "+text)

    # 수어 입력 영상 녹화 메소드
    def recordVideo(self, time_sec):
        # 녹화 화면으로 전환
        self.signal_ob.emit("startRecord", True)
        # record start
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FPS, 20)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.file_name, fourcc, 20, (640, 480))

        t_end = time.time() + time_sec

        while (cap.isOpened() and (time.time() < t_end) and self.is_on):
            ret, frame = cap.read()
            
            if ret:
                out.write(frame)
                # 캡쳐한 프레임을 UI로 구성하기 위해 convert하는 과정
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                p = convert_to_qt_format.scaled(400, 500, QtCore.Qt.KeepAspectRatio)
                self.signal_ob.emit("printImage", p)
                del(frame)
                
        cap.release()
        out.release()
        
        # 녹화 화면 끝 (토리 띄우기)
        self.signal_ob.emit("startRecord", False)
