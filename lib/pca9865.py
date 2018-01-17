# MicroPython PCA9865 16 servo controller driver.
#NOTE: I tried writing 16 bit values for PWM but it crashed the controller requiring a power cycle to reset.

import pyb
from time import sleep_us

class pca9865(object):
  """16 servo contoller. Use index 0-15 for the servo #."""

  _ADDRESS = 0x40
  _MODE1 = const(0)
  _PRESCALE = const(0xFE)

  _LED0_ON_L = const(0x6)                       #We only use LED0 and offset 0-16 from it.
#  _LED0_ON_H = const(0x7)
#  _LED0_OFF_L = const(0x8)
#  _LED0_OFF_H = const(0x9)

#  _ALLLED_ON_L = const(0xFA)
#  _ALLLED_ON_H = const(0xFB)
#  _ALLLED_OFF_L = const(0xFC)
#  _ALLLED_OFF_H = const(0xFD)

  _DEFAULTFREQ = const(60)
  _MINPULSE = const(150)
  _MAXPULSE = const(600)
  _PULSERANGE = const(450)

  def __init__(self, aLoc) :
    """aLoc I2C pin location is either 1, 'X', 2 or'Y'."""
    super(pca9865, self).__init__()
    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)
#    print(self.i2c)
    self._buffer = bytearray(4)
    sleep_us(50)
    self.reset()

  def read( self, aLoc ) :
    """Read 8 byte value and return in bytearray"""
    return self.i2c.mem_read(1, self._ADDRESS, aLoc)

  def write( self, aVal, aLoc ) :
    """Write 8 bit value to given address.  aVal may be an int buffer."""
    self.i2c.mem_write(aVal, self._ADDRESS, aLoc)

  def reset( self ):
    """Reset the controller and set default frequency."""
    self.write(0, _MODE1)
    self.setfreq(_DEFAULTFREQ)

  def setfreq( self, aFreq ) :
    """Set frequency for all servos.  A good value is 60hz (default)."""
    aFreq *= 0.9  #Correct for overshoot in frequency setting.
    prescalefloat = (6103.51562 / aFreq) - 1  #25000000 / 4096 / freq.
    prescale = int(prescalefloat + 0.5)

    data = self.read(_MODE1)
    oldmode = data[0]
    newmode = (oldmode & 0x7F) | 0x10
    self.write(newmode, _MODE1)
    self.write(prescale, _PRESCALE)
    self.write(oldmode, _MODE1)
    sleep_us(50)
    self.write(oldmode | 0xA1, _MODE1)  #This sets the MODE1 register to turn on auto increment.

  def setpwm( self, aServo, aOn, aOff ) :
    """aServo = 0-15.
       aOn = 16 bit on value.
       aOff = 16 bit off value.
    """
    if 0 <= aServo <= 15 :
      #Data = on-low, on-high, off-low and off-high.  That's 4 bytes each servo.
      loc = _LED0_ON_L + (aServo * 4)
#    print(loc)
      self._buffer[0] = aOn
      self._buffer[1] = aOn >> 8
      self._buffer[2] = aOff
      self._buffer[3] = aOff >> 8
      self.write(self._buffer, loc)
    else:
      raise Exception('Servo index {} out of range.'.format(str(aServo)))

  def off( self, aServo ) :
    """Turn off a servo."""
    self.setpwm(aServo, 0, 0)

  def setangle( self, aServo, aAng ) :
    """Set the angle 0-100%"""
    val = _MINPULSE + ((_PULSERANGE * aAng) // 100)
    self.setpwm(aServo, 0, val)
