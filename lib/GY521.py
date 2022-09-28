
#driver for gy-521 Accelerometer
#Translated by Guy Carver from the MPU6050 sample code.

import pyb

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

class accel(object) :
  """gy-521 Accelerometer."""

  _ADDRESS_LOW = const(0x68)  #address pin low (GND), default for InvenSense evaluation board
  _ADDRESS_HIGH = const(0x69) #address pin high (VCC)

#  _RA_XG_OFFS_TC     = const(0x00) #[7] PWR_MODE, [6:1] XG_OFFS_TC, [0] OTP_BNK_VLD
#  _RA_YG_OFFS_TC     = const(0x01) #[7] PWR_MODE, [6:1] YG_OFFS_TC, [0] OTP_BNK_VLD
#  _RA_ZG_OFFS_TC     = const(0x02) #[7] PWR_MODE, [6:1] ZG_OFFS_TC, [0] OTP_BNK_VLD
#  _RA_X_FINE_GAIN    = const(0x03) #[7:0] X_FINE_GAIN
#  _RA_Y_FINE_GAIN    = const(0x04) #[7:0] Y_FINE_GAIN
#  _RA_Z_FINE_GAIN    = const(0x05) #[7:0] Z_FINE_GAIN
#  _RA_XA_OFFS_H      = const(0x06) #[15:0] XA_OFFS
#  _RA_XA_OFFS_L_TC   = const(0x07)
#  _RA_YA_OFFS_H      = const(0x08) #[15:0] YA_OFFS
#  _RA_YA_OFFS_L_TC   = const(0x09)
#  _RA_ZA_OFFS_H      = const(0x0A) #[15:0] ZA_OFFS
#  _RA_ZA_OFFS_L_TC   = const(0x0B)
#  _RA_XG_OFFS_USRH   = const(0x13) #[15:0] XG_OFFS_USR
#  _RA_XG_OFFS_USRL   = const(0x14)
#  _RA_YG_OFFS_USRH   = const(0x15) #[15:0] YG_OFFS_USR
#  _RA_YG_OFFS_USRL   = const(0x16)
#  _RA_ZG_OFFS_USRH   = const(0x17) #[15:0] ZG_OFFS_USR
#  _RA_ZG_OFFS_USRL   = const(0x18)
  _RA_SMPLRT_DIV     = const(0x19)
  _RA_CONFIG         = const(0x1A)
  _RA_GYRO_CONFIG    = const(0x1B)
  _RA_ACCEL_CONFIG   = const(0x1C)
  _RA_FF_THR         = const(0x1D)
  _RA_FF_DUR         = const(0x1E)
  _RA_MOT_THR        = const(0x1F)
  _RA_MOT_DUR        = const(0x20)
  _RA_ZRMOT_THR      = const(0x21)
  _RA_ZRMOT_DUR      = const(0x22)
  _RA_FIFO_EN        = const(0x23)
  _RA_I2C_MST_CTRL   = const(0x24)
#  _RA_I2C_SLV0_ADDR  = const(0x25)
#  _RA_I2C_SLV0_REG   = const(0x26)
#  _RA_I2C_SLV0_CTRL  = const(0x27)
#  _RA_I2C_SLV1_ADDR  = const(0x28)
#  _RA_I2C_SLV1_REG   = const(0x29)
#  _RA_I2C_SLV1_CTRL  = const(0x2A)
#  _RA_I2C_SLV2_ADDR  = const(0x2B)
#  _RA_I2C_SLV2_REG   = const(0x2C)
#  _RA_I2C_SLV2_CTRL  = const(0x2D)
#  _RA_I2C_SLV3_ADDR  = const(0x2E)
#  _RA_I2C_SLV3_REG   = const(0x2F)
#  _RA_I2C_SLV3_CTRL  = const(0x30)
#  _RA_I2C_SLV4_ADDR  = const(0x31)
#  _RA_I2C_SLV4_REG   = const(0x32)
#  _RA_I2C_SLV4_DO    = const(0x33)
#  _RA_I2C_SLV4_CTRL  = const(0x34)
#  _RA_I2C_SLV4_DI    = const(0x35)
#  _RA_I2C_MST_STATUS = const(0x36)
  _RA_INT_PIN_CFG    = const(0x37)
#  _RA_INT_ENABLE     = const(0x38)
#  _RA_DMP_INT_STATUS = const(0x39)
#  _RA_INT_STATUS     = const(0x3A)
  _RA_ACCEL_XOUT_H   = const(0x3B)
#  _RA_ACCEL_XOUT_L   = const(0x3C)
#  _RA_ACCEL_YOUT_H   = const(0x3D)
#  _RA_ACCEL_YOUT_L   = const(0x3E)
#  _RA_ACCEL_ZOUT_H   = const(0x3F)
#  _RA_ACCEL_ZOUT_L   = const(0x40)
#  _RA_TEMP_OUT_H     = const(0x41)
#  _RA_TEMP_OUT_L     = const(0x42)
  _RA_GYRO_XOUT_H    = const(0x43)
#  _RA_GYRO_XOUT_L    = const(0x44)
#  _RA_GYRO_YOUT_H    = const(0x45)
#  _RA_GYRO_YOUT_L    = const(0x46)
#  _RA_GYRO_ZOUT_H    = const(0x47)
#  _RA_GYRO_ZOUT_L    = const(0x48)
#  _RA_EXT_SENS_DATA_00 = const(0x49)
#  _RA_EXT_SENS_DATA_01 = const(0x4A)
#  _RA_EXT_SENS_DATA_02 = const(0x4B)
#  _RA_EXT_SENS_DATA_03 = const(0x4C)
#  _RA_EXT_SENS_DATA_04 = const(0x4D)
#  _RA_EXT_SENS_DATA_05 = const(0x4E)
#  _RA_EXT_SENS_DATA_06 = const(0x4F)
#  _RA_EXT_SENS_DATA_07 = const(0x50)
#  _RA_EXT_SENS_DATA_08 = const(0x51)
#  _RA_EXT_SENS_DATA_09 = const(0x52)
#  _RA_EXT_SENS_DATA_10 = const(0x53)
#  _RA_EXT_SENS_DATA_11 = const(0x54)
#  _RA_EXT_SENS_DATA_12 = const(0x55)
#  _RA_EXT_SENS_DATA_13 = const(0x56)
#  _RA_EXT_SENS_DATA_14 = const(0x57)
#  _RA_EXT_SENS_DATA_15 = const(0x58)
#  _RA_EXT_SENS_DATA_16 = const(0x59)
#  _RA_EXT_SENS_DATA_17 = const(0x5A)
#  _RA_EXT_SENS_DATA_18 = const(0x5B)
#  _RA_EXT_SENS_DATA_19 = const(0x5C)
#  _RA_EXT_SENS_DATA_20 = const(0x5D)
#  _RA_EXT_SENS_DATA_21 = const(0x5E)
#  _RA_EXT_SENS_DATA_22 = const(0x5F)
#  _RA_EXT_SENS_DATA_23 = const(0x60)
#  _RA_MOT_DETECT_STATUS = const(0x61)
#  _RA_I2C_SLV0_DO     = const(0x63)
#  _RA_I2C_SLV1_DO     = const(0x64)
#  _RA_I2C_SLV2_DO     = const(0x65)
#  _RA_I2C_SLV3_DO     = const(0x66)
#  _RA_I2C_MST_DELAY_CTRL = const(0x67)
#  _RA_SIGNAL_PATH_RESET  = const(0x68)
#  _RA_MOT_DETECT_CTRL    = const(0x69)
  _RA_USER_CTRL       = const(0x6A)
  _RA_PWR_MGMT_1      = const(0x6B)
#  _RA_PWR_MGMT_2      = const(0x6C)
#  _RA_BANK_SEL        = const(0x6D)
#  _RA_MEM_START_ADDR  = const(0x6E)
#  _RA_MEM_R_W         = const(0x6F)
#  _RA_DMP_CFG_1       = const(0x70)
#  _RA_DMP_CFG_2       = const(0x71)
#  _RA_FIFO_COUNTH     = const(0x72)
#  _RA_FIFO_COUNTL     = const(0x73)
#  _RA_FIFO_R_W        = const(0x74)
#  _RA_WHO_AM_I        = const(0x75)

  #Value Location data.
  #Following are the bytes describing the data packed into each 8 bit value on the chip.
  #Nibble 1 = position, 0 = bits
  #NOTE: Commented out currently unused locations.

#  _TC_OTP_BNK_VLD = const(0x01)
#  _TC_OFFSET      = const(0x16)
#  _TC_PWR_MODE    = const(0x71)

  _CFG_DLPF_CFG     = const(0x03)
#  _CFG_EXT_SYNC_SET = const(0x33)

  _GCONFIG_FS_SEL = const(0x32)

#  _ACONFIG_ACCEL_HPF = const(0x03)
  _ACONFIG_AFS_SEL   = const(0x32)
#  _ACONFIG_ZA_ST     = const(0x51)
#  _ACONFIG_YA_ST     = const(0x61)
#  _ACONFIG_XA_ST     = const(0x71)

#  _SLV0_FIFO_EN  = const(0X01)
#  _SLV1_FIFO_EN  = const(0X11)
#  _SLV2_FIFO_EN  = const(0X21)
  _ACCEL_FIFO_EN = const(0X31)
  _ZG_FIFO_EN    = const(0X41)
  _YG_FIFO_EN    = const(0X51)
  _XG_FIFO_EN    = const(0X61)
  _TEMP_FIFO_EN  = const(0X71)

  _I2C_MST_CLK   = const(0X04)
#  _I2C_MST_P_NSR = const(0X41)
#  _SLV_3_FIFO_EN = const(0X51)
#  _WAIT_FOR_ES   = const(0X61)
#  _MULT_MST_EN   = const(0X71)

#  _I2C_SLV_LEN     = const(0X04)
#  _I2C_SLV_GRP     = const(0X41)
#  _I2C_SLV_REG_DIS = const(0X51)
#  _I2C_SLV_BYTE_SW = const(0X61)
#  _I2C_SLV_EN      = const(0X71)

#  _I2C_SLV_ADDR    = const(0X07)
#  _I2C_SLV_RW      = const(0X71)

#  _I2C_SLV4_MST_DLY = const(0X05)
#  _I2C_SLV4_REG_DIS = const(0X51)
#  _I2C_SLV4_INT_EN  = const(0X61)
#  _I2C_SLV4_EN      = const(0X71)

#  _I2C_SLV4_ADDR    = const(0X07)
#  _I2C_SLV4_RW      = const(0X71)

#  _MST_I2C_SLV0_NACK = const(0X01)
#  _MST_I2C_SLV1_NACK = const(0X11)
#  _MST_I2C_SLV2_NACK = const(0X21)
#  _MST_I2C_SLV3_NACK = const(0X31)
#  _MST_I2C_SLV4_NACK = const(0X41)
#  _MST_I2C_LOST_ARB  = const(0X51)
#  _MST_I2C_SLV4_DONE = const(0X61)
#  _MST_PASS_THROUGH  = const(0X71)

#  _INTERRUPT_DATA_RDY    = const(0X01)
#  _INTERRUPT_DMP_INT     = const(0X11)
#  _INTERRUPT_PLL_RDY_INT = const(0X21)
#  _INTERRUPT_I2C_MST_INT = const(0X31)
#  _INTERRUPT_FIFO_OFLOW  = const(0X41)
#  _INTERRUPT_ZMOT        = const(0X51)
#  _INTERRUPT_MOT         = const(0X61)
#  _INTERRUPT_FF          = const(0X71)

  # TODO: figure out what these actually do
  # UMPL source code is not very obivous
#  _DMPINT_0 = const(0X01)
#  _DMPINT_1 = const(0X11)
#  _DMPINT_2 = const(0X21)
#  _DMPINT_3 = const(0X31)
#  _DMPINT_4 = const(0X41)
#  _DMPINT_5 = const(0X51)

#  _MOTION_MOT_ZRMOT = const(0X01)
#  _MOTION_MOT_ZPOS  = const(0X21)
#  _MOTION_MOT_ZNEG  = const(0X31)
#  _MOTION_MOT_YPOS  = const(0X41)
#  _MOTION_MOT_YNEG  = const(0X51)
#  _MOTION_MOT_XPOS  = const(0X61)
#  _MOTION_MOT_XNEG  = const(0X71)

#  _DELAYCTRL_I2C_SLV0_DLY_EN = const(0X01)
#  _DELAYCTRL_I2C_SLV1_DLY_EN = const(0X11)
#  _DELAYCTRL_I2C_SLV2_DLY_EN = const(0X21)
#  _DELAYCTRL_I2C_SLV3_DLY_EN = const(0X31)
#  _DELAYCTRL_I2C_SLV4_DLY_EN = const(0X41)
#  _DELAYCTRL_DELAY_ES_SHADOW = const(0X71)

#  _PATHRESET_TEMP_RESET  = const(0X01)
#  _PATHRESET_ACCEL_RESET = const(0X11)
#  _PATHRESET_GYRO_RESET  = const(0X21)

#  _DETECT_MOT_COUNT      = const(0X02)
#  _DETECT_FF_COUNT       = const(0X22)
#  _DETECT_ACCEL_ON_DELAY = const(0X42)

#  _INTCFG_CLKOUT_EN       = const(0X01)
#  _INTCFG_I2C_BYPASS_EN   = const(0X11)
#  _INTCFG_FSYNC_INT_EN    = const(0X21)
#  _INTCFG_FSYNC_INT_LEVEL = const(0X31)
  _INTCFG_INT_RD_CLEAR    = const(0X41)
  _INTCFG_LATCH_INT_EN    = const(0X51)
  _INTCFG_INT_OPEN        = const(0X61)
  _INTCFG_INT_LEVEL       = const(0X71)

#  _USERCTRL_SIG_COND_RESET = const(0X01)
#  _USERCTRL_I2C_MST_RESET  = const(0X11)
#  _USERCTRL_FIFO_RESET     = const(0X21)
#  _USERCTRL_DMP_RESET      = const(0X31)
#  _USERCTRL_I2C_IF_DIS     = const(0X41)
#  _USERCTRL_I2C_MST_EN     = const(0X51)
  _USERCTRL_FIFO_EN        = const(0X61)
#  _USERCTRL_DMP_EN         = const(0X71)

  _PWR1_CLKSEL       = const(0X03)
#  _PWR1_TEMP_DIS     = const(0X31)
#  _PWR1_CYCLE        = const(0X51)
  _PWR1_SLEEP        = const(0X61)
  _PWR1_DEVICE_RESET = const(0X71)

#  _PWR2_STBY_ZG      = const(0X01)
#  _PWR2_STBY_YG      = const(0X11)
#  _PWR2_STBY_XG      = const(0X21)
#  _PWR2_STBY_ZA      = const(0X31)
#  _PWR2_STBY_YA      = const(0X41)
#  _PWR2_STBY_XA      = const(0X51)
#  _PWR2_LP_WAKE_CTRL = const(0X62)

#  _BANKSEL_MEM_SEL       = const(0X05)
#  _BANKSEL_CFG_USER_BANK = const(0X51)
#  _BANKSEL_PRFTCH_EN     = const(0X61)

#  _WHO_AM_I = const(0X06)

#Values, not currently in use.

#  _DLPF_BW_256 = const(0)
#  _DLPF_BW_188 = const(1)
#  _DLPF_BW_98  = const(2)
#  _DLPF_BW_42  = const(3)
#  _DLPF_BW_20  = const(4)
#  _DLPF_BW_10  = const(5)
#  _DLPF_BW_5   = const(6)

#  _DHPF_RESET = const(0)
#  _DHPF_5     = const(1)
#  _DHPF_2P5   = const(2)
#  _DHPF_1P25  = const(3)
#  _DHPF_0P63  = const(4)
#  _DHPF_HOLD  = const(7)

  _GYRO_FS_250  = const(0)
#  _GYRO_FS_500  = const(1)
#  _GYRO_FS_1000 = const(2)
#  _GYRO_FS_2000 = const(3)
#
  _ACCEL_FS_2  = const(0)
#  _ACCEL_FS_4  = const(1)
#  _ACCEL_FS_8  = const(2)
#  _ACCEL_FS_16 = const(3)
#
#
#  _CLOCK_DIV_348 = const(0x0)
#  _CLOCK_DIV_333 = const(0x1)
#  _CLOCK_DIV_320 = const(0x2)
#  _CLOCK_DIV_308 = const(0x3)
#  _CLOCK_DIV_296 = const(0x4)
#  _CLOCK_DIV_286 = const(0x5)
#  _CLOCK_DIV_276 = const(0x6)
#  _CLOCK_DIV_267 = const(0x7)
#  _CLOCK_DIV_258 = const(0x8)
#  _CLOCK_DIV_500 = const(0x9)
#  _CLOCK_DIV_471 = const(0xA)
#  _CLOCK_DIV_444 = const(0xB)
#  _CLOCK_DIV_421 = const(0xC)
#  _CLOCK_DIV_400 = const(0xD)
#  _CLOCK_DIV_381 = const(0xE)
#  _CLOCK_DIV_364 = const(0xF)
#
#  _INTMODE_ACTIVEHIGH = const(0)
#  _INTMODE_ACTIVELOW  = const(1)
#
#  _INTDRV_PUSHPULL    = const(0)
#  _INTDRV_OPENDRAIN   = const(1)
#
#  _INTLATCH_50USPULSE = const(0)
#  _INTLATCH_WAITCLEAR = const(1)
#
#  _INTCLEAR_STATUSREAD = const(0)
#  _INTCLEAR_ANYREAD    = const(1)
#
#  _DETECT_DECREMENT_RESET = const(0)
#  _DETECT_DECREMENT_1     = const(1)
#  _DETECT_DECREMENT_2     = const(2)
#  _DETECT_DECREMENT_4     = const(3)
#
#  _WAKE_FREQ_1P25     = const(0)
#  _WAKE_FREQ_2P5      = const(1)
#  _WAKE_FREQ_5        = const(2)
#  _WAKE_FREQ_10       = const(3)
#
#  _DMP_MEMORY_BANKS      = const(8)
#  _DMP_MEMORY_BANK_SIZE  = const(256)
#  _DMP_MEMORY_CHUNK_SIZE = const(16)

#  _VDDIO_LEVEL_VLOGIC = const(0)
#  _VDDIO_LEVEL_VDD    = const(1)

#  _EXT_SYNC_DISABLED     = const(0)
#  _EXT_SYNC_TEMP_OUT_L   = const(1)
#  _EXT_SYNC_GYRO_XOUT_L  = const(2)
#  _EXT_SYNC_GYRO_YOUT_L  = const(3)
#  _EXT_SYNC_GYRO_ZOUT_L  = const(4)
#  _EXT_SYNC_ACCEL_XOUT_L = const(5)
#  _EXT_SYNC_ACCEL_YOUT_L = const(6)
#  _EXT_SYNC_ACCEL_ZOUT_L = const(7)

#  _CLOCK_INTERNAL        = const(0)
  _CLOCK_PLL_XGYRO       = const(1)
#  _CLOCK_PLL_YGYRO       = const(2)
#  _CLOCK_PLL_ZGYRO       = const(3)
#  _CLOCK_PLL_EXT32K      = const(4)
#  _CLOCK_PLL_EXT19M      = const(5)
#  _CLOCK_KEEP_RESET      = const(7)

  def __init__( self, aLoc, aAddress = _ADDRESS_LOW ) :
    """aLoc I2C pin location is either 1, 'X', 2 or 'Y'.
       aAddress is either ADDRESS_LOW or ADDRESS_HIGH."""

    self._data = bytearray(1)
    self._data6 = bytearray(6)
    self._data14 = bytearray(14)
    self._address = aAddress
    self._i2c = pyb.I2C(aLoc, pyb.I2C.MASTER, baudrate = 400000)

    self.setclocksource(_CLOCK_PLL_XGYRO)
    self.setfullscalegyrorange(_GYRO_FS_250)
    self.setfullscaleaccelrange(_ACCEL_FS_2)
    self.setsleepenabled(False)

  def getrate( self ) :
    self._readdata(_RA_SMPLRT_DIV, self._data)
    return self._data[0]

  def setrate( self, aRate ) :
    self._writedata(_RA_SMPLRT_DIV, aRate)

  def getDLPF( self ) :
    return self._readbits(_RA_CONFIG, _CFG_DLPF_CFG)

  def setDLPF( self, aMode ) :
    self._writebits(_RA_CONFIG, _CFG_DLPF_CFG, aMode)

  def setclocksource( self, aSource ) :
    self._writebits(_RA_PWR_MGMT_1, _PWR1_CLKSEL, aSource)

  def getfullscalegyrorange( self ) :
    return self._readbits(_RA_GYRO_CONFIG, _GCONFIG_FS_SEL)

  def setfullscalegyrorange( self, aRange ) :
    self._writebits(_RA_GYRO_CONFIG, _GCONFIG_FS_SEL, aRange)

  def getfullscaleaccelrange( self ) :
    self._readbits(_RA_ACCEL_CONFIG, _ACONFIG_AFS_SEL)

  def setfullscaleaccelrange( self, aRange ) :
    self._writebits(_RA_ACCEL_CONFIG, _ACONFIG_AFS_SEL, aRange)

  def getsleepenabled( self ) :
    self._readbits(_RA_PWR_MGMT_1, _PWR1_SLEEP)

  def setsleepenabled( self, aTF ) :
    self._writebits(_RA_PWR_MGMT_1, _PWR1_SLEEP, aTF)

  def getfreefalldetectionthreshold( self ) :
    self._readdata(_RA_FF_THR, self._data)
    return self._data[0]

  def setfreefalldetectionthreshold( self, aValue ) :
    self._writedata(_RA_FF_THR, aValue)

  def getfreefalldetectionduration( self ) :
    self._readdata(_RA_FF_DUR, self._data)
    return self._data[0]

  def setfreefalldetectionduration( self, aValue ) :
    self._writedata(_RA_FF_DUR, aValue)

  def getmotiondetectionthreshold( self ) :
    self._readdata(_RA_MOT_THR, self._data)
    return self._data[0]

  def setmotiondetectionthreshold( self, aValue ) :
    self._writedata(_RA_MOT_THR, aValue)

  def getmotiondetectionduration( self ) :
    self._readdata(_RA_MOT_DUR, self._data)
    return self._data[0]

  def setmotiondetectionduration( self, aValue ) :
    self._writedata(_RA_MOT_DUR, aValue)

  def getzeromotiondetectionthreshold( self ) :
    self._readdata(_RA_ZRMOT_THR, self._data)
    return self._data[0]

  def setzeromotiondetectionthreshold( self, aValue ) :
    self._writedata(_RA_ZRMOT_THR, aValue)

  def getzeromotiondetectionduration( self ) :
    self._readdata(_RA_ZRMOT_DUR, self._data)
    return self._data[0]

  def setzeromotiondetectionduration( self, aValue ) :
    self._writedata(_RA_ZRMOT_DUR, aValue)

  def getFIFOenabled( self ) :
    return self._readbits(_RA_USER_CTRL, _USERCTRL_FIFO_EN)

  def setFIFOenabled( self, aTF ) :
    self._writebits(_RA_USER_CTRL, _USERCTRL_FIFO_EN, aTF)

  def gettempFIFOenabled( self ) :
    return self._readbits(_RA_FIFO_EN, _TEMP_FIFO_EN)

  def settempFIFFOenabled( self, aTF ) :
    self._writebits(_RA_FIFO_EN, _TEMP_FIFO_EN, aTF)

  def getxgyroFIFOenabled( self ) :
    return self._readbits(_RA_FIFO_EN, _XG_FIFO_EN)

  def setxgyroFIFOenabled( self, aTF ) :
    self._writebits(_RA_FIFO_EN, _XG_FIFO_EN, aTF)

  def getygyroFIFOenabled( self ) :
    return self._readbits(_RA_FIFO_EN, _YG_FIFO_EN)

  def setygyroFIFOenabled( self, aTF ) :
    self._writebits(_RA_FIFO_EN, _YG_FIFO_EN, aTF)

  def getzgyroFIFOenabled( self ) :
    return self._readbits(_RA_FIFO_EN, _ZG_FIFO_EN)

  def setzgyroFIFOenabled( self, aTF ) :
    self._writebits(_RA_FIFO_EN, _ZG_FIFO_EN, aTF)

  def getaccelFIFOenabled( self ) :
    return self._readbits(_RA_FIFO_EN, _ACCEL_FIFO_EN)

  def setaccelFIFOenabled( self, aTF ) :
    self._writebits(_RA_FIFO_EN, _ACCEL_FIFO_EN, aTF)

  def getmasterclockspeed( self ) :
    return self._readbits(_RA_I2C_MST_CTRL, _I2C_MST_CLK)

  def setmasterclockspeed( self, aValue ) :
    self._writebits(_RA_I2C_MST_CTRL, _I2C_MST_CLK, aValue)

  def getinterruptmode( self ) :
    return self._readbits(_RA_INT_PIN_CFG, _INTCFG_INT_LEVEL)

  def setinterruptmode( self, aValue ) :
    self._writebits(_RA_INT_PIN_CFG, _INTCFG_INT_LEVEL, aValue)

  def getinterruptdrive( self ) :
    return self._readbits(_RA_INT_PIN_CFG, _INTCFG_INT_OPEN)

  def setinterruptdrive( self, aValue ) :
    self._writebits(_RA_INT_PIN_CFG, _INTCFG_INT_OPEN, aValue)

  def getinterruptlatch( self ) :
    return self._readbits(_RA_INT_PIN_CFG, _INTCFG_LATCH_INT_EN)

  def setinterruptlatch( self, aValue ) :
    self._writebits(_RA_INT_PIN_CFG, _INTCFG_LATCH_INT_EN, aValue)

  def getinterruptlatchclear( self ) :
    return self._readbits(_RA_INT_PIN_CFG, _INTCFG_INT_RD_CLEAR)

  def setinterruptlatchclear( self, aValue ) :
    self._writebits(_RA_INT_PIN_CFG, _INTCFG_INT_RD_CLEAR, aValue)

  def getacceltemprot( self ) :
    self._readdata(_RA_ACCEL_XOUT_H, self._data14)
    return [(self._data14[i] << 8) | self._data14[i + 1] for i in range(0, len(self._data14), 2)]

  def getacceleration( self ) :
    self._readdata(_RA_ACCEL_XOUT_H, self._data6)
    return [(self._data6[i] << 8) | self._data6[i + 1] for i in range(0, len(self._data6), 2)]

  def getrotation( self ) :
    self._readdata(_RA_GYRO_XOUT_H, self._data6)
    return [(self._data6[i] << 8) | self._data6[i + 1] for i in range(0, len(self._data6), 2)]

  def reset( self ) :
    self._writebits(_RA_PWR_MGMT_1, _PWR1_DEVICE_RESET, True)

  def _writedata( self, aAddress, aData ) :
    self._i2c.mem_write(aData, self._address, aAddress)

  def _readdata( self, aAddress, aData ) :
    self._i2c.mem_read(aData, self._address, aAddress)

#  @micropython.native
  def _readbits( self, aAddress, aPosBits ) :
    self._readdata(aAddress, self._data)
    return getvalue(self._data[0], aPosBits)

#  @micropython.native
  def _writebits( self, aAddress, aPosBits, aValue ) :
    self._readdata(aAddress, self._data)
    self._data[0] = setvalue(self._data[0], aPosBits, aValue)
    self._writedata(aAddress, self._data)

