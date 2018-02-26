import pyb

class apds:

  _ADDRESS = const(0x39)
  # Register addresses
  REG_ENABLE  = 0x80
  REG_ATIME   = 0x81
  REG_WTIME   = 0x83
  REG_AILTL   = 0x84
  REG_AILTH   = 0x85
  REG_AIHTL   = 0x86
  REG_AIHTH   = 0x87
  REG_PILT    = 0x89
  REG_PIHT    = 0x8B
  REG_PERS    = 0x8C
  REG_CONFIG1 = 0x8D
  REG_PPULSE  = 0x8E
  REG_CONTROL = 0x8F
  REG_CONFIG2 = 0x90
  REG_ID      = 0x92
  REG_STATUS  = 0x93
  REG_CDATAL  = 0x94
  REG_CDATAH  = 0x95
  REG_RDATAL  = 0x96
  REG_RDATAH  = 0x97
  REG_GDATAL  = 0x98
  REG_GDATAH  = 0x99
  REG_BDATAL  = 0x9A
  REG_BDATAH  = 0x9B
  REG_PDATA   = 0x9C
  REG_POFFSET_UR  = 0x9D
  REG_POFFSET_DL  = 0x9E
  REG_CONFIG3 = 0x9F
  REG_GPENTH  = 0xA0
  REG_GEXTH   = 0xA1
  REG_GCONF1  = 0xA2
  REG_GCONF2  = 0xA3
  REG_GOFFSET_U   = 0xA4
  REG_GOFFSET_D   = 0xA5
  REG_GOFFSET_L   = 0xA7
  REG_GOFFSET_R   = 0xA9
  REG_GPULSE  = 0xA6
  REG_GCONF3  = 0xAA
  REG_GCONF4  = 0xAB
  REG_GFLVL   = 0xAE
  REG_GSTATUS = 0xAF
  REG_IFORCE  = 0xE4
  REG_PICLEAR = 0xE5
  REG_CICLEAR = 0xE6
  REG_AICLEAR = 0xE7
  REG_GFIFO_U = 0xFC
  REG_GFIFO_D = 0xFD
  REG_GFIFO_L = 0xFE
  REG_GFIFO_R = 0xFF
  # Enable register bits
  ENABLE_GEN  = 0b01000000    # Gesture enable
  ENABLE_PIEN = 0b00100000    # Proximity Interrupt Enable
  ENABLE_AIEN = 0b00010000    # ALS Interrupt Enable
  ENABLE_WEN  = 0b00001000    # Wait Enable
  ENABLE_PEN  = 0b00000100    # Proximity Enable
  ENABLE_AEN  = 0b00000010    # ALS Enable
  ENABLE_PON  = 0b00000001    # Power ON
  # Congiguration register 2
  CONFIG2_LEDBOOST_150 = (1 << 4) # LED boost 150%
  CONFIG2_LEDBOOST_200 = (2 << 4) # LED boost 200%
  CONFIG2_LEDBOOST_300 = (3 << 4) # LED boost 300%
  GCONFIG3_GDIMS_LR = 2
  GCONFIG3_GDIMS_UD = 1 # 01
  GCONFIG4_GMODE = 1 # Gesture mode

  def __init__( self, aLoc ) :
    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)
    self._b1 = bytearray(1)
    self.init()

  def read( self, aLoc ) :
    """Read 8 bit value and return."""
    self.i2c.mem_read(self._b1, _ADDRESS, aLoc)
#    print('Read {:02x} from {:02x}.'.format(self._b1[0], aLoc))
    return self._b1[0]

  def write( self, aLoc, aVal ) :
    """Write 8 bit value to given address.  aVal may be an int buffer."""
    self.i2c.mem_write(aVal, _ADDRESS, aLoc)
#    print('write {:02x} to {:02x}.'.format(aVal, aLoc))

  def init( self ) :
    if self.get_device_id() != 0xAB :
      return False

    self.write(self.REG_ENABLE, self.ENABLE_PON | self.ENABLE_PEN | self.ENABLE_GEN)
    self.write(self.REG_CONFIG2, self.CONFIG2_LEDBOOST_300)
    self.write(self.REG_GPENTH, 10)
    self.write(self.REG_GEXTH, 5)
    self.write(self.REG_GOFFSET_U, 0) #70)
    self.write(self.REG_GOFFSET_D, 0)
    self.write(self.REG_GOFFSET_L, 0) #10)
    self.write(self.REG_GOFFSET_R, 0) #34)
    self.write(self.REG_GCONF3, self.GCONFIG3_GDIMS_UD | self.GCONFIG3_GDIMS_LR)
    self.write(self.REG_GCONF4, self.GCONFIG4_GMODE)

  def get_device_id( self ) :
    return self.read(self.REG_ID)

  def readgesture( self ) :
    level = self.read(self.REG_GFLVL)
    if level == 0 :
      return # no data
    fifo_u = self.read(self.REG_GFIFO_U)
    fifo_d = self.read(self.REG_GFIFO_D)
    fifo_l = self.read(self.REG_GFIFO_L)
    fifo_r = self.read(self.REG_GFIFO_R)

    return (fifo_u, fifo_d, fifo_l, fifo_r)

