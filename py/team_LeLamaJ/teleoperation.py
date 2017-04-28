import fsm
import time
import sys
import pygame
import nao_cmd as nc
pygame.init()

# draw a little area (to focus on to get keys)
pygame.display.set_mode((100, 100))

# use keyboard to control the fsm

#  Enter : event "Start"
#  Echap : event "Stop"

#  c : event "Wait"

#  z : event "Go" 
#  q : event "Turn_left"
#  d : event "Turn_right"
#  a : event "SideStep_Left"
#  e : event "SideStep_Right"
#  1 : event "Shoot_Left" (pavé numérique : 1)
#  2 : event "Shoot_Right" (pavé numérique : 2)

# global variables
f = fsm.fsm();  # finite state machine

def getKey():
    c='c'
    cok=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                cok, c = True, "z"
            elif event.key == pygame.K_q:
                cok, c = True, "q"
            elif event.key == pygame.K_s:
                cok, c = True, "s"
            elif event.key == pygame.K_d:
                cok, c = True, "d"
            elif event.key == pygame.K_a:
                cok, c = True, "a"
            elif event.key == pygame.K_e:
                cok, c = True, "e"
            elif event.key == pygame.K_c:
                cok, c = True, "c"
            elif event.key == pygame.K_return:
                cok, c = True, "enter"
            elif event.key == pygame.K_escape:
                cok, c = True, "echap"
            elif event.key == pygame.K_KP1:
                cok, c = True, "1"
            elif event.key == pygame.K_KP2:
                cok, c = True, "2"
    return cok,c

# functions (actions of the fsm)
# example of a function doRun 
def doRun():
    print(">>>>>> action : run")
    nc.marche_droite()
    time.sleep(2.0)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="z":
            event="Go"  # new event if key "s" is pressed
        elif val=="echap":
            event="Stop"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
    return event # return event to be able to define the transition

def doWait():
    print(">>>>>> action : wait for 1 s")
    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="z":
            event="Go"  # new event if key "z" is pressed
        elif val=="echap":
            event="Stop"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
    return event # return event to be able to define the transition

def doStart():
    print("Bonjour !")
    nc.initialisation()
    time.sleep(2.0)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="z":
            event="Go"  # new event if key "g" is pressed
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
    return event # return event to be able to define the transition

def doStop():
    print("Au revoir !")
    nc.veille()
    
def doTurn_Right():
    print(">>>>>> action : turn right")
    nc.rotation_droite()
    time.sleep(2.0)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="z":
            event="Go"
    return event # return event to be able to define the transition

def doTurn_Left():
    print(">>>>>> action : turn left")
    nc.rotation_gauche()
    time.sleep(2.0)
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="z":
            event="Go"
    return event 

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle")
    f.add_state ("Ready")
    f.add_state ("Run")
    f.add_state ("Rotation")

    # defines the events 
    f.add_event ("Wait")
    f.add_event ("Stop")
    f.add_event ("Go")
    f.add_event ("Start")
    f.add_event ("Turn_Right")
    f.add_event ("Turn_Left")
    
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle", "Ready", "Start", doStart);
    f.add_transition ("Ready", "Ready", "Wait", doWait);
    f.add_transition ("Ready", "Run", "Go", doRun);
    f.add_transition ("Ready", "Idle", "Stop", doStop);
    f.add_transition ("Ready", "Rotation", "Turn_Right", doTurn_Right)
    f.add_transition ("Ready", "Rotation", "Turn_Left", doTurn_Left)
    f.add_transition ("Run", "Idle", "Stop", doStop);
    f.add_transition ("Run", "Ready", "Wait", doWait);
    f.add_transition ("Run", "Run", "Go", doRun);
    f.add_transition ("Run", "Rotation", "Turn_Right", doTurn_Right)
    f.add_transition ("Run", "Rotation", "Turn_Left", doTurn_Left)
    f.add_transition ("Rotation", "Ready", "Wait", doWait)
    f.add_transition ("Rotation", "Run", "Go", doRun)
    
    # initial state
    f.set_state ("Idle")
    # first event
    f.set_event ("Start")
    # end state
    end_state = "Idle"

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print ("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print ("End of the programm")



