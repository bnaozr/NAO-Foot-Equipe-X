#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 16:59:53 2017

@author: baresvi
"""
import sys
import motion
import time
from naoqi import ALProxy
import math
#
#robotIp="localhost"
#robotPort=11212
##
## Init proxies.
#try:
#    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
#except Exception, e:
#    print "Could not create proxy to ALMotion"
#    print "Error was: ", e
#
#try:
#    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
#except Exception, e:
#    print "Could not create proxy to ALRobotPosture"
#    print "Error was: ", e
#
#motionProxy.wakeUp()
#
#postureProxy.goToPosture("StandInit", 0.5)
#
#motionProxy.setWalkArmsEnabled(True, True)
#
#motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
class nao():
    def __init__(self):
        self.motionProxy = None
        self.postureProxy = None
        self.sonarProxy = None
        self.memoryProxy = None
#        robotIp = "172.20.12.134"
#        robotPort= 9559
        robotIp="localhost"
        robotPort=11212
        
        # Init proxies.
        try:
            self.motionProxy = ALProxy("ALMotion", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
        
        try:
            self.postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALRobotPosture"
            print "Error was: ", e
        try:
            self.sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
        
        try:
            self.memoryProxy = ALProxy("ALMemory",robotIp, robotPort)
        except Exception, e:
            print "Could not create proxy to ALMotion"
            print "Error was: ", e
            

        self.motionProxy.wakeUp()
    
        self.postureProxy.goToPosture("StandInit", 0.5)
    
        self.motionProxy.setWalkArmsEnabled(True, True)

        #self.motionProxy.setSecurityDistance(0.2)

        self.sonarProxy.subscribe("myApplication")
        
        self.motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    
    
    def avancer(self):  
        self.motionProxy.setWalkTargetVelocity(1, 0, 0, 0.01)
#        Left = self.memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
#        Right = self.memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value") 
#        if Left > Right and Right < 0.5 :
#            self.tournerDroite()
#        if Right > Left and Left <0.5:
#            self.tournerGauche()
    def tournerGauche(self):
        self.motionProxy.setWalkTargetVelocity(0, .0, math.pi/4, 0.01)
#        self.motionProxy.moveTo (0,0,math.pi/4)
        
    def tournerDroite(self):
        self.motionProxy.setWalkTargetVelocity(0, .0, -math.pi/4, 0.01)
#        self.motionProxy.moveTo (0,0,-math.pi/4)
        
    def arreter(self):
        self.motionProxy.stopMove()
        pass
    
    def tirerpieddroit(self):
        
        # Set NAO in Stiffness On
        #"StiffnessOn(self.motionProxy)
    
        # Send NAO to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)
    
        # Activate Whole Body Balancer
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)
    
        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        self.motionProxy.wbFootState(stateName, supportLeg)
    
        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        self.motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
    
        # Com go to LLeg
        supportLeg = "LLeg"
        duration   = 1.0
        self.motionProxy.wbGoToBalance(supportLeg, duration)
    
        # RLeg is free
        stateName  = "Free"
        supportLeg = "RLeg"
        self.motionProxy.wbFootState(stateName, supportLeg)
    
        # RLeg is optimized
        effectorName = "RLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT
    
    
        # Motion of the RLeg
        dx      = 0.065                # translation axis X (meters)
        dz      = 0.07               # translation axis Z (meters)
        dwy     =5*math.pi/180.0    # rotation axis Y (radian)
    
    
        times   = [1.0, 1.35, 2.25]
        isAbsolute = False
    
        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    
        self.motionProxy.positionInterpolation(effectorName, space, targetList,
                                     axisMask, times, isAbsolute)
    
    
#        # Example showing how to Enable Effector Control as an Optimization
#        isActive     = False
#        self.motionProxy.wbEnableEffectorOptimization(effectorName, isActive)
#    
#        # Com go to LLeg
#        supportLeg = "RLeg"
#        duration   = 2.0
#        self.motionProxy.wbGoToBalance(supportLeg, duration)
#    
#        # RLeg is free
#        stateName  = "Free"
#        supportLeg = "LLeg"
#        self.motionProxy.wbFootState(stateName, supportLeg)
#    
#        effectorName = "LLeg"
#        self.motionProxy.positionInterpolation(effectorName, space, targetList,
#                                    axisMask, times, isAbsolute)
    
        time.sleep(0.05)
    
        # Deactivate Head tracking
        isEnabled    = False
        self.motionProxy.wbEnable(isEnabled)
    
        # send robot to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)
    
    def tirerpiedgauche(self):
        
        # Set NAO in Stiffness On
        #"StiffnessOn(self.motionProxy)
    
        # Send NAO to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)
    
        # Activate Whole Body Balancer
        isEnabled  = True
        self.motionProxy.wbEnable(isEnabled)
    
        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        self.motionProxy.wbFootState(stateName, supportLeg)
    
        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        self.motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
        
#        # Example showing how to Enable Effector Control as an Optimization
#        isActive     = True
#        self.motionProxy.wbEnableEffectorOptimization(effectorName, isActive)
    
        # Com go to LLeg
        supportLeg = "RLeg"
        duration   = 1.0
        self.motionProxy.wbGoToBalance(supportLeg, duration)
    
        # RLeg is free
        stateName  = "Free"
        supportLeg = "LLeg"
        self.motionProxy.wbFootState(stateName, supportLeg)
    
        
        #self.motionProxy.positionInterpolation(effectorName, space, targetList,
        #                            axisMask, times, isAbsolute)
#    
#        # Com go to LLeg
#        supportLeg = "LLeg"
#        duration   = 1.0
#        self.motionProxy.wbGoToBalance(supportLeg, duration)
#    
#        # RLeg is free
#        stateName  = "Free"
#        supportLeg = "RLeg"
#        self.motionProxy.wbFootState(stateName, supportLeg)
#    
#         RLeg is optimized
        effectorName = "LLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT
    
    
        # Motion of the RLeg
        dx      = 0.065              # translation axis X (meters)
        dz      = 0.07             # translation axis Z (meters)
        dwy     =5*math.pi/180.0    # rotation axis Y (radian)
    
    
        times   = [1.0, 1.35, 2.25]
        isAbsolute = False
    
        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    
        self.motionProxy.positionInterpolation(effectorName, space, targetList,
                                     axisMask, times, isAbsolute)
    
        time.sleep(0.05)
    
        # Deactivate Head tracking
        isEnabled    = False
        self.motionProxy.wbEnable(isEnabled)
    
        # send robot to Pose Init
        self.postureProxy.goToPosture("StandInit", 0.5)

    
    
    def veille(self): 
        fractSpeed=0.3
        self.postureProxy.goToPosture("Crouch", fractSpeed)
        self.motionProxy.setStiffnesses("Body", 0.0)
        self.motionProxy.rest()