#Control a relay board.

from pyb import Pin

class relay(object):
  """Control a relay board with an output pin.  Set on to True to drive the relay pin low
     which turns the relay on."""

  def __init__( self, pin ) :
    """Pin may be a pin name or pyb.Pin object set for output."""

    if type(pin) == str:
      self._pin = Pin(pin, Pin.OUT_PP, Pin.PULL_DOWN)
    elif type(pin) == Pin:
      self._pin = pin
    else:
      raise Exception("pin must be pin name or pyb.Pin")

    self.on = False

  @property
  def on( self ) : return self._pin.value()

  @on.setter
  def on( self, value ) :
    if value:
      self._pin.low()
    else:
      self._pin.high()

