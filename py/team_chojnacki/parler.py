import sys
import motion
import time
from naoqi import ALProxy
import math

while 1<2 :

	robotIp="172.20.12.134"
	robotIp="172.20.12.134"
	robotPort=9559
	robotIp="172.20.12.134"
	robotPort=9559
	audio = ALProxy("ALAudioDevice", "172.20.28.198", 9559)
	stringdevier = input()
	audio.setOutputVolume(100)
	tts = ALProxy("ALTextToSpeech", "172.20.28.198", 9559)
	tts.setLanguage("French")
	tts.say(stringdevier)
