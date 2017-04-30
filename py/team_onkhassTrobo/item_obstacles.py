# IP et Port

robotIp = "#####"
robotPort = "#####"

# Appel des proxy

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

# Variables globales

security_distance = 0.5
obstacle_left = 0
obstacle_right = 0

# Fonction de detection d obstacles

def detection_obstacle():
    valL = memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
    valR = memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")

    global obstacle_left
    global obstacle_right

    if valL >= self.security_distance:
        obstacle_left = 0
    else:
        obstacle_left = 1

    if valR >= security_distance:
        obstacle_right = 0
    else:
        obstacle_right = 1
