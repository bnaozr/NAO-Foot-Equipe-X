import sys
import motion
import time
from naoqi import ALProxy
import math

def main(robotIp):
    robotPort=9559
    
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
        
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    motionProxy.setFallManagerEnabled(True)
    
    def eviter():
        sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
        sonarProxy.subscribe("myApplication")
        memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
        
        
        sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
        for i in range(4):
            print("SonarL",sonarL)
            print("SonarR",sonarR)
        #    while sonarL > 0.5 and sonarR > 0.5:
        #        x = 0.2
        #        y = 0.0
        #        theta = 0.0
        #        motionProxy.moveTo (x, y, theta)
        #        sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
        #        sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            """if sonarL <= 0.5 and sonarL>0.3:
                x = 0.2
                y = 0.0
                theta = -math.pi/1.5
                motionProxy.moveTo (x, y, theta)
                sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
                sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
            elif sonarR <= 0.5 and sonarR>0.3:
                x = 0.2
                y = 0.0
                theta = math.pi/1.5
                motionProxy.moveTo (x, y, theta)
                sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
                sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")"""
            
            if (sonarL<=0.3  or sonarR<=0.3) and (sonarL>0.2 or sonarR>0.2) :
                motionProxy.setWalkArmsEnabled(True, True)
                motionProxy.moveTo(0,0,0)
                sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
                sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
          
                
            """elif sonarL<=0.2 or sonarR<=0.2:
                if sonarL<0.2 :
                    motionProxy.moveTo(-0.2,0,-(math.pi)/4)
                    sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
                    sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
                elif sonarR<0.2: 
                    motionProxy.moveTo(-0.2,0,math.pi/4)
                    sonarL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
                    sonarR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")"""
            
            
        
        
        
