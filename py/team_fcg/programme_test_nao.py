"""refaire fonctions action robot avec le fichier test squarewalk"""

import naocmd
import fsm
import time
import pygame
import sys
pygame.init()
import select 
import naocmd

robotPORT=9559
#11212 pour simulateur
#9559 pour robot reel


robotIP = "172.20.16.13"
#127.0.0.1 pour simulateur

#11212 pour simulateur
#9559 pour robot reel

from naoqi import ALProxy

tts = ALProxy("ALTextToSpeech", robotIP, robotPORT)
tts.setLanguage("French")
tts.say("que les meilleurs perdent")




try:
    motionProxy = ALProxy("ALMotion", robotIP, robotPORT)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, robotPORT)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

pygame.display.set_mode((100, 100))
    
# Set NAO in Stiffness On
naocmd.StiffnessOn(motionProxy)

# Send NAO to Pose Init
postureProxy.goToPosture("StandInit", 0.5)

#####################
## Enable arms control by Walk algorithm
#####################
motionProxy.setWalkArmsEnabled(True, True)
#~ motionProxy.setWalkArmsEnabled(False, False)

#####################
## FOOT CONTACT PROTECTION
#####################
#~ motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", False]])
motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine


def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    c='w'
    cok=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            cok=True
            #print event.type,event.key,pygame.K_w,pygame.K_s
            if event.key == pygame.K_UP:
                c="g"
            elif event.key == pygame.K_LEFT:
                c="l"
            elif event.key == pygame.K_RIGHT:
                c="r"
            elif event.key == pygame.K_s:
                c="s"
            elif event.key == pygame.K_w:
                c="w"    
            elif event.key == pygame.K_DOWN:
                c="b"  
            elif event.key == pygame.K_a:
                c="kick_gauche"
            elif event.key == pygame.K_e:
                c="kick_droite"            
    return cok,c
    

    
# functions (actions of the fsm)
# example of a function doRun 
def doavancer():
    print ">>>>>> action : run for 1 s"   # do some work
    naocmd.marcher(motionProxy)
#    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="g" # define the default event
    if newKey:
        if val=="w":
            event="w"  # new event if key "w" is pressed
        elif val=="9":
            event=="courbe_droite_fwd"
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 

def doreculer():
    print ">>>>>> action : run for 1 s"   # do some work
    naocmd.reculer(motionProxy)
#    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="b" # define the default event
    if newKey:
        if val=="w":
            event="w"  # new event if key "w" is pressed
    return event # return event to be able to define the transition
# ...
def doleft():
    print ">>>>>> action : tourner a gauche pendant 1 s"
    naocmd.tournergauche(motionProxy)
#    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="l" # define the default event
    if newKey:
        if val=="w":
            event="w"  # new event if key "w" is pressed
    return event # return event to be able to define the transition
    

    
    
def doright():
    print ">>>>>> action : tourner a droite pendant 1 s"
    naocmd.tournerdroite(motionProxy)
#    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="r" # define the default event
    if newKey:
        if val=="w":
            event="w"  # new event if key "w" is pressed
    return event # return event to be able to define the transition
    
def dostop():
    print ">>>>>> action : arreter"
    naocmd.inactif(postureProxy, motionProxy)
#    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="s" # define the default event
    if newKey:
        if val=="w":
            event="w"  # new event if key "w" is pressed
    return event # return event to be able to define the transition

    
def dowait():
    print ">>>>>> action : retourner a l'etat d'attente"
    naocmd.arret_dpt(motionProxy)
#    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="w" # define the default event
    if newKey:
        if val=="r":
            event="r"  # new event if key "Right" is pressed
        elif val=="l":
            event="l"
        elif val=="s":
            event="s"
        elif val=="g":
            event="g"
        elif val=="b":
            event="b"
        elif val=="kick_gauche":
            event="kick_gauche"
        elif val=="kick_droite":
            event="kick_droite"
    return event

def dotirerdugauche():
    print ">>>>>> action : tir du gauche en cours"
    naocmd.kick_gauche(motionProxy)  #C'est l'autre groupe qui la fournira
    event="w"
    return event
    
def dotirerdudroit():
    print ">>>>>> action : tir du droit en cours"
    naocmd.kick_droit(motionProxy)  #C'est l'autre groupe qui la fournira
    event="w"
    return event
    
def doCourbeDroiteFwd():
    print ">>>>>> action : courbe vers la droite en avant"
    ''' faire encore les courbes a gauche et en arriere'''
    naocmd.fonction  #C'est l'autre groupe qui la fournira
    event="w"
    return event   
    
if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") # example
    # add here all the states you need
    f.add_state("rotation_G")
    f.add_state("rotation_D")
    f.add_state("avancer")
    f.add_state("stop")
    f.add_state("tir_du_gauche")
    f.add_state("tir_du_droit")
    # defines the events 
    f.add_event ("w") #attente
    # add here all the events you need
    f.add_event ("s") #stop
    f.add_event ("l") #gauche
    f.add_event ("r") #droite
    f.add_event ("g") #avancer
    f.add_event("b") #reculer
    f.add_event("kg")  #tirer du gauche
    f.add_event("kd")  #tirer du droit
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","w",dowait); # example
    # add here all the transitions you need
    f.add_transition ("Idle","rotation_G","l",doleft)
    f.add_transition ("Idle","rotation_D","r",doright)
    f.add_transition ("Idle","avancer","g",doavancer)
    f.add_transition ("Idle","reculer","b",doreculer)
    f.add_transition ("Idle","stop","s",dostop)
    f.add_transition ("avancer","avancer","g",doavancer)
    f.add_transition ("reculer","reculer","b",doreculer)
    f.add_transition ("avancer","Idle","w",dowait)
    f.add_transition ("reculer","Idle","w",dowait)
    f.add_transition ("rotation_G","rotation_G","l",doleft)
    f.add_transition ("rotation_G","Idle","w",dowait)
    f.add_transition ("rotation_D","rotation_D","r",doright)
    f.add_transition ("rotation_D","Idle","w",dowait)
    f.add_transition ("Stop","Idle","w",dowait)
    f.add_transition ("Idle","tir_du_gauche","kg",dotirerdugauche)
    f.add_transition ("Idle","tir_du_droit","kd",dotirerdudroit)    
    f.add_transition ("tir_du_gauche","Idle","w",dowait)     
    f.add_transition ("tir_du_droit","Idle","w",dowait)     
    
    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("w") # ...  replace with you first event 
    # end state
    end_state = "stop" # ... replace  with your end state

    #Initialiser
    
#    naocmd.initialiser("127.0.0.1")
#    print "zouz"
    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print "New Event : ",newEvent
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print "End of the programm"



