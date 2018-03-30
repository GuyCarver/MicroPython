#driver for the diymall 9.6 oled display.
#128x32 pixel support with help from adafruit libraries.

import pyb

_I2C_ADDRESS = const(0x3C)  # 011110+SA0+RW - 0x3C or 0x3D

_SETCONTRAST = const(0x81)
_DISPLAYALLON_RESUME = const(0xA4)
_DISPLAYALLON = const(0xA5)
_NORMALDISPLAY = const(0xA6)
_INVERTDISPLAY = const(0xA7)
_DISPLAYOFF = const(0xAE)
_DISPLAYON = const(0xAF)

_SETDISPLAYOFFSET = const(0xD3)
_SETCOMPINS = const(0xDA)

_SETVCOMDETECT = const(0xDB)

_SETDISPLAYCLOCKDIV = const(0xD5)
_SETPRECHARGE = const(0xD9)

_SETMULTIPLEX = const(0xA8)

#_SETLOWCOLUMN = const(0x00)
#_SETHIGHCOLUMN = const(0x10)

_SETSTARTLINE = const(0x40)

_MEMORYMODE = const(0x20)
_COLUMNADDR = const(0x21)
_PAGEADDR = const(0x22)

_COMSCANINC = const(0xC0)
_COMSCANDEC = const(0xC8)

_SEGREMAP = const(0xA0)

_CHARGEPUMP = const(0x8D)

_EXTRNALVCC = const(0x1)
_SWITCHAPVCC = const(0x2)

_ACTIVATE_SCROLL = const(0x2F)
_DEACTIVATE_SCROLL = const(0x2E)
_SET_VERTICAL_SCROLL_AREA = const(0xA3)
_RIGHT_HORIZONTAL_SCROLL = const(0x26)
_LEFT_HORIZONTAL_SCROLL = const(0x27)
_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = const(0x29)
_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = const(0x2A)

#Buffer layout in bits.  128 columns by 64 rows.
#Each byte represents 8 pixels in a row.
#   Column
# R 0   8   10 ... 3F8
# O 1   9   11 ... 3F9
# W 2   A   12 ... 3FA
#   3   B   13 ... 3FB
#   4   C   14 ... 3FC
#   5   D   15 ... 3FD
#   6   E   16 ... 3FE
#   7   F   17 ... 3FF
#   400 408
#   401 409
#   402 40A
#   403 40B
#   404 40C
#   405 40D
#   406 40E
#   407 40F

class oled(object) :
  """diyMall OLED 9.6 128x64 pixel display driver."""

  def __init__( self, aLoc, aHeight = 64 ) :
    """aLoc I2C pin location is either 1 for 'X' or 2 for 'Y'."""
    self._size = (128, aHeight)
    self._rotation = 0
    self._inverted = False
    self._on = False
    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER, baudrate = 200000)
    self.pages = aHeight // 8
    self.bytes = self.size[0] * self.pages
    self.buffer = bytearray(self.bytes + 1)
    self.buffer[0] = 0x40 #data write start command at very start of buffer.

    self.data = bytearray(2)
    self.data[0] = 0  #0 = Command mode.

    self.command = _DISPLAYOFF
    self.command = _SETDISPLAYCLOCKDIV
    self.command = 0x80 #suggested ratio.
    self.command = _SETMULTIPLEX
    self.command = aHeight - 1
    self.command = _SETDISPLAYOFFSET
    self.command = 0x0
    self.command = _SETSTARTLINE #| 0x0
    self.command = _CHARGEPUMP
    self.command = 0x14  #No external power.
    self.command = _MEMORYMODE
    self.command = 0x00  #Act like ks0108
    self.command = _SEGREMAP + 0x01
    self.command = _COMSCANDEC
    self.command = _SETCOMPINS
    self.command = 0x12 if aHeight == 64 else 0x02
    self.dim = 0xCF
    self.command = _SETPRECHARGE
    self.command = 0xF1
    self.command = _SETVCOMDETECT
    self.command = 0x40
    self.command = _DISPLAYALLON_RESUME
    self.command = _NORMALDISPLAY
    self.command = 0XB0
    self.command = 0x10
    self.command = 0x01 #Set original position to 0,0.

    self.on = True

    self.display()

  @property
  def size( self ) : return self._size

  @property
  def rotation( self ) : return self._rotation

  @rotation.setter
  def rotation( self, aValue ) :
    self._rotation = aValue & 3

  def write( self, aValue ) :
    self.i2c.send(aValue, _I2C_ADDRESS)

  @property
  def command( self ) : return 0

  @command.setter
  def command( self, aValue ) :
    self.data[1] = aValue
    self.write(self.data)

  @property
  def on( self ) : return self._on

  @on.setter
  def on( self, aTF ) :
    if aTF != self._on :
      self._on = aTF
      '''Turn display on or off.'''
      self.command = _DISPLAYON if aTF else _DISPLAYOFF

  @property
  def invert( self ) : return self._inverted

  @invert.setter
  def invert( self, aTF ) :
    if aTF != self._inverted :
      self._inverted = aTF
      self.command = _INVERTDISPLAY if aTF else _NORMALDISPLAY

  @property
  def dim( self ):
    return self._dim

  @dim.setter
  def dim( self, aValue ):
    self._dim = aValue
    self.command = _SETCONTRAST
    self.command = self._dim

  @micropython.native
  def fill( self, aValue ) :
    for x in range(1, self.bytes + 1):
      self.buffer[x] = aValue;

  def clear( self ) :
    self.fill(0)

  @micropython.native
  def pixel( self, aPos, aOn ) :
    '''Draw a pixel at the given position'''
    x, y = aPos
    w, h = self.size
    if 0 <= x < w and 0 <= y < h:
      if self._rotation == 1:
        aPos = (w - y - 1, x)
      elif self._rotation == 2:
        aPos = (w - x - 1, h - y - 1)
      elif self._rotation == 3:
        aPos = (y, h - x - 1)

      bit = 1 << (aPos[1] % 8)
      index = (aPos[0] + (aPos[1] // 8) * w) + 1

      if aOn :
        self.buffer[index] |= bit
      else :
        self.buffer[index] &= not bit

  @micropython.native
  def line( self, aStart, aEnd, aOn ) :
    '''Draws a line from aStart to aEnd in the given color.  Vertical or horizontal
       lines are forwarded to vline and hline.'''
    px, py = aStart
    ex, ey = aEnd
    dx = ex - px
    dy = ey - py
    inx = 1 if dx > 0 else -1
    iny = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)
    if (dx >= dy):
      dy <<= 1
      e = dy - dx
      dx <<= 1
      while (px != ex):
        self.pixel((px, py), aOn)
        if (e >= 0):
          py += iny
          e -= dx
        e += dy
        px += inx
    else:
      dx <<= 1
      e = dx - dy
      dy <<= 1
      while (py != ey):
        self.pixel((px, py), aOn)
        if (e >= 0):
          px += inx
          e -= dy
        e += dx
        py += iny

#   @micropython.native
  def fillrect( self, aStart, aSize, aOn ) :
    '''Draw a filled rectangle.  aStart is the smallest coordinate corner
       and aSize is a tuple indicating width, height.'''
    x, y = aStart
    w, h = aSize
    ex = x + w
    for i in range(y, y + h):
      self.line((x, i), (ex, i), aOn)

  @micropython.native
  def text( self, aPos, aString, aColor, aFont, aSize = 1 ) :
    '''Draw a text at the given position.  If the string reaches the end of the
       display it is wrapped to aPos[0] on the next line.  aSize may be an integer
       which will size the font uniformly on w,h or a or any type that may be
       indexed with [0] or [1].'''

    if aFont == None:
      return

    #Make a size either from single value or 2 elements.
    if (type(aSize) == int) or (type(aSize) == float):
      wh = (aSize, aSize)
    else:
      wh = aSize

    px, py = aPos
    width = wh[0] * aFont["Width"] + 1
    for c in aString:
      self.char((px, py), c, aColor, aFont, wh)
      px += width
      #We check > rather than >= to let the right (blank) edge of the
      # character print off the right of the screen.
      if px + width > self._size[0]:
        py += aFont["Height"] * wh[1] + 1
        px = aPos[0]

  @micropython.native
  def char( self, aPos, aChar, aOn, aFont, aSizes ) :
    '''Draw a character at the given position using the given font and color.
       aSizes is a tuple with x, y as integer scales indicating the
       # of pixels to draw for each pixel in the character.'''

    if aFont == None:
      return

    startchar = aFont['Start']
    endchar = aFont['End']

    ci = ord(aChar)
    if (startchar <= ci <= endchar):
      fontw = aFont['Width']
      fonth = aFont['Height']
      ci = (ci - startchar) * fontw

      charA = aFont["Data"][ci:ci + fontw]
      px = aPos[0]
      if aSizes[0] <= 1 and aSizes[1] <= 1 :
        for c in charA :
          py = aPos[1]
          for r in range(fonth) :
            if c & 0x01 :
              self.pixel((px, py), aOn)
            py += 1
            c >>= 1
          px += 1
      else:
        for c in charA :
          py = aPos[1]
          for r in range(fonth) :
            if c & 0x01 :
              self.fillrect((px, py), aSizes, aOn)
            py += aSizes[1]
            c >>= 1
          px += aSizes[0]

  def doscrollLR( self, start, stop, aDir ) :
    self.command = aDir
    self.command = 0x00
    self.command = start
    self.command = 0x00
    self.command = stop
    self.command = 0x01
    self.command = 0xFF
    self.command = _ACTIVATE_SCROLL

  def startscrollright( self, start, stop ) :
    self.doscrollLR(start, stop, _RIGHT_HORIZONTAL_SCROLL)

  def startscrollleft( self, start, stop ) :
    self.doscrollLR(start, stop, _LEFT_HORIZONTAL_SCROLL)

  def doscrollDiag( self, start, stop, aDir ) :
    self.command = _SET_VERTICAL_SCROLL_AREA
    self.command = 0x00
    self.command = self.size[1]
    self.command = aDir
    self.command = 0x00
    self.command = start
    self.command = 0x00
    self.command = stop
    self.command = 0x01
    self.command = _ACTIVATE_SCROLL

  def startscrolldiagright( self, start, stop ) :
    self.doscrollDiag(start, stop, _VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL)

  def startscrolldiagleft( self, start, stop ) :
    self.doscrollDiag(start, stop, _VERTICAL_AND_LEFT_HORIZONTAL_SCROLL)

  def stopscroll( self ) :
    self.command = _DEACTIVATE_SCROLL

  def display( self ) :
    self.command = _COLUMNADDR
    self.command = 0
    self.command = self.size[0] - 1
    self.command = _PAGEADDR
    self.command = 0
    self.command = self.pages - 1

    #buffer starts with 0x40 in 1st byte which is the command to start the buffer write.
    self.write(self.buffer)


