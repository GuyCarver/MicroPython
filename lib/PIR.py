#Passive infrared motipower sensor.

import pyb

class pir(object):
  '''Passive Infrared Motion Sensor driver.  Supports on/off through an output pin
     trigger reading as well as an interrupt callback on trigger high/low changes.'''

  def __init__(self, power, trigger, callback = None):
    '''Power and trigger pins, optional interrupt callback in the format
       of fun( bOnOff ).  This will be called whenever the trigger state
       changes.'''
    if power != None:
      self._power = pyb.Pin(power, pyb.Pin.OUT_PP)
      self._power.low()
    else:
      self._power = None
    self._trigger = pyb.Pin(trigger, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
    self.interrupt = callback

  def _onoff( self, aTF ) :
    '''Turn device on/off'''
    if (self._power != None):
      if (aTF):
        oldon = self.inton
        self.inton = False  #Make sure interrupt is off while turning on power to avoid false callbacks.
        self._power.high()
        if (oldon):
          pyb.delay(200)     #Need to wait a bit after turning on to make sure we don't get false values.
          self.inton = oldon
      else:
        self._power.low()

  @property
  def power( self ) : return True if (self._power == None) else self._power.value()

  @power.setter
  def power( self, value ) : self._onoff(value)

  def on( self ) : self.power = True
  def off( self ) : self.power = False

  @property
  def trigger( self ) : return self._trigger.value()

  @property
  def interrupt( self ) : return self._interrupt

  @interrupt.setter
  def interrupt( self, func ) :
    self._interrupt = None;
    self._func = func
    if (func != None):
      self._interrupt = pyb.ExtInt(self._trigger, pyb.ExtInt.IRQ_RISING_FALLING, pyb.Pin.PULL_DOWN, self._inthandler)
      self._inton = True

  def _inthandler( self, line ) :
    '''Function to handle interrupts and pass on to callback with on/off trigger state.'''
    if (self._func != None):
      self._func(self.trigger)

  @property
  def inton( self ) : return self._inton

  @inton.setter
  def inton( self, value ) :
    self._inton = value
    if self._interrupt != None:
      if value :
        self._interrupt.enable()
      else:
        self._interrupt.disable()
