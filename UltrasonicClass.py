
import time, threading, logging
import RPi.GPIO as GPIO

MAX_RANGE_CM = 400
SPEED_OF_SOUND_CM_PER_S = 34300

class Ultrasonic(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name,
                                  verbose=verbose)
        self.args = args
        self.kwargs = kwargs
        self.pin = self.kwargs['pin']
        self.distance = 0.0
        self.status = 0 # 0=running, 1=stopping, 2=stopped
        self.max_range_time = MAX_RANGE_CM / SPEED_OF_SOUND_CM_PER_S
        print '__init__ ultrasonic on pin %d' % (self.pin)
        return

    def run(self):
        while(self.status == 0):
            self.distance = self.ultrasonic_measure(self.pin)
        print 'run: stopping'
        self.status = 2
        return

    def shutdown(self):
        print 'shutdown: client requested shutdown...'
        self.status = 1
        while (self.status != 2):
            print 'shutdown: waiting for ultrasonic thread to finish...'
            time.sleep(.2)
        print 'shutdown: complete'
        return

    def get_last_distance(self):
        return self.distance

    def ultrasonic_trigger(self, pin):
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

    def ultrasonic_measure(self, pin):
        start_time = self.ultrasonic_trigger(pin)
        GPIO.setup(pin, GPIO.IN)  # Echo

        while GPIO.input(pin) == 0:
            start_time = time.time()

        while GPIO.input(pin) == 1:
            stop = time.time()
            if (stop - start_time > 5):
                print 'ultrasonic_measure: max time timeout occurred.'
                return -1

        # Calculate pulse length
        elapsed = stop - start_time

        # round-trip distance pulse travelled in that time * multiplied by the speed of sound (cm/s) / 2 trips
        return elapsed * SPEED_OF_SOUND_CM_PER_S / 2


