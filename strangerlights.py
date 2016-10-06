#!/usr/bin/python

# Stranger Things Christmas Lights
# Author: Paul Larson (djhazee@gmail.com)
#
# -Port of the Arduino NeoPixel library strandtest example (Adafruit).
# -Uses the WS2811 to animate RGB light strings (I am using a 5V, 50x RGB LED strand)
# -This will blink a designated light for each letter of the alphabet


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
PURPLE = Color(128,0,128)
YELLOW = Color(255,255,0)
ORANGE = Color(255,50,0)
TURQUOISE = Color(64,224,208)
RANDOM = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

#list of colors, tried to match the show as close as possible
COLORS = [YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,
          YELLOW,PURPLE,RED,GREEN,BLUE,YELLOW,RED,TURQUOISE,GREEN,RED,BLUE,GREEN,ORANGE,
          YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,BLUE, 
          ORANGE,RED,YELLOW,GREEN,PURPLE,BLUE,YELLOW,ORANGE,TURQUOISE,RED,GREEN,YELLOW,PURPLE,
          YELLOW,GREEN,RED,BLUE,ORANGE,TURQUOISE,GREEN,BLUE,ORANGE] 

#bitmasks used in scaling RGB values
REDMASK = 0b111111110000000000000000
GREENMASK = 0b000000001111111100000000
BLUEMASK = 0b000000000000000011111111

# Other vars
ALPHABET = '*******abcdefghijklm********zyxwvutsrqpon*********'  #alphabet that will be used
#LIGHTSHIFT = 24  #shift the lights down the strand to the other end 
LIGHTSHIFT = 0  #shift the lights down the strand to the other end 
FLICKERLOOP = 3  #number of loops to flicker

def initLights(strip):
  """
  initializes the light strand colors 

  inputs: 
    strip = color strip instance to action against

  outputs:
    <none>
  """
  colorLen = len(COLORS)
  #Initialize all LEDs
  for i in range(len(ALPHABET)):
    strip.setPixelColor(i+LIGHTSHIFT, COLORS[i%colorLen])
    strip.show()
    


def blinkWords(strip, word):
  """
  blinks a string of letters

  inputs: 
    strip = color strip instance to action against
    word = word to blink

  outputs:
    <none>
  """
  s = list(range(len(ALPHABET)))
  random.shuffle(s)

  #first, kill all lights in a semi-random fashion
  for led in range(len(ALPHABET)):
    strip.setPixelColor(s[led]+LIGHTSHIFT, OFF)
    strip.show()
    time.sleep(random.randint(10,80)/1000.0)

  #quick delay
  time.sleep(2)

  #if letter in alphabet, turn on for 1.5 seconds
  #otherwise, stall for 1.5 seconds
  for character in word:
    if character in ALPHABET:
      strip.setPixelColor(ALPHABET.index(character)+LIGHTSHIFT, RED)
      strip.show()
      time.sleep(1)
      strip.setPixelColor(ALPHABET.index(character)+LIGHTSHIFT, OFF)
      strip.show()
      time.sleep(.5)
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
    time.sleep(random.randint(10,50)/1000.0)

    #turn back on at random scaled color brightness
    #modifier = random.randint(30,120)/100
    modifier = 1
    #TODO: fix modifier so each RGB value is scaled. 
    #      Doesn't work that well so modifier is set to 1. 
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
    time.sleep(random.randint(10,80)/1000.0)

  #restore original LED color
  strip.setPixelColor(ledNo, origColor)

def runBlink(strip):
  """
  blinks the RUN letters

  inputs: 
    strip = color strip instance to action against

  outputs:
    <none>
  """
  word = "run"
  #first blink the word "run", one letter at a time
  blinkWords(strip, word)

  #now frantically blink all 3 letters
  for loop in range(20):
    #turn on all three letters at the same time
    for character in word:
      if character in ALPHABET:
        strip.setPixelColor(ALPHABET.index(character)+LIGHTSHIFT, RED)
        strip.show()

    time.sleep(random.randint(15,100)/1000.0)

    #turn off all three letters at the same time
    for character in word:
      if character in ALPHABET:
        strip.setPixelColor(ALPHABET.index(character)+LIGHTSHIFT, OFF)
        strip.show()

    time.sleep(random.randint(50,150)/1000.0)

  #now frantically blink all lights 
  for loop in range(10):
    #initialize all the lights
    initLights(strip)

    #kill all lights
    for led in range(len(ALPHABET)):
      strip.setPixelColor(led+LIGHTSHIFT, OFF)
      strip.show()

    time.sleep(random.randint(50,150)/1000.0)

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
  strip.begin()

  print ('Press Ctrl-C to quit.')


  while True:

    ##Initialize all LEDs
    #for i in range(len(ALPHABET)):
    #  strip.setPixelColor(i+LIGHTSHIFT, Color(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    #  strip.show()

    #initialize all the lights
    initLights(strip)
    
    time.sleep(5)

    #flicker each light, no delay between each
    for i in range(20):
      flicker(strip,random.randint(LIGHTSHIFT,len(ALPHABET)+LIGHTSHIFT))
      time.sleep(random.randint(10,70)/1000.0)

    time.sleep(2)

    #flash lights to word
    word = 'its here'
    blinkWords(strip, word)
    time.sleep(.5)
    runBlink(strip)

    time.sleep(1)
