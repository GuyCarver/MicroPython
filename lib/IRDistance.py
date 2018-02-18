
from pyb import Pin, ADC

class irdistance(object):
  """ Driver for Sharp Gp2y0a IR distance sensor.  The distance
      range is around 3 to 40 inches. """

  maxinches = 31.5 #Maximun range of IR board in inches.
  _v2i = -1.02 #Voltage to inches power.

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
    volts = self.distance * 0.0048828125
    return 65.0 * pow(volts, IRDistance._v2i)

  @property
  def centimeters( self ) : return self.inches * 2.54

