
# Import required Python libraries
import time, signal, sys
import RPi.GPIO as GPIO

def signal_handler(signal, frame):
    GPIO.cleanup()
    print 'You pressed Ctrl+C!'
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

def ultrasonic_trigger(pin):
    # Set trigger pin as output
    GPIO.setup(pin, GPIO.OUT)
    # Set trigger to False (Low)
    GPIO.output(pin, False)
    # Allow module to settle
    time.sleep(0.5)

    # Send 10us pulse to trigger
    GPIO.output(pin, True)
    time.sleep(0.00001)
    GPIO.output(pin, False)
    return time.time()

def ultrasonic_measure(pin):
    start_time = ultrasonic_trigger(pin)
    GPIO.setup(pin, GPIO.IN)  # Echo

    while GPIO.input(pin) == 0:
        start_time = time.time()

    while GPIO.input(pin) == 1:
        stop = time.time()

    # Calculate pulse length
    elapsed = stop - start_time

    # Distance pulse travelled in that time is time
    # multiplied by the speed of sound (cm/s)
    distance = elapsed * 34300

    # That was the distance there and back so halve the value
    return distance / 2


# Define GPIO to use on Pi
PIN = 5

print "starting Ultrasonic Measurements..."

while(True):
    distance = ultrasonic_measure(PIN)
    print "Distance: %.1f cm" % distance

# Reset GPIO settings
GPIO.cleanup()

