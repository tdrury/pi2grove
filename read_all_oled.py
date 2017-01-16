
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

import time, signal, sys
sys.path.append('/home/pi/git/SDL_Pi_Grove4Ch16BitADC/Adafruit_ADS1x15')
from Adafruit_ADS1x15 import ADS1x15
from UltrasonicClass import *

u = Ultrasonic(args=(), kwargs={'pin':5})

def signal_handler(signal, frame):
    u.shutdown()
    GPIO.cleanup()
    print 'Ctrl+C pressed - ending'
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
#print 'Press Ctrl+C to exit'


# Use BCM GPIO references instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

u.start()

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Note you can change the I2C address by passing an i2c_address parameter like:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
# Initialize library.
disp.begin()
# Clear display.
disp.clear()
disp.display()

ADS1115 = 0x01	# 16-bit ADC
# Select the gain
gain = 4096  # +/- 4.096V
# Select the sample rate
sps = 250  # 250 samples per second
# Initialise the ADC using the default mode (use default I2C address)
adc = ADS1x15(ic=ADS1115)


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Load default font.
font = ImageFont.load_default()

padding = 2
top = padding
bottom = height-padding
row_height = 10

draw.rectangle((0, 0, width, height), outline=0, fill=0)
disp.image(image)
disp.display()

while (1):
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    # read ultrasonic distance
    distance = u.get_last_distance()

    # Read channels  in single-ended mode using the settings above
    voltsCh0 = adc.readADCSingleEnded(0, gain, sps) / 1000
    rawCh0 = adc.readRaw(0, gain, sps)
    voltsCh1 = adc.readADCSingleEnded(1, gain, sps) / 1000
    rawCh1 = adc.readRaw(1, gain, sps)
    voltsCh2 = adc.readADCSingleEnded(2, gain, sps) / 1000
    rawCh2 = adc.readRaw(2, gain, sps)
    voltsCh3 = adc.readADCSingleEnded(3, gain, sps) / 1000
    rawCh3 = adc.readRaw(3, gain, sps)
    #print "%.2fV (0x%4x) - %.2fV (0x%4x) - %.2fV (0x%4x) - %.2fV (0x%4x)" %(voltsCh0, rawCh0, voltsCh1, rawCh1, voltsCh2, rawCh2, voltsCh3, rawCh3)
    x = padding
    y = padding
    draw.text((x, y), 'Ch0:', font=font, fill=255)
    draw.text((x+40, y), '{: 4.2f}'.format(voltsCh0), font=font, fill=255)
    y += row_height
    draw.text((x, y), 'Ch1:', font=font, fill=255)
    draw.text((x+40, y), '{: 4.2f}'.format(voltsCh1), font=font, fill=255)
    y += row_height
    draw.text((x, y), 'Ch2:', font=font, fill=255)
    draw.text((x+40, y), '{: 4.2f}'.format(voltsCh2), font=font, fill=255)
    y += row_height
    draw.text((x, y), 'Ch3:', font=font, fill=255)
    draw.text((x+40, y), '{: 4.2f}'.format(voltsCh3), font=font, fill=255)
    y += row_height
    draw.text((x, y), 'dist:', font=font, fill=255)
    draw.text((x+40, y), '{: 4.2f}'.format(distance), font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()

