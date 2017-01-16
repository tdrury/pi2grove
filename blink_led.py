import RPi.GPIO as GPIO
import time

# number matches Pi2Grover board connector
LED = 4

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

try:
    print "running - press a key to quit"
    while (1):
        GPIO.output(LED, GPIO.HIGH)
        time.sleep(.5)
        GPIO.output(LED, GPIO.LOW)
        time.sleep(0.5)

except KeyboardInterrupt:
    # here you put any code you want to run before the program
    # exits when you press CTRL+C
    print "keyboard Interrupt"

except:
    print "other error"

finally:
    GPIO.cleanup() # this ensures a clean exit
