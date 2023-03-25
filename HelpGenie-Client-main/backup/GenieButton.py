import MicrophoneStream as MS
import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws

KWSID = ['오늘', '지니야', '친구야', '자기야', 'help지니']
RATE = 16000
CHUNK = 512

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
btn_status = False

#For calling genie
def callback(channel):  
	print("falling edge detected from pin {}".format(channel))
	global btn_status
	btn_status = True
	print(btn_status)

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def btn_detect():
	global btn_status
	
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:
			GPIO.output(31, GPIO.HIGH)
			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))
			GPIO.output(31, GPIO.LOW)
			if (btn_status == True):
				rc = 1
				btn_status = False			
			if (rc == 1):
				GPIO.output(31, GPIO.HIGH)
				#MS.play_file("../data/sample_sound.wav")
				return 200
