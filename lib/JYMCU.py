# JY-MCU Bluetooth board ----------------------------------------

from pyb import UART, repl_uart, udelay

# This opens connection with Bluetooth module connected to Y1, Y2 (UART 6)
# Then it sets the repl output to this UART.
#COMMANDS AT - does nothing but get an ok.
#  The possible baudrates are:
#     AT+BAUD1-------1200
#     AT+BAUD2-------2400
#     AT+BAUD3-------4800
#     AT+BAUD4-------9600 - Default for hc-06
#     AT+BAUD5------19200
#     AT+BAUD6------38400
#     AT+BAUD7------57600 - Johnny-five speed
#     AT+BAUD8-----115200
#     AT+BAUD9-----230400
#     AT+BAUDA-----460800
#     AT+BAUDB-----921600
#     AT+BAUDC----1382400
#     AT+VERSION
#     AT+NAMEnewname  This is the name that will show up in windows.
#     AT+PIN???? set 4 digit pairing pin.

class jymcu(object):
  """JY-MCU Bluetooth serial device driver.  This is simply a light UART wrapper
     with addition AT command methods to customize the device."""

  def __init__( self, uart, baudrate ):
    """ uart = uart #1-6, baudrate must match what is set on the JY-MCU.
        Needs to be a #1-C. """
    self._uart = UART(uart, baudrate)

  def __del__( self ) : self._uart.deinit()

  def any( self ) : return self._uart.any()

  def write( self, astring ) : return self._uart.write(astring)
  def writechar( self, achar ) : self._uart.writechar(achar)

  def read( self, num = None ) : return self._uart.read(num)
  def readline( self ) : return self._uart.readline()
  def readchar( self ) : return self._uart.readchar()
  def readall( self ) : return self._uart.readall()
  def readinto( self, buf, count = None ) : return self._uart.readinto(buf, count)

  def _cmd( self, cmd ) :
    """ Send AT command, wait a bit then return result string. """
    self._uart.write("AT+" + cmd)
    udelay(500)
    return self.readline()

  def baudrate( self, rate ) :
    """ Set the baud rate.  Needs to be #1-C. """
    return self._cmd("BAUD" + str(rate))

  def name( self, name ) :
    """ Set the name to show up on the connecting device. """
    return self._cmd("NAME" + name)

  def pin( self, pin ) :
    """ Set the given 4 digit numeric pin. """
    return self._cmd("PIN" + str(pin))

  def version( self ) : return self._cmd("VERSION")

  def setrepl( self ) : repl_uart(self._uart)

