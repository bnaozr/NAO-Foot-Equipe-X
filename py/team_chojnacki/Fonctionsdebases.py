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

    def dab(self):
        
        self.motionProxy.setStiffnesses("Body", 1.0)
        self.postureProxy.goToPosture("StandInit", 0.5)
    
        # Example showing how to set angles, using a fraction of max speed
        names  = ["Body"]
        angles  = [-0.6872739791870117, 0.43254613876342773, -0.7271580696105957, 0.8636000156402588, 2.0785279273986816, -0.03490658476948738, -1.8238691091537476, 0.7567999958992004, -0.2438640594482422, -0.07359004020690918, -0.6626460552215576, 2.112546443939209, -1.1842899322509766, 0.07520794868469238, -0.2438640594482422, 0.052197933197021484, -0.6765360832214355, 2.112546443939209, -1.1857401132583618, -0.08125996589660645, 0.18565607070922852, 0.3141592741012573, 0.5920820236206055, 1.282465934753418, -0.0844118595123291, 0.8459999561309814]
        fractionMaxSpeed  = 0.2
        self.motionProxy.setAngles(names, angles, fractionMaxSpeed)
    
        time.sleep(3.0)
        self.motionProxy.setStiffnesses("Body", 1.0)
        angles = [0.7224719524383545, 0.46782803535461426, -0.15804386138916016, -0.1565098762512207, -0.3237159252166748, -1.2609061002731323, 0.19937801361083984, 0.7555999755859375, -0.23619413375854492, -0.06131792068481445, -0.5675380229949951, 2.112546443939209, -1.182755947113037, 0.07827591896057129, -0.23619413375854492, 0.05373191833496094, -0.5722239017486572, 2.112546443939209, -1.1857401132583618, -0.0827939510345459, -0.8497941493988037, -0.7501680850982666, 0.9771161079406738, 0.07674193382263184, -1.7012481689453125, 0.7192000150680542]
    
        fractionMaxSpeed  = 0.2
        self.motionProxy.setAngles(names, angles, fractionMaxSpeed)
        
        self.motionProxy.setStiffnesses("Body", 1.0)
    
        time.sleep(3.0)
        self.motionProxy.setStiffnesses("Body", 1.0)
        angles = [0.09966802597045898, 0.5092461109161377, 1.1565940380096436, 1.2839161157608032, -1.4742159843444824, -0.04597806930541992, 0.18250393867492676, 0.785599946975708, -0.2730100154876709, 0.21326804161071777, -0.8743381500244141, 2.112546443939209, -1.1842899322509766, 0.06753802299499512, -0.2730100154876709, 0.13810205459594727, -0.4418339729309082, 1.7349958419799805, -1.1136419773101807, 0.12582993507385254, -0.420274019241333, -1.115260124206543, 1.7533200979232788, 0.5093300342559814, -1.8238691091537476, 0.6979999542236328]
    
        fractionMaxSpeed  = 0.1
        self.motionProxy.setAngles(names, angles, fractionMaxSpeed)
       
        self.motionProxy.setStiffnesses("Body", 1.0)
    
        time.sleep(3.0)
        self.motionProxy.setStiffnesses("Body", 1.0)
        angles = [-0.5737578868865967, 0.35584592819213867, 1.992624044418335, 0.49697399139404297, -0.5584180355072021, -1.0798940658569336, -1.4051861763000488, 0.7087999582290649, -0.2638061046600342, -0.06592011451721191, -0.5782761573791504, 2.112546443939209, -1.185823917388916, 0.08594608306884766, -0.2638061046600342, 0.04912996292114258, -0.5890979766845703, 2.112546443939209, -1.1857401132583618, -0.0858621597290039, 0.3728039264678955, -0.5630199909210205, 1.6674160957336426, 1.432797908782959, -1.4849538803100586, 0.7588000297546387]
    
        fractionMaxSpeed  = 0.2
        self.motionProxy.setAngles(names, angles, fractionMaxSpeed)
        time.sleep(3.0)
        self.motionProxy.setStiffnesses("Body", 1.0) 
        fractionMaxSpeed  = 1
        for i in range(5):
        	self.motionProxy.closeHand('RHand')
        	time.sleep(0.1)
        	motionProxy.openHand('RHand')
        time.sleep(0.1)
        
    def veille(self): 
        fractSpeed=0.3
        self.postureProxy.goToPosture("Crouch", fractSpeed)
        self.motionProxy.setStiffnesses("Body", 0.0)
        self.motionProxy.rest()