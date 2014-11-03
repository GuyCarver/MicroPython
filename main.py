# main.py -- put your code here!

# import TreatThrower
# import Balance

# Balance.main()

from basicfont import *
from seriffont import *
from terminalfont import *
from bombs import bomber
from level import Level

t = makeg()

def tst( aColor ):
  s = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-=_+[]{}l;'<>?,./!@#$%^&*():"
  t.drawstring(Point(0, 0), s, aColor, basicfont)
  t.drawstring(Point(0, 40), s, aColor, seriffont)
  t.drawstring(Point(0, 80), s, aColor, terminalfont)

# tst(BLUE)

def s(aRot, aColor):
  t.setrotation(aRot)
  tst(aColor)

# b = bomber(t)
t.setrotation(2)
l = Level(t)
l.run()
