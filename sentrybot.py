#SentryBot control prototype.

#todo: Rotate head to max range
#  if head hits torso turn range, rotate torso
#  Do same for tilt.

#todo: May need to smooth out input.  Simple way is to average n values (3?)

#todo: May need to ease in/out of movement in addition to time scaling.

import pyb
from pca9865 import pca9865
import joystick

def moveto( aSource, aTarget, aRate ) :
  '''Move from aSource to aTarget by given rate.'''
  if aTarget < 0 :
    aSource = aTarget
  else:
    diff = (aTarget - aSource) * aRate
    aSource += diff
    if diff < 0 :
      aSource = max(aSource, aTarget)
    else:
      aSource = min(aSource, aTarget)

  return aSource

def clamp( aValue, aRange ) :
  '''Clamp value between +/- aRange.'''
  s = -1.0 if aValue < 0.0 else 1.0
  aValue = min(abs(aValue), aRange)
  return aValue * s

def smooth( aValue ) :
  '''If value isn't above a certain threshold just return 0.0'''
  return aValue if abs(aValue) > 0.2 else 0.0

class bot(pca9865) :
  _HEAD_TURN_RANGE = 45.0
  _HEAD_TILT_RANGE = 20.0
  _HEAD_TILT_CENTER = -90.0 + _HEAD_TILT_RANGE
  _TORSO_TURN_START = 30.0
  _TORSO_TURN_RANGE = 85.0
  _TORSO_TILT_START = 10.0
  _TORSO_TILT_RANGE = 10.0
  _TORSO_TILT_CENTER = -90.0 + _TORSO_TILT_RANGE
  _WHEEL_TURN_START = 80.0

  #Center value % for wheels.
  _LEFT_WHEEL_CENTER = -9.0 #45.0% = 81.0 deg or -9.0 if +/- 90.0
  _RIGHT_WHEEL_CENTER = -4.0 #48.0% = 86.4 deg or -4.0 if +/- 90.0

  _pcaloc = const(2)

  #Servo indexes.
  _ttwist = const(0)
  _ttilt = const(1)
  _htwist = const(2)
  _htilt = const(3)
  _lwheel = const(4)
  _rwheel = const(5)

  _updatefreq = const(16) #ms = 60hz.

  #torso twist, tilt, head twist, tilt, l wheel, r wheel.
  _servopinA = [12, 13, 14, 15, 8, 9]
  #turn rate in degrees/second.
  _servorateA = [66.0, -33.0, 66.0, -33.0, 11.0, 11.0]
  _servocenterA = [0.0, _TORSO_TILT_CENTER, 0.0, _HEAD_TILT_CENTER, _LEFT_WHEEL_CENTER, _RIGHT_WHEEL_CENTER]

  def __init__( self ) :
    super().__init__(_pcaloc)  #init PCA 9865
    self._joystick = joystick.joystick(pyb.Pin.board.Y11, pyb.Pin.board.Y12, pyb.Pin.board.X8)
    #Values +/-90 deg.  -100 = off.
    self._servoA = [0.0, -bot._TORSO_TILT_RANGE, 0.0, 0.0, 0.0, 0.0]
    self._time = pyb.millis()
    self.updateservos()

  def updateservos( self ) :
    '''Iterate through all servo angles and write to servo.'''
    for i, s in enumerate(self._servoA) :
      a = bot._servocenterA[i] + s
      self.setangle(bot._servopinA[i], a)

  def updatehead( self, aDT ) :
    '''Update movement from joystick.  aDT is seconds passed since last update.'''
    x = self._joystick.x
    y = self._joystick.y

    #Get turn/tilt rate for head.
    turn = x * bot._servorateA[_htwist] * aDT
    tilt = y * bot._servorateA[_htilt] * aDT

    #Move turn/tilt by the desired rate from the joystick input.
    h = clamp(self._servoA[_htwist] + turn, bot._HEAD_TURN_RANGE)
    self._servoA[_htwist] = h
    self._servoA[_htilt] = clamp(self._servoA[_htilt] + tilt, bot._HEAD_TILT_RANGE)

    #Now get the turn rate for torso.
    turn = x * bot._servorateA[_ttwist] * aDT

    th = self._servoA[_ttwist]

    #If head turn is > torso turn start angle and moving in the right direction then update torso turn.
    if abs(h) >= bot._TORSO_TURN_START and h * turn > 0 :
      th = clamp(th + turn, bot._TORSO_TURN_RANGE)
      self._servoA[_ttwist] = th

    lw = -1000.0
    rw = -1000.0

    if abs(th) >= bot._WHEEL_TURN_START and th * turn > 0 :
      lw = bot._servorateA[_lwheel]
      if th < 0 :
        lw = -lw

      rw = lw

    self._servoA[_lwheel] = lw
    self._servoA[_rwheel] = rw

  def updatetime( self ) :
    '''Update the time, then return delta time in seconds.'''
    delay = 1

    #Loop until we hit or exceed the target frame rate.
    while delay > 0 :
      ms = pyb.millis()
      dt = ms - self._time
      delay = _updatefreq - dt

      #If we need to wait longer then do so.
      if delay > 0 :
        pyb.delay(delay)

    self._time = ms
    return dt / 1000.0  #Convert ms to seconds.

  def update( self ) :
    dt = self.updatetime()

    #Read input and convert to rotations.
    self._joystick.update()

    #todo: Move wheels based on what input?

    #Apply rotations to head and torso.
    self.updatehead(dt)
    #Write values to the servos.
    self.updateservos()

def run(  ) :
  b = bot()
  while True :
    b.update()



