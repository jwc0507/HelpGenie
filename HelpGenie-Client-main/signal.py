from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QImage


class Signal(QObject):
	appendTextBlind = pyqtSignal(str) # 시각장애인 대화창 텍스트 추가
	appendTextDeaf = pyqtSignal(str) # 청각장애인 상담사 텍스트 추가
	appendTextDeaf2 = pyqtSignal(str) # 청각장애인 고객 텍스트 추가
	printImage = pyqtSignal(QImage) # 녹화영상 프레임 갱신
	startRecord = pyqtSignal(bool) # 녹화영상 시작 시 토리 사진->녹화 영상
	
	def __init__(self):
		super().__init__()

	# 객체(클래스 이름으로 구분)에 따라 등록한 시그널을 분기
	def registSignal(self, class_ob):
		if (class_ob.__class__.__name__ == "BlindLayer"):
			self.appendTextBlind.connect(class_ob.appendTextBlind)
		elif (class_ob.__class__.__name__ == "DeafLayer"):
			self.printImage.connect(class_ob.printImage)
			self.startRecord.connect(class_ob.startRecord)
			self.appendTextDeaf.connect(class_ob.appendTextDeaf)
			self.appendTextDeaf2.connect(class_ob.appendTextDeaf2)

	# 시그널 해제 함수
	def unregistSignal(self, class_ob):
		if (class_ob.__class__.__name__ == "BlindLayer"):
			self.appendTextBlind.disconnect(class_ob.appendTextBlind)
		elif (class_ob.__class__.__name__ == "DeafLayer"):
			self.printImage.disconnect(class_ob.printImage)
			self.startRecord.disconnect(class_ob.startRecord)
			self.appendTextDeaf.disconnect(class_ob.appendTextDeaf)
			self.appendTextDeaf2.disconnect(class_ob.appendTextDeaf2)

	# 시그널 신호 보내는 함수 (함수명과, 해당 함수의 인자값을 동적으로 받아서 처리
	def emit(self, function_name: str, *parameter):
		signal_object = eval("self.{}".format(function_name))
		signal_object.emit(*parameter)
