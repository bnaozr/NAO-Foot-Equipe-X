# -*- encoding: UTF-8 -*- 

''' Whole Body Motion: kick '''

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


def main(robotIP):

    ''' Example of a whole body kick
    Warning: Needs a PoseInit before executing
             Whole body balancer must be inactivated at the end of the script
    '''
    print 'a'
    # Init proxies.
    try:
        proxy = ALProxy("ALMotion", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, robotPort)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(proxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    # Activate Whole Body Balancer
    isEnabled  = True
    proxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateName  = "Fixed"
    supportLeg = "Legs"
    proxy.wbFootState(stateName, supportLeg)

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
    dx      = 0.1                # translation axis X (meters)  0.1
    dz      = 1                # translation axis Z (meters) 0.05
    dwy     = 175.0*math.pi/180.0    # rotation axis Y (radian)  6


    times   = [2.0, 2.7, 4.5]   #2,2.7,4.5
    isAbsolute = False

    targetList = [
      [0, 0.0, 0, 0.0, 0, 0.0],
      [0, 0.0, 0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

#    proxy.positionInterpolation(effectorName, space, targetList,
#                                 axisMask, times, isAbsolute)


#    # Example showing how to Enable Effector Control as an Optimization
#    isActive     = False
#    proxy.wbEnableEffectorOptimization(effectorName, isActive)

    # Com go to LLeg
    supportLeg = "RLeg"
    duration   = 2  #2
    proxy.wbGoToBalance(supportLeg, duration)

    # RLeg is free
    stateName  = "Free"
    supportLeg = "LLeg"
    proxy.wbFootState(stateName, supportLeg)

    effectorName = "LLeg"
    proxy.positionInterpolation(effectorName, space, targetList,
                                axisMask, times, isAbsolute)
    time.sleep(0.3)

    # Deactivate Head tracking
    isEnabled    = False
    proxy.wbEnable(isEnabled)

    # send robot to Pose Init
    postureProxy.goToPosture("StandInit", 0.2)  #0.2


if __name__ == "__main__":
    robotIp = "localhost"  #localhost ou 172.20.14.200
    robotPort=11212 #11212 ou 9559

    if len(sys.argv) <= 1:
        print "Usage python motion_wbKick.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
