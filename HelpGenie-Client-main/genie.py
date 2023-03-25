import TextToVoice
import VoiceToText
import dialogFlow
import MicrophoneStream as MS
import threading
import time
import geoMaster as GM
import signal


class GenieVoice(threading.Thread):
    def __init__(self, function_name, *parameter):
        threading.Thread.__init__(self)
        self.is_on = True
        self.function_name = function_name
        self.parameter = parameter
        self.signal_ob = signal.Signal() # 이 클래스에서 사용하는 시그널 객체

    # UI 쪽에서 자기자신 객체를 sinal에 넘겨 메소드를 등록하는 함수
    def setSignal(self, class_ob):
        self.signal_ob = signal.Signal()
        self.signal_ob.registSignal(class_ob)

    # 스레드 객체는 한번만 실행할 수 있고, 여러 가지 분리된 기능을 구현하기 위해 이렇게 작성
    def run(self):
        self.return_val = eval("self.{}(*self.parameter)".format(self.function_name))

    # 텍스트를 받아 지니가 음성으로 재생하는 메소드
    def strToVoice(self, voice_text: str):
        output_file = "output.wav"
        TextToVoice.getText2VoiceStream(voice_text, output_file)
        MS.play_file(output_file)

    # 고객으로부터 음성을 받아서 문자열로 반환
    def voiceToStr(self):
        return VoiceToText.getVoice2Text()

    # 헬프지니(상담사) 대화창 텍스트 추가 (시연용)
    def genieTalk(self, text: str, is_voice=True):
        self.signal_ob.emit("appendTextBlind", "헬프지니: " + text)
        if is_voice:
            self.strToVoice(text)

    # 시각장애인 상담 서비스 실행하는 메소드
    def voiceCounsel(self):
        self.genieTalk("이 서비스는 시각장애인분들을 위한 거에요. 원하시는 서비스를 말씀해주세요.")

        while self.is_on:
            voice_text = self.voiceToStr()
            self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
            # 고객이 말한 문장을 자연어 처리하여 핵심 키워드 추출
            keyword = dialogFlow.detect_intent_texts(voice_text)
            print("keyword: {}".format(keyword))

            # 추출된 핵심 키워드를 바탕으로 서비스 분기
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
            elif (keyword == "종료"):
                self.genieTalk("서비스를 종료합니다. 좋은 하루 되세요.")
                self.is_one = False
                break
            else:
                self.genieTalk("죄송해요. 다시 한번 말씀해주세요.")
                continue

            time.sleep(2)
            self.genieTalk("상담을 계속 진행하고 싶으시면 원하시는 서비스를 말씀해주세요.")

    # 신규 가입 기능 메소드
    def serviceJoin(self):
        self.genieTalk("가입절차를 시작하겠습니다. 가입정보를 말씀해주세요.")
        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))

        self.genieTalk("가입하실 수 있는 요금제를 말씀 드릴게요.")
        self.genieTalk("1번 55 요금제.\n 2번 시즌 초이스 요금제.\n 3번 슈퍼 플랜 요금제.\n 가입하고 싶은 요금제를 번호로 말씀해주세요.")

        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))

        choice_num = [i for i in " ".join(voice_text).split() if i.isdigit()]
        if (len(choice_num) == 0):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        choice_num = choice_num[0]
        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}

        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return

        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 가입이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))

    # 휴대폰 요금제 조회 기능 메소드
    def serviceCheck(self, have_this):
        if (not have_this):
            self.genieTalk("몇 월 요금제를 조회하시겠어요?")  # ex) 1월, 2월, 3월
            voice_text = self.voiceToStr()
            self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))

            # 고객이 말한 문장에서 첫 번째로 등장하는 숫자 추출
            choice_num = [i for i in " ".join(voice_text).split() if i.isdigit()]
            if (len(choice_num) == 0):
                self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
                return
            choice_num = choice_num[0]

            self.genieTalk("고객님께서 {}월 납부하실 금액은 65,000원 입니다.".format(choice_num))
        else:
            self.genieTalk("고객님께서 7월 납부하실 금액은 65,000원 입니다.")
            return

    # 서비스 조회 기능 메소드
    def serviceService(self):
        self.genieTalk("고객님이 가입하신 서비스는 다음과 같습니다.")
        self.genieTalk("1번 지니 뮤직.\n 2번 콜투유.\n 3번 KT Seezn 입니다.")

    # 요금제 변경 기능 메소드
    def serviceChange(self):
        self.genieTalk(
            "변경하실 수 있는 요금제를 말씀 드릴게요.\n 1번 55 요금제.\n 2번 시즌 초이스 요금제.\n 3번 슈퍼 플랜 요금제.\n변경하시고 싶은 요금제를 번호로 말씀해주세요.")

        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))
        # 고객이 말한 문장에서 첫 번째로 등장하는 숫자 추출
        choice_num = [i for i in " ".join(voice_text).split() if i.isdigit()]
        if (len(choice_num) == 0):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        choice_num = choice_num[0]

        choice_dict = {'1': '55', '2': '시즌 초이스', '3': '슈퍼 플랜'}

        if (choice_num not in choice_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return

        self.genieTalk("{}번 {} 요금제를 선택하셨습니다. 요금제 변경이 완료되었습니다. 감사합니다.".format(choice_num, choice_dict[choice_num]))

    # 요금제 납부 기능 메소드
    def servicePay(self):
        self.genieTalk("등록하신 카드 비밀번호 두 자리를 말씀해주세요.")
        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))

        self.genieTalk("이번 달 납부하실 금액은 65,000원입니다. 등록하신 카드로 결제 완료되었습니다. 감사합니다.")

    # 대리점 위치 조회 기능 메소드 (Geomaster)
    def serviceOffice(self):
        self.genieTalk("어떤 대리점의 위치를 확인하시겠어요?\n1번 인천 지점\n2번 대전 지점\n3번 광주 지점\n확인하시고 싶은 대리점 위치를 번호로 말씀해주세요.")

        voice_text = self.voiceToStr()
        self.signal_ob.emit("appendTextBlind", "고객님: {}.".format(voice_text))

        # 고객이 말한 문장에서 첫 번째로 등장하는 숫자 추출
        choice_num = [i for i in " ".join(voice_text).split() if i.isdigit()]
        if (len(choice_num) == 0):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        choice_num = choice_num[0]

        office_dict = {'1': 'incheon', '2': 'daejeon', '3': 'kwangju'}
        if (choice_num not in office_dict):
            self.genieTalk("죄송해요. 무슨 말씀인지 못 알아들었어요.")
            return
        GM.openMap(office_dict[choice_num])

        self.genieTalk("해당 대리점의 위치를 인터넷 창으로 띄워드렸어요.")
        time.sleep(5)
