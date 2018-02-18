'''IR temperature sensor using I2C interface.'''

import pyb

def c2f( aValue ):
  '''Celcius to Farenheit conversion.'''
  return (aValue * 9.0 / 5.0) + 32.0

class mlx(object):
  '''  '''

  _ADDRESS = const(0x5A)

  #RAM
#  _RAWIR1 = const(0x04)
#  _RAWIR2 = const(0x05)
  _TA = const(0x06)
  _TOBJ1 = const(0x07)
  _TOBJ2 = const(0x08)

  #EEPROM
#  _TOMAX = const(0x20)
#  _TOMIN = const(0x21)
#  _PWMCTRL = const(0x22)
#  _TARANGE = const(0x23)
#  _EMISS = const(0x24)
#  _CONFIG = const(0x25)
#  _ADDR = const(0x0E)
#  _ID1 = const(0x3C)
#  _ID2 = const(0x3D)
#  _ID3 = const(0x3E)
#  _ID4 = const(0x3F)

  def __init__(self, aLoc):
    '''aLoc is either 'X', 1, 'Y' or 2.'''
    super(mlx, self).__init__()

    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)
    self._w1 = bytearray(2)

  def read( self, aLoc ) :
    '''Read 16 bit value and return.'''
    self.i2c.mem_read(self._w1, _ADDRESS, aLoc) #, addr_size = 16)
    return (self._w1[0] << 8) | self._w1[1]

#  def write( self, aVal, aLoc ) :
#    """Write 16 bit value to given address.  aVal may be an int buffer."""
#    self.i2c.mem_write(aVal, _ADDRESS, aLoc, addr_size = 16)

  def readtemp( self, aLoc ) :
    ''' '''
    temp = self.read(aLoc)
    return (temp * 0.02) - 273.15

  def ambienttemp( self ) :
    return self.readtemp(_TA)

  def objecttemp( self ) :
    return self.readtemp(_TOBJ1)

  def object2temp( self ) :
    return self.readtemp(_TOBJ2)
