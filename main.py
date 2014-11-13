# main.py -- put your code here!

# import TreatThrower
# import Balance

# Balance.main()

# from seriffont import *
# from sysfont import *
from terminalfont import *
# from SonarDisplay import SonarDisplay

pyt = 0

if pyt :
  from ST7735 import makeg
  t = makeg()
else:
  t = pyb.TFT("x", "X1", "X2") #makegp()
  t.initg()

t.fill(0)

import TFT
TFT.run(t)

def tst( aColor ):
  s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-=_+[]{}l;'<>?,./!@#$%^&*():"
#   t.text(Point(0, 0), s, aColor, basicfont)
#   t.text(Point(0, 40), s, aColor, seriffont)
  t.text((0, 40), s, aColor, terminalfont)

# tst(BLUE)

def s(aRot, aColor):
  t.rotation(aRot)
  tst(aColor)

# from bombs import bomber
# t.rotation(2)
# b = bomber(t)
# b.run()

from level import Level
l = Level(t)
l.run()

# sd = SonarDisplay(t, "X3", "X4")
# sd.run()
