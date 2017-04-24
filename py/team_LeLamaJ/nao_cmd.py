import sys
import motion
import time
from naoqi import ALProxy
import math


def initialisation():
    robotIp="localhost"
    robotPort=11212
    
    try:
        global motionProxy
        motionProxy = ALProxy("ALMotion", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
    
    try:
        global postureProxy
        postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e
        
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

def veille():
    motionProxy.rest()

def marche_droite():
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    x = 0.5
    y = 0.0
    theta = 0.0
    motionProxy.moveTo (x, y, theta)

def rotation_droite():
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    x = 0.2
    y = 0.0
    theta = -math.pi/2.0
    motionProxy.moveTo (x, y, theta)

def rotation_gauche():
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    x = 0.2
    y = 0.0
    theta = math.pi/2.0
    motionProxy.moveTo (x, y, theta)
    
def Pas_droit():
    pass

def Pas_gauche():
    pass