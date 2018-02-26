# MicroPython apds9960 motion detection device driver.

#todo: Have a mix of styles here.  Some use properties for setters while others use functions.

import pyb
from utime import *

class apds(object) :

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

  _PON = const(0x01)
  _AEN = const(0x02)
  _PEN = const(0x04)
  _WEN = const(0x08)
  _AIEN = const(0x10)
  _PIEN = const(0x20)
  _GEN = const(0x40)

  _GVALID = const(0x01)

  _THRESHOLD_OUT = const(10)
  _SENSITIVITY_1 = const(50)
  _SENSITIVITY_2 = const(20)

  _ERROR = const(0xFF)

  #Device IDs
  _ID_1 = const(0xAB)
  _ID_2 = const(0x9C)

  _FIFO_PAUSE_TIME = const(30) # Wait period (ms) between FIFO reads

  #P Gain
  _PGAIN_1 = const(0)  #1x gain
  _PGAIN_2 = const(1)  #2x gain
  _PGAIN_4 = const(2)  #4x gain
  _PGAIN_8 = const(3)  #8x gain

    #LED Drive
  _LEDDRIVE_100MA  = const(0)  #100mA
  _LEDDRIVE_50MA   = const(1)  #50mA
  _LEDDRIVE_25MA   = const(2)  #25mA
  _LEDDRIVE_12_5MA = const(3)  #12.5mA

  #LED Boost
  _LEDBOOST_100 = const(0)
  _LEDBOOST_150 = const(1)
  _LEDBOOST_200 = const(2)
  _LEDBOOST_300 = const(3)

  #G Gain
  _GGAIN_1  = const(0)
  _GGAIN_2  = const(1)
  _GGAIN_4  = const(2)
  _GGAIN_8  = const(3)

  #G Gain
  _AGAIN_1  = const(0)
  _AGAIN_4  = const(1)
  _AGAIN_16 = const(2)
  _AGAIN_64 = const(3)

  #Following are the bytes describing the data packed into each 8 bit value on the chip.
  #Nibble 1 = position, 0 = bits

  _POWER             = const(0)
  _AMBIENT_LIGHT     = const(1)
  _PROXIMITY         = const(2)
  _WAIT              = const(3)
  _AMBIENT_LIGHT_INT = const(4)
  _PROXIMITY_INT     = const(5)
  _GESTURE           = const(6)
  _ALL               = const(7)

# Gesture wait time values
  GWTIME_0MS    = const(0)
  GWTIME_2_8MS  = const(1)
  GWTIME_5_6MS  = const(2)
  GWTIME_8_4MS  = const(3)
  GWTIME_14_0MS = const(4)
  GWTIME_22_4MS = const(5)
  GWTIME_30_8MS = const(6)
  GWTIME_39_2MS = const(7)

  _DEFAULT_ATIME = const(219) # 103ms
  _DEFAULT_WTIME = const(246) # 27ms
  _DEFAULT_PROX_PPULSE = const(0x87) # 16us, 8 pulses
  _DEFAULT_GESTURE_PPULSE = const(0x89) # 16us, 10 pulses
  _DEFAULT_POFFSET_UR = const(0) # 0 offset
  _DEFAULT_POFFSET_DL = const(0) # 0 offset
  _DEFAULT_CONFIG1 = const(0x60) # No 12x wait (WTIME) factor
  _DEFAULT_LDRIVE = const(0) #_LED_DRIVE_100MA
  _DEFAULT_PGAIN = const(2) #_PGAIN_4
  _DEFAULT_AGAIN = const(1) #_AGAIN_4
  _DEFAULT_PILT = const(0) # Low proximity threshold
  _DEFAULT_PIHT = const(50) # High proximity threshold
  _DEFAULT_AILT = const(0xFFFF) # Force interrupt for calibration
  _DEFAULT_AIHT = const(0)
  _DEFAULT_PERS = const(0x11) # 2 consecutive prox or ALS for int.
  _DEFAULT_CONFIG2 = const(0x01) # No saturation interrupts or LED boost
  _DEFAULT_CONFIG3 = const(0) # Enable all photodiodes, no SAI
  _DEFAULT_GPENTH = const(40) # Threshold for entering gesture mode
  _DEFAULT_GEXTH = const(30) # Threshold for exiting gesture mode
  _DEFAULT_GCONF1 = const(0x40) # 4 gesture events for int., 1 for exit
  _DEFAULT_GGAIN = const(2) #_GGAIN_4
  _DEFAULT_GLDRIVE = const(0) #_LED_DRIVE_100MA
  _DEFAULT_GWTIME = const(1) #_GWTIME_2_8MS
  _DEFAULT_GOFFSET = const(0) # No offset scaling for gesture mode
  _DEFAULT_GPULSE = const(0xC9) # 32us, 10 pulses
  _DEFAULT_GCONF3 = const(0) # All photodiodes active during gesture
  _DEFAULT_GIEN = const(0) # Disable gesture interrupts

  _DIR_NONE = const(0)
  _DIR_LEFT = const(1)
  _DIR_RIGHT = const(2)
  _DIR_UP = const(3)
  _DIR_DOWN = const(4)
  _DIR_NEAR = const(5)
  _DIR_FAR = const(6)
  _DIR_ALL = const(7)

  _NA_STATE = const(0)
  _NEAR_STATE = const(1)
  _FAR_STATE = const(2)
  _ALL_STATE = const(3)

  def __init__( self, aLoc ) :
    """aLoc I2C pin location is either 1, 'X', 2 or'Y'."""
    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)

    self._ud_delta = 0
    self._lr_delta = 0
    self._ud_count  = 0
    self._lr_count  = 0
    self._near_count = 0
    self._far_count = 0
    self._state = 0
    self._motion = _DIR_NONE
    self._udata = bytearray(32)
    self._ddata = bytearray(32)
    self._ldata = bytearray(32)
    self._rdata = bytearray(32)
    self._index = 0
    self._total_gestures= 0
    self._in_threshold = 0
    self._out_threshold = 0

    self._b1 = bytearray(1)

    sleep_us(50)
    self.init()

  def read( self, aLoc ) :
    """Read 8 bit value and return."""
    self.i2c.mem_read(self._b1, _ADDRESS, aLoc)
#    print('Read {:02x} from {:02x}.'.format(self._b1[0], aLoc))
    return self._b1[0]

  def readblock( self, aLoc, aDest ) :
    return self.i2c.mem_read(aDest, _ADDRESS, aLoc)

  def write( self, aLoc, aVal ) :
    """Write 8 bit value to given address.  aVal may be an int buffer."""
    self.i2c.mem_write(aVal, _ADDRESS, aLoc)
#    print('write {:02x} to {:02x}.'.format(aVal, aLoc))

  def init( self ) :
    id = self.read(_ID)

    if id != _ID_1 and id != _ID_2 :
      raise Exception('Incorrect apds9960 ID. {}'.format(id))

    self.setmode(_ALL, False)

    self.write(_ATIME, _DEFAULT_ATIME)
    self.write(_WTIME, _DEFAULT_WTIME)
    self.write(_PPULSE, _DEFAULT_PROX_PPULSE)
    self.write(_POFFSET_UR, _DEFAULT_POFFSET_UR)
    self.write(_POFFSET_DL, _DEFAULT_POFFSET_DL)
    self.write(_CONFIG1, _DEFAULT_CONFIG1)

    self.setleddrive(_DEFAULT_LDRIVE)
    self.setproximitygain(_DEFAULT_PGAIN)
    self.setambientlightgain(_DEFAULT_AGAIN)
    self.setproxintlowthresh(_DEFAULT_PILT)
    self.setproxinthighthresh(_DEFAULT_PIHT)
    self.setlightintlowthresh(_DEFAULT_AILT)
    self.setlightinthighthresh(_DEFAULT_AIHT)

    self.write(_PERS, _DEFAULT_PERS)
    self.write(_CONFIG2, _DEFAULT_CONFIG2)
    self.write(_CONFIG3, _DEFAULT_CONFIG3)

    self.setgestureenterthresh(_DEFAULT_GPENTH)
    self.setgestureexitthresh(_DEFAULT_GEXTH)

    self.write(_GCONF1, _DEFAULT_GCONF1)

    self.setgesturegain(_DEFAULT_GGAIN)
    self.setgestureleddrive(_DEFAULT_GLDRIVE)
    self.setgesturewaittime(_DEFAULT_GWTIME)

    self.write(_GOFFSET_U, _DEFAULT_GOFFSET)
    self.write(_GOFFSET_D, _DEFAULT_GOFFSET)
    self.write(_GOFFSET_L, _DEFAULT_GOFFSET)
    self.write(_GOFFSET_R, _DEFAULT_GOFFSET)
    self.write(_GPULSE, _DEFAULT_GPULSE)
    self.write(_GCONF3, _DEFAULT_GCONF3)

    self.setgestureintenable(_DEFAULT_GIEN)

  def getmode( self ) :
    return self.read(_ENABLE)

  def setmode( self, aMode, aEnable ) :
    v = self.getmode()
    if 0 <= aMode <= 6 :
      aMode = 1 << aMode
      if aEnable :
        v |= aMode
      else:
        v &= ~aMode
    elif aMode == _ALL :
      v = 0x7F if aEnable else 0

    self.write(_ENABLE, v)

  def enablelightsensor( self, aInt ) :
    self.setambientlightgain(_DEFAULT_AGAIN)
    self.setambientlightintenable(aInt)
    self.enablepower()
    self.setmode(_AMBIENT_LIGHT, True)

  def disablelightsensor( self ) :
    self.setambientlightintenable(False)
    self.setmode(_AMBIENT_LIGHT, False)

  def enableproximitysensor( self, aInt ) :
    self.setproximitygain(_DEFAULT_PGAIN)
    self.setleddrive(_DEFAULT_LDRIVE)
    self.setproximityintenable(aInt)
    self.enablepower()
    self.setmode(_PROXIMITY, True)

  def disableproximitysensor( self ) :
    self.setproximityintenable(False)
    self.setmode(_PROXIMITY, False)

  def enablegesturesensor( self, aInt ) :
    self.resetgestureparams()
    self.write(_WTIME, 0xFF)
    self.write(_PPULSE, _DEFAULT_GESTURE_PPULSE)
    self.setledboost(_LEDBOOST_300)
    self.setgestureintenable(aInt)
    self.setgesturemode(True)
    self.enablepower()
    self.setmode(_WAIT, True)
    self.setmode(_PROXIMITY, True)
    self.setmode(_GESTURE, True)

  def disablegesturesensor( self ) :
    self.resetgestureparams()
    self.setgestureintenable(False)
    self.setgesturemode(True)
    self.setmode(_GESTURE, False)

  def isgestureavailable( self ) :
    v = self.read(_GSTATUS)
    return (v & _GVALID) != 0

  def readgesture( self ) :
    if self.isgestureavailable() and (self.getmode() & 0x41) :
      while True :
        time.sleep_us(_FIFO_PAUSE_TIME)

        gstatus = self.read(_GSTATUS)
        if (gstatus & _GVALID) == _GVALID :
          fifo_level = self.read(_GFLVL)
          if fifo_level > 0 :
            bread = self.readblock(_GFIFO_U, self._fifo_data, fifo_level * 4)

            if bread >= 4 :
              for i in range(0, bread):
                self._udata[self.index] = self._fifo_data[i]
                self._ddata[self.index] = self._fifo_data[i + 1]
                self._ldata[self.index] = self._fifo_data[i + 2]
                self._rdata[self.index] = self._fifo_data[i + 3]
                self._index += 1
                self._total_gestures += 1

              if self.processgesturedata() :
                self._index = 0
                self._total_gestures = 0
        else:
          time.sleep_us(_FIFO_PAUSE_TIME)
          self.decodegesture()
          self.resetgestureparams()
          return self._motion

    return _DIR_NONE

  def enablepower( self, aOn ) :
    self.setmode(_POWER, aOn)

  def readlight( self, aData ) :
    l = self.read(aData)
    h = self.read(aData + 1)
    return (h << 8) | l

  def readambientlight( self ) :
    return self.readlight(_CDATAL)

  def readredlight( self ) :
    return self.readlight(_RDATAL)

  def readgreenlight( self ) :
    return self.readlight(_GDATAL)

  def readbluelight( self ) :
    return self.readlight(_BDATAL)

  def readproximity( self ) :
    return self.read(_PDATA)

  def resetgestureparams( self ) :
    self._index = 0
    self._total_gestures = 0
    self._ud_delta = 0
    self._lr_delta = 0
    self._ud_count = 0
    self._lr_count = 0
    self._near_count = 0
    self._far_count = 0
    self._state = 0
    self._motion = _DIR_NONE

  def processgesturedata( self ) :
    if self._total_gestures > 4 :
      if 0 < self._total_gestures <= 32 :
        found = False
        for i in range(0, self._total_gestures) :
          u = self._udata[i]
          d = self._ddata[i]
          l = self._ldata[i]
          r = self._rdata[i]
          if u > _THRESHOLD_OUT and d > _THRESHOLD_OUT and l > _THRESHOLD_OUT and r > _THRESHOLD_OUT :
            ufirst = u
            dfirst = d
            lfirst = l
            rfirst = r
            found = True
            break
        if found :
          for i in range(self._total_gestures - 1, -1, -1) :
            u = self._udata[i]
            d = self._ddata[i]
            l = self._ldata[i]
            r = self._rdata[i]
            ulast = u
            dlast = d
            llast = l
            rlast = r
            break
      ud_ratio_first = ((ufirst - dfirst) * 100) / (ufirst + dfirst)
      lr_ratio_first = ((lfirst - rfirst) * 100) / (lfirst + rfirst)
      ud_ratio_last = ((ulast - dlast) * 100) / (ulast + dlast)
      lr_ratio_last = ((llast - rlast) * 100) / (llast + rlast)

      ud_delta = ud_ratio_last - ud_ratio_first
      lr_delta = lr_ratio_last - lr_ratio_first

      self._ud_delta += ud_delta
      self._lr_delta += lr_delta

      if self._ud_delta >= _SENSITIVITY_1 :
        self._ud_count = 1
      elif self._ud_delta <= -_SENSITIVITY_1 :
        self._ud_count = -1
      else:
        self._ud_count = 0

      if self._lr_delta >= _SENSITIVITY_1 :
        self._lr_count = 1
      elif self._lr_delta <= -_SENSITIVITY_1 :
        self._lr_count = -1
      else:
        self._lr_count = 0

      if self._ud_count == 0 and self._lr_count == 0 :
        if abs(ud_delta) < _SENSITIVITY_2 and abs(lr_delta) < _SENSITIVITY_2 :
          if ud_delta == 0 and lr_delta == 0 :
            self._near_count += 1
          elif ud_delta != 0 and lr_delta != 0 :
            self._far_count += 1

          if self._near_count >= 10 and self._far_count >= 2 :
            if ud_delta == 0 and lr_delta == 0 :
              self._state = _NEAR_STATE
            elif ud_delta != 0 and lr_delta != 0 :
              self._state = _FAR_STATE

            return True
      else:
        if abs(ud_delta) < _SENSITIVITY_2 and abs(lr_delta) < _SENSITIVITY_2 :
          if ud_delta == 0 and lr_delta == 0 :
            self._near_count += 1

          if self._near_count >= 10 :
            self._ud_count = 0
            self._lr_count = 0
            self._ud_delta = 0
            self._lr_delta = 0

    return False

  def decodegesture( self ) :
    if self._state == _NEAR_STATE :
      self._motion = _DIR_NEAR
      return True
    elif self._state == _FAR_STATE :
      self._motion = _DIR_FAR
      return True

    if self._ud_count == -1 and self._lr_count == 0 :
      self._motion = _DIR_UP
    elif self._ud_count == 1 and self._lr_count == 0 :
      self._motion = _DIR_DOWN
    elif self._ud_count == 0 and self._lr_count == 1 :
      self._motion == _DIR_RIGHT
    elif self._ud_count == 0 and self._lr_count == -1 :
      self._motion == _DIR_LEFT
    elif self._ud_count == -1 and self._lr_count == 1 :
      if abs(self._ud_delta) > abs(self._lr_delta) :
        self._motion = _DIR_UP
      else:
        self._motion = _DIR_RIGHT
    elif self._ud_count == 1 and self._lr_count == -1 :
      if abs(self._ud_delta) > abs(self._lr_delta) :
        self._motion = _DIR_DOWN
      else:
        self._motion = _DIR_LEFT
    elif self._ud_count == -1 and self._lr_count == -1 :
      if abs(self._ud_delta) > abs(self._lr_delta) :
        self._motion = _DIR_UP
      else:
        self._motion = _DIR_LEFT
    elif self._ud_count == 1 and self._lr_count == 1 :
      if abs(self._ud_delta) > abs(self._lr_delta) :
        self._motion = _DIR_DOWN
      else:
        self._motion = _DIR_RIGHT
    else:
      return False

    return True

  def getproxintlowthresh( self ) :
    return self.read(_PILT)

  def setproxintlowthresh( self, aThresh ) :
    self.write(_PILT, aThresh)

  def getproxinthighthresh( self ) :
    return self._read(_PIHT)

  def setproxinthighthresh( self, aThresh ) :
    self.write(_PIHT, aThresh)

  def getleddrive( self ) :
    v = self.read(_CONTROL)
    return (v >> 6) & 0x03

  def setleddrive( self, aDrive ) :
    v = self.read(_CONTROL)
    aDrive &= 0x03
    aDrive <<= 6
    v &= 0x111111
    v |= aDrive

    self.write(_CONTROL, v)

  def getproximitygain( self ) :
    v = self.read(_CONTROL)
    return (v >> 2) & 0x03

  def setproximitygain( self, aGain ) :
    v = self.read(_CONTROL)
    aGain &= 0x03
    aGain <<= 2
    v &= 0xF3
    v |= aGain
    self.write(_CONTROL, v)

  def getambientlightgain( self ) :
    return self.read(_CONTROL) & 0x03

  def setambientlightgain( self, aGain ) :
    v = self.read(_CONTROL)
    aGain &= 0x03
    v &= 0xFC
    v |= aGain
    self.write(_CONTROL, v)

  def getledboost( self ) :
    v = self.read(_CONFIG2)
    return (v >> 4) & 0x03

  def setledboost( self, aBoost ) :
    v = self.read(_CONFIG2)

    aBoost &= 0x03
    aBoost <<= 4
    v &= 0xFC
    v |= aBoost
    self.write(_CONFIG2, v)

  def getproxgaincompenable( self ) :
    v = self.read(_CONFIG3)
    return (v >> 5) & 0x01

  def setproxgaincompenable( self, aEnable ) :
    v = self.read(_CONFIG3)

    aEnable &= 0x01
    aEnable <<= 5
    v &= 0xDF
    v |= aEnable

    self.write(_CONFIG3, v)

  def setgestureenterthresh( self, aThresh ) :
    self.write(_GPENTH, aThresh)

  def setgestureexitthresh( self, aThresh ) :
    self.write(_GEXTH, aThresh)

  def setgesturegain( self, aGain ) :
    v = self.read(_GCONF2)

    aGain &= 0x03
    aGain <<= 5
    v &= 0x9F
    v |= aGain

    self.write(_GCONF2, v)

  def setgestureleddrive( self, aDrive ) :
    v = self.read(_GCONF2)

    aDrive &= 0x03
    aDrive <<= 3
    v &= 0xE7
    v |= aDrive

    self.write(_GCONF2, v)

  def setgesturewaittime( self, aTime ) :
    v = self.read(_GCONF2)

    aTime &= 0x07
    v &= 0xF8
    v |= aTime

    self.write(_GCONF2, v)

  def setlightintlowthresh( self, aThresh ) :
    vl = aThresh & 0xFF
    vh = (aThresh >> 8) & 0xFF

    self.write(_AILTL, vl)
    self.write(_AILTH, vh)

  def setlightinthighthresh( self, aThresh ) :
    vl = aThresh & 0xFF
    vh = (aThresh >> 8) & 0xFF

    self.write(_AIHTL, vl)
    self.write(_AIHTH, vh)

  def setambientlightintenable( self, aEnable ) :
    v = self.read(_ENABLE)

    aEnable &= 0x01
    aEnable <<= 4
    v &= 0xEF
    v |= aEnable

    self.write(_ENABLE, v)

  def setproximityintenable( self, aEnable ) :
    v = self.read(_ENABLE)

    aEnable &= 0x01
    aEnable <<= 5
    v &= 0xDF
    v |= aEnable

    self.write(_ENABLE, v)

  def setgestureintenable( self, aEnable ) :
    v = self.read(_GCONF4)

    aEnable &= 0x01
    aEnable <<= 1
    v &= 0xFD
    v |= aEnable

    self.write(_GCONF4, v)

  def setgesturemode( self, aMode ) :
    v = self.read(_GCONF4)

    aMode &= 0x01
    v &= 0xFE
    v |= aMode

    self.write(_GCONF4, v)

