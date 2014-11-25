#Display distance in inches on ST7734 LCD.
#Distance is taken from the given distance sensor.

import pyb
import terminalfont

ZeroPoint = (0, 0)
DISPLAY_DELAY = 100
FONT_HEIGHT = terminalfont.terminalfont["Height"]
NUM_DISTANCES = 4 #The number of _distances to use for throwing away anomalies
THRESHOLD = 0.5

#100-15 = blue
#15-10  = green
#10-5   = yellow
#5-0    = red

COLORS = [(0, 255, 0, 0),
          (.35, 255, 255, 0),
          (.50, 0, 255, 0),
          (.75, 0, 255, 255),
          (1.0, 0, 0, 255)
         ]

def round( aValue ) :
  '''Round float value to 2 decimal places'''
  return (aValue - (aValue % 0.01))

def getrgb( aDisplay, aDistance, maxdist ) :
  '''Get an interpolated color based on distance.
     Uses the COLORS list.'''
  clr = aDisplay.NAVY

  def interp( l, v0, v1 ) :
    return int(v0 * (1.0 - l) + (v1 * l))

  for i in range(1, len(COLORS)) :
    c = COLORS[i]
    if c[0] * maxdist >= aDistance:
      rng0, r0, g0, b0 = COLORS[i - 1]
      rng1, r1, g1, b1 = c
      rng0 *= maxdist
      rng1 *= maxdist
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

  def __init__( self, size, maxrange ) :
    self._size = (50, size)
    self._pos = (-1, 0)
    self._prevdistance = -1
    self._maxrange = maxrange

  def update( self, aDisplay, aDistance, aTime ) :
    if (self._prevdistance != aDistance):
      self._draw(aDisplay, 0)
      clr = getrgb(aDisplay, aDistance, self._maxrange)
      y = min(1.0, aDistance / self._maxrange)
      self._pos = (int((aDisplay.size()[0] / 2) - (self._size[0] / 2)), int(y * aDisplay.size()[1] - self._size[1]))
      self._draw(aDisplay, clr)
      self._prevdistance = aDistance

  def _draw( self, aDisplay, aColor ) :
    if self._pos[0] >= 0:
      aDisplay.fillrect(self._pos, self._size, aColor)

def wrap( aVal, aMax ) : return aVal if aVal < aMax else 0

class Display(object):
  """Display distance on ST7735 LCD with text and a box"""
  def __init__( self, display, ranger ):
    self._display = display
    self._ranger = ranger
    self._rangepoint = RangePoint(4, ranger.maxinches)
    self._curdistance = 0.0
    self._distances = [0.0] * NUM_DISTANCES
    self._distindex = 0

  def printdistance( self, aDistance ) :
    s = "I:" + str(round(aDistance))
    self._display.fillrect(ZeroPoint, (self._display.size()[0], FONT_HEIGHT * 2), 0)
    self._display.text(ZeroPoint, s, self._display.CYAN, terminalfont.terminalfont, 2)

  def _getdistance( self ) :
    '''Throw away changes that are not averaged. This introduces
       a slight delay in update but gets rid of most bad _distances'''

    d = self._ranger.inches
#     self._curdistance = d
    good = 0
    for c in self._distances :
      if abs(c - d) < THRESHOLD:
        good += 1
        if good > 2:
          self._curdistance = d
          break

    self._distances[self._distindex] = d
    self._distindex = wrap(self._distindex + 1, NUM_DISTANCES)
    return self._curdistance

  def run( self ) :
    self._display.fill(0)
    sw = pyb.Switch()
    lasttime = pyb.millis()
    while sw() == False :
      pyb.delay(DISPLAY_DELAY)
      distance = self._getdistance()

      thistime = pyb.millis()
      t = thistime - lasttime
      self.printdistance(distance)
      self._rangepoint.update(self._display, distance, t / 1000.0)
      lasttime = thistime
