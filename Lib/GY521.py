#driver for GY-521 Accelerometer
#Translated by Guy Carver from the MPU6050 sample code.

import pyb

ADDRESS_LOW = 0x68  #address pin low (GND), default for InvenSense evaluation board
ADDRESS_HIGH = 0x69 #address pin high (VCC)

RA_XG_OFFS_TC     = 0x00 //[7] PWR_MODE, [6:1] XG_OFFS_TC, [0] OTP_BNK_VLD
RA_YG_OFFS_TC     = 0x01 //[7] PWR_MODE, [6:1] YG_OFFS_TC, [0] OTP_BNK_VLD
RA_ZG_OFFS_TC     = 0x02 //[7] PWR_MODE, [6:1] ZG_OFFS_TC, [0] OTP_BNK_VLD
RA_X_FINE_GAIN    = 0x03 //[7:0] X_FINE_GAIN
RA_Y_FINE_GAIN    = 0x04 //[7:0] Y_FINE_GAIN
RA_Z_FINE_GAIN    = 0x05 //[7:0] Z_FINE_GAIN
RA_XA_OFFS_H      = 0x06 //[15:0] XA_OFFS
RA_XA_OFFS_L_TC   = 0x07
RA_YA_OFFS_H      = 0x08 //[15:0] YA_OFFS
RA_YA_OFFS_L_TC   = 0x09
RA_ZA_OFFS_H      = 0x0A //[15:0] ZA_OFFS
RA_ZA_OFFS_L_TC   = 0x0B
RA_XG_OFFS_USRH   = 0x13 //[15:0] XG_OFFS_USR
RA_XG_OFFS_USRL   = 0x14
RA_YG_OFFS_USRH   = 0x15 //[15:0] YG_OFFS_USR
RA_YG_OFFS_USRL   = 0x16
RA_ZG_OFFS_USRH   = 0x17 //[15:0] ZG_OFFS_USR
RA_ZG_OFFS_USRL   = 0x18
RA_SMPLRT_DIV     = 0x19
RA_CONFIG         = 0x1A
RA_GYRO_CONFIG    = 0x1B
RA_ACCEL_CONFIG   = 0x1C
RA_FF_THR         = 0x1D
RA_FF_DUR         = 0x1E
RA_MOT_THR        = 0x1F
RA_MOT_DUR        = 0x20
RA_ZRMOT_THR      = 0x21
RA_ZRMOT_DUR      = 0x22
RA_FIFO_EN        = 0x23
RA_I2C_MST_CTRL   = 0x24
RA_I2C_SLV0_ADDR  = 0x25
RA_I2C_SLV0_REG   = 0x26
RA_I2C_SLV0_CTRL  = 0x27
RA_I2C_SLV1_ADDR  = 0x28
RA_I2C_SLV1_REG   = 0x29
RA_I2C_SLV1_CTRL  = 0x2A
RA_I2C_SLV2_ADDR  = 0x2B
RA_I2C_SLV2_REG   = 0x2C
RA_I2C_SLV2_CTRL  = 0x2D
RA_I2C_SLV3_ADDR  = 0x2E
RA_I2C_SLV3_REG   = 0x2F
RA_I2C_SLV3_CTRL  = 0x30
RA_I2C_SLV4_ADDR  = 0x31
RA_I2C_SLV4_REG   = 0x32
RA_I2C_SLV4_DO    = 0x33
RA_I2C_SLV4_CTRL  = 0x34
RA_I2C_SLV4_DI    = 0x35
RA_I2C_MST_STATUS = 0x36
RA_INT_PIN_CFG    = 0x37
RA_INT_ENABLE     = 0x38
RA_DMP_INT_STATUS = 0x39
RA_INT_STATUS     = 0x3A
RA_ACCEL_XOUT_H   = 0x3B
RA_ACCEL_XOUT_L   = 0x3C
RA_ACCEL_YOUT_H   = 0x3D
RA_ACCEL_YOUT_L   = 0x3E
RA_ACCEL_ZOUT_H   = 0x3F
RA_ACCEL_ZOUT_L   = 0x40
RA_TEMP_OUT_H     = 0x41
RA_TEMP_OUT_L     = 0x42
RA_GYRO_XOUT_H    = 0x43
RA_GYRO_XOUT_L    = 0x44
RA_GYRO_YOUT_H    = 0x45
RA_GYRO_YOUT_L    = 0x46
RA_GYRO_ZOUT_H    = 0x47
RA_GYRO_ZOUT_L    = 0x48
RA_EXT_SENS_DATA_00 = 0x49
RA_EXT_SENS_DATA_01 = 0x4A
RA_EXT_SENS_DATA_02 = 0x4B
RA_EXT_SENS_DATA_03 = 0x4C
RA_EXT_SENS_DATA_04 = 0x4D
RA_EXT_SENS_DATA_05 = 0x4E
RA_EXT_SENS_DATA_06 = 0x4F
RA_EXT_SENS_DATA_07 = 0x50
RA_EXT_SENS_DATA_08 = 0x51
RA_EXT_SENS_DATA_09 = 0x52
RA_EXT_SENS_DATA_10 = 0x53
RA_EXT_SENS_DATA_11 = 0x54
RA_EXT_SENS_DATA_12 = 0x55
RA_EXT_SENS_DATA_13 = 0x56
RA_EXT_SENS_DATA_14 = 0x57
RA_EXT_SENS_DATA_15 = 0x58
RA_EXT_SENS_DATA_16 = 0x59
RA_EXT_SENS_DATA_17 = 0x5A
RA_EXT_SENS_DATA_18 = 0x5B
RA_EXT_SENS_DATA_19 = 0x5C
RA_EXT_SENS_DATA_20 = 0x5D
RA_EXT_SENS_DATA_21 = 0x5E
RA_EXT_SENS_DATA_22 = 0x5F
RA_EXT_SENS_DATA_23 = 0x60
RA_MOT_DETECT_STATUS = 0x61
RA_I2C_SLV0_DO     = 0x63
RA_I2C_SLV1_DO     = 0x64
RA_I2C_SLV2_DO     = 0x65
RA_I2C_SLV3_DO     = 0x66
RA_I2C_MST_DELAY_CTRL = 0x67
RA_SIGNAL_PATH_RESET  = 0x68
RA_MOT_DETECT_CTRL    = 0x69
RA_USER_CTRL       = 0x6A
RA_PWR_MGMT_1      = 0x6B
RA_PWR_MGMT_2      = 0x6C
RA_BANK_SEL        = 0x6D
RA_MEM_START_ADDR  = 0x6E
RA_MEM_R_W         = 0x6F
RA_DMP_CFG_1       = 0x70
RA_DMP_CFG_2       = 0x71
RA_FIFO_COUNTH     = 0x72
RA_FIFO_COUNTL     = 0x73
RA_FIFO_R_W        = 0x74
RA_WHO_AM_I        = 0x75

TC_PWR_MODE_BIT    = 7
TC_OFFSET_BIT      = 6
TC_OFFSET_LENGTH   = 6
TC_OTP_BNK_VLD_BIT = 0

VDDIO_LEVEL_VLOGIC = 0
VDDIO_LEVEL_VDD    = 1

CFG_EXT_SYNC_SET_BIT    = 5
CFG_EXT_SYNC_SET_LENGTH = 3
CFG_DLPF_CFG_BIT    = 2
CFG_DLPF_CFG_LENGTH = 3

EXT_SYNC_DISABLED     = 0x0
EXT_SYNC_TEMP_OUT_L   = 0x1
EXT_SYNC_GYRO_XOUT_L  = 0x2
EXT_SYNC_GYRO_YOUT_L  = 0x3
EXT_SYNC_GYRO_ZOUT_L  = 0x4
EXT_SYNC_ACCEL_XOUT_L = 0x5
EXT_SYNC_ACCEL_YOUT_L = 0x6
EXT_SYNC_ACCEL_ZOUT_L = 0x7

DLPF_BW_256        = 0x00
DLPF_BW_188        = 0x01
DLPF_BW_98         = 0x02
DLPF_BW_42         = 0x03
DLPF_BW_20         = 0x04
DLPF_BW_10         = 0x05
DLPF_BW_5          = 0x06

GCONFIG_FS_SEL_BIT    = 4
GCONFIG_FS_SEL_LENGTH = 2

GYRO_FS_250       = 0x00
GYRO_FS_500       = 0x01
GYRO_FS_1000      = 0x02
GYRO_FS_2000      = 0x03

ACONFIG_XA_ST_BIT        = 7
ACONFIG_YA_ST_BIT        = 6
ACONFIG_ZA_ST_BIT        = 5
ACONFIG_AFS_SEL_BIT      = 4
ACONFIG_AFS_SEL_LENGTH   = 2
ACONFIG_ACCEL_HPF_BIT    = 2
ACONFIG_ACCEL_HPF_LENGTH = 3

ACCEL_FS_2         = 0x00
ACCEL_FS_4         = 0x01
ACCEL_FS_8         = 0x02
ACCEL_FS_16        = 0x03

DHPF_RESET         = 0x00
DHPF_5             = 0x01
DHPF_2P5           = 0x02
DHPF_1P25          = 0x03
DHPF_0P63          = 0x04
DHPF_HOLD          = 0x07

TEMP_FIFO_EN_BIT   = 7
XG_FIFO_EN_BIT     = 6
YG_FIFO_EN_BIT     = 5
ZG_FIFO_EN_BIT     = 4
ACCEL_FIFO_EN_BIT  = 3
SLV2_FIFO_EN_BIT   = 2
SLV1_FIFO_EN_BIT   = 1
SLV0_FIFO_EN_BIT   = 0

MULT_MST_EN_BIT    = 7
WAIT_FOR_ES_BIT    = 6
SLV_3_FIFO_EN_BIT  = 5
I2C_MST_P_NSR_BIT  = 4
I2C_MST_CLK_BIT    = 3
I2C_MST_CLK_LENGTH = 4

CLOCK_DIV_348      = 0x0
CLOCK_DIV_333      = 0x1
CLOCK_DIV_320      = 0x2
CLOCK_DIV_308      = 0x3
CLOCK_DIV_296      = 0x4
CLOCK_DIV_286      = 0x5
CLOCK_DIV_276      = 0x6
CLOCK_DIV_267      = 0x7
CLOCK_DIV_258      = 0x8
CLOCK_DIV_500      = 0x9
CLOCK_DIV_471      = 0xA
CLOCK_DIV_444      = 0xB
CLOCK_DIV_421      = 0xC
CLOCK_DIV_400      = 0xD
CLOCK_DIV_381      = 0xE
CLOCK_DIV_364      = 0xF

I2C_SLV_RW_BIT      = 7
I2C_SLV_ADDR_BIT    = 6
I2C_SLV_ADDR_LENGTH = 7
I2C_SLV_EN_BIT      = 7
I2C_SLV_BYTE_SW_BIT = 6
I2C_SLV_REG_DIS_BIT = 5
I2C_SLV_GRP_BIT     = 4
I2C_SLV_LEN_BIT     = 3
I2C_SLV_LEN_LENGTH  = 4

I2C_SLV4_RW_BIT         = 7
I2C_SLV4_ADDR_BIT       = 6
I2C_SLV4_ADDR_LENGTH    = 7
I2C_SLV4_EN_BIT         = 7
I2C_SLV4_INT_EN_BIT     = 6
I2C_SLV4_REG_DIS_BIT    = 5
I2C_SLV4_MST_DLY_BIT    = 4
I2C_SLV4_MST_DLY_LENGTH = 5

MST_PASS_THROUGH_BIT   = 7
MST_I2C_SLV4_DONE_BIT  = 6
MST_I2C_LOST_ARB_BIT   = 5
MST_I2C_SLV4_NACK_BIT  = 4
MST_I2C_SLV3_NACK_BIT  = 3
MST_I2C_SLV2_NACK_BIT  = 2
MST_I2C_SLV1_NACK_BIT  = 1
MST_I2C_SLV0_NACK_BIT  = 0

INTCFG_INT_LEVEL_BIT       = 7
INTCFG_INT_OPEN_BIT        = 6
INTCFG_LATCH_INT_EN_BIT    = 5
INTCFG_INT_RD_CLEAR_BIT    = 4
INTCFG_FSYNC_INT_LEVEL_BIT = 3
INTCFG_FSYNC_INT_EN_BIT    = 2
INTCFG_I2C_BYPASS_EN_BIT   = 1
INTCFG_CLKOUT_EN_BIT       = 0

INTMODE_ACTIVEHIGH = 0x00
INTMODE_ACTIVELOW  = 0x01

INTDRV_PUSHPULL    = 0x00
INTDRV_OPENDRAIN   = 0x01

INTLATCH_50USPULSE = 0x00
INTLATCH_WAITCLEAR = 0x01

INTCLEAR_STATUSREAD = 0x00
INTCLEAR_ANYREAD    = 0x01

INTERRUPT_FF_BIT          = 7
INTERRUPT_MOT_BIT         = 6
INTERRUPT_ZMOT_BIT        = 5
INTERRUPT_FIFO_OFLOW_BIT  = 4
INTERRUPT_I2C_MST_INT_BIT = 3
INTERRUPT_PLL_RDY_INT_BIT = 2
INTERRUPT_DMP_INT_BIT     = 1
INTERRUPT_DATA_RDY_BIT    = 0

# TODO: figure out what these actually do
# UMPL source code is not very obivous
DMPINT_5_BIT           = 5
DMPINT_4_BIT           = 4
DMPINT_3_BIT           = 3
DMPINT_2_BIT           = 2
DMPINT_1_BIT           = 1
DMPINT_0_BIT           = 0

MOTION_MOT_XNEG_BIT    = 7
MOTION_MOT_XPOS_BIT    = 6
MOTION_MOT_YNEG_BIT    = 5
MOTION_MOT_YPOS_BIT    = 4
MOTION_MOT_ZNEG_BIT    = 3
MOTION_MOT_ZPOS_BIT    = 2
MOTION_MOT_ZRMOT_BIT   = 0

DELAYCTRL_DELAY_ES_SHADOW_BIT = 7
DELAYCTRL_I2C_SLV4_DLY_EN_BIT = 4
DELAYCTRL_I2C_SLV3_DLY_EN_BIT = 3
DELAYCTRL_I2C_SLV2_DLY_EN_BIT = 2
DELAYCTRL_I2C_SLV1_DLY_EN_BIT = 1
DELAYCTRL_I2C_SLV0_DLY_EN_BIT = 0

PATHRESET_GYRO_RESET_BIT  = 2
PATHRESET_ACCEL_RESET_BIT = 1
PATHRESET_TEMP_RESET_BIT  = 0

DETECT_ACCEL_ON_DELAY_BIT    = 5
DETECT_ACCEL_ON_DELAY_LENGTH = 2
DETECT_FF_COUNT_BIT          = 3
DETECT_FF_COUNT_LENGTH       = 2
DETECT_MOT_COUNT_BIT         = 1
DETECT_MOT_COUNT_LENGTH      = 2

DETECT_DECREMENT_RESET = 0x0
DETECT_DECREMENT_1     = 0x1
DETECT_DECREMENT_2     = 0x2
DETECT_DECREMENT_4     = 0x3

USERCTRL_DMP_EN_BIT           = 7
USERCTRL_FIFO_EN_BIT          = 6
USERCTRL_I2C_MST_EN_BIT       = 5
USERCTRL_I2C_IF_DIS_BIT       = 4
USERCTRL_DMP_RESET_BIT        = 3
USERCTRL_FIFO_RESET_BIT       = 2
USERCTRL_I2C_MST_RESET_BIT    = 1
USERCTRL_SIG_COND_RESET_BIT   = 0

PWR1_DEVICE_RESET_BIT = 7
PWR1_SLEEP_BIT        = 6
PWR1_CYCLE_BIT        = 5
PWR1_TEMP_DIS_BIT     = 3
PWR1_CLKSEL_BIT       = 2
PWR1_CLKSEL_LENGTH    = 3

CLOCK_INTERNAL        = 0x00
CLOCK_PLL_XGYRO       = 0x01
CLOCK_PLL_YGYRO       = 0x02
CLOCK_PLL_ZGYRO       = 0x03
CLOCK_PLL_EXT32K      = 0x04
CLOCK_PLL_EXT19M      = 0x05
CLOCK_KEEP_RESET      = 0x07

PWR2_LP_WAKE_CTRL_BIT    = 7
PWR2_LP_WAKE_CTRL_LENGTH = 2
PWR2_STBY_XA_BIT         = 5
PWR2_STBY_YA_BIT         = 4
PWR2_STBY_ZA_BIT         = 3
PWR2_STBY_XG_BIT         = 2
PWR2_STBY_YG_BIT         = 1
PWR2_STBY_ZG_BIT         = 0

WAKE_FREQ_1P25     = 0x0
WAKE_FREQ_2P5      = 0x1
WAKE_FREQ_5        = 0x2
WAKE_FREQ_10       = 0x3

BANKSEL_PRFTCH_EN_BIT     = 6
BANKSEL_CFG_USER_BANK_BIT = 5
BANKSEL_MEM_SEL_BIT       = 4
BANKSEL_MEM_SEL_LENGTH    = 5

WHO_AM_I_BIT       = 6
WHO_AM_I_LENGTH    = 6

DMP_MEMORY_BANKS      = 8
DMP_MEMORY_BANK_SIZE  = 256
DMP_MEMORY_CHUNK_SIZE = 16

class Accel(object) :
  """GY-521 Accelerometer."""

  @staticmethod
  def color( aR, aG, aB ) :
    '''Create a 565 rgb TFTColor value'''
    return TFTColor(aR, aG, aB)

  def __init__( self, aLoc, aAddress = ADDRESS_LOW ) :
    """aLoc I2C pin location is either 1 for 'X' or 2 for 'Y'.
       aAddress is either ADDRESS_LOW or ADDRESS_HIGH."""

    if 1 > aLoc > 2 :
      raise Exception("aLoc must be 1 or 2.")

    self._data = bytearray(1)
    self._data6 = bytearray(6)
    self._data14 = bytearray(14)
    self._address = aAddress
    self._i2c = pyb.I2C(aLoc, pyb.I2C.MASTER, baudrate = 400000)

    self.setclocksource(CLOCK_PLL_XGYRO)
    self.setfullscalegyrorange(GYRO_FS_250)
    self.setfulscaleaccelrange(ACCEL_FS_2)
    self.setsleepenabled(False)

  def getrate( self ) :
    self._readdata(RA_SMPLRT_DIV, self._data)
    return self._data[0]

  def setrate( self, aRate ) :
    self._writedata(RA_SMPLRT_DIV, aRate)

  def getDLPF( self ) :
    return self._readbits(RA_CONFIG, CFG_DLPF_CFG_BIT, CFG_DLPF_CFG_LENGTH)

  def setDLPF( self, aMode ) :
    self._writebits(RA_CONFIG, CFG_DLPF_CFG_BIT, CFG_DLPF_CFG_LENGTH, aMode)

  def setclocksource( self, aSource ) :
    self._writebits(RA_PWR_MGMT_1, PWR1_CLKSEL_BIT, PWR1_CLKSEL_LENGTH, aSource)

  def getfullscalegyrorange( self ) :
    return self._readbits(RA_GYRO_CONFIG, GCONFIG_FS_SEL_BIT, GCONFIG_FS_SEL_LENGTH)

  def setfullscalegyrorange( self, aRange ) :
    self._writebits(RA_GYRO_CONFIG, GCONFIG_FS_SEL_BIT, GCONFIG_FS_SEL_LENGTH, aRange)

  def getfullscaleaccelrange( self ) :
    self._readbits(RA_ACCEL_CONFIG, ACONFIG_AFS_SEL_BIT, ACONFIG_AFS_SEL_LENGTH)

  def setfullscaleaccelrange( self, aRange ) :
    self._writebits(RA_ACCEL_CONFIG, ACONFIG_AFS_SEL_BIT, ACONFIG_AFS_SEL_LENGTH, aRange)

  def getsleepenabled( self ) :
    self._readbits(RA_PWR_MGMT_1, PWR1_SLEEP_BIT, 1)

  def setsleepenabled( self, aTF ) :
    self._writebits(RA_PWR_MGMT_1, PWR1_SLEEP_BIT, 1, aTF)

  def getfreefalldetectionthreshold( self ) :
    self._readdata(RA_FF_THR, self._data)
    return self._data[0]

  def setfreefalldetectionthreshold( self, aValue ) :
    self._writedata(RA_FF_THR, aValue)

  def getfreefalldetectionduration( self ) :
    self._readdata(RA_FF_DUR, self._data)
    return self._data[0]

  def setfreefalldetectionduration( self, aValue ) :
    self._writedata(RA_FF_DUR, aValue)

  def getmotiondetectionthreshold( self ) :
    self._readdata(RA_MOT_THR, self._data)
    return self._data[0]

  def setmotiondetectionthreshold( self, aValue ) :
    self._writedata(RA_MOT_THR, aValue)

  def getmotiondetectionduration( self ) :
    self._readdata(RA_MOT_DUR, self._data)
    return self._data[0]

  def setmotiondetectionduration( self, aValue ) :
    self._writedata(RA_MOT_DUR, aValue)

  def getzeromotiondetectionthreshold( self ) :
    self._readdata(RA_ZRMOT_THR, self._data)
    return self._data[0]

  def setzeromotiondetectionthreshold( self, aValue ) :
    self._writedata(RA_ZRMOT_THR, aValue)

  def getzeromotiondetectionduration( self ) :
    self._readdata(RA_ZRMOT_DUR, self._data)
    return self._data[0]

  def setzeromotiondetectionduration( self, aValue ) :
    self._writedata(RA_ZRMOT_DUR, aValue)

  def getFIFOenabled( self ) :
    return self._readbits(RA_USER_CTRL, USERCTRL_FIFO_EN_BIT, 1)

  def setFIFFOenabled( self, aTF ) :
    self._writebits(RA_USER_CTRL, USERCTRL_FIFO_EN_BIT, 1, aTF)

  def gettempFIFOenabled( self ) :
    return self._readbits(RA_FIFO_EN, TEMP_FIFO_EN_BIT, 1)

  def settempFIFFOenabled( self, aTF ) :
    self._writebits(RA_FIFO_EN, TEMP_FIFO_EN_BIT, 1, aTF)

  def getxgyroFIFOenabled( self ) :
    return self._readbits(RA_FIFO_EN, XG_FIFO_EN_BIT, 1)

  def setxgyroFIFOenabled( self, aTF ) :
    self._writebits(RA_FIFO_EN, XG_FIFO_EN_BIT, 1, aTF)

  def getygyroFIFOenabled( self ) :
    return self._readbits(RA_FIFO_EN, YG_FIFO_EN_BIT, 1)

  def setygyroFIFOenabled( self, aTF ) :
    self._writebits(RA_FIFO_EN, YG_FIFO_EN_BIT, 1, aTF)

  def getzgyroFIFOenabled( self ) :
    return self._readbits(RA_FIFO_EN, ZG_FIFO_EN_BIT, 1)

  def setzgyroFIFOenabled( self, aTF ) :
    self._writebits(RA_FIFO_EN, ZG_FIFO_EN_BIT, 1, aTF)

  def getaccelFIFOenabled( self ) :
    return self._readbits(RA_FIFO_EN, ACCEL_FIFO_EN_BIT, 1)

  def setaccelFIFOenabled( self, aTF ) :
    self._writebits(RA_FIFO_EN, ACCEL_FIFO_EN_BIT, 1, aTF)

  def getmasterclockspeed( self ) :
    return self._readbits(RA_I2C_MST_CTRL, I2C_MST_CLK_BIT, I2C_MST_CLK_LENGTH)

  def setmasterclockspeed( self, aValue ) :
    self._writebits(RA_I2C_MST_CTRL, I2C_MST_CLK_BIT, I2C_MST_CLK_LENGTH, aValue)

  def getinterruptmode( self ) :
    return self._readbits(RA_INT_PIN_CFG, INTCFG_INT_LEVEL_BIT, 1)

  def setinterruptmode( self, aValue ) :
    self._writebits(RA_INT_PIN_CFG, INTCFG_INT_LEVEL_BIT, 1, aValue)

  def getinterruptdrive( self ) :
    return self._readbits(RA_INT_PIN_CFG, INTCFG_INT_OPEN_BIT, 1)

  def setinterruptdrive( self, aValue ) :
    self._writebits(RA_INT_PIN_CFG, INTCFG_INT_OPEN_BIT, 1, aValue)

  def getinterruptlatch( self ) :
    return self._readbits(RA_INT_PIN_CFG, INTCFG_LATCH_INT_EN_BIT, 1)

  def setinterruptlatch( self, aValue ) :
    self._writebits(RA_INT_PIN_CFG, INTCFG_LATCH_INT_EN_BIT, 1, aValue)

  def getinterruptlatchclear( self ) :
    return self._readbits(RA_INT_PIN_CFG, INTCFG_INT_RD_CLEAR_BIT, 1)

  def setinterruptlatchclear( self, aValue ) :
    self._writebits(RA_INT_PIN_CFG, INTCFG_INT_RD_CLEAR_BIT, 1, aValue)

  def getacceltemprot( self ) :
    self._readdata(RA_ACCEL_XOUT_H, self._data14)
    return [(self._data14[i] << 8) | self._data14[i + 1] for i in range(0, len(self._data14), 2)]

  def getacceleration( self ) :
    self._readdata(RA_ACCEL_XOUT_H, self._data6)
    return [(self._data6[i] << 8) | self._data6[i + 1] for i in range(0, len(self._data6), 2)]

  def getrotation( self ) :
    self._readdata(RA_GYRO_XOUT_H, self.data6)
    return [(self._data6[i] << 8) | self._data6[i + 1] for i in range(0, len(self._data6), 2)]

  def reset( self ) :
    self._writebits(RA_PWR_MGMT_1, PWR1_DEVICE_RESET_BIT, 1, True)

  def _writedata( self, aAddress, aData ) :
    self._i2c.mem_write(aData, self._address, aAddress)

  def _readdata( self, aAddress, aData ) :
    self._i2c.mem_read(aData, self._address, aAddress)

#  @micropython.native
  def _readbits( self, aAddress, aStart, aLen ) :
    self._readdata(aAddress, self._data)
    b = (self._data[0] >> (aStart - aLen + 1)) & ((1 << aLen) - 1)

#  @micropython.native
  def _writebits( self, aAddress, aStart, aLen, aValue ) :
    self._readdata(aAddress, self._data)
    mask = ((1 << aLen) - 1) << (aStart - aLen + 1)
    aValue = (buffer[0] << (aStart - aLen + 1)) & mask #shift data into correct position
    val &= ~mask
    self._data[0] |= aValue
    self._writedata(aAddress, self._data)

