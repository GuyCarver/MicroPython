# MicroPython APDS9960 motion detection device driver.

import pyb

class APDS9960(object) :

  _ADDRESS = 0x39
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

  #A Gain
  _AGAIN_1X  = const(0x00)  #No gain
  _AGAIN_4X  = const(0x01)  #2x gain
  _AGAIN_16X = const(0x02)  #16x gain
  _AGAIN_64X = const(0x03)  #64x gain

  #P Gain
  _PGAIN_1X = const(0x00)  #1x gain
  _PGAIN_2X = const(0x04)  #2x gain
  _PGAIN_4X = const(0x08)  #4x gain
  _PGAIN_8X = const(0x0C)  #8x gain

  #Pulse Length
  _PPULSELEN_4US  = 0x00  #4uS
  _PPULSELEN_8US  = 0x40  #8uS
  _PPULSELEN_16US = 0x80  #16uS
  _PPULSELEN_32US = 0xC0  #32uS

  #LED Drive
  _LEDDRIVE_100MA = const(0x00)  #100mA
  _LEDDRIVE_50MA  = const(0x40)  #50mA
  _LEDDRIVE_25MA  = const(0x80)  #25mA
  _LEDDRIVE_12MA  = const(0xC0)  #12.5mA

  #LED Boost
  _LEDBOOST_100PCNT = const(0x00)  #100%
  _LEDBOOST_150PCNT = const(0x10)  #150%
  _LEDBOOST_200PCNT = const(0x20)  #200%
  _LEDBOOST_300PCNT = const(0x30)  #300%

  #Dimensions
  _DIMENSIONS_ALL        = const(0x00)
  _DIMENSIONS_UP_DOWM    = const(0x01)
  _DIMENSIONS_LEFT_RIGHT = const(0x02)

  #FIFO
  _GFIFO_1  = const(0x00)
  _GFIFO_4  = const(0x01)
  _GFIFO_8  = const(0x02)
  _GFIFO_16 = const(0x03)

  #G Gain
  _GGAIN_1  = const(0x00),
  _GGAIN_2  = const(0x01),
  _GGAIN_4  = const(0x02),
  _GGAIN_8  = const(0x03),

  #G Pulse
  _GPULSE_4US   = const(0x00)
  _GPULSE_8US   = const(0x01)
  _GPULSE_16US  = const(0x02)
  _GPULSE_32US  = const(0x03)

  def __init__( self, aLoc ) :
    """aLoc I2C pin location is either 1, 'X', 2 or'Y'."""
    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)

    #Gesture Config 1.
    self._gexpers = 0
    self._gexmsk = 0
    self._gfifoth = 0

    #Gesture Config 2
    self._gwtime = 0
    self._gldrive = 0
    self._ggain = 0

    #Gesture Config 3
    self._gdims = 0

    #Gesture Config 4.
    self._gmode = 0
    self._gien = 0

    #GPulse
    self._gpulse = APDS9960._GPULSE_32US
    self._gplen = 9 #10 pulses.

    #PPulse
    self._ppulse = 0
    self._pplen = 0

    #Enable
    self._pon = 0
    self._aen = 0
    self._pen = 0
    self._wen = 0
    self._aien = 0
    self._pien = 0
    self._gen = 0

    #Control
    self._again = 0
    self._pgain = 0
    self._ldrive = 0

    #Pers
    self._apers = 0
    self._ppers = 0

    #Status
    self._status = 0

    #GStatus
    self._gstatus = 0

    sleep_us(50)
    self.begin()

  def read( self, aLoc ) :
    """Read 8 byte value and return in bytearray"""
    return self.i2c.mem_read(1, self._ADDRESS, aLoc)

  def write( self, aVal, aLoc ) :
    """Write 8 bit value to given address.  aVal may be an int buffer."""
    self.i2c.mem_write(aVal, self._ADDRESS, aLoc)

  def reset( self ):
    """Reset the controller and set default frequency."""
    self.write(0, _MODE1)
    self.setfreq(_DEFAULTFREQ)

  def writec3( self ) :
    v = (self._pcmp << 5) | (self._sai << 4) | (self._pmask_u << 3) | (self._mask_d << 2) | (self._pmask_l << 1) | self._pmask_r
    self.write(APDS9960._CONFIG3, v)

  def writegc2( self ) :
    v = (self._ggain << 5) | (self._gldrive << 3) | self._gwtime
    self.write(APDS9960._GCONF2, v)

  def writegc1( self ) :
    v = (self._gfifoth << 7) | (self._gexmsk << 5) | self._gexpers
    self.write(APDS9960._GCONF1, v)

  def writegc4( self ) :
    v = (self._gien << 1) | self._gmode
    self.write(APDS9960._GCONF4, v)

  def writegpulse( self ) :
    v = (self._plen << 6) | self._gpulse
    self.write(APDS9960._GPULSE, v)

  def writepers( self ) :
    v = (self._ppers << 4) | self._apers
    self.write(APDS9960._PERS, v)

  def writecontrol( self ) :
    v = (self._ldrive << 6) | (self._pgain << 2) | self._again
    self.write(APSD9960._CONTROL, v)

  def writeenable( self ) :
    v = (self._gen << 6) | (self._pien << 5) | (self._aien << 4) | (self._wen << 3) | (self._pen << 2) | (self._aen << 1) | self._pon
    self.write(APDS9960._ENABLE)

  def resetCounts( self ) :
    self._gestCnt = 0
    #todo - put these in an array.
    self._ucount = 0
    self._dcount = 0
    self._lcount = 0
    self._rcount = 0

  @property
  def status( self ) :
    self._status = this.read(APDS9960._STATUS)[0]
    return self._status

  @property
  def gstatus( self ) :
    self._gstatus = this.read(APDS9960._GSTATUS)[0]
    return self._gstatus

  @property
  def gpulse( self ) :
    return (self._gplen << 6) | self._gpulse

  @property
  def proximityenable( self ) :
    return self._pen

  @proximityenable.setter
  def proximityenable( self, aValue ) :
    self._pen = aValue & 0x01
    self.writeenable()

  @property
  def proximityintenable( self ) :
    return self._pien

  @proximityint.setter
  def proximityintenable( self, aValue ) :
    self._pien = aValue & 0x01
    self.writeenable()
    self.clearInterrupt()

  def proximityintthreshold( self, aValue, aPersistance ) :
    self.write(APDS9960._PILT, aValue & 0xFF)
    self.write(APDS9960._PIHT, aValue >> 8)
    self._ppers = min(aPersistance, 7)
    self.writepers()

  @property
  def proximityint( self ) :
    return self.status & 0x20

  @property
  def proximity( self ) :
    return self.read(APDS9960._PDATA)[0]

  @property
  def gesturevalid( self ) :
    return self.gstatus & 0x01

  @property
  def gesturedims( self ) :
    return self._gdims

  @gesturedims.setter
  def gesturedims( self, aValue ) :
    self._gdims = aValue & 0x03
    self.write(APDS9960._GCONF3, self._gdims)

  @property
  def gesturefifothreshold( self ) :
    return self._gfifoth

  @gesturefifothreshold.setter
  def gesturefifothreshold( self, aValue ) :
    self._gfifoth = aValue & 0x03
    self.writegc1()

  @property
  def gesturegain( self ) :
    return self._ggain

  @gesturegain.setter
  def gesturegain( self, aValue ) :
    self._ggain = aValue & 0x03
    self.writegc2()

  def gestureproximitythreshold( self, aValue ) :
    self.write(APDS9960._GPENTH, aValue)

  def gestureoffset( self, aUp, aDown, aLeft, aRight ) :
    self.write(APDS9960._GOFFSET_U, aUp)
    self.write(APDS9960._GOFFSET_D, aDown)
    self.write(APDS9960._GOFFSET_L, aLeft)
    self.write(APDS9960._GOFFSET_R, aRight)

  @property
  def gestureenable( self ) :
    return self._gen

  @gestureenable.setter
  def gestureenable( self, aEnable ) :
    self._gen = aEnable & 0x01

    if not aEnable :
      self._gmode = 0
      self.writegc4()

    self.writeenable()
    self.resetCounts()

  def colorenable( self, aEnable ) :
      self._aen = aEnable & 0x01
      self.writeenable()

  @property
  def colorintenable( self ) :
    return self._aien

  @colorintenable.setter
  def colorintenable( self, aEnable ) :
    self._aien = aEnable & 0x01
    self.writeenable()

  @property
  def colordataready( self ) :
    return self.status & 0x01

  @property
  def colordata( self ) :
    #todo: Maybe try and read 16 bit data.
    #NOTE: The l and h may be backwards here.
    c = self.read(APDS9960._CDATAL)[0]
    c |= self.read(APDS9960._CDATAH)[0] << 8
    r = self.read(APDS9960._RDATAL)[0]
    r |= self.read(APDS9960._RDATAH)[0] << 8
    g = self.read(APDS9960._GDATAL)[0]
    g |= self.read(APDS9960._GDATAH)[0] << 8
    b = self.read(APDS9960._BDATAL)[0]
    b |= self.read(APDS9960._BDATAH)[0] << 8

    return (c, r, g, b)

  def clearInterrupt( self ) :
    #NOTE: The .ccp writes 0 bytes to this address.  I don't know how
    # to do that so I'm writing a 0 to AICLEAR.
    self.write(APDS9960._AICLEAR, 0)

  def intlimits( self, aLow, aHigh ) :
    self.write(APDS9960._AILTL, aLow & 0xFF)
    self.write(APDS9960._AILTH, aLow >> 8)
    self.write(APDS9960._AIHTL, aHigh & 0xFF)
    self.write(APDS9960._AIHTH, aHigh >> 8)

/////////////////////////////////

  def readgesture( self ) :
    #todo: implement
    pass

  def calculatecolortemp( self, aRed, aGreen, aBlue ) :
    #todo: implement
    pass

  def calculatelux( self, aRed, aGreen, aBlue ) :
    #todo: implement
    pass

  @property
  def adcintegrationtime( self ):
    return (256.0 - self.read(APDS9960._ATIME)[0]) * 2.78

  @adcintegrationtime.setter
  def adcintegrationtime( self, aValue ) :
    temp = max(0.0, min(255.0, 256.0 - (aValue / 2.78)))
    self.write(APSD9960._ATIME, temp)


  @property
  def avalid( self ) :
    return self._status & 0x01

  @property
  def pvalid( self ) :
    return self._status & 0x02

  @property
  def gint( self ) :
    return self._status & 0x04

  @property
  def aint( self ) :
    return self._status & 0x10

  @property
  def pint( self ) :
    return self._status & 0x20

  @property
  def pgsat( self ) :
    return self._status & 0x40

  @property
  def cpsat( self ) :
    return self._status & 0x80

  @property
  def adcgain( self ):
    return self._again

  @ADCGain.setter
  def adcgain( self, aValue ) :
    self._again = aValue & 0x03
    self.writecontrol()

  @property
  def proxgain( self ):
    return self._pgain

  @ProxGain.setter
  def proxgain( self, aValue ) :
    self._pgain = aValue & 0x03
    self.writecontrol()

  @property
  def enabled( self ) :
    return self._pon

  @enabled.setter
  def enabled( self, aValue ) :
    self._pon = aValue
    self.writeenable()

  def proxpulse( self, aLen, aPulses ) :
    self._pplen = aLen
    self._ppulse = min(64, max(aPulses, 1)) - 1
    self.write(APDS9960._PPULSE, self._pplen << 6 | self._ppulse)

  def begin( self, aTime, aGain ) :
    if self.read(APDS9960._ID)[0] != 0xAB :
      raise Exception('Incorrect APDS9960 ID.')

    # Set default integration time and gain
    self.ADCIntegrationTime = APDS9960._DefaultIntTimeMS
    self.ADCGain = APDS9960._DefaultAGain

    self.gestureenable(False)
    self.proximityenable(False)
    self.colorenable(False)
    self.colorintenable(False)
    self.proximityintenable(False)

    self.enabled = False
    sleep_us(50)
    self.enabled = True
    sleep_us(50)

    self.gesturedimensions(APDS9960._DIMENSIONS_ALL)
    self.gesturefifothreshold(APDS9960._GFIFO_4)
    self.gesturegain(APDS9960._GGAIN_4)
    self.gestureproximitythreshold(50)
    self.resetcounts()

    self._gplen = APDS9960._GPULSE_32US
    self._gpulse = 9
    self.writegpulse()

