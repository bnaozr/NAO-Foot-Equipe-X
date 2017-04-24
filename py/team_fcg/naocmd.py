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



def arret_dpt(motionProxy):      
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency =1.0 
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def inactif(postureProxy, motionProxy):
   dowait # Send NAO to Pose Init
    fractSpeed=0.3
    postureProxy.goToPosture("Crouch", fractSpeed)
    motionProxy.setStiffnesses("Body", 0.0)
    motionProxy.rest()
