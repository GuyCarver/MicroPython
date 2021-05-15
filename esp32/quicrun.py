# Controller for the quicrun 1060 Electronic Speed Control (ESP)
#This controller works through the pca9865 servo controller.

from time import sleep_ms

#todo: May need to move speed values over time if the battery cannot handle it.

class quicrun(object):
  '''docstring for quicrun'''
  _STOP = const(50)
  _FORWARD_MAX = const(68)
  _FORWARD_MIN = const(52)
  _BACKWARD_MAX = const(30)
  _BACKWARD_MIN = const(48)
  _BACKWARD_INIT = const(45)

  @staticmethod
  def getperc( aMin, aMax, aPerc  ) :
    return (((aMax - aMin) * aPerc) // 100) + aMin

  def __init__(self, aPCA, aIndex):
    '''aPCA = pca9865 object to use for PWM control of the ESC.
       aIndex = Servo index on pca9865 (0-15).
    '''
    super(quicrun, self).__init__()
    self._pca = aPCA
    self._index = aIndex
    self.reset()

  def reset( self ) :
    self._pca.set(self._index, 75)
    sleep_ms(500)
    self._pca.set(self._index, 100)
    sleep_ms(500)
    self._pca.set(self._index, _STOP)
    self._curspeed = 0

  def _set( self, aValue ) :
    self._pca.set(self._index, aValue)

  def _reverse( self ) :
    if self._currspeed >= 0 :
      self._set(_STOP)
      sleep_ms(100)
      self._set(_BACKWARD_INIT)
      sleep_ms(100)
      self._set(_STOP)
      sleep_ms(100)

  def speed( self, aSpeed ) :
    '''Set speed -100 to 100.'''
    aSpeed = max(min(100, aSpeed), -100)

    if aSpeed == 0 :
      self._set(_STOP)
    else:
      if aSpeed > 0 :
        self._set(quicrun.getperc(_FORWARD_MIN, _FORWARD_MAX, aSpeed))
      else:
        self._reverse()
        self._set(quicrun.getperc(_BACKWARD_MAX, _BACKWARD_MIN, 100 + aSpeed))

    self._currspeed = aSpeed

