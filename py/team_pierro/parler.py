from naoqi import ALProxy
import time
tts = ALProxy("ALTextToSpeech", "172.20.12.134", 9559)


tts.say("il a pas dit bonjour")

tts.say("du coup")


tts.say("il s'est fait niquer sa mere")


