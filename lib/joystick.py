import pyb

class joystick(object) :
  _X_CENTER = 2084.0
  _Y_CENTER = 2114.0
  _POS_X = 4095.0 - _X_CENTER
  _POS_Y = 4095.0 - _Y_CENTER

  def __init__( self, aX, aY, aB ) :
    self._jx = pyb.ADC(aX)
    self._jy = pyb.ADC(aY)
    #PULL_DOWN doesn't report button press, need to use pull up resistor.
    self._js = pyb.Pin(aB, pyb.Pin.IN, pyb.Pin.PULL_UP)

    self._x = 0.0
    self._y = 0.0
    self._button = False

    self._index = 0
    self._xA = [0, 0, 0]
    self._yA = [0, 0, 0]

  @property
  def x( self ) :
    '''Return value from -1.0 to 1.0.'''
    return self._x

  @property
  def y( self ) :
    '''Return value from -1.0 to 1.0.'''
    return self._y

  @property
  def button( self ) :
    '''return True or False.'''
    return self._button

  def update( self ) :
    self._xA[self._index] = self._jx.read()
    self._yA[self._index] = self._jy.read()

    self._index += 1
    if self._index >= 3 :
      self._index = 0

    rx = float(sum(self._xA)) / 3.0 - joystick._X_CENTER
    ry = float(sum(self._yA)) / 3.0 - joystick._Y_CENTER
    dx = joystick._POS_X if rx >= 0 else joystick._X_CENTER
    dy = joystick._POS_Y if ry >= 0 else joystick._Y_CENTER
    self._x = rx / dx
    self._y = ry / dy

    #Button in pressed when value is 0.
    self._button = not self._js.value()

