
from pyb import UART, udelay

#AT commands for the ESP8266
#For comprehensive instructions visit http://www.electrodragon.com/w/Wi07c
#AT command strings must end with "\r\n" to trigger command processing.
#Any commands takin ssid or passwords must have id or password surrounded by quotes.
#AT - return "ok" if connection works.
#AT+RST - reset.  Will write back a bunch of gibberish then "ready"
#AT+GMR - firmware version.
#AT+CIOBAUD? or AT+CIOBAUD=? - return baud rate, AT+CIOBAUD=xxx - set baud rate.
#AT+CWMODE or CWMODE? 1=Sta, 2=AP, 3=both. AP for devices STA for router.
#AT+CWJAP=ssid,pwd or CWJAP? Join or report AP.
#AT+CWLAP - list APs.
#AT+CWQAP - Quit AP.
#AT+CWSAP=ssid,pwd,chnl,encryption or CWSAP? = Set AP params.
#AT+CWLIF - Check join devices.
#AT+CIPSTATUS - Get connection status.
#AT+CIPSTART
#AT+CIPMODE=mode - 0 no data mode, 1 data mode, CIPMODE? reports mode.
#AT+CIPSEND=lengh - send data.
#AT+CIPCLOSE - Close TCP/UDP connection.
#AT+CIFSR - Get IP addresses
#AT+CIPMUX=mode or CIPMUX? - set/get multiple connection mode.
#AT+CIPSERVER=mode,port - Set as server.
#AT+CIPSTO=timout or CIPSTO? - Set/get server timout.
#AT+IPD - Receive data
#AT+CSYSWDTENABLE or DISABLE - enable/disable restart on error watchdog.

class wifi:
  """docstring for wifi"""

  def __init__(self, uart, baudrate = 115200):
    """ uart = uart #1-6, baudrate must match what is set on the ESP8266. """
    self._uart = UART(uart, baudrate)

  def write( self, aMsg ) :
    self._uart.write(aMsg)
    res = self._uart.readall()
    if res:
      print(res.decode("utf-8"))

  def read( self ) : return self._uart.readall().decode("utf-8")

  def _cmd( self, cmd ) :
    """ Send AT command, wait a bit then return results. """
    self._uart.write("AT+" + cmd + "\r\n")
    udelay(500)
    return self.read()

  @property
  def IP(self): return self._cmd("CIFSR")

  @property
  def networks( self ) : return self._cmd("CWLAP")

  @property
  def baudrate(self): return self._cmd("CIOBAUD?")

  @baudrate.setter
  def baudrate(self, value): return self._cmd("CIOBAUD=" + str(value))

  @property
  def mode(self): return self._cmd("CWMODE?")

  @mode.setter
  def mode(self, value): self._cmd("CWMODE=" + str(value))

  def connect( self, ssid, password = "" ) :
    """ Connect to the given network ssid with the given password """
    constr = "CWJAP=\"" + ssid + "\",\"" + password + "\""
    return self._cmd(constr)

  def disconnect( self ) : return self._cmd("CWQAP")

  def reset( self ) : return self._cmd("RST")

