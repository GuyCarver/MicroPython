#!/usr/bin/env python3

#LynxMotion PS2 wireless controller driver.
#See http://www.lynxmotion.com/images/files/ps2cmd01.txt for command list.
#See http://sophiateam.undrgnd.free.fr/psx/index.html for explanation of communication protocol.

from machine import Pin
from time import sleep_us

class ps2():
  '''PS2 wireless controller driver. Each button tracks up/down state as well
     as just pressed/released state.  These values may be read directly or
     state changes may be reported to a given callback function.  The L/R Joystick
     values are in the range of +/- 256 and must be read using the joy() function.
     The PS2 controller is put into analog mode without pressure sensitivity on the buttons.
     Rumble is not enabled.  Enabling rumble for some reason causes input to be extremely slow.'''

  #Button values. Bit 1 = changed, Bit 0 = Down state.
  _UP         = const(0)
  _DOWN       = const(1) #Button is down.
  _RELEASED   = const(2) #Indiciates button was just released.
  _PRESSED    = const(3) #Indicate button was just pressed.

  #_buttons array indexes
  _SELECT     = const(0)
  _L_HAT      = const(1)
  _R_HAT      = const(2)
  _START      = const(3)
  _DPAD_U      = const(4)
  _DPAD_R      = const(5)
  _DPAD_D      = const(6)
  _DPAD_L      = const(7)
  _L_TRIGGER  = const(8)
  _R_TRIGGER  = const(9)
  _L_SHOULDER = const(10)
  _R_SHOULDER = const(11)
  _TRIANGLE   = const(12)
  _CIRCLE     = const(13)
  _CROSS      = const(14)
  _SQUARE     = const(15)

  #_joys array indexes.
  _RX = const(0)
  _RY = const(1)
  _LX = const(2)
  _LY = const(3)

  #Controller commands.
  _qmode = (1,0x41,0,0,0)       #Add the below bytes in to read analog (analog button mode needs to be set)
  _qdata = (1,0x42,0,0,0,0,0,0,0) #,0,0,0,0,0,0,0,0,0,0,0,0,0)
  _enter_config = (1,0x43,0,1,0)
  _exit_config = (1,0x43,0,0,0x5A,0x5A,0x5A,0x5A,0x5A)
  _set_mode = (1,0x44,0,1,3,0,0,0,0) #1 = analog stick mode, 3 = lock mode button.
#  _ds2_native = (1,0x4F,0,0xFF,0xFF,03,00,00,00)
#  _enable_analog = (1,0x4F,0,0xFF,0xFF,3,0,0,0) #enable analog pressure input from button.
#  _enable_rumble = (0x01,0x4D,0,0,1)
#  _type_read= bytearray((1,0x45,0,0,0,0,0,0,0))

  def __init__( self, aCmd, aData, aClk, aAtt, aCallback = None ):
    '''Create a ps2 object with the given Command, Data, Clock, Attn and Callback values.'''
    self._cmd = Pin(aCmd, Pin.OUT, Pin.PULL_DOWN)
    self._data = Pin(aData, Pin.IN)
    self._clk = Pin(aClk, Pin.OUT, Pin.PULL_DOWN)
    self._att = Pin(aAtt, Pin.OUT, Pin.PULL_DOWN)
    self._res = bytearray(9)  #Set this to 22 for analog button data reading.
    #Double buffered buttons.
    self._buttons = (bytearray(16), bytearray(16))
    self._buttonIndex = 0                       #Index into _buttons array.
    self._joys = [0, 0, 0, 0]
    #If we don't set these high to start the 1st command doesn't work.
    self._att(1)
    self._clk(1)
    self._callback = None
    self._initpad()
    #Set callback after _initpad() because button states change during init.
    self.callback = aCallback

  def _shiftinout( self, aChar ):
    '''Shift bits of aChar out on the _cmd pin while reading bits
       in from _data pin.  Returns 8 bit data value.'''
    value = 0
    for i in range(0, 8):
      self._cmd(aChar & 1)  #Set/Clear pin for bit of aChar.
      aChar >>= 1           #Next bt.
      self._clk(0)          #Clock pin low to start send.
      sleep_us(4)           #Wait a bit.
      value |= self._data() << i  #Read bit from data pin.
      self._clk(1)          #Set clock high.
    sleep_us(1)
    return value

  def _sendrcv( self, aSend ):
    '''Send data in aSend while reading data into _res'''
    self._att(0)            #Get attention of controller.
    sleep_us(1)             #Wait a bit before sending.

    #Send each byte and receive a byte.
    for i, b in enumerate(aSend):
      self._res[i] = self._shiftinout(b)
    self._att(1)            #Tell controller we are done.
    return self._res

  def _initpad( self ):
    '''Initialize the gamepad in analog stick mode.'''
    self.qdata()
    sleep_us(100)
    self._sendrcv(ps2._enter_config)
    sleep_us(1)
    self._sendrcv(ps2._set_mode)
    sleep_us(1)
    #Put these in to enable rumble and analog button modes.
#    self.display()
#    self._sendrcv(ps2._enable_rumble)
#    sleep_us(1)
#    self.display()
#    self._sendrcv(ps2._enable_analog)
#    sleep_us(1)
#    self.display()
    self._sendrcv(ps2._exit_config)
    #Read data a few times to get junk out of the way.
    for i in range(0, 6):
      sleep_us(1)
      self.qdata()

#  def qmode( self ):
#    '''  '''
#    return self._sendrcv(ps2._qmode)

  @property
  def callback( self ):
    return self._callback

  @callback.setter
  def callback( self, aCallback ):
    self._callback = aCallback

  @property
  def curbuttons( self ):
    return self._buttons[self._buttonIndex]

  @property
  def prevbuttons( self ):
    return self._buttons[not self._buttonIndex]

  def button( self, aIndex ):
    return self.curbuttons[aIndex]

  def joy( self, aIndex ):
    return self._joys[aIndex]

  def qdata( self ):
    '''Read button/joystick data from controller.  Data will be in _res.'''
    self._sendrcv(ps2._qdata)

    #Swap buffer for current button values.
    self._buttonIndex = not self._buttonIndex
    #Get previous and current button buffers.
    prev = self.prevbuttons
    buttons = self.curbuttons
    b = self._res[3] | (self._res[4] << 8) #Merge 16 bits of button data.
    for i in range(16):
      bv = not (b & 1)   #Button on if bit is 0 so swap that.
      if bv != (prev[i] & 1):  #If button changed, set bit 1.
        bv |= 2
      buttons[i] = bv

      #If value not _UP and we have a callback function, then call it.
      if bv and self._callback:
        self._callback(i, bv)

      b >>= 1           #Next button bit.

    #Convert joystick values 0-0xFF with 0x80 in center to values +/- 0-256
    sgn = 1
    for i in range(5, 9):
      self._joys[i - 5] = ((self._res[i] - 0x80) << 1) * sgn
      sgn = -sgn  #Every other value (y) needs to be reversed so +y is up.

    return self._res

#  def displaymode( self ):
#    self.display(self.qmode())

#  def displaydata( self ):
#    self.display(self.qdata())

#  def displaymodel( self ):
#    self.display(self._sendrcv(ps2._type_read))

#  def display( self, aBuf = None ):
#    if aBuf == None :
#      aBuf = self._res
#
#    for b in aBuf:
#      print(hex(b), end='')
#      print(',', end='')
#    print(';', end='\r')

#  def test( self ):
#    while 1:
#      self.qdata()
#      print(self.curbuttons, end=' ')
#      print(self._joys, end='\r')
#      sleep_us(50000)

#btnnames = ['SELECT', 'L_HAT', 'R_HAT', 'START', 'DPAD_U', 'DPAD_R',
#      'DPAD_D', 'DPAD_L', 'L_TRIGGER', 'R_TRIGGER', 'L_SHOULDER',
#      'R_SHOULDER', 'TRIANGLE', 'CIRCLE', 'CROSS', 'SQUARE']
#
#statenames = ['UP', 'DOWN', 'RELEASED', 'PRESSED']
#
#def MyCallback( aIndex, aState ):
#  ''' '''
#  print('{} : {}'.format(btnnames[aIndex], statenames[aState]))
#
#def test(  ):
#  p = ps2('X8', 'X7', 'X6', 'Y9', MyCallback)
#  while 1:
#    p.qdata()
#    sleep_us(50000)
