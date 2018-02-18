'''IR temperature sensor using I2C interface.'''

import machine, time

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

  def __init__(self, aSDA, aSCL):
    '''aLoc is either 'X', 1, 'Y' or 2.'''
    super(mlx, self).__init__()

    self.i2c = machine.I2C(scl = machine.Pin(aSCL), sda = machine.Pin(aSDA))
    self._w1 = bytearray(2)

  def read( self, aLoc ) :
    '''Read 16 bit value and return.'''
    self.i2c.readfrom_mem_into(_ADDRESS, aLoc, self._w1)
    return (self._w1[1] << 8) | self._w1[0]

#  def write( self, aVal, aLoc ) :
#    """Write 16 bit value to given address.  aVal may be an int buffer."""
#    self.i2c.mem_write(aVal, _ADDRESS, aLoc, addr_size = 16)

  def readtemp( self, aLoc ) :
    ''' '''
    temp = self.read(aLoc)
    return (temp * 0.02) - 273.15

  def temp( self ) :
    return self.readtemp(_TA)

  def objecttemp( self ) :
    return self.readtemp(_TOBJ1)

  def object2temp( self ) :
    return self.readtemp(_TOBJ2)

  def display( self ) :
    while True :
      t1 = c2f(self.temp())
      t2 = c2f(self.objecttemp())
      t3 = c2f(self.object2temp())
      print("1: {} 2: {} 3: {}      \r".format(t1, t2, t3), end = '')
      time.sleep_ms(500)
