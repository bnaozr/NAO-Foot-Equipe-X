#-*- coding:utf8 -*
from threading import Thread
import math

import sys
import motion
import time
from naoqi import ALProxy
import math
import time

import almath




if len(sys.argv) < 2:
	robotIp="localhost"
	robotPort=11212
elif sys.argv[1] == "robot":
	robotIp="172.20.28.198"
	robotPort=9559
	print("TRying to connect to robot..")
else:
	robotIp="localhost"
	robotPort=11212	


#if (len(sys.argv) >= 2):
#    robotIp = sys.argv[1]
#if (len(sys.argv) >= 3):
#    robotPort = int(sys.argv[2])

print robotIp
print robotPort

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

try:
    voicePxy = ALProxy("ALTextToSpeech", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to text2speech"
    print "Error was: ", e

try:
    memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ", e

try:
    sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALSonar"
    print "Error was: ", e

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)



class Robot:
	def __init__(self, rt, ia, am, space):
		self.d_mvt = {}
		self.reference_time = rt
		self.isAbsolute = ia
		self.axisMask = am
		self.space = space

	def mvt(self, where, path):
		if not self.d_mvt.has_key(where):
			self.d_mvt[where] = path
		else:
			old_path = self.d_mvt[where]
			saved_path = [el1 + el2 for el1, el2 in zip(path, old_path)]
			self.d_mvt[where] = saved_path
		
		motionProxy.positionInterpolation(where, self.space, path, self.axisMask, self.reference_time, self.isAbsolute)

	def setNeutral(self):
		for key, value in self.d_mvt.items():
			neutral_path = [-el for el in value]
			motionProxy.positionInterpolation(key, self.space, neutral_path, self.axisMask, self.reference_time, self.isAbsolute)

def leftShoot():
	effectorF = "LLeg"
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(0.75, isAbsolute, axisMask, space)


	robot.mvt("Torso", [0.0,  -0.05,  0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [-0.1,  0.0,  0.03, 0.0, 0.0, 0.0])	
	robot.mvt(effectorF, [0.2,  0.0,  0.0, 0.0, 0.0, 0.0])	


	robot.setNeutral()

def rightShoot():
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(1.0, isAbsolute, axisMask, space)

	effector   = "Torso"
		     # x      y     z   wx   wy   wz
	path       = [0.0,  0.05,  0.0, 0.0, 0.0, 0.0]
	times      = 0.5                    # seconds

	robot.mvt(effector, path)
	
	effector   = "RLeg"
		     # x      y     z   wx   wy   wz
	path       = [-0.1,  0.0,  0.03, 0.0, 0.0, 0.0]
	times      = 0.5                    # seconds



	robot.mvt(effector, path)	

	effector   = "RLeg"
		     # x      y     z   wx   wy   wz
	path       = [0.2,  0.0,  0.0, 0.0, 0.0, 0.0]
	times      = 0.5

	robot.mvt(effector, path)	

	effector   = "RLeg"
		     # x      y     z   wx   wy   wz
	path       = [-0.1,  0.0,  -0.03, 0.0, 0.0, 0.0]
	times      = 0.5                    # seconds

	#robot.mvt(effector, path)

	effector   = "Torso"
		     # x      y     z   wx   wy   wz
	path       = [0.0,  -0.05,  0.0, 0.0, 0.0, 0.0]
	times      = 0.5                    # seconds

	#robot.mvt(effector, path)

	robot.setNeutral()


def sideLeftShoot():
	effectorF = "LLeg"
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(1, isAbsolute, axisMask, space)


	robot.mvt("Torso", [0.0,  -0.05,  0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [0.0,  0.0,  0.05, 0.0, 0.0, 0.0])	

	robot.mvt(effectorF, [0.0,  0.1,  0.0, 0.0, 0.0, 0.0])		

	postureProxy.goToPosture("StandInit", 0.5)


def main():
	#leftShoot()
	#rightShoot()
	sideLeftShoot()

if __name__ == "__main__":
	main()
	

	












