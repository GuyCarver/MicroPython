
import pyb
import time

#todo: Pick a ransom spot, random radius, random color
#todo: Animate the spot

class bomb(object):
  """Animate a circle on the screen."""
  def __init__(self, aPos, aRadius, aColor, aSpeed):
    self.pos = aPos
    self.radius = aRadius
    self.color = aColor
    self.speed = aSpeed
    self.curradius = 0.0
    self.state = 0

  def update( self, aDisplay, aTime ) :
    self.curradius += self.speed * aTime
    rad = self.curradius
    color = self.color
    if self.curradius > self.radius:
      rad = self.radius
      self.state += 1
      self.color = 0
      self.curradius = 1.0

    aDisplay.fillcircle(self.pos, int(rad), color)

    return self.state != 2

def randval( aVal ) :
  v = pyb.rng() & 0xFFFF
  return aVal * (v / 65535.0)

class bomber(object):
  """Control a bunch of bombs."""
  def __init__(self, aDisplay):
    self.display = aDisplay
    self.ds = self.display.size()
    self.numbombs = 4
    self.bombs = []
    self.sw = pyb.Switch()

  def addbomb( self ) :
    x = int(randval(self.ds[0]))
    y = int(randval(self.ds[1]))
    rad = randval(20) + 5
    r = pyb.rng() & 0xFF
    g = pyb.rng() & 0xFF
    b = pyb.rng() & 0xFF
    spd = randval(30.0) + 1.0
    clr = self.display.color(r,g,b)
    self.bombs.insert(0, bomb((x, y), rad, clr, spd))

  def run( self ) :
    while self.sw() == False :
      pyb.delay(100)
      if len(self.bombs) < self.numbombs:
        self.addbomb()
      self.bombs = [b for b in self.bombs if b.update(self.display, 0.1) ]
