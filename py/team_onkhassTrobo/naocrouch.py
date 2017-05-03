import sys
import motion
import time
from naoqi import ALProxy
import math


robotIp="localhost"
robotPort=11212

# Init proxies.
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
    
def main():

    motionProxy.wakeUp()
    motionProxy.setStiffnesses("Body", 1.0)
    
    fractSpeed=0.3
    postureProxy.goToPosture("Crouch", fractSpeed)
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()
