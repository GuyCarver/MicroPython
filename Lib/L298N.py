#Driver for the L298N Dual HBridge motor controller.

from PWM import PWM
from pyb import Pin, delay

class Motor(  ):
  """Control a motor connected to the L298N Dual motor controller."""

  def __init__( self, forward, backward, speed ) :
    """forward pin name, backward pin name, speed = (pin name, timer#)
       Need to make sure the given timer # is associated with the speed
       pin or an exception will be raised.  The speed pin must support
       PWM."""
    self._forward = Pin(forward, Pin.OUT_PP)
    self._backward = Pin(backward, Pin.OUT_PP)
    self._speedControl = PWM(speed[0], speed[1])
    self._speed = 0

  @property
  def speed( self ) : return self._speed

  @speed.setter
  def speed( self, value ) :
    self._speed = value
    if (value == 0):
      self._forward.low()
      self._backward.low()
    elif (value < 0):
      self._forward.low()
      self._backward.high()
    else:
      self._forward.high()
      self._backward.low()

    self._speedControl.pulse_width_percent = min(100, abs(value))

  def brake( self ) :
    """ Brake the motor by sending power both directions. """
    self._forward.high()
    self._backward.high()
    self._speedControl.pulse_width_percent = 100
    delay(1000)
    self.speed = 0
