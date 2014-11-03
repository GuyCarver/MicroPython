# Control bot that throws treats using a servo

import pyb

servoNum = 1
servoCenter = 1440
servoSpeed = 100
servoTime = 1450
ledNum = 3
triggerInput = 'X3'

def runservo( aServo, aSpeed, aDelay ):
  aServo.speed(aSpeed)
  pyb.delay(aDelay)
  aServo.speed(0)

def main(  ) :
  s1 = pyb.Servo(servoNum)
  btn = pyb.Pin(triggerInput, pyb.Pin.IN, pyb.Pin.PULL_UP)
  mn, mx, _, a, s = s1.calibration()
  s1.calibration(mn, mx, servoCenter, a, s)
  s1.speed(0)
  l = pyb.LED(ledNum)

  def throwit(  ):
    l.on()
    runservo(s1, servoSpeed, servoTime)
    l.off()

  sw = pyb.Switch()
#  sw.callback(throwit)

  while(1):
    if (btn.value() == 0):
      throwit()
    if sw():
      break;
    pyb.delay(20)

if __name__ == '__main__':
  main()
