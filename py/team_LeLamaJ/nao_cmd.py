import sys
import motion
import time
from naoqi import ALProxy
import math

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
    
def initialisation():
    """robotIp="localhost"
    robotPort=11212"""
    robotIp="172.20.28.198"
    robotPort=9559
    tts = ALProxy("ALTextToSpeech", robotIp, robotPort)
    
    try:
        global motionProxy
        motionProxy = ALProxy("ALMotion", robotIp, robotPort)
    except Exception as e:
        print ("Could not create proxy to ALMotion")
        print ("Error was: ", e)
    
    try:
        global postureProxy
        postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
    except Exception as e:
        print ("Could not create proxy to ALRobotPosture")
        print ("Error was: ", e)
        
    StiffnessOn(motionProxy)   
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    motionProxy.setWalkArmsEnabled(True, True)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    tts.say("Les lamas vaincront")
    tts.say("Je s'appelle Groot")
    tts.say("I am Groot")

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

def marche_arriere():
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    x = -0.5
    y = 0.0
    theta = 0.0
    motionProxy.moveTo (x, y, theta)
    
def pas_cote_droit():
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    footStepsList = []

    footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])

    footStepsList.append([["LLeg"], [[0.00, 0.1, 0.0]]])

    footStepsList.append([["RLeg"], [[0.00, -0.16, 0.0]]])

    footStepsList.append([["LLeg"], [[0.04, 0.1, 0.0]]])

    stepFrequency = 0.8
    clearExisting = False
    nbStepDance = 4 

    for j in range( nbStepDance ):
        for i in range( len(footStepsList) ):
            motionProxy.setFootStepsWithSpeed(
                footStepsList[i][0],
                footStepsList[i][1],
                [stepFrequency],
                clearExisting)
    
    pass

def pas_cote_gauche():
    motionProxy.wakeUp()
    postureProxy.goToPosture("StandInit", 0.5)
    # On definit les pas un par un
    footStepsList = []

    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])

    footStepsList.append([["RLeg"], [[0.00, -0.1, 0.0]]])
    
    footStepsList.append([["LLeg"], [[0.00, 0.16, 0.0]]])

    footStepsList.append([["RLeg"], [[-0.04, -0.1, 0.0]]])

    # Le nao bouge ses pieds un par un 
    stepFrequency = 0.8
    clearExisting = False
    nbStepDance = 4 # on lui demande de faire 4 pas de cote

    for j in range( nbStepDance ):
        for i in range( len(footStepsList) ):
            motionProxy.setFootStepsWithSpeed(
                footStepsList[i][0],
                footStepsList[i][1],
                [stepFrequency],
                clearExisting)