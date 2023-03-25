import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import user_auth as UA
import os

HOST = 'gate.gigagenie.ai'
PORT = 4080

def getText2VoiceStream(inText, inFileName):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
	#print("a")
	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	#print("b")
	writeFile=open(inFileName,'wb')
	#print("c")
	for response in stub.getText2VoiceStream(message):
		#print("die?")
		if response.HasField("resOptions"):
			pass
			#print ("\n\nResVoiceResult: %d" %(response.resOptions.resultCd))
		if response.HasField("audioContent"):
			#print ("Audio Stream\n\n")
			writeFile.write(response.audioContent)
	writeFile.close()
	
	return response.resOptions.resultCd
