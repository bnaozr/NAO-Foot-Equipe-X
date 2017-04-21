import sys
import motion
import time
from naoqi import ALProxy
import math


robotIp="172.20.26.29"
robotIp="betanao"
robotIp="172.20.11.241"
robotPort=9559

robotIp="localhost"
robotPort=11212


if (len(sys.argv) < 4):
    print "args are : jointNum, jointMode (0 read/ 1 write), jointVal (degr.)"
    exit(0)

iJoint = int(sys.argv[1])
rdWr = int(sys.argv[2])
ang = math.pi*float(sys.argv[3])/180.0

print robotIp
print robotPort

jointsName = ["HeadYaw","HeadPitch",
              "LShoulderPitch","LShoulderRoll","LElbowYaw",
              "LElbowRoll","LWristYaw","LHand",
              "LHipYawPitch","LHipRoll","LHipPitch","LKneePitch",
              "LAnklePitch","LAnkleRoll",
              "RHipYawPitch","RHipRoll","RHipPitch","RKneePitch",
              "RAnklePitch","RAnkleRoll",
              "RShoulderPitch","RShoulderRoll","RElbowYaw",
              "RElbowRoll","RWristYaw","RHand"]

for i in range(len(jointsName)):
    print jointsName[i],i


jointName = jointsName[iJoint]

# Init proxies.
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


# Set NAO in Stiffness On 
# using wakeUp (new feature in 1.14.1)
#motionProxy.wakeUp()

print "test joint : ",jointName
if rdWr == 1:
    print ang
    motionProxy.setAngles([jointName], [ang], 0.5)
    time.sleep(1.0)

useSensors=True
angRd = motionProxy.getAngles([jointName], useSensors)
print angRd

print "Angle is : ",angRd[0]*180.0/math.pi


# End Walk (putting NAO at rest position to save power)
#motionProxy.rest()
