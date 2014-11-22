#Driver for the L298N Dual HBridge motor controller.

from PWM import PWM
from pyb import Pin

#motordata
#Forward pin
#Back pin
#Speed pin (PWM)

class Motor(  ):
  """docstring for Motor"""

  def __init__(self, forward, backward, speed):
    """Speed = (pin name, timer#)"""
    self._forward = Pin(forward, Pin.OUT_PP)
    self._backward = Pin(backward, Pin.OUT_PP)
    self._speedControl = PWM(speed[0], speed[1])
    self._speed = 0

  @property
  def speed(self): return self._speed

  @speed.setter
  def speed(self, value):
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

    self._speedControl.pulse_width_percent = abs(value)

  def brake( self ) :
    """  """
    self._forward.high()
    self._backward.high()
    self._speedControl.pulse_width_percent(1.0)

