import sys
sys.path.append("../../pynaoqi-python-2.7-naoqi-1.14-linux64")
import fsm
import select
from time import sleep
from naoqi import ALProxy
import pygame
import sys
import numpy as np

pygame.init()


x = 0.0
y = 0.0
theta = 0.0
robotPort1=11212
robotPort2=11214
robotPort3=11216
robotPort4=11218

security_distance = 0.2

#  Enter : event "Start"
#  s : event "Stop"

#  c : event "Wait"

#  z : event "Go"
#  q : event "Turn_left"
#  d : event "Turn_right"
#  a : event "SideStep_Left"
#  e : event "SideStep_Right"

# draw a little area (to fucus on to get keys)
pygame.display.set_mode((100, 100))

f = fsm.fsm();  # finite state machine


##global deltat
deltat=1.0

def initNet(robotIP,robotPort):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e
    try:
        voiceProxy = ALProxy("ALTextToSpeech", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to text2speech"
        print "Error was: ", e
    try:
        memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e

    return motionProxy,postureProxy,voiceProxy,memoryProxy



if __name__ =="__main__":
    robotIp = "localhost"
    robotPort = 11212

    if len(sys.argv) <= 1:
        print "Usage python motion_setFootStepDance.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]
    motionProxy,postureProxy,voiceProxy,memoryProxy = initNet(robotIp,robotPort)

def detection_obstacleGauche():
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    if valL >= security_distance:
        return True
    else:
        return False


def detection_obstacleRight():
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    if valR >= security_distance:
        return True
    else:
        return False


def shoot():
    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    nbStepDance = 2
    x = 0.25
    y = 0.0
    theta = 0
    motionProxy.moveTo (x, y, theta)


def getKey():
    c='c'
    cok=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                cok, c = True, "g"
            elif event.key == pygame.K_q:
                cok, c = True, "l"
            elif event.key == pygame.K_s:
                cok, c = True, "s"
            elif event.key == pygame.K_d:
                cok, c = True, "r"
            elif event.key == pygame.K_a:
                cok, c = True, "a"
            elif event.key == pygame.K_e:
                cok, c = True, "e"
            elif event.key == pygame.K_c:
                cok, c = True, "c"
            elif event.key == pygame.K_t:
                cok, c = True, "shoot"
            elif event.key == pygame.K_u:
                cok, c = True, "standup"
    return cok,c
# functions (actions of the fsm)
# example of a function doRun
def doRun():
    x=0.2
    motionProxy.moveTo (x, y, theta)# do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="l":
            event = "Left"
        if val == "r":
            event = "Right"
        if val == "s":
            event = "Stop"# new event if key "w" is pressed
    x=0
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm


def doStop():
    motionProxy.rest()
    #motionProxy.setStiffnesses("Body", 0.0)
     # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Stop" # define the default event
    if newKey:
        if val=="u":
            event = "StandUp"
    return event

def doStandUp():
    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    sleep(deltat)
    newKey , val = getKey()
    event = "Wait"
    if newKey:
        if val=="s":
            event="Stop"
        if val=="g":
            event="Go"
        if val=="l":
            event="Left"
        if val=="r":
            event="Right"
    return event

def doWait():
    motionProxy.moveInit()
    sleep(deltat//10)
    newKey , val = getKey()
    event = "Wait"
    if newKey:
        if val=="s":
            event="Stop"
        if val=="g":
            event="Go"
        if val=="l":
            event="Left"
        if val=="r":
            event="Right"
        if val=="shoot":
            event="Shoot"
        if val=="standup":
            event="StandUp"
    return event


def doRight():
    theta= -(np.pi/6)
    motionProxy.moveTo (x, y, theta)# do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val == "s":
            event="Stop"
        if val == "g":
            event = "Go"
        if val == "l":
            event = "Left"
        if val == "r":
            event = "Right"
    theta=0.0
    return event

def doLeft():
    theta= (np.pi/6)
    motionProxy.moveTo (x, y, theta)# do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val == "s":
            event="Stop"
        if val == "g":
            event = "Go"
        if val == "l":
            event = "Left"
        if val == "r":
            event = "Right"
    theta=0.0
    return event

def doShoot():
    shoot()
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val == "s":
            event="Stop"
        if val == "g":
            event = "Go"
        if val == "l":
            event = "Left"
        if val == "r":
            event = "Right"
    return event






if __name__== "__main__":


    f.add_state ("Idle")
    f.add_state("Standing")
    f.add_state ("Running")
    f.add_state ("Turning_Left")
    f.add_state ("Turning_Right")
    f.add_state ("Waiting")
    f.add_state ("Shooting")

    # defines the events
    f.add_event ("Stop")
    f.add_event("StandUp")
    f.add_event ("Go")
    f.add_event ("Left")
    f.add_event ("Right")
    f.add_event ("Wait")
    f.add_event ("Shoot")

    f.add_transition ("Idle" , "Idle" , "Stop" , doStop)
    f.add_transition ("Idle" , "Standing" , "StandUp" , doStandUp)

    f.add_transition ("Standing","Idle","Stop",doStop)
    f.add_transition ("Standing","Running","Go",doRun)
    f.add_transition ("Standing","Turning_Left","Left",doLeft)
    f.add_transition ("Standing","Turning_Right","Right",doRight)
    f.add_transition ("Standing","Waiting","Wait",doWait)

    f.add_transition ("Running","Idle","Stop",doStop)
    f.add_transition ("Running","Running","Go",doRun)
    f.add_transition ("Running","Turning_Left","Left",doLeft)
    f.add_transition ("Running","Turning_Right","Right",doRight)
    f.add_transition ("Running","Waiting","Wait",doWait)
    f.add_transition ("Running","Shooting","Shoot",doShoot)

    f.add_transition ("Turning_Left","Idle","Stop",doStop)
    f.add_transition ("Turning_Left","Running","Go",doRun)
    f.add_transition ("Turning_Left","Turning_Left","Left",doLeft)
    f.add_transition ("Turning_Left","Turning_Right","Right",doRight)
    f.add_transition ("Turning_Left","Waiting","Wait",doWait)

    f.add_transition ("Turning_Right","Idle","Stop",doStop)
    f.add_transition ("Turning_Right","Running","Go",doRun)
    f.add_transition ("Turning_Right","Turning_Left","Left",doLeft)
    f.add_transition ("Turning_Right","Turning_Right","Right",doRight)
    f.add_transition ("Turning_Right","Waiting","Wait",doWait)

    f.add_transition ("Waiting","Idle","Stop",doStop)
    f.add_transition ("Waiting","Running","Go",doRun)
    f.add_transition ("Waiting","Turning_Left","Left",doLeft)
    f.add_transition ("Waiting","Turning_Right","Right",doRight)
    f.add_transition ("Waiting","Waiting","Wait",doWait)
    f.add_transition ("Waiting","Shooting","Shoot",doShoot)
    f.add_transition ("Waiting","Standing" , "StandUp",doStandUp)

    f.add_transition ("Shooting","Shooting","Shoot",doShoot)
    f.add_transition ("Shooting","Waiting","Wait",doWait)
    f.add_transition ("Shooting","Turning_Right","Right",doRight)
    f.add_transition ("Shooting","Turning_Left","Left",doLeft)



    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("StandUp") # ...  replace with you first event
    # end state



    end_state = "End" # ... replace  with your end state
    # fsm loop
    run = True
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
##            print("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False

##    print("End of the programm")
