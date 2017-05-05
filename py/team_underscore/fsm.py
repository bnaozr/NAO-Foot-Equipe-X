#-*- coding:utf8 -*
from threading import Thread
import math

import sys
import motion
import time
from naoqi import ALProxy
import math
import time

import pygame

from foot import *
import foot

pygame.init()

if len(sys.argv) < 2:
	robotIp="localhost"
	robotPort=11212
elif sys.argv[1] == "robot":
	robotIp="172.20.12.165"
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


foot.motionProxy = motionProxy
foot.postureProxy = postureProxy
foot.voicePxy =voicePxy
foot.memoryProxy = memoryProxy
foot.sonarProxy=sonarProxy

STATE_FORWARD = 0
STATE_TURN_LEFT = 1
STATE_TURN_RIGHT = 2
STATE_TERMINATED = 3
STATE_STANDBYE = 4
STATE_BACKWARD = 5
STATE_STAND = 6
STATE_SHOOTING = 7

CONTROL_STATE_DODGE = 1




class Fsm:
	def __init__(self):
		self.state = STATE_STANDBYE
		self.ask_state = 0
		self.next_state = 9
		self.standed_by = False
		self.theta = 0
		self.x = 0
		self.y = 0
		self.control_state = 0
		self.saved_time = 0
		
		sonarProxy.subscribe("SonarApp")

	def global_next_state(self, key):
		if key == 'g':
			self.next_state = STATE_FORWARD
		elif key == 'b':
			self.next_state = STATE_BACKWARD
		elif key == 'l':
			self.next_state = STATE_TURN_LEFT
		elif key == 'r':
			self.next_state = STATE_TURN_RIGHT
		elif key == 's':
			self.next_state = STATE_TERMINATED
		elif key == 'w':	
			self.next_state = STATE_STANDBYE
		elif key == 'y':	
			self.next_state = STATE_STAND
	
	def test_stand_by(self):
		if self.standed_by:
			self.standed_by = False
			motionProxy.wakeUp()
			postureProxy.goToPosture("StandInit", 0.5)
			motionProxy.setWalkArmsEnabled(True, True)
			motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
			

	def run(self):

		if self.control_state  == CONTROL_STATE_DODGE:
			valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    			valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
			
			if (valL < 1) or (valR < 1) and (time.clock() - self.saved_time) < 2:
				self.next_state = STATE_TURN_RIGHT
			else:
				self.next_state = STATE_FORWARD
				self.control_state = 0

		if self.next_state == STATE_FORWARD:

			if self.state != STATE_FORWARD:
				if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
					print("stop move")
					motionProxy.stopMove()

				self.test_stand_by()
				motionProxy.moveInit()
				print("setting celerity")
				motionProxy.setWalkTargetVelocity(0.5, 0, 0, 0)
			self.state = STATE_FORWARD
			
			valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    			valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
			
			#if (valL < 0.5) or (valR < 0.5):
			#	self.control_state = CONTROL_STATE_DODGE
			#	self.save_time = time.clock()

			#sonarProxy.unsubscribe("SonarApp")
    			#print valL, valR
    #sonarProxy.unsubscribe("SonarApp");

		elif self.next_state == STATE_BACKWARD:

			if self.state != STATE_BACKWARD:
				if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
					print("stop move")
					motionProxy.stopMove()

				self.test_stand_by()
				motionProxy.moveInit()
				print("setting celerity")
				motionProxy.setWalkTargetVelocity(-0.4, 0, 0, 0)
			self.state = STATE_BACKWARD
			
			valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    			valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
			
			if (valL < 0.2) or (valR < 0.2):
				self.control_state = CONTROL_STATE_DODGE
				self.save_time = time.clock()
			#sonarProxy.unsubscribe("SonarApp")
    			#print valL, valR
    #sonarProxy.unsubscribe("SonarApp");

			
		elif self.next_state == STATE_TURN_LEFT:
			if self.state != STATE_TURN_LEFT:
				if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
					print("stop move")
					motionProxy.stopMove()

				self.test_stand_by()	
				motionProxy.moveInit()
				motionProxy.move(0, 0, 0.3)
			self.state = STATE_TURN_LEFT

		elif self.next_state == STATE_TURN_RIGHT:
			if self.state != STATE_TURN_RIGHT:
				if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
					print("stop move")
					motionProxy.stopMove()

				self.test_stand_by()
				motionProxy.moveInit()
				motionProxy.move(0, 0, -0.3)
			self.state = STATE_TURN_RIGHT


		elif self.next_state == STATE_TERMINATED:
			if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
				print("stop move")
				motionProxy.stopMove()
			self.standed_by = True
			postureProxy.goToPosture("Crouch", 0.3)
			motionProxy.setStiffnesses("Body", 0.0)
			motionProxy.rest()

			self.state = STATE_TERMINATED
			

		elif self.next_state == STATE_STANDBYE:
			if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
				print("stop move")
				motionProxy.stopMove()

			if not self.standed_by:
				self.standed_by = True
				motionProxy.rest()
			self.state = STATE_STANDBYE

		elif self.next_state == STATE_STAND:
			
			if ((self.state != STATE_TERMINATED) and (self.state != STATE_STANDBYE)):
				print("stop move")
				motionProxy.stopMove()
				motionProxy.moveInit()

			if self.state != STATE_STAND and self.state != STATE_SHOOTING:
				postureProxy.goToPosture("StandInit", 0.5)
			
			self.state = STATE_STAND


		elif self.next_state == STATE_SHOOTING:
			self.state = STATE_SHOOTING


				





class Key_listener(Thread):
	def __init__(self, fsm):
		Thread.__init__(self)
		self.fsm = fsm
		self.joy = pygame.joystick.Joystick(0)
		self.joy.init()
	
	def run(self):
   		screen = pygame.display.set_mode((550,351))
   		#pygame.display.set_caption("Key_recognition_test")
   		background=pygame.Surface(screen.get_size())
    
  		background=background.convert()
   		FPS=60
   		keepgoing = True
   		clock=pygame.time.Clock()
   	 	screen.blit(background,(0,0))
		ps = 0
		c = STATE_STAND
		tirG = 0
		tirD = 0
		tirLG = 0
		tirLD = 0
		while True:
		        for event in pygame.event.get():
		            if event.type == pygame.QUIT:
		                keepgoing = False
				pygame.quit()

			Roulis = self.joy.get_axis(0)
			Tangage = self.joy.get_axis(1)
			start =self.joy.get_button(0)
			stop = self.joy.get_button(1)
			
			#if self.joy.get_button(2) != tirG:
			#	tirG = self.joy.get_button(2)
			#tirG = self.joy.get_button(2) - tirG
			#tirD = self.joy.get_button(3) - tirD
			#tirLG = self.joy.get_button(4) - tirLG
			#tirLD = self.joy.get_button(5) - tirLD
			sleep = self.joy.get_button(6)


        		if start:
				c = STATE_STAND

       		 	elif stop:
				c = STATE_TERMINATED

     		   	elif Tangage < -0.5:
				c = STATE_FORWARD
            
     		   	elif sleep:
				c =  STATE_STANDBYE
       	     
        		elif Roulis < -0.5:
				c = STATE_TURN_LEFT
            
        		elif Roulis > 0.5:
				c = STATE_TURN_RIGHT
  
        		elif Tangage > 0.5:
				c = STATE_BACKWARD

  			elif Roulis == 0 and Tangage == 0:
				print("back")
				if not self.fsm.standed_by:
					c= STATE_STAND
				else:
					c=-1
    
        		else:
				c=-1



        		if self.joy.get_button(3) == 1:
				if tirD == 0:
					tirD = 1
					try:
						self.fsm.next_state = STATE_SHOOTING
						foot.rightShoot()
					except Exception as e:
						print(e)
					c = STATE_STAND
			elif self.joy.get_button(3) == 0:
				tirD = 0

  
        		if self.joy.get_button(2) == 1:
				if tirG == 0:
					tirG = self.joy.get_button(2)
					try:
						self.fsm.next_state = STATE_SHOOTING
						foot.leftShoot()
					except Exception:
						pass
					c = STATE_STAND
			elif self.joy.get_button(2) == 0:
				tirG = 0

  
        		if self.joy.get_button(4) == 1:
				if tirLG == 0:
					tirLG = self.joy.get_button(4)
					try:
						self.fsm.next_state = STATE_SHOOTING
						foot.sideLeftShoot()
					except Exception:
						pass
					c = STATE_STAND
			elif self.joy.get_button(4) == 0:
				tirLG = 0 

  
        		if self.joy.get_button(5) == 1:
				if tirLD == 0:
					tirLD = 1
					try:
						self.fsm.next_state = STATE_SHOOTING
						foot.sideRightShoot()
					except Exception:
						pass
					c = STATE_STAND

			elif self.joy.get_button(5) == 0:
				tirLD = 0



			print(c)
			if c != -1  and self.fsm.control_state != CONTROL_STATE_DODGE:
				self.fsm.next_state = c
			
	


if __name__ == "__main__":
	fsm = Fsm()
	kl = Key_listener(fsm)
	kl.start()
	while True:
		fsm.run()
	












