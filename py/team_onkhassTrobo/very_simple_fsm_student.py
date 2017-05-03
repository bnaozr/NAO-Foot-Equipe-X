import fsm
from time import sleep
import sys
from key import *

# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine

#def getKey():
#    c='s'
#    cok=False
#    # insert your code here
#    # this function must return cok=True if a key has been hit
#    #                           and cok=False if no key has been hit
#    # c is the code of key
#    return cok,c
    
global deltat
deltat=1.0
# functions (actions of the fsm)
# example of a function doRun 
def doRun():
    print("run")  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Go" # define the default event
    if newKey:
        if val=="w":
            event="Wait"  # new event if key "w" is pressed
    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 


def doWait():
    print("wait")  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Wait" # define the default event
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
    print("right")  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Right" # define the default event
    if newKey:
        if val=="w":
            event="Wait"
    return event  
    
def doLeft():
    print("left")  # do some work
    sleep(deltat)
    newKey,val = getKey() # check if key pressed
    event="Left" # define the default event
    if newKey:
        if val=="w":
            event="Wait"
    return event    
    

if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") # example
    # add here all the states you need
    f.add_state ("Running")
    f.add_state ("Waiting")
    f.add_state ("Turning_Left")
    f.add_state ("Turning_Right")

    # defines the events 
    f.add_event ("Wait") # example
    f.add_event ("Go")
    f.add_event ("Left")
    f.add_event ("Right")
    f.add_event ("Stop")
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Wait",doWait); # example
    # add here all the transitions you need
    f.add_transition ("Idle","Idle","Wait",doWait)
    f.add_transition ("Idle","Running","Go",doRun)
    f.add_transition ("Running","Running","Go",doRun)
    f.add_transition ("Idle","Waiting","Stop",doWait)
    f.add_transition ("Idle","Turning_Left","Left",doLeft)
    f.add_transition ("Turning_Left","Turning_Left","Left",doLeft)
    f.add_transition ("Idle","Turning_Right","Right",doRight)
    f.add_transition ("Turning_Right","Turning_Right","Right",doRight)
    
    

    # initial state
    f.set_state ("Idle") # ... replace with your initial state
    # first event
    f.set_event ("Wait") # ...  replace with you first event 
    # end state
    end_state = "End" # ... replace  with your end state

 
    # fsm loop
    run = True   
    while (run):
        funct = f.run () # function to be executed in the new state
        if f.curState != end_state:
            newEvent = funct() # new event when state action is finished
            print("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print("End of the programm")



