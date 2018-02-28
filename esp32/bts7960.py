
#Driver for the bts7960 43A high power motor controller.

from machine import Pin, PWM
from utime import sleep_ms

class motor(  ):
  '''Control a motor connected to the bts7960 motor controller.'''

  _MAXDUTY = const(1023)

  def __init__( self, aForward, aBackward, aFreq = 100 ) :
    '''aForward = tuple (On Pin #, PWM Pin #)
       aBackward = tuple (On Pin #, PWM Pin #)
       aFreq = PWM freq.
       #Example:
       m1 = motor((19, 22), (21, 23))
    '''
    self._onf = Pin(aForward[0], Pin.OUT)
    self._forward = PWM(Pin(aForward[1], Pin.OUT))
    self._onb = Pin(aBackward[0], Pin.OUT)
    self._backward = PWM(Pin(aBackward[1], Pin.OUT))
    self._freq = aFreq
    self._speed = 0

  @staticmethod
  def seton( aPin, aOn ) :
    '''Set on/off (free wheeling) state of motor.'''
    aPin.value(1 if aOn else 0)

  @property
  def frequency( self ) :
    return self._freq

  @frequency.setter
  def frequency( self, aValue ) :
    '''Set frequency for forward/backward PWM pins.'''
    self._freq = aValue
    self._forward.freq(self._freq)
    self._backward.freq(self._freq)

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

    motor.seton(self._onf, pos)
    motor.seton(self._onb, not pos)
    duty = (min(100, aValue) * _MAXDUTY) // 100
    self._forward.duty(duty)
    self._backward.duty(duty)

  def brake( self ) :
    '''Brake the motor by sending power both directions, then shut it all down.'''
    self._forward.duty(_MAXDUTY)
    self._backward.duty(_MAXDUTY)
    motor.seton(self._onf, True)
    motor.seton(self._onb, True)
    sleep_ms(500)
    self.speed = 0

