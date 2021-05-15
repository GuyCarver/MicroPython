
from machine import Pin
from time import sleep_ms

class cattest(object):
  '''docstring for cattest'''
  _LEDPINS = (2, 0, 4, 5)
  _SWITCHONPIN = 1
  _SWITCHPINS = (15, 13, 12, 10)


  def __init__( self ):
    super(cattest, self).__init__()

    self._leds = [Pin(p, Pin.OUT) for p in cattest._LEDPINS]
    self._switches = [Pin(p, Pin.IN) for p in cattest._SWITCHPINS]
#    self._switchon = Pin(cattest._SWITCHONPIN, Pin.OUT)

  def updateleds( self ):
    '''  '''
    for i, s in enumerate(self._switches):
      self._leds[i].value(s.value())

  def read( self, ind ):
    return self._switches[ind].value()

  def run( self ):
    '''  '''
    while(1):
      self.updateleds()
      sleep_ms(100)