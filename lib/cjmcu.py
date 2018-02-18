#Driver for CJMCU-IR temperature sensor.  Uses mlx90614 but adds serial interface to it.

from pyb import UART

#Format of data output from the device:
#length: 9
#  Byte0 Header Flags 0x66
#  Byte1 Header Flags 0x66
#  Byte2 data output mode (0x01 continuous output; 0x02 query output, the default for continuous output mode)
#  Byte3 Measured data length (counted by Byte)
#  Byte4 Temperature 1 Upper 8 bits
#  Byte5 Temperature 1 Lower 8 bits
#  Byte6 Temperature 2 Upper 8 bits
#  Byte7 Temperature 2 Lower 8 bits
#  Byte8 data parity (all data accumulation, take the low 8-bit)
#
#Celcius Temperature calculation method:
#
#Temperature = Data High 8 bits << 8 | Lower 8 bits of data, the result is the actual temperature multiplied by 100.
#
#Command instructions:
#Lenght: 4
#Byte0 Header Flags 0x66
#Byte1 Header Flags 0x66
#Byte2 Sets the command:
#    0x01 Continuous output mode
#    0x02 Query output mode
#    0x11 Set the baud rate to 9600
#    0x12 Set the baud rate to 57600
#    0x13 Set the baud rate to 115200
#Byte3 End of frame flag 0x56

def c2f( aValue ):
  '''Celcius to Farenheit conversion.'''
  return (aValue * 9.0 / 5.0) + 32.0

class cjmcu(object) :
  """docstring for cjmcu"""
  _CONTINUOUS = const(1)
  _POLL = const(2)

  _RATEBASE = 0x11
  _BAUD9600 = const(0)
  _BAUD19200 = const(1)
  _BAUD38400 = const(2)

  def __init__(self, aLoc):
    super(cjmcu, self).__init__()
    self._uart = UART(aLoc, 9600)
    self._mode = _POLL
    self._output = bytearray(4)
    self._output[0] = 0x66
    self._output[1] = 0x66
    self._output[2] = self._mode
    self._output[3] = 0x56
    self._input = bytearray(9)

    self.update()

  def write( self ) :
    self._uart.write(self._output)

  def read( self ) :
    self._uart.readinto(self._input)

  def update( self ) :
    self.write()
    self.read()

  def setbaud( self, aBaud ) :
    self._output[2] = _BAUDBASE + aBaud
    self.update()
    self._output[2] = self._mode
    self._uart.deinit()
    self._uart.init(9600 << aBaud)

  def temps( self ) :
    v1 = (self._input[4] << 8) | self._input[5]
    v2 = (self._input[6] << 8) | self._input[7]
    return (v1 / 100.0, v2 / 100.0)



