import sys
import motion
import time
from naoqi import ALProxy
import math
import threading

# test program to get NAO's left and right sonars (9999.0 if nothing, max range 1.5 m)
# this is the easy way to use sonars

robotIp = "11111111111111111111111"
robotPort = "111111111111111111111"

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])

class Dectect_Obstacle(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
    # Appel des proxy
        try:
            self.memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALMemory"
            print "Error was: ", e

        try:
            self.sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALSonar"
            print "Error was: ", e

        try:
            self.motionProxy = ALProxy("ALMotion", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e

        self.duration_wait = 0.25
        self.security_distance = 0.5
        self.obstacle_left = 0
        self.obstacle_right = 0

    def run(self):
        self.motionProxy.wakeUp()
        self.motionProxy.moveInit()

        for i in range(200):

            self.sonarProxy.subscribe("SonarApp");
            time.sleep(self.duration_wait)

            self.detection_obstacle()
            self.gestion_obstacle()

        self.sonarProxy.unsubscribe("SonarApp");
        time.sleep(self.duration_wait)

        self.motionProxy.stopMove()

    def detection_obstacle(self):
        valL = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        valR = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")

        if valL >= self.security_distance:
            self.obstacle_left = 0
        else:
            self.obstacle_left = 1

        if valR >= self.security_distance:
            self.obstacle_right = 0
        else:
            self.obstacle_right = 1

    def gestion_obstacle(self):
        if self.obstacle_left == 1 or self.obstacle_right == 1:
            self.motionProxy.stopMove()


