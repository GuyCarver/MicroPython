
from machine import UART, Pin
from time import sleep_ms

# HC05 Bluetooth board ----------------------------------------
#See docs at:
# https://www.itead.cc/wiki/Serial_Port_Bluetooth_Module_(Master/Slave)_:_HC-05

#COMMANDS:
#    AT - Does nothing but get an ok.
# All of the following commands start with AT+ and end with \r\n
#    VERSION?
#    NAME= : This is the name that will show up in windows.
#    NAME? :
#    ADDR? : see default address
#    UART? : See baudrate
#    UART= : Set baudrate, stop, parity
#    ROLE? : See role of bt module(1=master/0=slave)
#    ROLE= : Set role of bt module(1=master/0=slave/2=slave loop)
#    RESET : Reset and exit AT mode
#    ORGL : Restore factory settings
#    PSWD? : see default password
#    PSWD= : set default password
#    RMAAD : Remove all paired devices.
#    CMODE? : Get the CMODE.
#    CMODE= : 0 = fixed addr, 1 = connect any, 2 = slave loop.
#    BIND= : Param is fixed address (Default 00:00:00:00:00:00). Send data separated by ,
#    BIND? : Return data is separated by :
#    INQM=<P1>,<P2>,<P3> : P1 = 0:standard, 1:rssi, P2 = Max # of devices. P3 = Timeout (1-48: 1-61s)
#    INQ : Start inquiring state.
#    INQC : Cancel inquiring state.
#    PAIR=<addr>  : Match device.  Don't know what the difference between PAIR and LINK are.
#    LINK=<addr> : Connect device.
#    CLASS= : Device class.
#    POLAR=<P1>,<P2> : 1, 0 for example.
#    STATE? : Get Initialized, Ready, Pairable, Inquiring, Connectin, Connected, Disconnected, Unknown
#    MRAD? : Get address of most recently used authenticated device.
#    ADCN? : Get authenticated device count.
#    DISC : Disconnect

#HC05 notes:
# My HC05 has an AT button on it.  I do not use that button at all.
# I've found that connecting at baud 38400 is the best way to ensure communication in both AT and DATA mode.
# To send most AT commands the 'EN' pin must be pulled high.
# When the LED is flashing quickly, all AT commands work at all baud rates.
# But on reset command, the LED will blink slowly.  In this state AT commands will only work on baud 38400.

#Master connect sequence:
# h.at = 1
# h.clearpaired()
# h.role(1)
# h.reset()
# h.cmode(1)
# h.inqm(0,5,5)
# h.init()
# h.inq()

class hc05(object):
  '''hc05 Bluetooth serial device driver.  This is simply a light UART wrapper
     with addition AT command methods to customize the device.'''

  _OK = 'OK\r\n'
  _COMMA = ','
  _EQUAL = '='
  _AT = 'AT+'

  #Commands that are both ? and =.
  _NAME = 'NAME'
  _PSWD = 'PSWD'
  _UART = 'UART'
  _ROLE = 'ROLE'
  _CMODE = 'CMODE'

  def __init__( self, atpin, uart, aBaud = 38400, aParity = None, aStop = 1 ):
    ''' uart = uart #0-2, baudrate must match what is set on the hc05 or 38400 (at-mode).
        It is suggested to set the baud rate to 38400, then at mode will always work with the current baud rate.
        atpin is the pin connected to the hc05 "en" pin.  This is used to enter at mode.'''
    self._uart = UART(uart, aBaud, parity = aParity, stop = aStop)
    self._at = Pin(atpin, Pin.OUT, Pin.PULL_UP)

  def __del__( self ) : self._uart.deinit()

  def any( self ) : return self._uart.any()

  def write( self, astring ) : return self._uart.write(astring)
  def writechar( self, achar ) : self._uart.writechar(achar)

  def read( self, num = None ) : return self._uart.read(num)
  def readline( self ) :
    res = self._uart.readline()
    return res.decode('utf-8') if res else ''

  def readchar( self ) : return self._uart.readchar()
  def readinto( self, buf, count = None ) : return self._uart.readinto(buf, count)

  def clear( self ) :
    while self.any() :
      self._uart.readline()

  def _test( self ) :
    self.clear()
    self._uart.write('AT\r\n')
    for i in range(1, 100) :
      sleep_ms(10)
      if self.any():
        return self.readline() == hc05._OK
    return False

  @property
  def at( self ) :
    return self._at()

  @at.setter
  def at( self, aArg ) :
    '''Put into at Mode.'''
    self._at(aArg)

  def _write( self, aValue ) :
    return self._uart.write(aValue)

  def _getreply( self ) :
    res = ''
    for i in range(1, 100) :
      if self.any() :
        res = self.readline()
        break
      sleep_ms(10)
    return res

  def _cmd( self, *aCommands ) :
    '''Send AT command, wait a bit then return True if OK'''
    self.clear()
    self._write(hc05._AT)
    for c in aCommands:
      self._write(c)
    self._write('\r\n')
    return self._getreply()

  def _qcmd( self, *aCommands ) :
    '''Send AT command, wait a bit then return result string'''
    self.clear()
    self._write(hc05._AT)
    for c in aCommands:
      self._write(c)
    self._write('?\r\n')
    bres = self._getreply()
    self.readline() #Read the 'OK\r\n' line.
    return bres

  def qaddr( self ) :
    return self._qcmd('ADDR')

  def qname( self ) :
    '''Get the name (AT mode only)'''
    return self._qcmd(hc05._NAME)

  def name( self, aName ) :
    '''Set the name to show up on the connecting device'''
    return self._cmd(hc05._NAME, hc05._EQUAL, aName)

  def qpswd( self ) :
    '''Get the password'''
    return self._qcmd(hc05._PSWD)

  def pswd( self, aPin ) :
    '''Set the password'''
    return self._cmd(hc05._PSWD, hc05._EQUAL, str(aPin))

  def qversion( self ) :
    '''Get version #'''
    return self._qcmd('VERSION')

  def quart( self ) :
    '''Get uart baud, stop, parity'''
    return self._qcmd(hc05._UART)

  def uart( self, aBaud, aStop, aParity ) :
    '''Set uart baud, stop, parity'''
    return self._cmd(hc05._UART, hc05._EQUAL, str(aBaud), hc05._COMMA, str(aStop), hc05._COMMA, str(aParity))

  def qrole( self ) :
    '''Get role, 0 = slave, 1 = master'''
    return self._qcmd(hc05._ROLE)

  def role( self, aRole ) :
    '''Set role, 0 = slave, 1 = master'''
    return self._cmd(hc05._ROLE, hc05._EQUAL, str(aRole))

  def reset( self ) :
    '''Reset hc05'''
    return self._cmd('RESET')

  def clearpaired( self ) :
    '''Clear all paired device'''
    return self._cmd('RMAAD')

  def qcmode( self ) :
    '''Get connect mode: 0 = fixed address, 1 = any, 2 = slave loop'''
    return self._qcmd(hc05._CMODE)

  def cmode( self, aMode ) :
    '''Set connect mode: 0 = fixed address, 1 = any, 2 = slave loop'''
    return self._cmd(hc05._CMODE, hc05._EQUAL, str(aMode))

  def inqm( self, aProtocol, aDevices, aTimeout ) :
    '''Set inquiry mode: aProtocol = 0/standard, 1/rssi, aDevices = Max # devices, aTimeout = 1-48'''
    return self._cmd('INQM=', str(aProtocol), hc05._COMMA, str(aDevices), hc05._COMMA, str(aTimeout))

  def init( self ) :
    '''Initialize hc05 with given settings.'''
    return self._cmd('INIT')

  def inq( self ) :
    '''Enter inquiry state'''
    return self._cmd('INQ')

  def inqcancel( self ) :
    '''Cancel inquiry state'''
    return self._cmd('INQC')

  def setclass( self, aClass ) :
    '''Set class #'''
    return self._cmd('CLASS=', str(aClass))

  def polar( self, av1, av2 ) :
    return self._cmd('POLAR=', str(av1), hc05._COMMA, str(av2))

  def qstate( self ) :
    '''Get current state'''
    return self._qcmd('STATE')

  def qdevicecount( self ) :
    '''Get authenticated defice count'''
    return self._qcmd('ADCN')

  def qmrad( self ) :
    '''Get most recently used device address'''
    return self._qcmd('MRAD')

  def pair( self, aDevice, aTimeout ) :
    '''Pair with given device'''
    return self._cmd('PAIR=', aDevice, str(aTimeout))

  def link( self, aAddress ) :
    '''Link with given device'''
    return self._cmd('LINK=', aAddress)

  def disconnect( self ) :
    '''Disconnect from device'''
    return self._cmd('DISC')

