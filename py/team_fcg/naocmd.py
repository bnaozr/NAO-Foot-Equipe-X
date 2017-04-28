#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 16:22:26 2017

@author: houdeval
"""
"""
Les fonctions de base seront par exemple :
| Initialiser le robot (i.e. ouvrir les "proxys" de communication avec le robot)
| Faire avancer le robot en ligne droite
| Faire tourner le robot
| Arr^eter le robot
| Mettre le robot en veille (
n de mission)

IP est 127.0.0.1 (ou localhost) et le port est
11212
"""


import sys
import motion
import time
import math
from naoqi import ALProxy

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

    
def initialiser(robotIP):
    try:
        motionProxy = ALProxy("ALMotion", robotIP, robotPORT)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPORT)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by Walk algorithm
    #####################
    motionProxy.setWalkArmsEnabled(True, True)
    #~ motionProxy.setWalkArmsEnabled(False, False)

    #####################
    ## FOOT CONTACT PROTECTION
    #####################
    #~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #TARGET VELOCITY
def marcher(motionProxy):
    
    X = 0.8
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # high speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def reculer(motionProxy):
    
    X = -0.8
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 # high speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    

def tournergauche(motionProxy):
    X = 0.0 
    Y = 0.0
    Theta = 1
    Frequency =1.0 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)



def tournerdroite(motionProxy):
    X = 0.0 
    Y = 0.0
    Theta = -1
    Frequency =1.0 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def PCG(motionProxy):
    X = 0.0 
    Y = 1.0
    Theta = 0
    Frequency =0.5 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def PCD(motionProxy):
    X = 0.0 
    Y = -1.0
    Theta = 0
    Frequency =0.5 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def CDF(motionProxy):
    X = 1.0 
    Y = 0.0
    Theta = -0.5
    Frequency =0.5 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def CGF(motionProxy):
    X = 1.0 
    Y = 0.0
    Theta = 0.5
    Frequency =0.5 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def CGB(motionProxy):
    X = -1.0 
    Y = 0.0
    Theta = -0.5
    Frequency =0.5 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def CDB(motionProxy):
    X = -1.0 
    Y = 0.0
    Theta = 0.5
    Frequency =0.5 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def arret_dpt(motionProxy):      
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def inactif(postureProxy, motionProxy):
    # Send NAO to Pose Init
    fractSpeed=0.3
    postureProxy.goToPosture("Crouch", fractSpeed)
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()

    
    
def kick_gauche(postureProxy, motionProxy):
    motionProxy.setWalkTargetVelocity(0, 0, 0, 0)
    ''' Example of a whole body kick
    Warning: Needs a PoseInit before executing
             Whole body balancer must be inactivated at the end of the script
    '''


    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Activate Whole Body Balancer
    isEnabled  = True
    motionProxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    motionProxy.wbFootState(stateName, supportLeg)

#    # Constraint Balance Motion
#    isEnable   = True
#    supportLeg = "Legs"
#    proxy.wbEnableBalanceConstraint(isEnable, supportLeg)
#
#    # Com go to LLeg
#    supportLeg = "LLeg"
#    duration   = 2.0
#    proxy.wbGoToBalance(supportLeg, duration)
#
#    # RLeg is free
#    stateName  = "Free"
#    supportLeg = "RLeg"
#    proxy.wbFootState(stateName, supportLeg)

    # RLeg is optimized
#    effectorName = "RLeg"
    axisMask     = 63
    space        = motion.FRAME_ROBOT


    # Motion of the RLeg
    dx      = 0.1                # translation axis X (meters)
    dz      = 0.05                 # translation axis Z (meters)
    dwy     = 6.0*math.pi/180.0    # rotation axis Y (radian)


    times   = [2.0, 2.7, 4.5]
    isAbsolute = False

    targetList = [
      [-dx, 0.0, dz, 0.0, +dwy, 0.0],
      [+dx, 0.0, dz, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

#    proxy.positionInterpolation(effectorName, space, targetList,
#                                 axisMask, times, isAbsolute)


#    # Example showing how to Enable Effector Control as an Optimization
#    isActive     = False
#    proxy.wbEnableEffectorOptimization(effectorName, isActive)

    # Com go to LLeg
    supportLeg = "RLeg"
    duration   = 2
    motionProxy.wbGoToBalance(supportLeg, duration)

    # RLeg is free
    stateName  = "Free"
    supportLeg = "LLeg"
    motionProxy.wbFootState(stateName, supportLeg)

    effectorName = "LLeg"
    motionProxy.positionInterpolation(effectorName, space, targetList,
                                axisMask, times, isAbsolute)
    time.sleep(1.0)

    # Deactivate Head tracking
    isEnabled    = False
    motionProxy.wbEnable(isEnabled)

    # send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    
def kick_droit(postureProxy, motionProxy):
    motionProxy.setWalkTargetVelocity(0, 0, 0, 0)
    ''' Example of a whole body kick
    Warning: Needs a PoseInit before executing
             Whole body balancer must be inactivated at the end of the script
    '''

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Activate Whole Body Balancer
    isEnabled  = True
    motionProxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    motionProxy.wbFootState(stateName, supportLeg)

    # Constraint Balance Motion
    isEnable   = True
    supportLeg = "Legs"
    motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

    # Com go to LLeg
    supportLeg = "LLeg"
    duration   = 2.0
    motionProxy.wbGoToBalance(supportLeg, duration)

    # RLeg is free
    stateName  = "Free"
    supportLeg = "RLeg"
    motionProxy.wbFootState(stateName, supportLeg)

    # RLeg is optimized
    effectorName = "RLeg"
    axisMask     = 63
    space        = motion.FRAME_ROBOT


    # Motion of the RLeg
    dx      = 0.1                # translation axis X (meters)
    dz      = 0.05                 # translation axis Z (meters)
    dwy     = 6.0*math.pi/180.0    # rotation axis Y (radian)


    times   = [2.0, 2.7, 4.5]
    isAbsolute = False

    targetList = [
      [-dx, 0.0, dz, 0.0, +dwy, 0.0],
      [+dx, 0.0, dz, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    motionProxy.positionInterpolation(effectorName, space, targetList,
                                 axisMask, times, isAbsolute)

    # Deactivate Head tracking
    isEnabled    = False
    motionProxy.wbEnable(isEnabled)

    # send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)