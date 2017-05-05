import select
from naoqi import ALProxy
import motion 

robotIp="localhost"
#robotIp="172.20.16.13"
robotPort=11212
#robotPort=9559

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def Esquive():
    sonar_left=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    sonar_right=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    dmini=min(sonar_left,sonar_right)
	if dmini < 0.3 and dmini>0.1:
		f.curState="Idle"
		motionProxy.setWalkTargetVelocity(0,0,0,0)
		if sonar_left<sonar_right:
			motionProxy.setWalkTargetVelocity(0.8,0,-0.5,0.5)
		else:
			motionProxy.setWalkTargetVelocity(0.8,0,0.5,0.5)
	elif dmini<0.1:
		f.curState="Idle"
		if abs(sonar_left-sonar_right)<0.005:
			motionProxy.setWalkTargetVelocity(-1,0,0,0.5)
		elif sonar_left<sonar_right:
			motionProxy.setWalkTargetVelocity(-1,0,-0.5,0.5)
		else:
			motionProxy.setWalkTargetVelocity(-1,0,0.5,0.5)  
			
		 



sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
sonarProxy.subscribe("myApplication")
memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
