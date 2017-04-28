import fsm
import time
import evitement
import sys
import pygame
import nao_cmd as nc
import test_droit as td
import test_gauche as tg
pygame.init()

# draw a little area (to focus on to get keys)
pygame.display.set_mode((100, 100))

robotIp="172.20.28.198"
robotPort=9559

# use keyboard to control the fsm

#  Enter : event "Start"
#  Echap : event "Stop"

#  c : event "Wait"

#  z : event "Go" 
#  q : event "Turn_left"
#  s : event "Go_Back"
#  d : event "Turn_right"
#  a : event "SideStep_Left"
#  e : event "SideStep_Right"
#  1 : event "Shoot_Left" (pave numerique : 1)
#  2 : event "Shoot_Right" (pave numerique : 2)

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
            elif event.key == pygame.K_RETURN:
                cok, c = True, "enter"
            elif event.key == pygame.K_ESCAPE:
                cok, c = True, "echap"
            elif event.key == pygame.K_KP1:
                cok, c = True, "1"
            elif event.key == pygame.K_KP2:
                cok, c = True, "2"
    return cok,c

# functions (actions of the fsm)
def doRun():
    print(">>>>>> action : run")
    nc.marche_droite()
    newKey,val = getKey();
    event="Wait"
    if newKey:
        if val=="z":
            event="Go"
        elif val=="echap":
            event="Stop"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event 

def doWait():
    print(">>>>>> action : wait")
    evitement.eviter()
    time.sleep(0.5)
    newKey,val = getKey(); 
    event="Wait"
    if newKey:
        if val=="z":
            event="Go" 
        elif val=="echap":
            event="Stop"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event 

def doStart():
    print("Bonjour !")
    nc.initialisation()
    time.sleep(1.0)
    newKey,val = getKey(); 
    event="Wait"
    if newKey:
        if val=="echap":
            event="Stop"  
    return event 

def doStop():
    print("Au revoir !")
    nc.veille()
    
def doTurn_Right():
    print(">>>>>> action : turn right")
    nc.rotation_droite()
    newKey,val = getKey(); # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event 

def doTurn_Left():
    print(">>>>>> action : turn left")
    nc.rotation_gauche()
    newKey,val = getKey(); 
    event="Wait" 
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event 

def doSideStep_Right():
    print(">>>>>> action : side step right")
    nc.pas_cote_droit()
    newKey,val = getKey(); 
    event="Wait" 
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event

def doSideStep_Left():
    print(">>>>>> action : side step left")
    nc.pas_cote_gauche()
    newKey,val = getKey(); 
    event="Wait" 
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event

def doGo_Back():
    print(">>>>>> action : go back")
    nc.marche_arriere()
    newKey,val = getKey();
    event="Wait"
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event

def doShoot_Right():
    print(">>>>>> action : shoot right")
    td.main(robotIp)
    newKey,val = getKey(); 
    event="Wait" 
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
    return event

def doShoot_Left():
    print(">>>>>> action : shoot left")
    tg.main(robotIp)
    newKey,val = getKey(); 
    event="Wait" 
    if newKey:
        if val=="z":
            event="Go"
        elif val=="d":
            event="Turn_Right"
        elif val=="q":
            event="Turn_Left"
        elif val=="s":
            event="Go_Back"
        elif val=="a":
            event="SideStep_Left"
        elif val=="e":
            event="SideStep_Right"
        elif val=="1":
            event="Shoot_Left"
        elif val=="2":
            event="Shoot_Right"
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
    f.add_event ("Go_Back")
    f.add_event ("SideStep_Right")
    f.add_event ("SideStep_Left")
    f.add_event ("Shoot_Left")
    f.add_event ("Shoot_Right")
    
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle", "Ready", "Start", doStart);
    f.add_transition ("Ready", "Ready", "Wait", doWait);
    f.add_transition ("Ready", "Idle", "Stop", doStop);
    f.add_transition ("Ready", "Rotation", "Turn_Right", doTurn_Right)
    f.add_transition ("Ready", "Rotation", "Turn_Left", doTurn_Left)
    f.add_transition ("Ready", "Run", "SideStep_Left", doSideStep_Left)
    f.add_transition ("Ready", "Run", "SideStep_Right", doSideStep_Right)
    f.add_transition ("Ready", "Run", "Shoot_Left", doShoot_Left)
    f.add_transition ("Ready", "Run", "Shoot_Right", doShoot_Right)
    f.add_transition ("Ready", "Run", "Go_Back", doGo_Back)
    f.add_transition ("Ready", "Run", "Go", doRun);
    f.add_transition ("Run", "Idle", "Stop", doStop);
    f.add_transition ("Run", "Ready", "Wait", doWait);
    f.add_transition ("Run", "Run", "Go", doRun);
    f.add_transition ("Run", "Rotation", "Turn_Right", doTurn_Right)
    f.add_transition ("Run", "Rotation", "Turn_Left", doTurn_Left)
    f.add_transition ("Run", "Run", "SideStep_Left", doSideStep_Left)
    f.add_transition ("Run", "Run", "SideStep_Right", doSideStep_Right)
    f.add_transition ("Run", "Run", "Shoot_Left", doShoot_Left)
    f.add_transition ("Run", "Run", "Shoot_Right", doShoot_Right)
    f.add_transition ("Run", "Run", "Go_Back", doGo_Back)
    f.add_transition ("Rotation", "Ready", "Wait", doWait)
    f.add_transition ("Rotation", "Run", "Go", doRun)
    f.add_transition ("Rotation", "Rotation", "Turn_Right", doTurn_Right)
    f.add_transition ("Rotation", "Rotation", "Turn_Left", doTurn_Left)
    f.add_transition ("Rotation", "Run", "SideStep_Left", doSideStep_Left)
    f.add_transition ("Rotation", "Run", "SideStep_Right", doSideStep_Right)
    f.add_transition ("Rotation", "Run", "Shoot_Left", doShoot_Left)
    f.add_transition ("Rotation", "Run", "Shoot_Right", doShoot_Right)
    f.add_transition ("Rotation", "Run", "Go_Back", doGo_Back)
    
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



