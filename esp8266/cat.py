#cat trainer and treat dispenser.

from machine import Pin, PWM
from time import sleep_ms
from uos import urandom

class cat(object):
  '''Control activation of triggers and LEDs, look for input and dispense a treat
       as a result.  The LED indicates which switch is active.  If that switch is
       triggered, a treat is dispensed and a new switch is activated.'''

  _LEDPINS = (2, 0, 4, 5)
  _SWITCHPINS = (15, 13, 12, 10)
  _SERVOPIN = 14
  _RANDOMCOUNT = 256
  _UPVALUE = 10
  _DOWNVALUE = 60
  _UPDOWNPAUSE = 300
  _DELAYTIME = 500  #Delay for 5 seconds between switch activations.

  def __init__( self ):
    super(cat, self).__init__()

    rs = urandom(cat._RANDOMCOUNT)
    div = 255 / len(cat._LEDPINS)
    #Create array of random indexes for the LED/switches.
    self._randoms = [0 for r in rs] #int(r / div) for r in rs]
    self._randindex = 0

    self._active = -1
    self._delay = 0

    self._leds = [Pin(p, Pin.OUT) for p in cat._LEDPINS]
    self._switches = [Pin(p, Pin.IN) for p in cat._SWITCHPINS]

    self._servo = PWM(Pin(cat._SERVOPIN), freq = 50)
    self._servo.duty(cat._DOWNVALUE)
    self._prev = 0

    self.next() #Pick 1st active LED/switch.

  def noactive( self ):
    ''' Turn all LED/switches off. '''
    self._active = -1
    self.updateleds()

  def updateleds( self ):
    ''' Update LED to turn the correct one on. '''
    for i, l in enumerate(self._leds):
      l.value(1 if i == self._active else 0)

  def next( self ):
    ''' Pick a new switch/LED to make active. '''
    self._active = self._randoms[self._randindex]
    self._randindex += 1
    if self._randindex >= len(self._randoms):
      self._randindex = 0

    self.updateleds()

  def dispense( self ):
    ''' Dispense a treat and pick a new active switch. '''
    self._servo.duty(cat._UPVALUE)
    sleep_ms(cat._UPDOWNPAUSE)
    self._servo.duty(cat._DOWNVALUE)
    self._delay = cat._DELAYTIME
    self.noactive()

  def check( self ):
    ''' Check to see if switch was hit and released. '''
    v = self._switches[self._active].value()
    if v != self._prev:
      if v == 0: #If the switch isn't touched, but it was before.
        print('dispense')
        self.dispense()
      self._prev = v

  def run( self ):
    '''Main loop for cat treat dispenser.'''
    while 1:
      if self._delay:
        self._delay -= 100
        if self._delay <= 0:
          self.next()
          self._delay = 0
      else:
        self.check()

      sleep_ms(100)


