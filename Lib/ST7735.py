#driver for Sainsmart 1.8" TFT display ST7735
#Translated by Guy Carver from the ST7735 sample code.

import pyb
from math import sqrt

ST_NOP = 0x0
ST_SWRESET = 0x01
ST_RDDID = 0x04
ST_RDDST = 0x09

ST_SLPIN  = 0x10
ST_SLPOUT  = 0x11
ST_PTLON  = 0x12
ST_NORON  = 0x13

ST_INVOFF = 0x20
ST_INVON = 0x21
ST_DISPOFF = 0x28
ST_DISPON = 0x29
ST_CASET = 0x2A
ST_RASET = 0x2B
ST_RAMWR = 0x2C
ST_RAMRD = 0x2E

ST_COLMOD = 0x3A
ST_MADCTL = 0x36

ST_FRMCTR1 = 0xB1
ST_FRMCTR2 = 0xB2
ST_FRMCTR3 = 0xB3
ST_INVCTR = 0xB4
ST_DISSET5 = 0xB6

ST_PWCTR1 = 0xC0
ST_PWCTR2 = 0xC1
ST_PWCTR3 = 0xC2
ST_PWCTR4 = 0xC3
ST_PWCTR5 = 0xC4
ST_VMCTR1 = 0xC5

ST_RDID1 = 0xDA
ST_RDID2 = 0xDB
ST_RDID3 = 0xDC
ST_RDID4 = 0xDD

ST_PWCTR6 = 0xFC

ST_GMCTRP1 = 0xE0
ST_GMCTRN1 = 0xE1

#TFTRotations and TFTRGB are bits to set
# on MADCTL to control display rotation/color layout
#Looking at display with pins on top.
#00 = upper left printing right
#10 = does nothing (MADCTL_ML)
#20 = upper left printing down (backwards) (Vertical flip)
#40 = upper right printing left (backwards) (X Flip)
#80 = lower left printing right (backwards) (Y Flip)
#04 = (MADCTL_MH)

#60 = 90 right rotation
#C0 = 180 right rotation
#A0 = 270 right rotation
TFTRotations = [0x00, 0x60, 0xC0, 0xA0]
TFTBGR = 0x08 #When set color is bgr else rgb.
TFTRGB = 0x00

class Point(object):
  """2D point class"""

  def __init__(self, x = 0, y = 0) :
    self.x = x
    self.y = y

  def __str__(self) :
    return "ST7735.Point(" + str(self.x) + "," + str(self.y)+ ")"

  def __repr__(self) :
    return self.__str__()

  def clone( self ) :
    return Point(self.x, self.y)

def clamp( aValue, aMin, aMax ) :
  return max(aMin, min(aMax, aValue))

def TFTColor( aR, aG, aB ) :
  '''Create a 16 bit rgb value from the given R,G,B from 0-255.
     This assumes rgb 565 layout and will be incorrect for bgr.'''
  return ((aR & 0xF8) << 8) | ((aG & 0xFC) << 3) | (aB >> 3)

BLACK = 0
RED = TFTColor(0xFF, 0x00, 0x00)
MAROON = TFTColor(0x80, 0x00, 0x00)
GREEN = TFTColor(0x00, 0xFF, 0x00)
BLUE = TFTColor(0x00, 0x00, 0xFF)
NAVY = TFTColor(0x00, 0x00, 0x80)
CYAN = TFTColor(0x00, 0xFF, 0xFF)
YELLOW = TFTColor(0xFF, 0xFF, 0x00)
PURPLE = TFTColor(0xFF, 0x00, 0xFF)
WHITE = TFTColor(0xFF, 0xFF, 0xFF)
GRAY = TFTColor(0x80, 0x80, 0x80)

ScreenSize = Point(128, 160)

class TFT(object) :
  """Sainsmart TFT 7735 display driver."""

  @staticmethod
  def makecolor(aR, aG, aB):
    '''Create a 565 rgb TFTColor value'''
    return TFTColor(aR, aG, aB)

  def __init__(self, aLoc, aDC, aReset) :
    """aLoc SPI pin location is either 1 for 'X' or 2 for 'Y'.
       aDC is the DC pin and aReset is the reset pin."""
    self.size = ScreenSize.clone()
    self.rotate = 0                    #Vertical with top toward pins.
    self.rgb = TFTRGB                  #color order of rgb.
    self.dc  = pyb.Pin(aDC, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)
    self.reset = pyb.Pin(aReset, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)
    rate = 100000000 #Set way high but will be clamped to a maximum in SPI constructor.
    cs = "X5" if aLoc == 1 else "Y5"
    self.cs = pyb.Pin(cs, pyb.Pin.OUT_PP, pyb.Pin.PULL_DOWN)
    self.cs.high()
    self.spi = pyb.SPI(aLoc, pyb.SPI.MASTER, baudrate = rate, polarity = 0, phase = 1, crc=None)
    self.colorData = bytearray(2)
    self.windowLocData = bytearray(4)

  def on( self, aTF = True ) :
    '''Turn display on or off.'''
    self._writecommand(ST_DISPON if aTF else ST_DISPOFF)

  def invertcolor( self, aBool ) :
    '''Invert the color data IE: Black = White.'''
    self._writecommand(ST_INVON if aBool else ST_INVOFF)

  def setrgb( self, aTF = True ) :
    '''True = rgb else bgr'''
    self.rgb = TFTRBG if aTF else TFTBGR
    self._setMADCTL()

  def setrotation( self, aRot ) :
    '''0 - 3. Starts vertical with top toward pins and rotates 90 deg
       clockwise each step.'''
    if (0 <= aRot < 4):
      rotchange = self.rotate ^ aRot
      self.rotate = aRot
      #If switching from vertical to horizontal swap x,y
      # (indicated by bit 0 changing).
      if (rotchange & 1):
        self.size.x, self.size.y = self.size.y, self.size.x
      self._setMADCTL()

  def drawpixel( self, aPos, aColor ) :
    '''Draw a pixel at the given position'''
    if 0 <= aPos.x < self.size.x and 0 <= aPos.y < self.size.y:
      self._setwindowpoint(aPos)
      self._pushcolor(aColor)

  def drawstring( self, aPos, aString, aColor, aFont, aSize = 1 ) :
    '''Draw a string at the given position.  If the string reaches the end of the
       display it is wrapped to aPos.x on the next line.  aSize may be an integer
       which will size the font uniformly on w,h or a Point with x,y scales or
       any type that may be indexed with [0] or [1].'''

    #Make a size either from single value or 2 elements.
    if (type(aSize) == int) or (type(aSize) == float):
      wh = Point(aSize, aSize)
    elif (type(aSize) == Point):
      wh = aSize
    else:
      wh = Point(aSize[0], aSize[1])

    pos = aPos.clone()
    width = wh.x * aFont["Width"] + 1
    for c in aString:
      self.drawchar(pos, c, aColor, aFont, wh)
      pos.x += width
      #We check > rather than >= to let the right (blank) edge of the
      # character print off the right of the screen.
      if pos.x + width > self.size.x:
        pos.y += aFont["Height"] * wh.y + 1
        pos.x = aPos.x

  def drawchar( self, aPos, aChar, aColor, aFont, aSizes ) :
    '''Draw a character at the given position using the given font and color.
       aSizes is a Point with x, y as integer scales indicating the
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
      pos = aPos.clone()
      if aSizes.x <= 1 and aSizes.y <= 1 :
        for c in charA :
          pos.y = aPos.y
          for r in range(fonth) :
            if c & 0x01 :
              self.drawpixel(pos, aColor)
            pos.y += 1
            c >>= 1
          pos.x += 1
      else:
        for c in charA :
          pos.y = aPos.y
          for r in range(fonth) :
            if c & 0x01 :
              self.fillrect(pos, aSizes, aColor)
            pos.y += aSizes.y
            c >>= 1
          pos.x += aSizes.x

  def drawline( self, aStart, aEnd, aColor ) :
    '''Draws a line from aStart to aEnd in the given color.  Vertical or horizontal
       lines are forwarded to vline and hline.'''
    if aStart.x == aEnd.x:
      #Make sure we use the smallest y.
      pnt = aEnd if (aEnd.y < aStart.y) else aStart
      self.vline(pnt, abs(aEnd.y - aStart.y) + 1, aColor)
    elif aStart.y == aEnd.y:
      #Make sure we use the smallest x.
      pnt = aEnd if aEnd.x < aStart.x else aStart
      self.hline(pnt, abs(aEnd.x - aStart.x) + 1, aColor)
    else:
      slope = float(aEnd.y - aStart.y) / (aEnd.x - aStart.x)
      if (abs(slope) < 1.0):
        for x in range(aStart.x, aEnd.x + 1) :
          y = (x - aStart.x) * slope + aStart.y
          self.drawpixel(Point(x, int(y + 0.5)), aColor)
      else:
        for y in range(aStart.y, aEnd.y + 1) :
          x = (y - aStart.y) / slope + aStart.x
          self.drawpixel(Point(int(x + 0.5), y), aColor)

  def vline( self, aStart, aLen, aColor ) :
    '''Draw a vertical line from aStart for aLen. aLen may be negative.'''
    start = Point(clamp(aStart.x, 0, self.size.x), clamp(aStart.y, 0, self.size.y))
    stop = Point(start.x, clamp(start.y + aLen, 0, self.size.y))
    #Make sure smallest y 1st.
    if (stop.y < start.y):
      start, stop = stop, start
    self._setwindowloc(start, stop)
    self._draw(aLen, aColor)

  def hline( self, aStart, aLen, aColor ) :
    '''Draw a horizontal line from aStart for aLen. aLen may be negative.'''
    start = Point(clamp(aStart.x, 0, self.size.x), clamp(aStart.y, 0, self.size.y))
    stop = Point(clamp(start.x + aLen, 0, self.size.x), start.y)
    #Make sure smallest x 1st.
    if (stop.x < start.x):
      start, stop = stop, start
    self._setwindowloc(start, stop)
    self._draw(aLen, aColor)

  def rect( self, aStart, aSize, aColor ) :
    '''Draw a hollow rectangle.  aStart is the smallest coordinate corner
       and aSize is a Point indicating width, height.'''
    self.hline(aStart, aSize.x, aColor)
    self.hline(Point(aStart.x, aStart.y + aSize.y - 1), aSize.x, aColor)
    self.vline(aStart, aSize.y, aColor)
    self.vline(Point(aStart.x + aSize.x - 1, aStart.y), aSize.y, aColor)

  def fillrect( self, aStart, aSize, aColor ) :
    '''Draw a filled rectangle.  aStart is the smallest coordinate corner
       and aSize is a Point indicating width, height.'''
    start = Point(clamp(aStart.x, 0, self.size.x), clamp(aStart.y, 0, self.size.y))
    end = Point(clamp(start.x + aSize.x - 1, 0, self.size.x), clamp(start.y + aSize.y - 1, 0, self.size.y))

    if (end.x < start.x):
      end.x, start.x = start.x, end.x
    if (end.y < start.y):
      end.y, start.y = start.y, end.y

    self._setwindowloc(start, end)
    numPixels = (end.x - start.x + 1) * (end.y - start.y + 1)
    self._draw(numPixels, aColor)

  def circle( self, aPos, aRadius, aColor ) :
    '''Draw a hollow circle with the given radius and color with aPos as center.'''
    self.colorData[0] = aColor >> 8
    self.colorData[1] = aColor
    xend = int(0.7071 * aRadius) + 1
    rsq = aRadius * aRadius
    for x in range(xend) :
      y = int(sqrt(rsq - x * x))
      xp = aPos.x + x
      yp = aPos.y + y
      xn = aPos.x - x
      yn = aPos.y - y
      xyp = aPos.x + y
      yxp = aPos.y + x
      xyn = aPos.x - y
      yxn = aPos.y - x

      self._setwindowpoint(Point(xp, yp))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xp, yn))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xn, yp))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xn, yn))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xp, yn))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xyp, yxp))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xyp, yxn))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xyn, yxp))
      self._writedata(self.colorData)
      self._setwindowpoint(Point(xyn, yxn))
      self._writedata(self.colorData)

  def fillcircle( self, aPos, aRadius, aColor ) :
    '''Draw a filled circle with given radius and color with aPos as center'''
    rsq = aRadius * aRadius
    for x in range(aRadius) :
      y = int(sqrt(rsq - x * x))
      y0 = aPos.y - y
      ln = y * 2
      self.vline(Point(aPos.x + x, y0), ln, aColor)
      self.vline(Point(aPos.x - x, y0), ln, aColor)

  def fill( self, aColor ) :
    '''Fill screen with the given color.'''
    self.fillrect(Point(0, 0), self.size, aColor)
    self._draw(self.size.x * self.size.y, aColor)

  def _draw( self, aPixels, aColor ) :
    '''Send given color to the device aPixels times.'''
    self.colorData[0] = aColor >> 8
    self.colorData[1] = aColor

    self.dc.high()
    self.cs.low()
    for i in range(aPixels):
      self.spi.send(self.colorData)
    self.cs.high()

  def _setwindowpoint( self, aPos ) :
    '''Set a single point for drawing a color to.'''
    x = int(aPos.x)
    y = int(aPos.y)
    self._writecommand(ST_CASET)            #Column address set.
    self.windowLocData[0] = 0x00
    self.windowLocData[1] = x
    self.windowLocData[2] = 0x00
    self.windowLocData[3] = x
    self._writedata(self.windowLocData)

    self._writecommand(ST_RASET)            #Row address set.
    self.windowLocData[1] = y
    self.windowLocData[3] = y
    self._writedata(self.windowLocData)
    self._writecommand(ST_RAMWR)            #Write to RAM.

  def _setwindowloc( self, aPos0, aPos1 ) :
    '''Set a rectangular area for drawing a color to.'''
    self._writecommand(ST_CASET)            #Column address set.
    self.windowLocData[0] = 0x00
    self.windowLocData[1] = int(aPos0.x)
    self.windowLocData[2] = 0x00
    self.windowLocData[3] = int(aPos1.x)
    self._writedata(self.windowLocData)

    self._writecommand(ST_RASET)            #Row address set.
    self.windowLocData[1] = int(aPos0.y)
    self.windowLocData[3] = int(aPos1.y)
    self._writedata(self.windowLocData)

    self._writecommand(ST_RAMWR)            #Write to RAM.

  def _writecommand( self, aCommand ) :
    '''Write given command to the device.'''
    self.dc.low()
    self.cs.low()
    self.spi.send(aCommand)
    self.cs.high()

  def _writedata( self, aData ) :
    '''Write given data to the device.  This may be
       either a single int or a bytearray of values.'''
    self.dc.high()
    self.cs.low()
    self.spi.send(aData)
    self.cs.high()

  def _pushcolor( self, aColor ) :
    '''Push given color to the device.'''
    self.colorData[0] = aColor >> 8
    self.colorData[1] = aColor
    self._writedata(self.colorData)

  def _setMADCTL( self ) :
    '''Set screen rotation and RGB/BGR format.'''
    self._writecommand(ST_MADCTL)
    self._writedata(TFTRotations[self.rotate] | self.rgb)

  def _reset(self):
    '''Reset the device.'''
    self.dc.low()
    self.reset.high()
    pyb.delay(500)
    self.reset.low()
    pyb.delay(500)
    self.reset.high()
    pyb.delay(500)

  def _initb(self):
    '''Initialize blue tab version.'''
    self.size.x = ScreenSize.x + 2
    self.size.y = ScreenSize.y + 1
    self._reset()
    self._writecommand(ST_SWRESET)              #Software reset.
    pyb.delay(50)
    self._writecommand(ST_SLPOUT)               #out of sleep mode.
    pyb.delay(500)

    data1 = bytearray(1)
    self._writecommand(ST_COLMOD)               #Set color mode.
    data1[0] = 0x05                             #16 bit color.
    self._writedata(data1)
    pyb.delay(10)

    data3 = bytearray([0x00, 0x06, 0x03])       #fastest refresh, 6 lines front, 3 lines back.
    self._writecommand(ST_FRMCTR1)              #Frame rate control.
    self._writedata(data3)
    pyb.delay(10)

    self._writecommand(ST_MADCTL)
    data1[0] = 0x08                             #row address/col address, bottom to top refresh
    self._writedata(data1)

    data2 = bytearray(2)
    self._writecommand(ST_DISSET5)              #Display settings
    data2[0] = 0x15                             #1 clock cycle nonoverlap, 2 cycle gate rise, 3 cycle oscil, equalize
    data2[1] = 0x02                             #fix on VTL
    self._writedata(data2)

    self._writecommand(ST_INVCTR)               #Display inversion control
    data1[0] = 0x00                             #Line inversion.
    self._writedata(data1)

    self._writecommand(ST_PWCTR1)               #Power control
    data2[0] = 0x02   #GVDD = 4.7V
    data2[1] = 0x70   #1.0uA
    self._writedata(data2)
    pyb.delay(10)

    self._writecommand(ST_PWCTR2)               #Power control
    data1[0] = 0x05                             #VGH = 14.7V, VGL = -7.35V
    self._writedata(data1)

#Took this out because with it the screen stays all white.
#But I tested on green tab version so maybe it will work for blue.
#     self._writecommand(ST_PWCTR3)           #Power control
#     data2[0] = 0x01   #Opamp current small
#     data2[1] = 0x02   #Boost frequency
#     self._writedata(data2)

    self._writecommand(ST_VMCTR1)               #Power control
    data2[0] = 0x3C   #VCOMH = 4V
    data2[1] = 0x38   #VCOML = -1.1V
    self._writedata(data2)
    pyb.delay(10)

    self._writecommand(ST_PWCTR6)               #Power control
    data2[0] = 0x11
    data2[1] = 0x15
    self._writedata(data2)

    #These different values don't seem to make a difference.
#     dataGMCTRP = bytearray([0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22, 0x1f,
#                             0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10])
    dataGMCTRP = bytearray([0x02, 0x1c, 0x07, 0x12, 0x37, 0x32, 0x29, 0x2d, 0x29,
                            0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10])
    self._writecommand(ST_GMCTRP1)
    self._writedata(dataGMCTRP)

#     dataGMCTRN = bytearray([0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e, 0x30,
#                             0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10])
    dataGMCTRN = bytearray([0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c, 0x29, 0x2d, 0x2e,
                            0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10])
    self._writecommand(ST_GMCTRN1)
    self._writedata(dataGMCTRN)
    pyb.delay(10)

    self._writecommand(ST_CASET)                #Column address set.
    self.windowLocData[0] = 0x00
    self.windowLocData[1] = 2                   #Start at column 2
    self.windowLocData[2] = 0x00
    self.windowLocData[3] = self.size.x - 1
    self._writedata(self.windowLocData)

    self._writecommand(ST_RASET)                #Row address set.
    self.windowLocData[1] = 1                   #Start at row 2.
    self.windowLocData[3] = self.size.y - 1
    self._writedata(self.windowLocData)

    self._writecommand(ST_NORON)                #Normal display on.
    pyb.delay(10)

    self._writecommand(ST_RAMWR)
    pyb.delay(500)

    self._writecommand(ST_DISPON)
    self.cs.high()
    pyb.delay(500)

  def _initr(self):
    '''Initialize a red tab version.'''
    self._reset()

    self._writecommand(ST_SWRESET)              #Software reset.
    pyb.delay(150)
    self._writecommand(ST_SLPOUT)               #out of sleep mode.
    pyb.delay(500)

    data3 = bytearray([0x01, 0x2C, 0x2D])       #fastest refresh, 6 lines front, 3 lines back.
    self._writecommand(ST_FRMCTR1)              #Frame rate control.
    self._writedata(data3)

    self._writecommand(ST_FRMCTR2)              #Frame rate control.
    self._writedata(data3)

    data6 = bytearray([0x01, 0x2c, 0x2d, 0x01, 0x2c, 0x2d])
    self._writecommand(ST_FRMCTR3)              #Frame rate control.
    self._writedata(data6)
    pyb.delay(10)

    data1 = bytearray(1)
    self._writecommand(ST_INVCTR)               #Display inversion control
    data1[0] = 0x07                             #Line inversion.
    self._writedata(data1)

    self._writecommand(ST_PWCTR1)               #Power control
    data3[0] = 0xA2
    data3[1] = 0x02
    data3[2] = 0x84
    self._writedata(data3)

    self._writecommand(ST_PWCTR2)               #Power control
    data1[0] = 0xC5   #VGH = 14.7V, VGL = -7.35V
    self._writedata(data1)

    data2 = bytearray(2)
    self._writecommand(ST_PWCTR3)               #Power control
    data2[0] = 0x0A   #Opamp current small
    data2[1] = 0x00   #Boost frequency
    self._writedata(data2)

    self._writecommand(ST_PWCTR4)               #Power control
    data2[0] = 0x8A   #Opamp current small
    data2[1] = 0x2A   #Boost frequency
    self._writedata(data2)

    self._writecommand(ST_PWCTR5)               #Power control
    data2[0] = 0x8A   #Opamp current small
    data2[1] = 0xEE   #Boost frequency
    self._writedata(data2)

    self._writecommand(ST_VMCTR1)               #Power control
    data1[0] = 0x0E
    self._writedata(data1)

    self._writecommand(ST_INVOFF)

    self._writecommand(ST_MADCTL)               #Power control
    data1[0] = 0xC8
    self._writedata(data1)

    self._writecommand(ST_COLMOD)
    data1[0] = 0x05
    self._writedata(data1)

    self._writecommand(ST_CASET)                #Column address set.
    self.windowLocData[0] = 0x00
    self.windowLocData[1] = 0x00
    self.windowLocData[2] = 0x00
    self.windowLocData[3] = self.size.x - 1
    self._writedata(self.windowLocData)

    self._writecommand(ST_RASET)                #Row address set.
    self.windowLocData[3] = self.size.y - 1
    self._writedata(self.windowLocData)

    dataGMCTRP = bytearray([0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22, 0x1f,
                            0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10])
    self._writecommand(ST_GMCTRP1)
    self._writedata(dataGMCTRP)

    dataGMCTRN = bytearray([0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e, 0x30,
                            0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10])
    self._writecommand(ST_GMCTRN1)
    self._writedata(dataGMCTRN)
    pyb.delay(10)

    self._writecommand(ST_DISPON)
    pyb.delay(100)

    self._writecommand(ST_NORON)                #Normal display on.
    pyb.delay(10)

    self.cs.high()

  def _initg(self):
    '''Initialize a green tab version.'''
    self._reset()

    self._writecommand(ST_SWRESET)              #Software reset.
    pyb.delay(150)
    self._writecommand(ST_SLPOUT)               #out of sleep mode.
    pyb.delay(255)

    data3 = bytearray([0x01, 0x2C, 0x2D])       #fastest refresh, 6 lines front, 3 lines back.
    self._writecommand(ST_FRMCTR1)              #Frame rate control.
    self._writedata(data3)

    self._writecommand(ST_FRMCTR2)              #Frame rate control.
    self._writedata(data3)

    data6 = bytearray([0x01, 0x2c, 0x2d, 0x01, 0x2c, 0x2d])
    self._writecommand(ST_FRMCTR3)              #Frame rate control.
    self._writedata(data6)
    pyb.delay(10)

    self._writecommand(ST_INVCTR)               #Display inversion control
    self._writedata(0x07)

    self._writecommand(ST_PWCTR1)               #Power control
    data3[0] = 0xA2
    data3[1] = 0x02
    data3[2] = 0x84
    self._writedata(data3)

    self._writecommand(ST_PWCTR2)               #Power control
    self._writedata(0xC5)

    data2 = bytearray(2)
    self._writecommand(ST_PWCTR3)               #Power control
    data2[0] = 0x0A   #Opamp current small
    data2[1] = 0x00   #Boost frequency
    self._writedata(data2)

    self._writecommand(ST_PWCTR4)               #Power control
    data2[0] = 0x8A   #Opamp current small
    data2[1] = 0x2A   #Boost frequency
    self._writedata(data2)

    self._writecommand(ST_PWCTR5)               #Power control
    data2[0] = 0x8A   #Opamp current small
    data2[1] = 0xEE   #Boost frequency
    self._writedata(data2)

    self._writecommand(ST_VMCTR1)               #Power control
    self._writedata(0x0E)

    self._writecommand(ST_INVOFF)

    self._setMADCTL()

    self._writecommand(ST_COLMOD)
    self._writedata(0x05)

    self._writecommand(ST_CASET)                #Column address set.
    self.windowLocData[0] = 0x00
    self.windowLocData[1] = 0x01                #Start at row/column 1.
    self.windowLocData[2] = 0x00
    self.windowLocData[3] = self.size.x - 1
    self._writedata(self.windowLocData)

    self._writecommand(ST_RASET)                #Row address set.
    self.windowLocData[3] = self.size.y - 1
    self._writedata(self.windowLocData)

    dataGMCTRP = bytearray([0x02, 0x1c, 0x07, 0x12, 0x37, 0x32, 0x29, 0x2d, 0x29,
                            0x25, 0x2b, 0x39, 0x00, 0x01, 0x03, 0x10])
    self._writecommand(ST_GMCTRP1)
    self._writedata(dataGMCTRP)

    dataGMCTRN = bytearray([0x03, 0x1d, 0x07, 0x06, 0x2e, 0x2c, 0x29, 0x2d, 0x2e,
                            0x2e, 0x37, 0x3f, 0x00, 0x00, 0x02, 0x10])
    self._writecommand(ST_GMCTRN1)
    self._writedata(dataGMCTRN)

    self._writecommand(ST_NORON)                #Normal display on.
    pyb.delay(10)

    self._writecommand(ST_DISPON)
    pyb.delay(100)

    self.cs.high()

def maker():
  t = TFT(1, "X1", "X2")
  print("Initializing")
  t._initr()
  t.fill(0)
  return t

def makeb( ):
  t = TFT(1, "X1", "X2")
  print("Initializing")
  t._initb()
  t.fill(0)
  return t

def makeg( ):
  t = TFT(1, "X1", "X2")
  print("Initializing")
  t._initg()
  t.fill(0)
  return t
