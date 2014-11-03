#Show level bubble run by the accelerometer

import pyb
from ST7735 import RED, CYAN, Point
import terminalfont

ZeroPoint = Point(0, 0)

class Bubble(object):
  """Circle simulating the level bubble."""

  def __init__(self, aCenter, aSpeed, aRadius, aColor):
    self.center = aCenter.clone()
    self.pos = aCenter.clone()
    self.oldpos = pos.clone()
    self.speed = aSpeed
    self.radius = aRadius
    self.color = aColor
    self.accel = pyb.Accel()

  def update( self, aDisplay, aTime ) :
    xtilt, ytilt, _ = self.accel.filtered_xyz()
#     xtilt = self.accel.x()
#     ytilt = self.accel.y()

    xs = (aDisplay.size.x / 2) / 70.0
    ys = (aDisplay.size.y / 2) / 60.0

    self.oldpos.x = self.pos.x
    self.oldpos.y = self.pos.y
    self.pos.x = int(self.center.x + xtilt * xs)
    self.pos.y = int(self.center.y - ytilt * ys)
    s = "x: " + str(xtilt) + " y: " + str(ytilt)
    aDisplay.fillrect(ZeroPoint, Point(aDisplay.size.x, 10), 0)
    aDisplay.drawstring(ZeroPoint, s, CYAN, terminalfont.terminalfont)
#     aTime *= self.speed
#     self.pos.x += xtilt * aTime
#     self.pos.y -= ytilt * aTime

    self._clamp(aDisplay)
    aDisplay.fillcircle(self.oldpos, self.radius, 0)
    self._draw(aDisplay, self.color)

  def _draw( self, aDisplay, aColor ) :
    aDisplay.fillcircle(self.pos, self.radius, aColor)

  def _clamp( self, aDisplay ) :
    l = self.radius
    t = l
    r = aDisplay.size.x - l
    b = aDisplay.size.y - l
    self.pos.x = max(l, min(self.pos.x, r))
    self.pos.y = max(t, min(self.pos.y, b))

class Level(object):
  """Simulate a level by controlling a bubble on the aDisplay
     controlled by the accelerometer."""
  def __init__(self, aDisplay):
    self.display = aDisplay
    center = aDisplay.size.clone()
    center.x /= 2
    center.y /= 2
    self.bubble = Bubble(center, 10.0, 5, RED)

  def run( self ) :
    self.display.fill(0)
    sw = pyb.Switch()
    while sw() == False :
      pyb.delay(100)
      self.bubble.update(self.display, 0.1)
