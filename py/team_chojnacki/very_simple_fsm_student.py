import fsm
import time
import sys
import select
import Fonctionsdebases as fdb
import pygame
t = 0.05
# use keyboard to control the fsm
#  z : event 'haut'
#  w : event "Wait"
#  s : event "Stop"
#  g : event "Go" 

# global variables
f = fsm.fsm();  # finite state machine
nao = fdb.nao()

pygame.init()
pygame.display.set_mode((100, 100))




#def isData():
#    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
#
#def getKey():
#    #tty.setcbreak(sys.stdin.fileno())
#    c='s'
#    cok=False
#    if isData():
#        c = sys.stdin.read(1)
#        cok=True
#    return cok,c



pygame.init()
pygame.display.set_mode((100, 100))

def getKey():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #print event.type,event.key,pygame.K_w,pygame.K_s
            if event.key == pygame.K_z:
                return  True,'z'
                print('Forward')
            elif event.key == pygame.K_a:
                return  True, 'a'
                print('Backward')
            elif event.key == pygame.K_q:
                return True,'q'
            elif event.key == pygame.K_s:
                return True,'s'
            elif event.key == pygame.K_d:
                return True,'d'
            elif event.key == pygame.K_w:
                return True, 'w'
            elif event.key == pygame.K_t:
                return True, 't'
            elif event.key == pygame.K_r:
                return True, 'r'
            elif event.key == pygame.K_g:
                return True, 'g'
            
            else :
                return False, 'faux'
    return False, 'faux'
#
#def getKey():
#    c='s'
#    cok=False
#    # insert your code here
#    # this function must return cok=True if a key has been hit
#    #                           and cok=False if no key has been hit
#    # c is the code of key
#    return cok,c




# functions (actions of the fsm)
# example of a function doRun 

#def DoRun():
#    print (">>>>>> action : run for 1 s")   # do some work
#    time.sleep(1)
#    newKey,val = getKey(); # check if key pressed
#    event="Go" # define the default event
#    if newKey:
#        if val=="w":
#            event="Wait"  # new event if key "w" is pressed
#    return event # return event to be able to define the transition
# define here all the other functions (actions) of the fsm 
# ...
def DoWait():
    print("Le robot attend")
    time.sleep(t)
    newKey,val = getKey()
    event ="Wait"
    nao.arreter()
    if newKey : 
        if val =="w":
            event = "Wait"
        if val == "a":
            event = "Demarrer"
        
    return event

def DoMarcher():
    print ('Le robot avance')
    time.sleep(t)
    newKey,val = getKey()
    event ="Marcher"
    nao.avancer()
    if newKey : 
        if val =="s":
            event = "Pause"
    return event
    
def Pause():
    print("Le robot attend une instructions")
    time.sleep(t)
    newKey,val = getKey()
    event = "Pause"
    nao.arreter()
    if newKey: 
        if val == "z":
            event = "Marcher"
        if val == "d":
            event = "Turn right"
        if val == "q":
            event = "Turn left"
        if val == "w":
            event = "Fin"
        if val == "t":
            event = "TirD"
        if val == "g":
            event = "Dabe"
        if val == "r":
            event = "TirG"
    return event
            
def DoDemarrer():
    print("Le robot est en mission pret a bouger")
    time.sleep(t)
    newKey,val = getKey()
    event ="Demarrer"
    nao.arreter()
    if newKey : 
        if val == "z":
            event = "Marcher"
        if val == "d":
            event = "Turn right"
        if val == "q":
            event = "Turn left"
        if val == "w":
            event = "Fin"
        if val == "t":
            event = "TirD"
        if val == "r":
            event = "TirG"
        if val == "g":
            event = "Dabe"
            
    return event

def DoTurnLeft ():
    print ('Le robot tourne a gauche')
    time.sleep(t)
    newKey,val = getKey()
    event ="Turn left"
    nao.tournerGauche()
    if newKey : 
        if val =="s":
            event = "Pause"
    return event

def DoEnd ():
    print('Bonne nuit le robot.')
    nao.veille()
    time.sleep(t)
    

def DoTurnRight():
    print ('Le robot tourne a droite')
    time.sleep(t)
    newKey,val = getKey()
    event ="Turn right"
    nao.tournerDroite()
    if newKey : 
        if val =="s":
            event = "Pause"
    return event

def DoTirD():
    print("Le robot met une lulu")
    newKey,val = getKey()
    event = "TirD"
    nao.tirerpieddroit()
    event = "Pause"
    return event

def DoTirG():
    print("Le robot met une guezzzz dans la lulu")
    newKey,val = getKey()
    event = "TirG"
    nao.tirerpiedgauche()
    event = "Pause"
    return event
    
def DoDab():
    print("J'effectue le dab")
    newKey,val = getKey()
    event = "Dabe"
    nao.dab()
    event = "Pause"
    return event 
    
if __name__== "__main__":
    
    # define the states
    f.add_state ("Idle") # example
    f.add_state ("Mission")
    f.add_state ("Avancer")
    f.add_state ("Tourner a gauche")
    f.add_state ("Tourner a droite")
    f.add_state("TirerDroit")
    f.add_state("TirerGauche")
    f.add_state ("End")
    f.add_state("Dab")
    # add here all the states you need
    # ...

    # defines the events 
    f.add_event ("Wait") # example
    f.add_event ("Walk")
    f.add_event ("Demarrer")
    f.add_event ("Turn Right")
    f.add_event ("Turn left")
    f.add_event ("Fin")
    f.add_event ("Pause")
    f.add_event ("TirD")
    f.add_event ("TirG")
    f.add_event ("Dabe")
    
    # add here all the events you need
    # ...
   
    # defines the transition matrix
    # current state, next state, event, action in next state
    f.add_transition ("Idle","Idle","Wait",DoWait); # example
    f.add_transition ("Idle", "Mission", "Demarrer",DoDemarrer)
    f.add_transition ("Mission", "Avancer", "Marcher", DoMarcher)
    f.add_transition ("Mission", "Tourner a gauche", "Turn left", DoTurnLeft)
    f.add_transition ("Mission","Tourner a droite", "Turn right", DoTurnRight)
    f.add_transition ("Mission", "End", "Fin", DoEnd)
    f.add_transition ("TirerDroit","Mission","Pause", Pause)
    f.add_transition ("TirerGauche","Mission","Pause", Pause)
    f.add_transition("Mission","TirerDroit","TirD", DoTirD)
    f.add_transition("Mission","TirerGauche","TirG", DoTirG)
    f.add_transition ("Avancer","Mission", "Pause", Pause)
    f.add_transition ("Tourner a gauche","Mission", "Pause", Pause)
    f.add_transition ("Tourner a droite","Mission", "Pause", Pause)
    f.add_transition ("Mission", "Mission", "Pause", Pause) 
    f.add_transition ("Avancer","Avancer", "Marcher", DoMarcher)
    f.add_transition ("Tourner a gauche", "Tourner a gauche", "Turn left", DoTurnLeft)
    f.add_transition ("Tourner a droite","Tourner a droite", "Turn right", DoTurnRight)
    f.add_transition ("Mission", "Mission", "Demarrer", DoDemarrer)
    
    f.add_transition ("Mission", "Dab", "Dabe", DoDab)
    f.add_transition ("Idle", "Dab", "Dabe", DoDab)
    f.add_transition ("Avancer", "Dab","Dabe", DoDab)
    
    f.add_transition ("Dab","Mission","Pause", Pause)
    # add here all the transitions you need
    # ...

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
            print ("New Event : ",newEvent)
            f.set_event(newEvent) # set new event for next transition
        else:
            funct()
            run = False
            
    print ("End of the programm")



