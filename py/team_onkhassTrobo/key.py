import sys
import select 
import time 

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c


#c=""
#while (c != "!"):
#    cok,c = getKey()
#    if (cok):
#        print c
#    time.sleep(0.1)
