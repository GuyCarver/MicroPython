#Display distance reported by the HC-SR04 on the ST7735 LCD.

import ultrasonic
import pyb
from ST7735 import NAVY, CYAN, Point, TFTColor
import terminalfont

ZeroPoint = Point(0, 0)
SONAR_DELAY = 100
FONT_HEIGHT = terminalfont.terminalfont["Height"]

#100-15 = blue
#15-10  = green
#10-5   = yellow
#5-0    = red

COLORS = [(0, 255, 0, 0)
          (5, 255, 255, 0),
          (10, 0, 255, 0),
          (15, 0, 0, 255),
         ]

def getrgb( aDistance ) :
  '''Get an interpolated TFTColor based on distance.
     Uses the COLORS list.'''
  clr = NAVY

  def interp(l, v0, v1):
    return (v0 * (1.0 - l) + (v1 * l))

  for i in range(1, len(COLORS)) :
    c = colors[i]
    if c[0] >= aDistance:
      rng0, r0, g0, b0 = colors[i - 1]
      rng1, r1, g1, b1 = c
      #interpolate between rng0 and rng1
      l = (aDistance - rng0) / float(rng1 - rng0)
      r = interp(l, r0, r1)
      g = interp(l, g0, g1)
      b = interp(l, b0, b1)
      clr = TFTColor(r,g,b)

  return clr

class RangePoint(object):
  """Display a point on the screen"""

  def __init__(self, aSize):
    self.size = aSize
    self.pos = Point(-1, 0)
    self.prevdistance = -1

  def update( self, aDisplay, aDistance, aTime ) :
    if (self.prevdistance != aDistance):
      self._draw(aDisplay, 0)
      clr = getrgb(aDistance)
      self.pos.x = int((aDisplay.size.x / 2) - (self.size / 2))
      y = min(1.0, aDistance / MAXRANGE)
      self.pos.y = int(y * aDisplay.size.y)
      self._draw(aDisplay, clr)
      self.prevdistance = aDistance

  def _draw( self, aDisplay, aColor ) :
    if self.pos.x >= 0:
      aDisplay.fillrect(self.pos, self.size, aColor)

class SonarDisplay(object):
  """Display HC-SR04 distance on ST7735 LCD with text and a box"""
  def __init__( self, aDisplay, aTrigger, aEcho ):
    self.display = aDisplay
    self.triggerpin = aTrigger
    self.echopin = aEcho
    self.rangepoint = RangePoint(4)
    self.hc = ultrasonic.Ultrasonic(self.triggerpin, self.echopin)

  def printdistance( self, aDistance ) :
    s = "I: " + str(aDistance)
    aDisplay.fillrect(ZeroPoint, Point(aDisplay.size.x, FONT_HEIGHT), 0)
    aDisplay.drawstring(ZeroPoint, s, CYAN, terminalfont.terminalfont)

  def run( self ):
    self.display.fill(0)
    sw = pyb.Switch()
    lasttime = pyb.millis()
    while sw() == False :
      pyb.delay(SONAR_DELAY)
      distance = self.hc.distance_in_inches()
      thistime = pyb.millis()
      t = thistime - lasttime
      self.printdistance(distance)
      self.rangepoint.update(self.display, distance, t / 1000.0)
      lasttime = thistime

# sensor1_trigPin = pyb.Pin.board.X8
# sensor1_echoPin = pyb.Pin.board.X7

# sensor1 = ultrasonic.Ultrasonic(sensor1_trigPin, sensor1_echoPin)

# switch = pyb.Switch()

# # function that prints each sensor's distance
# def print_sensor_values():
#   # get sensor1's distance in cm
#   distance1 = sensor1.distance_in_inches()

#   print("Sensor1", distance1, "inches")

# # prints values every second
# while True:
#   print("Sensing")
#   print_sensor_values()
# #   ultrasonic.wait(10000)
#   pyb.delay(100)
