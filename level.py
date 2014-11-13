#Show level bubble run by the accelerometer

import pyb
from ST7735 import RED, CYAN
import terminalfont

ZeroPoint = (0, 0)

class Bubble(object):
  """Circle simulating the level bubble."""

  def __init__(self, aCenter, aSpeed, aRadius, aColor):
    self.center = aCenter
    self.pos = aCenter
    self.oldpos = self.pos
    self.speed = aSpeed
    self.radius = aRadius
    self.color = aColor
    self.accel = pyb.Accel()

  def update( self, aDisplay, aTime ) :
    xtilt, ytilt, _ = self.accel.filtered_xyz()
#     xtilt = self.accel.x()
#     ytilt = self.accel.y()

    xs = (aDisplay.size[0] / 2) / 70.0
    ys = (aDisplay.size[1] / 2) / 60.0

    self.oldpos = self.pos
    self.pos = (int(self.center[0] + xtilt * xs), int(self.center[1] - ytilt * ys))
    s = "x: " + str(xtilt) + " y: " + str(ytilt)
    aDisplay.fillrect(ZeroPoint, (aDisplay.size[0], 10), 0)
    aDisplay.text(ZeroPoint, s, CYAN, terminalfont.terminalfont)
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
    r = aDisplay.size[0] - l
    b = aDisplay.size[1] - l
    self.pos = (max(l, min(self.pos[0], r)), max(t, min(self.pos[1], b)))

class Level(object):
  """Simulate a level by controlling a bubble on the aDisplay
     controlled by the accelerometer."""
  def __init__(self, aDisplay):
    self.display = aDisplay
    cx, cy = aDisplay.size
    cx /= 2
    cy /= 2
    self.bubble = Bubble((cx, cy), 10.0, 5, RED)

  def run( self ) :
    self.display.fill(0)
    sw = pyb.Switch()
    while sw() == False :
      pyb.delay(100)
      self.bubble.update(self.display, 0.1)
