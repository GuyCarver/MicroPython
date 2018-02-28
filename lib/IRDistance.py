
from pyb import Pin, ADC

class irdistance(object):
  """ Driver for Sharp Gp2y0a IR distance sensor.  The distance
      range is around 3 to 40 inches. """

  def __init__( self, pin ) :
    """pin may be name or pin object.  It must be able to handle ADC input."""

    if type(pin) == str:
      p = Pin(pin)
    elif type(pin) == Pin:
      p = pin
    else:
      raise Exception("pin must be pin name or pyb.Pin able to support ADC")

    self._adc = ADC(p)

  @property
  def distance( self ) : return self._adc.read()

  @property
  def inches( self ) :
    #distance / 204.8?  Why?
    volts = self.distance * 0.0048828125
    #inches = v^-1.02.
    return 65.0 * pow(volts, -1.02)

  @property
  def centimeters( self ) : return self.inches * 2.54

