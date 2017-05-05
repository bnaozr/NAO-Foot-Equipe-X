
class machina:
	def __init__(self,graphe={}):
		self.graphe = graphe
		self.cur_state = None
		self.cur_event = None
		self.prev_state= None

	def add_state(self,state):
		if not(state in self.graphe):
			self.graphe[state]={}

	def add_transition(self,ei,transition,ef,function):
		if not(ei in self.graphe or ef in self.graphe):
			self.add_state(ei)
			self.add_state(ef)
		else:
			self.graphe[ei][transition]=(ef,fonction)

	def set_state(self, state):
        	self.curState = state

	def set_event(self, event):
		self.curEvent = event	
			
			
	def run(self):
		try :
        		event = self.cur_event
        		state = self.cur_state
        		self.prev_state = state
        		self.cur_state = self.graphe[state][event][0]
        		st = "Transition - Old State : "+str(state)+"; Event : "+ str(event) +"; New state : " + str(self.cur_state)
        		st = st+"; Action : "+str(self.graphe[state][event][1])
        		print st
        		return self.graphe[state][event][1]

		except Exception as e:
			print "erreur", e

	def clear(self):
		self.graphe={}	

