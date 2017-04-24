#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 11:36:49 2017

@author: brugieju
"""

import sys
import motion
import time
from naoqi import ALProxy
import math

#INITIALISATION

robotIp="localhost"
robotPort=11212

# Init proxies.
try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception, e:
    print ("Could not create proxy to ALMotion")
    print ("Error was: ", e)

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception, e:
    print( "Could not create proxy to ALRobotPosture")
    print ("Error was: ", e)

motionProxy.wakeUp()
motionProxy.setStiffnesses("Body", 1.0)