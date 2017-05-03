#import func_file
import motion_walk
import naocrouch

class fsm():
    def __init__(self):
        self.transitions = {}
        self.states = []
        self.events = []
        self.curState = None
        self.curEvent = None
        self.prevState =None

    def add_transition(self, state1, state2, event, funct):
        key = state1+'.'+event
        self.transitions[key] = (state2, funct)

    def add_state(self, state):
        self.states.append(state)

    def add_event(self, event):
        self.events.append(event)

    def set_state(self, state):
        self.curState = state

    def set_event(self, event):
        self.curEvent = event

    def create(self):
        self.add_event('z')
        self.add_event('c')
        self.add_state('walking')
        self.add_state('crouching')

        self.set_event(self.events[1])
        self.set_state(self.states[1])

        for sta in self.states:
            for sta2 in self.states:
                if sta != sta2:
                    if sta2 == 'walking':
                        self.add_transition(sta , sta2 , 'z' , motion_walk.main)
                    elif sta2 == 'crouching':
                        self.add_transition(sta , sta2 , 'c' , naocrouch.main)

    def run(self):
        event = self.curEvent
        state = self.curState
        key = state+'.'+event
        self.prevState = state
        self.curState = self.transitions[key][0]
        func = self.transitions[key][1]
        st = "Transition - Old State : "+state+"; Event : "+event+"; New state : "+self.curState
        st = st+"; Action : "+func() #.__name__+"()"
        print(st)
        return self.transitions [key][1]

#
#a = fsm()
#a.add_event('d')
#a.add_event('z')
#a.add_event('q')
#a.add_event('s')
#a.add_state('droite')
#a.add_state('avant')
#a.add_state('gauche')
#a.add_state('reculon')

#for sta in a.states:
#    for sta2 in a.states:
#        if sta != sta2:
#            if sta2 == 'droite':
#                a.add_transition(sta , sta2 , 'd' , turn_right)
#            elif sta2 == 'gauche':
#                a.add_transition(sta , sta2 , 'q' , turn_left)
#            elif  sta2 == 'reculon':
#                a.add_transition(sta , sta2 , 's' , move_back)
#            elif sta2 == 'avant':
#                a.add_transition(sta , sta2 , 'z' , move_forward)

#a.set_event(a.events[0])
#a.set_state(a.states[1])
