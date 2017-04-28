import fsm
import select 
from time import sleep
import sys
from key import isData , getKey
from funct_file import *


f = fsm.fsm();  # finite state machine

    
##global deltat
deltat=1.0
# functions (actions of the fsm)
# example of a function doRun 
def doRun():
    nao_run()  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val=="l":
            event = "Left"
        if val == "r":
            event = "Right"
        if val == "s":
            event = "Stop"# new event if key "w" is pressed
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 


def doStop():
    nao_pls()  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Stop" # define the default event
    if newKey:
        if val=="u":
            event = "StandUp"
    return event

def doStandUp():
    nao_stand_up()
    sleep(deltat)
    newKey , val = getKey()
    event = "Wait"
    if newKey:
        if val=="s":
            event="Stop"
        if val=="g":
            event="Go"
        if val=="l":
            event="Left"
        if val=="r":
            event="Right"
    return event
    
def doWait():
##    print("I m waiting for a keyboard input")    
    sleep(deltat)
    newKey , val = getKey()
    event = "Wait"
    if newKey:
        if val=="s":
            event="Stop"
        if val=="g":
            event="Go"
        if val=="l":
            event="Left"
        if val=="r":
            event="Right"
    return event
    
    
def doRight():
    nao_turn_right()  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val == "s":
            event="Stop"
        if val == "g":
            event = "Go"
        if val == "l":
            event = "Left"
        if val == "r":
            event = "Right"
    return event  
    
def doLeft():
    nao_turn_left()  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
    if newKey:
        if val == "s":
            event="Stop"
        if val == "g":
            event = "Go"
        if val == "l":
            event = "Left"
        if val == "r":
            event = "Right"
    return event   
    

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle")
    f.add_state("Standing")
    f.add_state ("Running")
    f.add_state ("Turning_Left")
    f.add_state ("Turning_Right")
    f.add_state ("Waiting")

    # defines the events 
    f.add_event ("Stop")
    f.add_event("StandUp")
    f.add_event ("Go")
    f.add_event ("Left")
    f.add_event ("Right")
    f.add_event ("Wait")
    
    f.add_transition ("Idle" , "Idle" , "Stop" , doStop)
    f.add_transition ("Idle" , "Standing" , "StandUp" , doStandUp)
    
    f.add_transition ("Standing","Idle","Stop",doStop)
    f.add_transition ("Standing","Running","Go",doRun)
    f.add_transition ("Standing","Turning_Left","Left",doLeft)
    f.add_transition ("Standing","Turning_Right","Right",doRight)
    f.add_transition ("Standing","Waiting","Wait",doWait)
    
    f.add_transition ("Running","Idle","Stop",doStop)
    f.add_transition ("Running","Running","Go",doRun)
    f.add_transition ("Running","Turning_Left","Left",doLeft)
    f.add_transition ("Running","Turning_Right","Right",doRight)
    f.add_transition ("Running","Waiting","Wait",doWait)
    
    f.add_transition ("Turning_Left","Idle","Stop",doStop)
    f.add_transition ("Turning_Left","Running","Go",doRun)
    f.add_transition ("Tuning_Left","Tuning_Left","Left",doLeft)
    f.add_transition ("Turning_Left","Turning_Right","Right",doRight)
    f.add_transition ("Turning_Left","Waiting","Wait",doWait)
    
    f.add_transition ("Turning_Right","Idle","Stop",doStop)
    f.add_transition ("Turning_Right","Running","Go",doRun)
    f.add_transition ("Turning_Right","Turning_Left","Left",doLeft)
    f.add_transition ("Turning_Right","Turning_Right","Right",doRight)
    f.add_transition ("Turning_Right","Waiting","Wait",doWait)
    
    f.add_transition ("Waiting","Idle","Stop",doStop)
    f.add_transition ("Waiting","Running","Go",doRun)
    f.add_transition ("Waiting","Turning_Left","Left",doLeft)
    f.add_transition ("Waiting","Turning_Right","Right",doRight)
    f.add_transition ("Waiting","Waiting","Wait",doWait)
    
    

    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("StandUp") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
##            print("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
##    print("End of the programm")



