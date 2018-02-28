
from pyb import Pin, Timer, udelay

# WARNING: Should place a 1k resistor on the echo pin.

class sr04distance(object):
  """Driver for SR05 sonic distance sensor.  """

#  _MAXINCHES = const(20) #maximum range of SR04.

  def __init__( self, tpin, epin, timer = 2 ) :
    '''tpin = Timer pin.
       epin = Echo pin.
       timer = Timer #.
    '''

    if type(tpin) == str:
      self._tpin = Pin(tpin, Pin.OUT_PP, Pin.PULL_NONE)
    elif type(tpin) == Pin:
      self._tpin = tpin
    else:
      raise Exception("trigger pin must be pin name or pyb.Pin configured for output.")

    self._tpin.low()

    if type(epin) == str:
      self._epin = Pin(epin, Pin.IN, Pin.PULL_NONE)
    elif type(epin) == Pin:
      self._epin = epin
    else:
      raise Exception("echo pin must be pin name or pyb.Pin configured for input.")

    # Create a microseconds counter.
    self._micros = Timer(timer, prescaler = 83, period = 0x3fffffff)

  def __del__( self ) :
    self._micros.deinit()

  @property
  def counter( self ) :
    return self._micros.counter()

  @counter.setter
  def counter( self, value ) :
    self._micros.counter(value)

  @property
  def centimeters( self ) :
    '''Get # of centimeters distance sensor is reporting.'''
    start = 0
    end = 0

    self.counter = 0

    #Send 10us pulse.
    self._tpin.high()
    udelay(10)
    self._tpin.low()

    while not self._epin.value():
      start = self.counter

    j = 0

    # Wait 'till the pulse is gone.
    while self._epin.value() and j < 1000:
      j += 1
      end = self.counter

    # Calc the duration of the recieved pulse, divide the result by
    # 2 (round-trip) and divide it by 29 (the speed of sound is
    # 340 m/s and that is 29 us/cm).
    return (end - start) / 58.0

  @property
  def inches( self ) :
    #Get distance in inches.
    return self.centimeters * 0.3937

