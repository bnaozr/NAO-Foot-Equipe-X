from machine_fini import *
import time
import sys
import math
import select
from naoqi import ALProxy
import motion 
import random

robotIp="localhost"
#robotIp="172.20.16.13"
robotPort=11212
#robotPort=9559




def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

def init():
 motionProxy.rest()
 deus_ex.cur_state='IDLE'
 deus_ex.cur_event='wait'

def demarrage():
 motionProxy.wakeUp()
 postureProxy.goToPosture("StandInit", 0.5)
 motionProxy.setWalkArmsEnabled(True, True)
 motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
 deus_ex.cur_event = 'wait'
 print'Initialisation'

def avance():
    motionProxy.setWalkTargetVelocity(0.8,0,0,1)	
    print'Avance'

def rotation():
     motionProxy.setWalkTargetVelocity(0,0,0,0)	
     sonar_left=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
     sonar_right=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
     if sonar_left<sonar_right:
         motionProxy.moveTo(0,0,-math.pi/8)
         print('droite')
         deus_ex.cur_event='cepe_party'
     elif sonar_left>=sonar_right:
         motionProxy.moveTo(0,0,math.pi/8)
         print('gauche')
         deus_ex.cur_event='cepe_party'
     else:
         deus_ex.cur_event = 'rotation'

def stop():
 motionProxy.setWalkTargetVelocity(0,0,0,0)	
 postureProxy.goToPosture("StandInit", 0.5)
 deus_ex.cur_event='wait'
 motionProxy.rest()
 print'STOOOOOOOOOOOOOOOOOP!!'

def recule():
	motionProxy.moveTo (-0.2, 0, 0)

def pause_IDLE():
    a,b=getKey()
    if b=='z':
        deus_ex.cur_event='go'
 
def pause_START():
    if getKey()[1] == 'x':
        deus_ex.cur_event='stooop!!'
    deus_ex.cur_event = "rotation"

def pause_ROTATE():
    if getKey()[1] == 'x':
        deus_ex.cur_event='stooop!!'
    deus_ex.cur_event = "cepe_party"    
        
def pause_WALK():
    if getKey()[1] == 'x':
        deus_ex.cur_event='stooop!!'
    sonar_left=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    sonar_right=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print sonar_left,sonar_right
    if min(sonar_left,sonar_right) < 0.5:
        deus_ex.cur_event = "rotation"


    
graphe={'IDLE':{'wait':('IDLE',pause_IDLE),'go':('START',demarrage)},'START':{'wait':('START', pause_START),'rotation':('ROTATE', rotation),'stooop!!':('IDLE', stop)},'ROTATE':{'rotation':('ROTATE', pause_ROTATE),'cepe_party':('WALK', avance),'stooop!!':('IDLE', stop)},'WALK':{'cepe_party':('WALK', pause_WALK),'stooop!!':('IDLE', stop),'rotation':('ROTATE', rotation)}} 
deus_ex=machina(graphe)

try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
sonarProxy.subscribe("myApplication")
memoryProxy = ALProxy("ALMemory", robotIp, robotPort)


print 'Zzz'
init()
tts = ALProxy("ALTextToSpeech",robotIp , robotPort)
while 1 :
    if getKey()[1]=='p':
        aup.stopAll()
        tts.say(deus_ex.cur_event)
    deus_ex.run()()




