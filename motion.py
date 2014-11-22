
import pyb
import PIR
from terminalfont import terminalfont

class motion(PIR.PIR):
  NONE = 0
  UP = 1
  DOWN = 2
  txtsize = 2
  displaytime = 4000
  processdelay = 100

  """detect motion and print msg on TFT"""
  def __init__(self, display):
    super(motion, self).__init__(None, "X12", self.msg)
    self._extpower = pyb.Pin("X11", pyb.Pin.OUT_PP)
    self._extpower.high()
    self._display = display
    display.rotation(1)
    self._state = motion.NONE
    self._timer = 0
    self._dirty = False
    self._font = terminalfont
    self._fontW = terminalfont['Width']
    self._fontH = terminalfont['Height']

  def msg( self, aArg ) :
    self._state = motion.UP if aArg else motion.DOWN

  def txt( self, aText, aColor ) :
    x, y = self._display.size()
    y >>= 1
    y -= (self._fontH >> 1) * motion.txtsize
    self._display.fillrect((0, y), (self._display.size()[0], self._fontH * motion.txtsize), self._display.BLACK)
    self._dirty = (aText != None)
    if self._dirty:
      self._timer = 0
      x >>= 1
      x -= len(aText) * (self._fontW >> 1) * motion.txtsize
      print(aText)
      self._display.text((x, y), aText, aColor, terminalfont, motion.txtsize)

  def processmsg( self, dt ) :
    state = self._state
    if state != motion.NONE:
      self._state = motion.NONE
      if state == motion.UP:
        self.txt("Hello", self._display.GREEN)
      else:
        self.txt("Goodbye", self._display.RED)
    elif self._dirty:
      self._timer += dt
      if self._timer >= motion.displaytime:
        self._timer = 0
        self.txt(None, 0)

  def run( self ) :
    self._display.fill(0)
    self.on()
    sw = pyb.Switch()
    while sw() == False :
      self.processmsg(motion.processdelay)
      pyb.delay(motion.processdelay)
    self.off()