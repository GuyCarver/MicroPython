#Driver for the bts7960 43A high power motor controller.

from pwm import pwm
from pyb import Pin
from utime import sleep_ms

class motor(  ):
  """Control a motor connected to the bts7960 motor controller."""

  def __init__( self, aOnOff, aForward, aBackward ) :
    """aOnOff is the pin to control free movement of the motor.
       aForward and aBackward are tuples indicating pin and timer channel # for PWM pins.
       aForward = (pin name, timer channel #)
       aBackward = (pin name, timer channel #)
       Need to make sure the given timer channel # is associated with the pin
       or an exception will be raised.
       #Examples:
       m1 = motor('Y1', ('Y2', 8), ('Y3', 10))
       m2 = motor('X1', ('X2', 5), ('X3', 5)) """
    self._onoff = Pin(aOnOff, Pin.OUT_PP)
    self._forward = pwm(*aForward)
    self._backward = pwm(*aBackward)
    self._speed = 0

  self.seton( self, aOn ) :
    '''Set on/off (free wheeling) state of motor.'''
    if aOn :
      self._onoff.high()
    else:
      self._onoff.low()

  @property
  def speed( self ) : return self._speed

  @speed.setter
  def speed( self, aValue ) :
    '''Set velocity and direction of motor with -100 <= aValue <= 100.'''
    self._speed = aValue

    on = False
    f = 0
    b = 0

    if aValue < 0 :
      on = True
      f = 0
      b = min(100, -aValue)
    else:
      on = True
      f = min(100, aValue)
      b = 0

    self.seton(on)
    self._forward.pulse_width_percent = f
    self._backward.pulse_width_percent = b

  def brake( self ) :
    """ Brake the motor by sending power both directions, then shut it all down. """
    self._forward.pulse_width_percent = 100
    self._backward.pulse_width_percent = 100
    self.seton(True)
    sleep_ms(500)
    self.speed = 0

