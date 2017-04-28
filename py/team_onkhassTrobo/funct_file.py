import motion
from naoqi import ALProxy


def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
    
robotIP = ##......##

try:
    motionProxy = ALProxy("ALMotion", robotIP, 9559)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

def nao_stand_up():
    postureProxy.goToPosture("StandInit", 0.5)
    
def nao_run():
    X = 1.0  #backward
    Y = 0.0
    Theta = 0.0
    Frequency =0.0 # low speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def nao_turn_left():
    X = 0.  #backward
    Y = 0.0
    Theta = 90.0
    Frequency = 0.0 # low speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def nao_turn_right():
    X = 0.  #backward
    Y = 0.0
    Theta = - 1.6
    Frequency = 0.0 # low speed
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)
    
def nao_pls():
    motionProxy.rest()
    
def initialisation():
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    #####################
    ## Enable arms control by Walk algorithm
    #####################
    motionProxy.setWalkArmsEnabled(True, True)