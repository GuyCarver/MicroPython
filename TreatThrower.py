# Control bot that throws treats using a servo

import pyb
import motion

class TreatThrower(object):
  """Watch for trigger and throw treat using servo
     when trigger is activated."""

  servoCenter = 1440
  servoSpeed = 100
  servoTime = 1450
  ledNum = 3

  def __init__( self, sensor, servonum = 3 ) :
    self._sensor = sensor
    self._servo = pyb.Servo(servonum)
    mn, mx, _, a, s = self._servo.calibration()
    self._servo.calibration(mn, mx, TreatThrower.servoCenter, a, s)
    self._servo.speed(0)
    self._led = pyb.LED(TreatThrower.ledNum)

  def runservo( self, time ) :
    '''Run the servo for the given time.'''
    self._servo.speed(TreatThrower.servoSpeed)
    pyb.delay(time)
    self._servo.speed(0)

  def throwit( self ):
    self._led.on()
    self.runservo(TreatThrower.servoTime)
    self._led.off()
    while(self._sensor.trigger):
      pass

  def adjust( self, time = 50 ) :
    '''Adjust the servo position by running the servo
       for the given amount of time.'''
    for i in range(step) :
      self.runservo(50)

  def run( self ) :
    sw = pyb.Switch()
    while(not sw()):
      if self._sensor.trigger:
        self.throwit()
      pyb.delay(20)

