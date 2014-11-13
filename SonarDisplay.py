#Display distance reported by the HC-SR04 on the ST7735 LCD.

import ultrasonic
import pyb
import terminalfont

ZeroPoint = (0, 0)
SONAR_DELAY = 100
MAX_RANGE = 25.0
FONT_HEIGHT = terminalfont.terminalfont["Height"]
NUM_DISTANCES = 4 #The number of distances to use for throwing away anomalies
THRESHOLD = 1.0

#100-15 = blue
#15-10  = green
#10-5   = yellow
#5-0    = red

COLORS = [(0, 255, 0, 0),
          (5, 255, 255, 0),
          (10, 0, 255, 0),
          (15, 0, 255, 255),
          (20, 0, 0, 255)
         ]

def round( aValue ) :
  '''Round float value to 2 decimal places'''
  return (aValue - (aValue % 0.01))

def getrgb( aDisplay, aDistance ) :
  '''Get an interpolated color based on distance.
     Uses the COLORS list.'''
  clr = aDisplay.NAVY

  def interp(l, v0, v1):
    return int(v0 * (1.0 - l) + (v1 * l))

  for i in range(1, len(COLORS)) :
    c = COLORS[i]
    if c[0] >= aDistance:
      rng0, r0, g0, b0 = COLORS[i - 1]
      rng1, r1, g1, b1 = c
      #interpolate between rng0 and rng1
      l = (aDistance - rng0) / float(rng1 - rng0)
      r = interp(l, r0, r1)
      g = interp(l, g0, g1)
      b = interp(l, b0, b1)
      clr = aDisplay.color(r,g,b)
      break

  return clr

class RangePoint(object):
  """Display a point on the screen"""

  def __init__(self, aSize):
    self.size = (50, aSize)
    self.pos = (-1, 0)
    self.prevdistance = -1

  def update( self, aDisplay, aDistance, aTime ) :
    if (self.prevdistance != aDistance):
      self._draw(aDisplay, 0)
      clr = getrgb(aDistance)
      y = min(1.0, aDistance / MAX_RANGE)
      self.pos = (int((aDisplay.size[0] / 2) - (self.size[0] / 2)), int(y * aDisplay.size[1] - self.size[1]))
      self._draw(aDisplay, clr)
      self.prevdistance = aDistance

  def _draw( self, aDisplay, aColor ) :
    if self.pos[0] >= 0:
      aDisplay.fillrect(self.pos, self.size, aColor)

def wrap( aVal, aMax ) :
  return aVal if aVal < aMax else 0

class SonarDisplay(object):
  """Display HC-SR04 distance on ST7735 LCD with text and a box"""
  def __init__( self, aDisplay, aTrigger, aEcho ):
    self.display = aDisplay
    self.triggerpin = aTrigger
    self.echopin = aEcho
    self.rangepoint = RangePoint(4)
    self.curdistance = 0.0
    self.distances = [0.0] * NUM_DISTANCES
    self.distindex = 0
    self.hc = ultrasonic.Ultrasonic(self.triggerpin, self.echopin)

  def printdistance( self, aDistance ) :
    s = "I:" + str(round(aDistance))
    self.display.fillrect(ZeroPoint, (self.display.size[0], FONT_HEIGHT), 0)
    self.display.text(ZeroPoint, s, CYAN, terminalfont.terminalfont)

  def _getdistance( self ) :
    '''Throw away changes that are not averaged. This introduces
       a slight delay in update but gets rid of most bad distances'''

    d = self.hc.distance_in_inches()
    good = 0
    for c in self.distances :
      if abs(c - d) < THRESHOLD:
        good += 1
        if good > 2:
          self.curdistance = d
          break

    self.distances[self.distindex] = d
    self.distindex = wrap(self.distindex + 1, NUM_DISTANCES)
    return self.curdistance

  def run( self ):
    self.display.fill(0)
    sw = pyb.Switch()
    lasttime = pyb.millis()
    while sw() == False :
      pyb.delay(SONAR_DELAY)
      distance = self._getdistance()

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
