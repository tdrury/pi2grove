
import time, signal, sys
import RPi.GPIO as GPIO
from UltrasonicClass import *

u = Ultrasonic(args=(), kwargs={'pin':5})

def signal_handler(signal, frame):
    u.shutdown()
    GPIO.cleanup()
    print 'Ctrl+C pressed - ending'
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

print "starting Ultrasonic Measurements..."
u.start()

while(True):
    distance = u.get_last_distance()
    print "Distance: %.1f cm" % distance



