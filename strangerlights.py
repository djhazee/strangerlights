# Stranger Things Christmas Lights
# Author: Paul Larson (djhazee@gmail.com)
#
# -Port of the Arduino NeoPixel library strandtest example (Adafruit).
# -Uses the WS2811 to animate RGB light strings (I am using a 5V, 50x RGB LED strand)
# -TODO:Initialize lights to general Christmas colors
  # --> Look at tv show to ensure they all match
#This will blink a designated light for each letter of the alphabet
  # --> Ready to test
# -TODO:Flicker Effects to kick off communication
  # Works, but needs tweaking


# Import libs used
import time
import random
from neopixel import *

random.seed()

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#Predefined Colors and Masks
OFF = Color(0,0,0)
WHITE = Color(255,255,255)
RED = Color(255,0,0)
GREEN = Color(0,255,0)
BLUE = Color(0,0,255)
RANDOM = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

REDMASK = 0b111111110000000000000000
GREENMASK = 0b000000001111111100000000
BLUEMASK = 0b000000000000000011111111

# Other vars
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
FLICKERLOOP = 10  #number of loops to flicker

def blinkWords(strip, word):
  """
  blinks a string of letters

  inputs: 
    strip = color strip instance to action against
    word = word to blink

  outputs:
    <none>
  """

  #first, kill all lights
  for led in range(len(ALPHABET)):
    strip.setPixelColor(led, OFF)
    strip.show()

  #if letter in alphabet, turn on for 1.5 seconds
  #otherwise, stall for 1.5 seconds
  for character in word:
    if character in ALPHABET:
      strip.setPixelColor(ALPHABET.index(character), BLUE)
      strip.show()
      time.sleep(1)
      strip.setPixelColor(ALPHABET.index(character), OFF)
      strip.show()
      time.sleep(1)
    else:
      time.sleep(1)

def flicker(strip, ledNo):
  """
  creates a flickering effect on a bulb

  inputs: 
    strip = color strip instance to action against
    ledNo = LED position on strand, as integer.

  outputs:
    <none>
  """
  #get origin LED color
  origColor = strip.getPixelColor(ledNo)

  #do FLICKERLOOP-1 loops of flickering  
  for i in range(0,FLICKERLOOP-1):

    #get current LED color, break out to individuals
    currColor = strip.getPixelColor(ledNo)
    currRed = (currColor & REDMASK) >> 16
    currGreen = (currColor & GREENMASK) >> 8
    currBlue = (currColor & BLUEMASK)

    #turn off for a random short period of time
    strip.setPixelColor(ledNo, OFF)
    strip.show()
    time.sleep(random.randint(10,100)/1000.0)

    #turn back on at random scaled color brightness
#    modifier = random.randint(30,120)/100
    modifier = 1
#TODO:remove modifier?
    newBlue = int(currBlue * modifier)
    if newBlue > 255:
      newBlue = 255
    newRed = int(currRed * modifier)
    if newRed > 255:
      newRed = 255
    newGreen = int(currGreen * modifier) 
    if newGreen > 255:
      newGreen = 255
    strip.setPixelColor(ledNo, Color(newRed,newGreen,newBlue))
    strip.show()
    #leave on for random short period of time
    time.sleep(random.randint(10,100)/1000.0)

  #restore original LED color
  strip.setPixelColor(ledNo, origColor)

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
  strip.begin()

  print ('Press Ctrl-C to quit.')


  while True:

    #Initialize all LEDs
    for i in range(len(ALPHABET)):
      strip.setPixelColor(i, RANDOM)
      strip.show()

    #flicker each light, no delay between each
    for i in range(5):
      flicker(strip,random.randint(0,LED_COUNT-1))

    #flash lights to word
    word = 'run'
    blinkWords(strip, word)
