#LED testing.

from pyb import *

dC = 5

def test(  ):
  l = LED(4)
  for i in range(255):
    l.intensity(i)
    delay(dC)
  for i in range(255, 0, -1):
    l.intensity(i)
    delay(dC)
  l.off()
