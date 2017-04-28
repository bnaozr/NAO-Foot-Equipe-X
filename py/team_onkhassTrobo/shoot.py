# -*- encoding: UTF-8 -*- 

''' setFootStep: Small example to make Nao execute     '''
'''              The Cha Cha Basic Steps for Men       '''
'''              Using setFootStep API                 '''
''' http://www.dancing4beginners.com/cha-cha-steps.htm '''
import sys , math
from naoqi import ALProxy
robotPort1=11212
robotPort2=11214
robotPort3=11216
robotPort4=11218


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def shoot(robotIP,robotPort):
    # Init proxies.
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
        voicePxy = ALProxy("ALTextToSpeech", robotIp, robotPort)
    except Exception, e:
        print "Could not create proxy to text2speech"
        print "Error was: ", e
    # Set NAO in stiffness On
    StiffnessOn(motionProxy)
    postureProxy.goToPosture("StandInit", 0.5)


    motionProxy.wakeUp()
    
    motionProxy.setStiffnesses("Body", 1.0)
    
    # Send NAO to Pose Init : it not standing then standing up
    postureProxy.goToPosture("StandInit", 0.5)
    
    # Enable arms control by Walk algorithm
    motionProxy.setWalkArmsEnabled(True, True)
    
    # allow to stop motion when losing ground contact, NAO stops walking
    # when lifted  (True is default)
    motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])   
    nbStepDance = 2 # defined the number of cycle to make

    x = 0.75
    y = 0.0
    theta = 0
    motionProxy.moveTo (x, y, theta)
    print "Side 1"


if __name__ == "__main__":
    robotIp = "localhost"
    robotPort = robotPort1

    if len(sys.argv) <= 1:
        print "Usage python motion_setFootStepDance.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    shoot(robotIp,robotPort)

