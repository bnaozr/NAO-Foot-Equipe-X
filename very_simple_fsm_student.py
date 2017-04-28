import fsm
import time
import sys
from naoqi import ALProxy
import motion
import select
import pygame
pygame.init()

robotIP = "localhost"
port = 11212
Frequency = 0.0 #low speed

try:
    motionProxy = ALProxy("ALMotion", robotIP, port)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e
try:
    postureProxy = ALProxy("ALRobotPosture", robotIP, port)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e


# use keyboard to control the fsm
#  a : event "Wait"
#  f : event "Sleep"
#  e : event "End"
#  r : event "Go" 
#  d : event "Droite"
#  q : event "Gauche"
#  z : event "Avancer"



# global variables
f = fsm.fsm();  # finite state machine

#stiffness for real NAO Robot
def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)



def getKey():
	cok = False
	c = 'i'
 	pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
		c,cok = 'r',True

        elif pressed[pygame.K_e]:
		c,cok = 'e',True
            
        elif pressed[pygame.K_a]:
		c,cok = 'a',True
            
        elif pressed[pygame.K_z]:
		c,cok = 'z',True
            
        elif pressed[pygame.K_f]:
		c,cok = 'f',True
            
        elif pressed[pygame.K_q]:
		c,cok = 'q',True
            
        elif pressed[pygame.K_d]:
		c,cok = 'd',True
  
        elif pressed[pygame.K_w]:
		c,cok = 'w',True 
  
        elif pressed[pygame.K_i]:
		c,cok = 'i',True 
  
        elif pressed[pygame.K_u]:
		c,cok = 'u',True 
  
        elif pressed[pygame.K_y]:
		c,cok = 'y',True 
  
        elif pressed[pygame.K_o]:
		c,cok = 'o',True 
    

        return cok,c

# functions (actions of the fsm)
def doInitialisation():
    print ">>>>>> Initialisation"   
    
    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    event="Pause" 
    return event # return event to be able to define the transition

def doStandby():
    print ">>>>>> Wait"
    X = 0
    Y = 0
    Theta = 0
    try:
        
	motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()
    newKey,val = getKey(); # check if key pressed
    event="Pause" # define the default event
    if newKey:
        if val=="d":
            event="Droite"  # new event if key "d" is pressed
        if val=="q":
            event="Gauche"  # new event if key "q" is pressed
        if val=="z":
            event="Avancer"
        if val=="w":
            event="Reculer"# new event if key "z" is pressed
        if val=="i":
            event="Shootdroit"
        if val=="u":
            event="Shootgauche"
        if val=="y":
            event="Shootlatgauche"
        if val=="o":
            event="Shootlatdroit"
        if val=="e":
            event="End"  # new event if key "d" is pressed
    return event # return event to be able to define the transition

def doWait():
    print ">>>>>> Wait"
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="r":
            event="Go"  # new event if key "d" is pressed
    return event # return event to be able to define the transition


def doRotateRight():
    print ">>>>>> Rotation Right"
    X = 0
    Y = 0
    Theta = -1
    try:
        motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()
    newKey,val = getKey(); # check if key pressed
    event="Droite" # define the default event
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition	
    
    
def doMarcheArriere():
    print ">>>>>>> Backward: run for 1 s"
    X = -1
    Y = 0
    Theta = 0

    try:
        motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()
    newKey,val = getKey(); # check if key pressed
    event="Reculer" # define the default event
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition

    

def doRotateLeft():
    print ">>>>>> Rotation"
    X = 0
    Y = 0
    Theta = 1
    try:
	motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()
    newKey,val = getKey(); # check if key pressed
    event="Gauche" # define the default event
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition


def doForward():
    print ">>>>>>> Forward : run for 1 s"
    X = 1
    Y = 0
    Theta = 0

    try:
        motionProxy.moveToward(X, Y, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        print "This example is not allowed on this robot."
        exit()
    newKey,val = getKey(); # check if key pressed
    event="Avancer" # define the default event
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition

def doCrouch():
    print ">>>>>>>>>> Crouch : run for 5 s"
    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)
    time.sleep(5.0)
    motionProxy.rest()
    newKey,val = getKey(); # check if key pressed
    event="End" # define the default event
    if newKey:
        if val=="f":
            event="Sleep"  # new event if key "a" is pressed
    return event # return event to be able to define the transition
    
def shootR():
    print ">>>>>>>>>> Shoot Droit : run for 1 s"
    newKey,val = getKey(); # check if key pressed
    event="Shootdroit"
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition
    
def shootL():
    print ">>>>>>>>>> Shoot Gauche : run for 1 s"
    newKey,val = getKey(); # check if key pressed
    event="Shootgauche"
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition

def shootLatR():
    print ">>>>>>>>>> Shoot lat Droit : run for 1 s"
    newKey,val = getKey(); # check if key pressed
    event="Shootlatdroit"
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition

def shootLatL():
    print ">>>>>>>>>> Shoot lat Gauche : run for 1 s"
    newKey,val = getKey(); # check if key pressed
    event="Shootlatgauche"
    if newKey:
        if val=="a":
            event="Pause"  # new event if key "a" is pressed
    return event # return event to be able to define the transition


if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") 
    f.add_state ("Start")
    f.add_state ("RotR")
    f.add_state ("RotL")
    f.add_state ("Forward")
    f.add_state ("Stop")
    f.add_state ("MarcheAr")
    f.add_state ("Shootdroit")
    f.add_state ("Shootgauche")
    f.add_state ("Shootlatdroit")
    f.add_state ("Shootlatgauche")

    # defines the events 
    f.add_event ("Go") 
    f.add_event ("Sleep") 
    f.add_event ("End") 
    f.add_event ("Droite") 
    f.add_event ("Gauche") 
    f.add_event ("Avancer") 
    f.add_event ("Pause") 
    f.add_event ("Wait")
    f.add_event ("Reculer")
    f.add_event ("Shootdroit")
    f.add_event ("Shootgauche")
    f.add_event ("Shootlatdroit")
    f.add_event ("Shootlatgauche")
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Wait", doWait)
    f.add_transition ("Start","Start","Pause", doStandby)
    f.add_transition ("Idle","Start","Go", doInitialisation)
    f.add_transition ("Start","RotR","Droite",doRotateRight)
    f.add_transition ("RotR","RotR","Droite",doRotateRight)
    f.add_transition ("RotR","Start","Pause",doStandby)
    f.add_transition ("Start","RotL","Gauche",doRotateLeft)
    f.add_transition ("RotL","RotL","Gauche",doRotateLeft)
    f.add_transition ("RotL","Start","Pause",doStandby)
    f.add_transition ("Start","Forward","Avancer",doForward)
    f.add_transition ("Forward","Forward","Avancer",doForward)
    f.add_transition ("Forward","Start","Pause",doStandby)
    f.add_transition ("Start","Stop","End",doCrouch)
    f.add_transition ("Stop", "Stop", "End", doRotateRight)
    f.add_transition ("Stop","Idle","Sleep",doWait)
    f.add_transition ("Start","MarcheAr","Reculer",doMarcheArriere)
    f.add_transition ("MarcheAr","Start","Pause",doStandby)
    f.add_transition ("MarcheAr","MarcheAr","Reculer",doMarcheArriere)
    f.add_transition ("Start","Shootdroit","Shootdroit",shootR)
    f.add_transition ("Shootdroit","Start","Pause",doStandby)
    f.add_transition ("Shootdroit","Shootdroit","Shootdroit",shootR)
    f.add_transition ("Start","Shootgauche","Shootgauche",shootL)
    f.add_transition ("Shootgauche","Start","Pause",doStandby)
    f.add_transition ("Shootgauche","Shootgauche","Shootgauche",shootL)
    f.add_transition ("Start","Shootlatdroit","Shootlatdroit",shootLatR)
    f.add_transition ("Shootlatdroit","Start","Pause",doStandby)
    f.add_transition ("Shootlatdroit","Shootlatdroit","Shootlatdroit",shootLatR)
    f.add_transition ("Start","Shootlatgauche","Shootlatgauche",shootLatL)
    f.add_transition ("Shootlatgauche","Start","Pause",doStandby)
    f.add_transition ("Shootlatgauche","Shootlatgauche","Shootlatgauche",shootLatL)
    

    # initial state
    f.set_state ("Idle") # initial state
    # first event
    f.set_event ("Wait") # first event 
    # end state
    end_state = "Stop" # end state
    #Pygame_stuff
    screen = pygame.display.set_mode((50,50))
    pygame.display.set_caption("Key_recognition_test")
    background=pygame.Surface(screen.get_size())
    background.fill((0,0,0))
    
    background=background.convert()
    FPS=60
    keepgoing = True
    clock=pygame.time.Clock()
    screen.blit(background,(0,0))    
 
    # fsm loop
    while keepgoing :
        clock.tick(FPS)
	funct = f.run ()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepgoing = False
		pygame.quit()
	if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print "New Event : ",newEvent
            f.set_event(newEvent) # set new event for next transition

            
    print "End of the programm"
    pygame.display.flip()  




