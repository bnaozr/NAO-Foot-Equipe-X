import fsm
import time
import sys
import pygame
import motion
from naoqi import ALProxy
import math
pygame.init()
pygame.display.set_mode((100, 100))

#robotIp="localhost"
#robotPort=11212

robotIp="172.20.12.134"
robotPort=9559

if (len(sys.argv) >= 2):
    robotIp = sys.argv[1]
if (len(sys.argv) >= 3):
    robotPort = int(sys.argv[2])
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
    memoryProxy = ALProxy("ALMemory", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMemory"
    print "Error was: ", e

try:
    sonarProxy = ALProxy("ALSonar", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALSonar"
    print "Error was: ", e
 
# use keyboard to control the fsm
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables

f = fsm.fsm();  # finite state machine

def getKey():
    c='p'
    cok=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #print event.type,event.key,pygame.K_w,pygame.K_s
            cok = True
            if event.key == pygame.K_z:
                print('Forward')
                c='z'
            elif event.key == pygame.K_s:
                c='s'
                print('Backward')
            elif event.key == pygame.K_q:
                print('Left')
                c='q'
            elif event.key == pygame.K_d:
                print('Right')
                c='d'
            elif event.key == pygame.K_d:
                print('PC_Left')
                c='a'
            elif event.key == pygame.K_d:
                print('PC_Right')
                c='e'
            elif event.key == pygame.K_p:
                print("PAUSE")
                c='p'
            elif event.key == pygame.K_m:
                print("STOP")
                c='m'
            elif event.key == pygame.K_l:
                print("START")
                c='l'
            elif event.key == pygame.K_r:
                print("TirGauche")
                c='r'
            elif event.key == pygame.K_t:
                print("TirDroit")
                c='t'
    return cok,c

# functions (actions of the fsm)

def doTirD():
    
        #Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 0.5)
    
        # Activate Whole Body Balancer
        isEnabled  = True
        motionProxy.wbEnable(isEnabled)
    
        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        motionProxy.wbFootState(stateName, supportLeg)
    
        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
    
        # Com go to LLeg
        supportLeg = "LLeg"
        duration   = 1.0
        motionProxy.wbGoToBalance(supportLeg, duration)
    
        # RLeg is free
        stateName  = "Free"
        supportLeg = "RLeg"
        motionProxy.wbFootState(stateName, supportLeg)
    
        # RLeg is optimized
        effectorName = "RLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT
    
    
        # Motion of the RLeg
        dx      = 0.065                # translation axis X (meters)
        dz      = 0.07               # translation axis Z (meters)
        dwy     =5*math.pi/180.0    # rotation axis Y (radian)
    
    
        times   = [1.0, 1.35, 2.25]
        isAbsolute = False
    
        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    
        motionProxy.positionInterpolation(effectorName, space, targetList,
                                     axisMask, times, isAbsolute)
        time.sleep(0.05)
        # Deactivate Head tracking
        isEnabled    = False
        motionProxy.wbEnable(isEnabled)
    
        # send robot to Pose Init
        postureProxy.goToPosture("StandInit", 0.5)
        event='go'
        return event

def doTirG():
    
        # Send NAO to Pose Init
        postureProxy.goToPosture("StandInit", 0.5)
    
        # Activate Whole Body Balancer
        isEnabled  = True
        motionProxy.wbEnable(isEnabled)
    
        # Legs are constrained fixed
        stateName  = "Fixed"
        supportLeg = "Legs"
        motionProxy.wbFootState(stateName, supportLeg)
    
        # Constraint Balance Motion
        isEnable   = True
        supportLeg = "Legs"
        motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)
     
        supportLeg = "RLeg"
        duration   = 1.0
        motionProxy.wbGoToBalance(supportLeg, duration)
    
        # RLeg is free
        stateName  = "Free"
        supportLeg = "LLeg"
        motionProxy.wbFootState(stateName, supportLeg)
    
        effectorName = "LLeg"
        axisMask     = 63
        space        = motion.FRAME_ROBOT
    
    
        # Motion of the RLeg
        dx      = 0.065              # translation axis X (meters)
        dz      = 0.07             # translation axis Z (meters)
        dwy     =5*math.pi/180.0    # rotation axis Y (radian)
    
    
        times   = [1.0, 1.35, 2.25]
        isAbsolute = False
    
        targetList = [
          [-dx, 0.0, dz, 0.0, +dwy, 0.0],
          [+dx, 0.0, dz, 0.0, 0.0, 0.0],
          [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    
        motionProxy.positionInterpolation(effectorName, space, targetList,
                                     axisMask, times, isAbsolute)    
        time.sleep(0.05)
        isEnabled    = False
        motionProxy.wbEnable(isEnabled)
        postureProxy.goToPosture("StandInit", 0.5)
        event='go'
        return event
  
def doAvance():
    print (">>>>>> action : run for 1 s")
    x = 0.5
    y = 0.0
    theta = 0.0
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(x, y, theta, Frequency)
    
    #time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="z" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'
        elif val == 'r':
            event=  'tg'
        elif val == 't' :
            event ='td'
    sonarProxy.subscribe("SonarApp");
    time.sleep(0.25)
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print(valL)
    print(valR)
    if valL > valR and valR<0.5:
        event ='q'
    elif valL<valR and valL<0.5:
        event ='d'
    sonarProxy.unsubscribe("SonarApp");
    time.sleep(1.0-0.25)
   
   
   
    return event # return event to be able to define the transition

def doRecule():
    print (">>>>>> action : back for 1 s")
    x = -0.5
    y = 0.0
    theta = 0.0
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(x, y, theta, Frequency)
    #time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="s" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'
        elif val == 'r':
            event ='tg'
        elif val == 't' :
            event ='td'
            
    sonarProxy.subscribe("SonarApp");
    time.sleep(0.25)
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
    print(valL)
    print(valR)
    if valL > valR and valR<0.5:
        event ='q'
    elif valL<valR and valL<0.5:
        event ='d'
    sonarProxy.unsubscribe("SonarApp");
    time.sleep(1.0-0.25)
    
    return event # return event to
    
def doRight():
    print (">>>>>> action : Right for 1 s")
    x = 0.0
    y = 0.0
    theta = -1
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(x, y, theta, Frequency)
    # do some work
    #time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="d" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'

        elif val == 'r':
            event ='tg'
        elif val == 't' :
            event ='td'
    return event # return event to

    
def doLeft():    
    print (">>>>>> action : Left for 1 s") 
    x = 0.0
    y = 0.0
    theta = -1
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(x, y, -theta, Frequency)# do some work
    # time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="q" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'
        elif val == 'r':
            event= 'tg'
        elif val == 't' :
            event= 'td'
    return event # return event to

def doRightPC():
    print (">>>>>> action : RightPC for 1 s")
    x = 0.0
    y = -1
    theta = 0
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(x, y, theta, Frequency)
    # do some work
    #time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="e" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'

def doLeftPC():
    print (">>>>>> action : LeftPC for 1 s")
    x = 0.0
    y = 1
    theta = 0
    Frequency = 1.0
    motionProxy.setWalkTargetVelocity(x, y, theta, Frequency)
    # do some work
    #time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="a" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'

def doChill():
    print (">>>>>> action :STOP for 1 s")
    motionProxy.rest()# do some work   # do some work
    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="Chill"
    if newKey:
        if val=="l":
            event="go"
    # define the default event
    
    return event # return event to

def doStart():
    
    #motionProxy.rest()
    
    motionProxy.wakeUp()
    
    #print("1")
    #motionProxy.setWalkArmsEnabled(True, True)
    #time.sleep(1.0)
    #print("2")
    #postureProxy.goToPosture("StandCrouch", 0.5)
    #time.sleep(1.0)
    #print("3")    
    #motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
    #time.sleep(1.0)
    
    #motionProxy.rest()
    
    motionProxy.stopMove()
    print (">>>>>> action : START for 1 s")   # do some work
    time.sleep(1.0)
    newKey,val = getKey(); # check if key pressed
    event="go" # define the default event
    if newKey:
        if val=="z":
            event="z"
        elif val=='s':
            event='s'
        elif val=='q':
            event='q'
        elif val=='d':
            event='d'
        elif val=='a':
            event='a'
        elif val=='e':
            event='e'
        elif val=='p':
            event='go'
        elif val == 'm':
            event='Chill'
        elif val == 'r':
            event= 'tg'
        elif val == 't' :
            event ='td'
    return event # return event to
    
# define here all the other functions (actions) of the fsm 
# ...

if __name__== "__main__":
    
    # define the states

    f.add_state("Start")
    f.add_state("Avance")
    f.add_state("Recule")
    f.add_state("Gauche")
    f.add_state("Droite")
    f.add_state("GauchePC")
    f.add_state("DroitePC")
    f.add_state("Stop")
    f.add_state("TirDroit")
    f.add_state("TirGauche")

    # example
    # add here all the states you need
    # ...

    # defines the events 
    
    f.add_event ("z")
    f.add_event ("q")
    f.add_event ("s")
    f.add_event ("d")
    f.add_event ("go")
    f.add_event ("a")
    f.add_event ("e")
    f.add_event ("Chill")
    f.add_event ("td")
    f.add_event ("tg")
    
    # example
    # add here all the events you need
    # ...
   
    # defines the transition matrix
    # current state, next state, event, action in next state

    f.add_transition ("Stop","Stop","Chill",doChill);
    f.add_transition ("Stop","Start","go",doStart);


    f.add_transition ("Start","Avance","z",doAvance);
    f.add_transition ("Start","Recule","s",doRecule);
    f.add_transition ("Start","Droite","d",doRight);
    f.add_transition ("Start","Gauche","q",doLeft);
    f.add_transition ("Start","DroitePC","e",doRightPC);
    f.add_transition ("Start","GauchePC","a",doLeftPC);
    f.add_transition ("Start","Start","go",doStart);   
    f.add_transition ("Start","Stop","Chill",doChill);
    f.add_transition ("Start","TirGauche","tg",doTirG);
    f.add_transition ("Start","TirDroit","td",doTirD);

    #f.add_transition ("Avance","Stop","Chill",doChill);
    f.add_transition ("Avance","Avance","z",doAvance);
    f.add_transition ("Avance","Recule","s",doRecule);
    f.add_transition ("Avance","Droite","d",doRight);
    f.add_transition ("Avance","Gauche","q",doLeft);
    f.add_transition ("Avance","DroitePC","e",doRightPC);
    f.add_transition ("Avance","GauchePC","a",doLeftPC);
    f.add_transition ("Avance","Start","go",doStart);
    f.add_transition ("Avance","TirGauche","tg",doTirG);
    f.add_transition ("Avance","TirDroit","td",doTirD);
    
    #f.add_transition ("Recule","Stop","Chill",doChill);
    f.add_transition ("Recule","Recule","s",doRecule);
    f.add_transition ("Recule","Droite","d",doRight);
    f.add_transition ("Recule","Gauche","q",doLeft);
    f.add_transition ("Recule","DroitePC","e",doRightPC);
    f.add_transition ("Recule","GauchePC","a",doLeftPC);
    f.add_transition ("Recule","Avance","z",doAvance);
    f.add_transition ("Recule","Start","go",doStart);
    f.add_transition ("Recule","TirGauche","tg",doTirG);
    f.add_transition ("Recule","TirDroit","td",doTirD);

    #f.add_transition ("Gauche","Stop","Chill",doChill);
    f.add_transition ("Gauche","Gauche","q",doLeft);
    f.add_transition ("Gauche","Avance","z",doAvance);
    f.add_transition ("Gauche","Recule","s",doRecule);
    f.add_transition ("Gauche","Droite","d",doRight);
    f.add_transition ("Gauche","Start","go",doStart);
    f.add_transition ("Gauche","TirGauche","tg",doTirG);
    f.add_transition ("Gauche","TirDroit","td",doTirD);
    f.add_transition ("Gauche","DroitePC","e",doRightPC);
    f.add_transition ("Gauche","GauchePC","a",doLeftPC);

    #f.add_transition ("Droite","Stop","Chill",doChill);
    f.add_transition ("Droite","Droite","d",doRight);
    f.add_transition ("Droite","Avance","z",doAvance);
    f.add_transition ("Droite","Recule","s",doRecule);
    f.add_transition ("Droite","Gauche","q",doLeft);
    f.add_transition ("Droite","Start","go",doStart);
    f.add_transition ("Droite","TirGauche","tg",doTirG);
    f.add_transition ("Droite","TirDroit","td",doTirD);
    f.add_transition ("Droite","DroitePC","e",doRightPC);
    f.add_transition ("Droite","GauchePC","a",doLeftPC);

    f.add_transition ("TirDroit","Strat","go",doStart);
    f.add_transition ("TirGauche","Start","go",doStart);
 # example
    # add here all the transitions you need
    # ...

    # initial state
    f.set_state ("Start") # ... replace with your initial state
    # first event
    f.set_event ("go") # ...  replace with you first event 
    # end state
    end_state = "Chill" # ... replace  with your end state

 
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



