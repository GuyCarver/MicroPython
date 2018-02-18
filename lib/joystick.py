import pyb

class joystick(object) :
  _x_center = 2084.0
  _y_center = 2114.0
  _pos_x = 4095.0 - _x_center
  _pos_y = 4095.0 - _y_center

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

    rx = float(sum(self._xA)) / 3.0 - joystick._x_center
    ry = float(sum(self._yA)) / 3.0 - joystick._y_center
    dx = joystick._pos_x if rx >= 0 else joystick._x_center
    dy = joystick._pos_y if ry >= 0 else joystick._y_center
    self._x = rx / dx
    self._y = ry / dy

    #Button in pressed when value is 0.
    self._button = not self._js.value()

