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

if __name__ == "__main__":
	robotIp="172.20.12.165"
	robotPort=9559

#if len(sys.argv) < 2:
#	robotIp="localhost"
#	robotPort=11212
#elif sys.argv[1] == "robot":
#	robotIp="172.20.13.134"
#	robotPort=9559
#	print("TRying to connect to robot..")
#else:
#	robotIp="localhost"
#	robotPort=11212	


	if (len(sys.argv) >= 2):
    		robotIp = sys.argv[1]
	if (len(sys.argv) >= 3):
    		robotPort = int(sys.argv[2])

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
		self.tempo_time = 0

	def mvt(self, where, path):
		reference_time = 0
		if self.tempo_time != 0:
			reference_time = self.tempo_time
			self.tempo_time = 0
		else:
			reference_time = self.reference_time
			
		if not self.d_mvt.has_key(where):
			self.d_mvt[where] = path
		else:
			old_path = self.d_mvt[where]
			saved_path = [el1 + el2 for el1, el2 in zip(path, old_path)]
			self.d_mvt[where] = saved_path
		
		motionProxy.positionInterpolation(where, self.space, path, self.axisMask, reference_time, self.isAbsolute)

	def setNeutral(self):
		for key, value in self.d_mvt.items():
			neutral_path = [-el for el in value]
			motionProxy.positionInterpolation(key, self.space, neutral_path, self.axisMask, reference_time, self.isAbsolute)
	def changeReferenceTimeForNextAction(self, time):
		self.tempo_time = time

def leftShoot():
	effectorF = "LLeg"
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(0.75, isAbsolute, axisMask, space)


	robot.mvt("Torso", [0.02,  -0.08,  0.0, 0.0, 0.0, 0.0])
	robot.mvt("RArm",  [0.0, -0.08, 0.05, 0.0, 0.0, 0.0])
	robot.mvt("RArm",  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [ 0.0, 0.0,  0.03, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [ -0.04, 0.0,  0.0, 0.0, 0.0, 0.0])
	robot.changeReferenceTimeForNextAction(0.2)
	robot.mvt(effectorF, [ 0.1, 0.0,  0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [ -0.08, 0.0,  0.0, 0.0, 0.0, 0.0])

	postureProxy.goToPosture("StandInit", 0.3)


def rightShoot():
	effectorF = "RLeg"
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(0.75, isAbsolute, axisMask, space)


	robot.mvt("Torso", [-0.02,  0.07,  0.0, 0.0, 0.0, 0.0])
	robot.mvt("LArm",  [0.0, 0.07, 0.06, 0.0, 0.0, 0.0])
	robot.mvt("LArm",  [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [ 0.0, 0.0,  0.03, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [ -0.04, 0.0,  0.0, 0.0, 0.0, 0.0])
	robot.changeReferenceTimeForNextAction(0.2)
	robot.mvt(effectorF, [ 0.1, 0.0,  0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [ -0.08, 0.0,  -0.01, 0.0, 0.0, 0.0])

	postureProxy.goToPosture("StandInit", 0.3)
	


def sideLeftShoot():
	effectorF = "LLeg"
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(1, isAbsolute, axisMask, space)


	robot.mvt("Torso", [0.0,  -0.083,  0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [0.0,  0.0,  0.05, 0.0, 0.0, 0.0])
	robot.changeReferenceTimeForNextAction(0.25)
	robot.mvt(effectorF, [0.0,  0.08,  0.0, 0.0, 0.0, 0.0])		

	postureProxy.goToPosture("StandInit", 0.5)

def sideRightShoot():
	effectorF = "RLeg"
	StiffnessOn(motionProxy)

	# Send NAO to Pose Init
	postureProxy.goToPosture("StandInit", 0.5)

	space      = motion.FRAME_ROBOT
	axisMask   = almath.AXIS_MASK_ALL   # full control
	isAbsolute = False

	robot = Robot(1, isAbsolute, axisMask, space)


	robot.mvt("Torso", [0.0,  0.07,  0.0, 0.0, 0.0, 0.0])
	robot.mvt(effectorF, [0.0,  0.0,  0.05, 0.0, 0.0, 0.0])	
	robot.changeReferenceTimeForNextAction(0.25)
	robot.mvt(effectorF, [0.0,  -0.12,  0.0, 0.0, 0.0, 0.0])		

	postureProxy.goToPosture("StandInit", 0.5)



def main():
	leftShoot() #fini
	rightShoot() #fini
	sideLeftShoot() #fini
	sideRightShoot() #fini

if __name__ == "__main__":
	main()
	

	












