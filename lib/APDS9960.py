# MicroPython apds9960 motion detection device driver.

#todo: Have a mix of styles here.  Some use properties for setters while others use functions.

import pyb
from utime import *

def setvalue( aOriginal, aPosBits, aValue ) :
  '''Set a specific bit on a variable.  aPosBits = 0xpm (p = pos, m = # mask bits).'''
  mask = (1 << (aPosBits & 0xf)) - 1
  pos = aPosBits >> 4
  aOriginal &= ~(mask << pos)
  return aOriginal | (aValue & mask) << pos

def getvalue( aOriginal, aPosBits ) :
  '''Get a specific bit from a variable.  aPosBits = 0xpm (p = pos, m = # mask bits).'''
  mask = (1 << (aPosBits & 0xf)) - 1
  pos = aPosBits >> 4
  return (aOriginal >> pos) & mask

class apds9960(object) :

  _ADDRESS = const(0x39)
  _RAM = const(0x00)
  _ENABLE = const(0x80)
  _ATIME = const(0x81)
  _WTIME = const(0x83)
  _AILTL = const(0x84)
  _AILTH = const(0x85)
  _AIHTL = const(0x86)
  _AIHTH = const(0x87)
  _PILT = const(0x89)
  _PIHT = const(0x8B)
  _PERS = const(0x8C)
  _CONFIG1 = const(0x8D)
  _PPULSE = const(0x8E)
  _CONTROL = const(0x8F)
  _CONFIG2 = const(0x90)
  _ID = const(0x92)
  _STATUS = const(0x93)
  _CDATAL = const(0x94)
  _CDATAH = const(0x95)
  _RDATAL = const(0x96)
  _RDATAH = const(0x97)
  _GDATAL = const(0x98)
  _GDATAH = const(0x99)
  _BDATAL = const(0x9A)
  _BDATAH = const(0x9B)
  _PDATA = const(0x9C)
  _POFFSET_UR = const(0x9D)
  _POFFSET_DL = const(0x9E)
  _CONFIG3 = const(0x9F)
  _GPENTH = const(0xA0)
  _GEXTH = const(0xA1)
  _GCONF1 = const(0xA2)
  _GCONF2 = const(0xA3)
  _GOFFSET_U = const(0xA4)
  _GOFFSET_D = const(0xA5)
  _GOFFSET_L = const(0xA7)
  _GOFFSET_R = const(0xA9)
  _GPULSE = const(0xA6)
  _GCONF3 = const(0xAA)
  _GCONF4 = const(0xAB)
  _GFLVL = const(0xAE)
  _GSTATUS = const(0xAF)
  _IFORCE = const(0xE4)
  _PICLEAR = const(0xE5)
  _CICLEAR = const(0xE6)
  _AICLEAR = const(0xE7)
  _GFIFO_U = const(0xFC)
  _GFIFO_D = const(0xFD)
  _GFIFO_L = const(0xFE)
  _GFIFO_R = const(0xFF)

  #Device IDs
  _ID_1 = const(0xAB)
  _ID_2 = const(0x9C)

  #A Gain
  _AGAIN_1X  = const(0)  #No gain
  _AGAIN_4X  = const(1)  #2x gain
  _AGAIN_16X = const(2)  #16x gain
  _AGAIN_64X = const(3)  #64x gain

  #P Gain
  _PGAIN_1X = const(0)  #1x gain
  _PGAIN_2X = const(1)  #2x gain
  _PGAIN_4X = const(2)  #4x gain
  _PGAIN_8X = const(3)  #8x gain

  #Pulse Length
  _PPULSELEN_4US  = const(0)  #4uS
  _PPULSELEN_8US  = const(1)  #8uS
  _PPULSELEN_16US = const(2)  #16uS
  _PPULSELEN_32US = const(3)  #32uS

  #LED Drive
  _LEDDRIVE_100MA = const(0)  #100mA
  _LEDDRIVE_50MA  = const(1)  #50mA
  _LEDDRIVE_25MA  = const(2)  #25mA
  _LEDDRIVE_12MA  = const(3)  #12.5mA

  #LED Boost
  _LEDBOOST_100 = const(0)  #100%
  _LEDBOOST_150 = const(1)  #150%
  _LEDBOOST_200 = const(2)  #200%
  _LEDBOOST_300 = const(3)  #300%

  #Dimensions
  _DIMENSIONS_ALL        = const(0)
  _DIMENSIONS_UP_DOWM    = const(1)
  _DIMENSIONS_LEFT_RIGHT = const(2)

  #FIFO
  _GFIFO_1  = const(0)
  _GFIFO_4  = const(1)
  _GFIFO_8  = const(2)
  _GFIFO_16 = const(3)

  #G Gain
  _GGAIN_1  = const(0)
  _GGAIN_2  = const(1)
  _GGAIN_4  = const(2)
  _GGAIN_8  = const(3)

  #G Pulse
  _GPULSE_4US   = const(0)
  _GPULSE_8US   = const(1)
  _GPULSE_16US  = const(2)
  _GPULSE_32US  = const(3)

  #Following are the bytes describing the data packed into each 8 bit value on the chip.
  #Nibble 1 = position, 0 = bits

  ENABLE_PON = const(0x01)
  ENABLE_AEN = const(0x11)
  ENABLE_PEN = const(0x21)
  ENABLE_WEN = const(0x31)
  ENABLE_AIEN = const(0x41)
  ENABLE_PIEN = const(0x51)
  ENABLE_GEN = const(0x61)

  PERS_APERS = const(0x04)
  PERS_PPERS = const(0x44)

  PPULSE_PPULSE = const(0x06)
  PPULSE_PPLEN = const(0x62)

  CONTROL_AGAIN = const(0x02)
  CONTROL_PGAIN = const(0x22)
  CONTROL_LDRIVE = const(0x42)

  CONFIG2_LED_BOOST = const(0x42)
  CONFIG2_CPSIEN = const(0x61)  #Clear photo diode saturation int enable.
  CONFIG2_PSIEN = const(0x71)   #Proximity saturation interrupt enable.

  CONFIG3_PMASK_R = const(0x01)
  CONFIG3_PMASK_L = const(0x11)
  CONFIG3_PMASK_D = const(0x21)
  CONFIG3_PMASK_U = const(0x31)
  CONFIG3_SAI = const(0x41)
  CONFIG3_PCMP = const(0x51)

  GCONFIG1_GEXPERS = const(0x02)
  GCONFIG1_GEXMSK = const(0x24)
  GCONFIG1_GFIFOTH = const(0x62)

  GCONFIG2_GWTIME = const(0x03)
  GCONFIG2_GLDRIVE = const(0x32)
  GCONFIG2_GGAIN = const(0x52)

  GCONFIG3_GDIMS = const(0x02)

  GCONFIG4_GMODE = const(0x01)
  GCONFIG4_GIEN = const(0x12)

  GPULSE_GPULSE = const(0x06)
  GPULSE_GPLEN = const(0x62)

  STATUS_AVALID = const(0x01)
  STATUS_PVALID = const(0x11)
  STATUS_GINT = const(0x21)
  STATUS_AINT = const(0x41)
  STATUS_PINT = const(0x51)
  STATUS_PGSTAT = const(0x61)
  STATUS_CPSTAT = const(0x71)

  GSTATUS_GVALID = const(0x01)
  GSTATUS_GFOV = const(0x11)

# Gesture wait time values
  _GWTIME_0MS    = const(0)
  _GWTIME_2_8MS  = const(1)
  _GWTIME_5_6MS  = const(2)
  _GWTIME_8_4MS  = const(3)
  _GWTIME_14_0MS = const(4)
  _GWTIME_22_4MS = const(5)
  _GWTIME_30_8MS = const(6)
  _GWTIME_39_2MS = const(7)

  _NONE = const(0)
  _UP = const(1)
  _DOWN = const(2)
  _LEFT = const(3)
  _RIGHT = const(4)

  _DefaultIntTimeMS = const(10)

  def __init__( self, aLoc ) :
    """aLoc I2C pin location is either 1, 'X', 2 or'Y'."""
    self._i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)

    #Mirrors data on the controller.
    self._enable = 0    #Enable
    self._pers = 0      #Pers
    self._ppulse = 0    #PPulse
    self._gpulse = 0    #GPulse
    self._control = 0   #Control
    self._config2 = 0   #Config 2.
    self._config3 = 0   #Config 3.
    self._gconfig1 = 0  #Gesture Config 1.
    self._gconfig2 = 0  #Gesture Config 2
    self._gconfig3 = 0  #Gesture Config 3
    self._gconfig4 = 0  #Gesture Config 4.
    self._status = 0    #Status
    self._gstatus = 0   #GStatus

    self.resetcounts()

    self._millis = 0

    self._b1 = bytearray(1)
    self._b2 = bytearray(2)

    sleep_us(50)
    self.begin()

  def read( self, aLoc ) :
    """Read 8 bit value and return."""
    self._i2c.mem_read(self._b1, _ADDRESS, aLoc)
    return self._b1[0]

  def read16( self, aLoc ) :
    """Read 16 bit value and return."""
    self._i2c.mem_read(self._b2, _ADDRESS, aLoc)
    return (self._b2[1] << 8) | self._b2[0]

  def write( self, aLoc, aVal ) :
    """Write 8 bit value to given address.  aVal may be a byte array."""
    self._i2c.mem_write(aVal, _ADDRESS, aLoc)

  def write16( self, aLoc, aVal ) :
    """Write 16 bit value to given address."""
    self._b2[0] = aVal
    self._b2[1] = aVal >> 8
    self._i2c.mem_write(self._b2, _ADDRESS, aLoc)

  def reset( self ):
    """Reset the controller and set default frequency."""
    self.write(0, _MODE1)
    self.setfreq(_DEFAULTFREQ)

  #Enable
  def setenable( self, aMember, aValue ) :
    self._enable = setvalue(self._enable, aMember, aValue)
    self.write(_ENABLE, self._enable)

  def getenable( self, aMember ) :
    return getvalue(self._enable, aMember)

  #Pers
  def setpers( self, aMember, aValue ) :
    self._pers = setvalue(self._pers, aMember, aValue)
    self.write(_PERS, self._pers)

  def getpers( self, aMember ) :
    return getvalue(self._pers, aMember)

  #Control
  def setcontrol( self, aMember, aValue ) :
    self._control = setvalue(self._control, aMember, aValue)
    self.write(_CONTROL, self._control)

  def getcontrol( self, aMember ) :
    return getvalue(self._control, aMember)

  #Config 3
  def setconfig2( self, aMember, aValue ) :
    self._config2 = setvalue(self._config2, aMember, aValue)
    self.write(_CONFIG2, self._config2)

  def getconfig2( self, aMember ) :
    return getvalue(self._config2, aMember)

  #Config 3
  def setconfig3( self, aMember, aValue ) :
    self._config3 = setvalue(self._config3, aMember, aValue)
    self.write(_CONFIG3, self._config3)

  def getconfig3( self, aMember ) :
    return getvalue(self._config3, aMember)

  #GConfig 1
  def setgconfig1( self, aMember, aValue ) :
    self._gconfig1 = setvalue(self._gconfig1, aMember, aValue)
    self.write(_GCONF1, self._gconfig1)

  def getgconfig1( self, aMember ) :
    return getvalue(self._gconfig1, aMember)

  #GConfig 2
  def setgconfig2( self, aMember, aValue ) :
    self._gconfig2 = setvalue(self._gconfig2, aMember, aValue)
    self.write(_GCONF2, self._gconfig2)

  def getgconfig2( self, aMember ) :
    return getvalue(self._gconfig2, aMember)

  #GConfig 3
  def setgconfig3( self, aMember, aValue ) :
    self._gconfig3 = setvalue(self._gconfig3, aMember, aValue)
    self.write(_GCONF3, self._gconfig3)

  def getgconfig3( self, aMember ) :
    return getvalue(self._gconfig3, aMember)

  #GConfig 4
  def setgconfig4( self, aMember, aValue ) :
    self._gconfig4 = setvalue(self._gconfig4, aMember, aValue)
    self.write(_GCONF4, self._gconfig4)

  def getgconfig4( self, aMember ) :
    return getvalue(self._gconfig4, aMember)

  #Status
  def getstatus( self, aMember ) :
    '''Get member of status'''
    self._status = self.read(_STATUS)
    return getvalue(self._status, aMember)

  #GStatus
  def getgstatus( self, aMember ) :
    self._gstatus = self.read(_GSTATUS)
    return getvalue(self._gstatus, aMember)

  def resetcounts( self ) :
    self._gestCnt = 0
    #todo - put these in an array.
    self._ucount = 0
    self._dcount = 0
    self._lcount = 0
    self._rcount = 0

  def enableproximityint( self, aValue ) :
    self.setenable(ENABLE_PIEN, aValue)
    self.clearInterrupt()

  def proximityintthreshold( self, aValue, aPersistance ) :
    self.write(_PILT, aValue & 0xFF)
    self.write(_PIHT, aValue >> 8)
    self.setpers(PERS_PPERS, min(aPersistance, 7))

  def proximity( self ) :
    return self.read(_PDATA)

  def gestureenterthreshold( self, aValue ) :
    self.write(_GPENTH, aValue)

  def gestureexitthreshold( self, aValue ) :
    self.write(_GEXTH, aValue)

  def gestureoffset( self, aUp, aDown, aLeft, aRight ) :
    self.write(_GOFFSET_U, aUp)
    self.write(_GOFFSET_D, aDown)
    self.write(_GOFFSET_L, aLeft)
    self.write(_GOFFSET_R, aRight)

  def enablegesture( self, aEnable ) :
    #If disabling make sure we aren't currently in gesture mode.
    # Gesture mode is auto entered when proximity enter threshold is hit
    # so we don't need to enable it.
    if not aEnable :
      self.setgconfig4(GCONFIG4_GMODE, False)
    self.setenable(ENABLE_GEN, aEnable)
    self.resetcounts()

  @property
  def gesturevalid( self ) :
    """Return True if gesture data exists."""
    return self.getgstatus(GSTATUS_GVALID)

  def gesturedata( self ) :
    """Read gesture data and return as (u,d,l,r).  Returns None of no data ready."""
    level = self.read(_GFLVL)
    if level == 0 :
      return # no data
    fifo_u = self.read(_GFIFO_U)
    fifo_d = self.read(_GFIFO_D)
    fifo_l = self.read(_GFIFO_L)
    fifo_r = self.read(_GFIFO_R)

    return (fifo_u, fifo_d, fifo_l, fifo_r)

  @property
  def colordataready( self ) :
    """Return true if color data ready to read."""
    return self.getstatus(STATUS_AVALID)

  def colordata( self ) :
    """Return color data as (c,r,g,b)."""
    c = self.read16(_CDATAL)
    r = self.read16(_RDATAL)
    g = self.read16(_GDATAL)
    b = self.read16(_BDATAL)

    return (c, r, g, b)

  def clearInterrupt( self ) :
    #NOTE: The .ccp writes 0 bytes to this address.  I don't know how
    # to do that so I'm writing a 0 to AICLEAR.
    self.write(_AICLEAR, 0)

  def intlimits( self, aLow, aHigh ) :
    self.write16(_AILTL, aLow)
    self.write16(_AIHTL, aHigh)

  def adcintegrationtime( self, aValue ) :
    t = max(0.0, min(255.0, 256.0 - (aValue / 2.78)))
    self.write(_ATIME, int(t))

  @property
  def enabled( self ) :
    return self.getenable(ENABLE_PON)

  @enabled.setter
  def enabled( self, aValue ) :
    self.setenable(ENABLE_PON, aValue)

  def proxpulse( self, aLen, aPulses ) :
    setvalue(self._ppulse, PPULSE_PPULSE, min(64, max(aPulses, 1)) - 1)
    setvalue(self._ppulse, PPULSE_PPLEN, aLen)
    self.write(PPULSE_PPULSE, self._ppulse)

  def gpulse( self, aLen, aPulses ) :
    setvalue(self._gpulse, GPULSE_GPULSE, min(64, max(aPulses, 1)) - 1)
    setvalue(self._gpulse, GPULSE_GPLEN, aLen)
    self.write(PPULSE_PPULSE, self._gpulse)

  def begin( self ) :
    id = self.read(_ID)
    if id != _ID_1 and id != _ID_2:
      raise Exception('Incorrect apds9960 ID {}.'.format(id))

    self.enabled = False
    sleep_us(50)

    # Set default integration time and gain
    self.adcintegrationtime(_DefaultIntTimeMS)
    self.write(_WTIME, 249)
    self.write(_POFFSET_UR, 0)
    self.write(_POFFSET_DL, 0)
    self.write(_CONFIG1, 0x60)
    self.setcontrol(CONTROL_LDRIVE, _LEDDRIVE_100MA)
    self.setcontrol(CONTROL_AGAIN, _AGAIN_16X)
    self.setcontrol(CONTROL_PGAIN, _PGAIN_8X)

    self.proxpulse(_PPULSELEN_16US, 10)
    self.gpulse(_GPULSE_32US, 9)

    self.proximityintthreshold(0x3200, 1)
    self.enableproximityint(False)        #Proximity Interrupt
#    self.intlimits(0xFFFF, 0)

    #100 makes the results a bit more erratic, No value boosts distance.  It seems
    # the higher the boost the more stable the data is.
    self.setconfig2(CONFIG2_LED_BOOST, _LEDBOOST_300)

    #NOTE: This must be 1 if enter threshold is < exit or we will never get gesture input because we
    # won't stay in the gesture state for more than 1 cycle.
    self.setgconfig1(GCONFIG1_GFIFOTH, _GFIFO_1)
    self.setgconfig2(GCONFIG2_GWTIME, _GWTIME_2_8MS)
    self.setgconfig2(GCONFIG2_GGAIN, _GGAIN_4)
    self.setgconfig3(GCONFIG3_GDIMS, _DIMENSIONS_ALL)
    #NOTE: An enter value lower than the exit value means we are constantly entering/exiting the state machine.
    #  If we don't do this we will not get proximity and color input because those are not updated when in gesture state.
    self.gestureenterthreshold(5)   #When proximity value is above this we enter the gesture state machine.
    self.gestureexitthreshold(255)  #When all gesture values are below this we exit the gesture state machine.
    self.gestureoffset(0, 0, 0, 0)

    self.setenable(ENABLE_PEN, True)  #enable proximity
    self.setenable(ENABLE_AEN, True)  #enable color
    self.enablegesture(True)

    self.enabled = True
    sleep_us(50)

  def readgesture( self ) :
    #todo: implement
    while True :
      ud_diff = 0
      lr_diff = 0
      gesturereceived = 0
      if not self.gesturevalid :
        return 0

      sleep_us(20) #todo: find correct value for this.

      toread = self.read(_GFLVL)
      buf = self._i2c.mem_read(toread, _ADDRESS, _GFIFO_U)

      diff = buf[0] - buf[1]
      if abs(diff) > 13 :
        ud_diff += diff

      diff = buf[2] - buf[3]
      if abs(diff) > 13 :
        lr_diff += diff

      if ud_diff != 0 :
        if ud_diff < 0 :
          if self._dcount > 0 :
            gesturereceived = _UP
          else:
            self._ucount += 1
        elif ud_diff > 0 :
          if self._ucount > 0 :
            gesturereceived = _DOWN
          else:
            self._dcount += 1

      if lr_diff != 0 :
        if lr_diff < 0 :
          if self._rcount > 0 :
            gesturereceived = _LEFT
          else:
            self._lcount += 1
        elif lr_diff > 0 :
          if self._lcount > 0 :
            gesturereceived = _RIGHT
          else:
            self._rcount += 1

      if (ud_diff != 0) or (lr_diff != 0) :
        self._millis = ticks_ms()

      if gesturereceived or (ticks_ms() - self._millis > 300) :
        self.resetcounts()

      return gesturereceived

#  def calculatecolortemp( self, aRed, aGreen, aBlue ) :
#    x = (-0.14282 * aRed) + (1.54924 * aGreen) + (-0.95641 * aBlue)
#    y = self.calculatelux(aRed, aGreen, aBlue)
#    z = (-0.68202 * aRed) + (0.77073 * aGreen) + (0.56332 * aBlue)
#
#    den = x + y + z
#    xc = x / den
#    yc = y / den
#
#    n = (xc - 0.332) / (0.1858 - yc)
#
#    cct = (449.0 * pow(n, 3)) + (35250 * pow(n, 2)) + (6823.3 * n) + 5520.33
#
#    return cct
#
#  def calculatelux( self, aRed, aGreen, aBlue ) :
#    return (-0.32466 * aRed) + (1.57837 * aGreen) + (-0.73191 * aBlue)

