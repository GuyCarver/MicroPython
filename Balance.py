# Control bot that throws treats using a servo

import pyb

servoNums = [1, 2]
ledNum = 3

def pitchtoangle( aPitch ):
  return aPitch * 90 / 32

def setservo( aServo, aPitch ):
  aServo.angle(pitchtoangle(aPitch))

def main(  ) :
  a = pyb.Accel()
  pitches = [ a.x, a.y ]
  servos = [ pyb.Servo(sn) for sn in servoNums ]
  curangles = [-100, -100]

#   mn, mx, _, a, s = s1.calibration()
#   s1.calibration(mn, mx, servoCenter, a, s)
#   s1.speed(0)

  l = pyb.LED(ledNum)
  sw = pyb.Switch()

  while(1):
    if sw():
      break;
    for i in range(len(pitches)):
      p = pitches[i]()
      if curangles[i] != p:
        curangles[i] = p
        setservo(servos[i], p)
    pyb.delay(20)

if __name__ == '__main__':
  main()
