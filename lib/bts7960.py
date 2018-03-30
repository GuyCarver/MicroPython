
#Driver for the bts7960 43A high power motor controller.

from machine import Pin, PWM
from utime import sleep_ms

class motor(  ):
  """Control a motor connected to the bts7960 motor controller."""

  def __init__( self, aForward, aBackward, aFreq = 100 ) :
    """aForward = tuple (On Pin #, PWM Pin #)
       aBackward = tuple (On Pin #, PWM Pin #)
       aFreq = max frequency.
       #Example:
       m1 = motor((19, 22), (21, 23))
    """
    self._onf = Pin(aForward[0], Pin.OUT)
    self._forward = PWM(Pin(aForward[1], Pin.OUT))
    self._onb = Pin(aBackward[0], Pin.OUT)
    self._backward = PWM(Pin(aBackward[1], Pin.OUT))
    self._maxfreq = aFreq
    self._speed = 0

  @staticmethod
  def seton( aPin, aOn ) :
    '''Set on/off (free wheeling) state of motor.'''
    aPin.value(1 if aOn else 0)

  @property
  def speed( self ) : return self._speed

  @speed.setter
  def speed( self, aValue ) :
    '''Set velocity and direction of motor with -100 <= aValue <= 100.'''
    self._speed = aValue
    pos = True

    if aValue == 0 :
      motor.seton(self._onb, False)
      motor.seton(self._onf, False)
      return
    elif aValue < 0 :
      aValue = -aValue
      pos = False

    f = self.p2hz(min(100, aValue))
    motor.seton(self._onf, pos)
    motor.seton(self._onb, not pos)
    self._forward.freq(f)
    self._backward.freq(f)

  def p2hz( self, aPerc ) :
    return int((self._maxfreq * aPerc) // 100)

  def brake( self ) :
    """ Brake the motor by sending power both directions, then shut it all down. """
    self._forward.freq(self.p2hz(100))
    self._backward.freq(self.p2hz(100))
    motor.seton(self._onf, True)
    motor.seton(self._onb, True)
    sleep_ms(500)
    self.speed = 0

