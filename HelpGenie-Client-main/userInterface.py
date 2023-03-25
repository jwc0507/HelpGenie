#########################
#### 메인 프로그램 파일 ####
#########################
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import genie
import CameraStream


# UI 윈도우 창 클래스
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_widget = None  # 현재 출력할 화면
        self.setupInterface()
        self.genie_ob = None  # 이 클래스에서 사용할 지니 스레드 객체
        # 5초 입력 없을 시 시각장애인 UI로 변경
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: self.changeLayer(BlindLayer(self.central_widget), 1280, 720))
        self.timer.setSingleShot(True)
        self.action()

        # 버튼 콜백 함수 연결
        self.btn_start.clicked.connect(lambda: self.changeLayer(DeafLayer(self.central_widget), 1280, 720))
        self.btn_exit.clicked.connect(QtCore.QCoreApplication.quit)

    # UI 객체 생성 함수
    def setupInterface(self):
        self.setWindowTitle("Help Genie Project :)")
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.setGeometry(center_point.x() - 800 / 2, center_point.y() - 600 / 2, 800, 600)  # 윈도우 창 사이징

        # 배경 중심 레이어
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setStyleSheet("background-color: rgb(149, 228, 223)")
        self.setCentralWidget(self.central_widget)

        self.current_widget = StartLayer(self.central_widget)

        # 상담 시작 버튼
        self.btn_start = QtWidgets.QPushButton(self)
        self.btn_start.setGeometry(QtCore.QRect(325, 400, 150, 40))
        self.btn_start.setStyleSheet("font: 11pt '맑은 고딕';"
                                     "color: rgb(255, 255, 255);"
                                     "font-weight: bold;"
                                     "border-style: solid;"
                                     "border-width: 2px;"
                                     "border-radius: 10px;"
                                     "background-color: rgb(47, 186, 181);")  # 85 134 125
        self.btn_start.setText("상담 시작")

        # 종료 버튼
        self.btn_exit = QtWidgets.QPushButton(self)
        self.btn_exit.setGeometry(QtCore.QRect(325, 450, 150, 40))
        self.btn_exit.setStyleSheet("font: 11pt '맑은 고딕';"
                                    "color: rgb(255, 255, 255);"
                                    "font-weight: bold;"
                                    "border-style: solid;"
                                    "border-width: 2px;"
                                    "border-radius: 10px;"
                                    "background-color: rgb(47, 186, 181);")  # 85 134 125
        self.btn_exit.setText("종료하기")

    # 윈도우 내 레이어 창 변경 함수
    def changeLayer(self, new_widget, x, y):  # 새로 들어올 레이어, 윈도우 창 width, height
        # 5초 대기 timer kill
        self.timer.stop()
        self.timer.deleteLater()
        ##
        if (self.current_widget is not None):
            self.current_widget.hide()
            self.btn_start.hide()
            self.btn_exit.hide()
            self.current_widget = new_widget

        self.resize(x, y)
        center_point = QtWidgets.QDesktopWidget().availableGeometry().center()
        self.setGeometry(center_point.x() - x / 2, center_point.y() - y / 2, x, y)

        self.current_widget.show()
        self.repaint()

    # 현재 레이어 백그라운드에서 동작할 기능을 실행하는 함수
    def action(self):
        self.genie_ob = genie.GenieVoice("strToVoice",
                                         "안녕하세요. 수어를 이해하는 AI 고객센터 헬프지니에요. 시각장애인분들은 5초 대기를. 청각장애인분들은 상담 시작 버튼을 눌러주세요.")
        self.genie_ob.start()  # 지니 스레드 실행
        self.timer.start(15000)


# 메인 시작 UI 레이어 클래스
class StartLayer(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupInterface()

    # UI 객체 생성 함수
    def setupInterface(self):
        self.setGeometry(QtCore.QRect(0, 0, 800, 600))

        # KT 로고
        self.img_kt = QtGui.QPixmap('image/kt.png')
        self.label_kt = QtWidgets.QLabel(self)
        self.label_kt.setPixmap(self.img_kt)
        self.label_kt.setGeometry(720, 520, 80, 80)

        # 타이틀
        self.label_title1 = QtWidgets.QLabel(self)
        self.label_title1.setGeometry(QtCore.QRect(290, 50, 320, 80))
        self.label_title1.setStyleSheet("color: rgb(255, 255, 255);"
                                        "font: 36pt '맑은 고딕';"
                                        "font-weight: bold;")
        self.label_title1.setText("Help Genie")

        # 지니 이미지
        self.img_genie = QtGui.QPixmap('image/genie.png')
        self.label_genie = QtWidgets.QLabel(self)
        self.label_genie.setPixmap(self.img_genie)
        self.label_genie.setGeometry(80, 150, 520, 230)


# 청각장애인 서비스 UI 클래스
class DeafLayer(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupInterface()
        self.camera_ob = None # 이 UI에서 사용할 카메라 관련 스레드 객체

        # 버튼 콜백 함수 연결
        self.btn_exit.clicked.connect(self.exit)

        self.action()

    # UI 객체 생성 함수
    def setupInterface(self):
        self.setGeometry(QtCore.QRect(0, 0, 1280, 720))

        # KT 로고
        self.img_tmp = QtGui.QPixmap('image/kt.png')
        self.label_kt = QtWidgets.QLabel(self)
        self.label_kt.setPixmap(self.img_tmp)
        self.label_kt.setGeometry(1200, 640, 80, 80)

        # 아이콘
        self.img_icon = QtGui.QPixmap('image/icon.png')

        self.label_icon = QtWidgets.QLabel(self)
        self.label_icon.setPixmap(self.img_icon)
        self.label_icon.setGeometry(0, 0, 91, 91)

        # 헬프 지니 문구
        self.label_title1 = QtWidgets.QLabel(self)
        self.label_title1.setGeometry(QtCore.QRect(100, 0, 250, 90))
        self.label_title1.setStyleSheet("color: rgb(252, 255, 255);"
                                        "font: 28pt '맑은 고딕';"
                                        "font-weight: bold;")
        self.label_title1.setText("Help Genie")

        # 종료 버튼
        self.btn_exit = QtWidgets.QPushButton(self)
        self.btn_exit.setGeometry(QtCore.QRect(1100, 20, 150, 40))
        self.btn_exit.setStyleSheet("font: 13pt '맑은 고딕';"
                                    "color: rgb(255, 255, 255);"
                                    "font-weight: bold;"
                                    "border-style: solid;"
                                    "border-width: 2px;"
                                    "border-radius: 10px;"
                                    "background-color: rgb(47, 186, 181);")  # 85 134 125
        self.btn_exit.setText("종료하기")

        # 코리
        self.img_tmp = QtGui.QPixmap('image/kori.png')
        self.label_kori = QtWidgets.QLabel(self)
        self.label_kori.setPixmap(self.img_tmp)
        self.label_kori.setGeometry(150, 70, 343, 454)

        # 상담사 안내 문구
        self.text_counselor = QtWidgets.QTextBrowser(self)
        self.text_counselor.setGeometry(QtCore.QRect(120, 550, 400, 120))
        self.text_counselor.setStyleSheet("background-color: rgb(255, 255, 255);"
                                          "border-style: solid;"
                                          "border-width: 2px;"
                                          "font: 16pt '맑은 고딕';"
                                          "font-weight: bold;")

        # 토리
        self.img_tmp = QtGui.QPixmap('image/tori.png')
        self.label_tori = QtWidgets.QLabel(self)
        self.label_tori.setPixmap(self.img_tmp)
        self.label_tori.setGeometry(790, 70, 343, 454)

        # 고객 스트리밍 화면 (임시 paint 처리)
        self.label_recording = QtWidgets.QLabel(self)
        self.label_recording.setGeometry(760, 70, 400, 500)
        self.label_recording.hide()

        # 고객 문구
        self.text_customer = QtWidgets.QTextBrowser(self)
        self.text_customer.setGeometry(QtCore.QRect(760, 550, 400, 120))
        self.text_customer.setStyleSheet("background-color: rgb(255, 255, 255);"
                                         "border-style: solid;"
                                         "border-width: 2px;"
                                         "font: 16pt '맑은 고딕';"
                                         "font-weight: bold;")

    # 녹화 영상 프레임 갱신 함수 (슬롯)
    @pyqtSlot(QtGui.QImage)
    def printImage(self, image):
        self.label_recording.setPixmap(QtGui.QPixmap.fromImage(image))

    # 상담사 대화창 텍스트 추가 함수 (슬롯)
    @pyqtSlot(str)
    def appendTextDeaf(self, text):
        self.text_counselor.append(text)

    # 고객 대화창 텍스트 추가 함수 (슬롯)
    @pyqtSlot(str)
    def appendTextDeaf2(self, text):
        self.text_customer.append(text)

    # 녹화 시작시, 토리 -> 녹화화면 전환 함수 (슬롯)
    @pyqtSlot(bool)
    def startRecord(self, is_start):
        if is_start:
            self.label_tori.hide()
            self.label_recording.show()
        else:
            self.label_recording.hide()
            self.label_tori.show()

    # 카메라 스레드 객체 종료 함수
    def exit(self):
        import sys
        print("wait camera thread quiting...")
        self.camera_ob.is_on = False
        self.camera_ob.nonDefine()
        sys.exit()

    # 현재 레이어 백그라운드에서 동작할 기능을 실행하는 함수
    def action(self):
        self.camera_ob = CameraStream.Camera("counsel")
        self.camera_ob.setSignal(self)
        self.camera_ob.start()

    # 자동 호출 함수 (오버라이딩)
    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)

        # 가운데 라인
        painter.setPen(QtGui.QPen(QtGui.QColor(47, 186, 181), 6))
        painter.drawLine(640, 60, 640, 660)  # length: 600


# 시각장애인 서비스 UI 클래스
class BlindLayer(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupInterface()
        self.genie_ob = None  # 이 레이어에서 사용할 지니 스레드 객체

        self.action()

    # UI 객체 생성 함수
    def setupInterface(self):
        self.setGeometry(QtCore.QRect(0, 0, 1280, 720))

        # KT 로고
        self.img_kt = QtGui.QPixmap('image/kt.png')
        self.label_kt = QtWidgets.QLabel(self)
        self.label_kt.setPixmap(self.img_kt)
        self.label_kt.setGeometry(1200, 640, 80, 80)

        # 아이콘
        self.img_icon = QtGui.QPixmap('image/icon.png')

        self.label_icon = QtWidgets.QLabel(self)
        self.label_icon.setPixmap(self.img_icon)
        self.label_icon.setGeometry(0, 0, 91, 91)

        # 헬프 지니 문구
        self.label_title1 = QtWidgets.QLabel(self)
        self.label_title1.setGeometry(QtCore.QRect(100, 0, 250, 90))
        self.label_title1.setStyleSheet("color: rgb(252, 255, 255);"
                                        "font: 28pt '맑은 고딕';"
                                        "font-weight: bold;")
        self.label_title1.setText("Help Genie")

        # 코리 토리
        self.img_kt = QtGui.QPixmap('image/kori_tori.png')
        self.label_kt = QtWidgets.QLabel(self)
        self.label_kt.setPixmap(self.img_kt)
        self.label_kt.setGeometry(100, 130, 600, 480)

        # 대화 다이얼로그
        self.text_dialog = QtWidgets.QTextBrowser(self)
        self.text_dialog.setGeometry(QtCore.QRect(750, 160, 400, 400))
        self.text_dialog.setStyleSheet("background-color: rgb(255, 255, 255);"
                                       "border-style: solid;"
                                       "border-width: 2px;"
                                       "font: 20pt '맑은 고딕';"
                                       "font-weight: bold;")

    # 고객 대화창 텍스트 추가 (슬롯)
    @pyqtSlot(str)
    def appendTextBlind(self, text):
        self.text_dialog.append(text)

    # 현재 레이어 백그라운드에서 동작할 기능을 실행하는 함수
    def action(self):
        self.genie_ob = genie.GenieVoice("voiceCounsel")
        self.genie_ob.setSignal(self)
        self.genie_ob.start()
