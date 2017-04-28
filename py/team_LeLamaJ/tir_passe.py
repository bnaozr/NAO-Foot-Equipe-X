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
import select
import actions

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c
    
def doShoot_right():
    print(">>>>>>> action: tirer avec le pied droit")
    actions.SR()
    newKey,val = getKey(); # check if key pressed
    event="Frappe_droite" # define the default event
    if newKey:
        if val=="w":
            event="Wait" # new event if key "w" is pressed
        if val=="s":
            event="Stop" 
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm def doRun():
