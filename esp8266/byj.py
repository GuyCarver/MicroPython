
from machine import Pin

# 28byj stepper motor controller

#2, 0, 4, 5
#WAVE and FULL steps don't really work at less than 500us timing.

class byj(object):
  '''docstring for byj '''

  _STEPANGLE = 5.625
  _RATIO = 64.0
  _ANGH = _STEPANGLE / _RATIO
  _FULLROTATIONH = 360.0 / _ANGH
#  _FULLROTATIONH = 360.0 / _STEPANGLE * _RATIO

  _HALFSTEP = (0x1, 0x3, 0x2, 0x6, 0x4, 0xC, 0x8, 0x9)
  _WAVESTEP = (0x1, 0x2, 0x4, 0x8, 0x1, 0x2, 0x4, 0x8)
  _FULLSTEP = (0x3, 0x6, 0xC, 0x9, 0x3, 0x6, 0xC, 0x9)
  _STEPLEN = len(_HALFSTEP)
  _STEPS = (_HALFSTEP, _WAVESTEP, _FULLSTEP)
  _DEG = (_ANGH, _ANGH * 2.0, _ANGH * 2.0)

  _HALF, _WAVE, _FULL = range(len(_STEPS))

  def __init__( self, aStepType, aPins ):
    super(byj, self).__init__()
    if len(aPins) != 4:
      raise('Need 4 pins')

    self.steptype = aStepType
    self._pins = [Pin(p, Pin.OUT) for p in aPins]
    self._index = 0
    self._direction = 1
    self._angle = 0                             #Angle in degrees.
    self._steps = 0

  @property
  def angle( self ):
    return self._angle

  @angle.setter
  def angle( self, aValue ):
    delta = aValue - self._angle
    self.move(delta)

  def reset( self, aAngle ):
    '''  '''
    self._angle = aAngle

  def move( self, aDelta ):
    '''  '''
    self.direction = aDelta
    self._angle = (self._angle + aDelta) % 360
    self._steps = abs(aDelta) / byj._DEG[self.steptype]

  @property
  def moving( self ): return self._steps > 0

  @property
  def steptype( self ):
    return self._steptype

  @steptype.setter
  def steptype( self, aValue ):
    self._steptype = max(0, min(len(byj._STEPS), aValue))

  @property
  def direction( self ):
    return self._direction

  @direction.setter
  def direction( self, aValue ):
    self._direction = 1 if aValue >= 0 else -1

  def _nextindex( self ):
    #This works as long as _STEPLEN is 8.
    self._index = (self._index + self.direction) & 0x07

  def stop( self ):
    '''  '''
    for p in self._pins:
      p.value(0)

  def _setpins( self, aValue ):
    '''  '''
#    print(aValue)
    for p in self._pins:
      v = aValue & 1
      aValue >>= 1
      p.value(v)

  def update( self, aDT ):
    '''  '''
    if self.moving:
      st = byj._STEPS[self.steptype]
      s = st[self._index]
      self._setpins(s)
      self._nextindex()
      self._steps -= 1;

from utime import sleep_us
def make(aType):
  return byj(aType, (2, 0, 4, 5))

def test( b, aDelay, aAngle ):
  ''' '''
  def domove():
    print(b.angle)
    while b.moving:
      b.update(aDelay)
      sleep_us(aDelay)

  b.angle = aAngle
  domove()
  b.angle -= 45
  domove()
  b.angle += 180
  domove()

def move(b, aDelay, aAngle):
  b.angle = aAngle
  print(b.angle)
  while b.moving:
    b.update(aDelay)
    sleep_us(aDelay)
