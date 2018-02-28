# PWM driver.

from pyb import Timer, Pin

class pwm(object):
  """Class to help with PWM pin and clock initialization."""

  #Dict pin name: timer #, channel #.
  PinChannels = {
    'X1': [(2,1), (5,1)],
    'X2': [(2,2), (5,2)],
    'X3': [(2,3), (5,3), (9,1)],
    'X4': [(2,4), (5,4), (9,2)],
    'X6': [(2,1), (8,1)],
    'X7': [(13, 1)],
    'X8': [(1,1), (8,1), (14,1)],
    'X9': [(4,1)],
    'X10': [(4,2)],
    'Y1': [(8,1)],
    'Y2': [(8,2)],
    'Y3': [(4,3), (10,1)],
    'Y4': [(4,4), (11,1)],
    'Y6': [(1,1)],
    'Y7': [(1,2), (8,2), (12,1)],
    'Y8': [(1,3), (8,3), (12,2)],
    'Y9': [(2,3)],
    'Y10': [(2,4)],
    'Y11': [(1,2), (8,2)],
    'Y12': [(1,3), (8,3)]
  }

  class PWMException(Exception):
      def __init__( self, msg ) :
          self.msg = msg

  @staticmethod
  def timerandchannel( pinname, timernum ) :
    try:
      a = pwm.PinChannels[pinname]
      if timernum <= 0:
        return a[0]
      else:
        for v in a:
          if v[0] == timernum:
            return v
    except Exception as e :
      raise pwm.PWMException("Pin {} cannot be used for PWM".format(pinname))

    raise pwm.PWMException("Pin {} cannot use timer {}".format(pinname, timernum))

  def __init__( self, aPin, timernum, afreq = 100 ) :
    '''aPin may be a pyb.Pin or a pin name.
       timernum must be a number corresponding to the given pin.
       afreq is the frequency for the PWM signal.
    '''
    isname = type(aPin) == str
    pinname = aPin if isname else aPin.name()
    timernum, channel = pwm.timerandchannel(pinname, timernum)
    if isname:
      aPin = Pin(pinname)

    self._timer = Timer(timernum, freq = afreq)
    self._channel = self._timer.channel(channel, Timer.PWM, pin = aPin)

  @property
  def pulse_width( self ) : return self._channel.pulse_width()

  @pulse_width.setter
  def pulse_width( self, value ) : self._channel.pulse_width(value)

  @property
  def pulse_width_percent( self ) : return self._channel.pulse_width_percent()

  @pulse_width_percent.setter
  def pulse_width_percent( self, value ) : self._channel.pulse_width_percent(value)

  @property
  def freq( self ) : return self._timer.freq()

  @freq.setter
  def freq( self, value ) : self._timer.freq(value)

  def callback( self, value ) :
    self._channel.callback(value)

