# main.py -- put your code here!

# from seriffont import *
# from sysfont import *
# from terminalfont import *
pyt = 0
if pyt :
  from ST7735 import makeg
  t = makeg()
else:
  t = pyb.TFT("x", "X1", "X2")
  t.initg()

# t.fill(0)

# import TFT
# TFT.run(t)

# Display animated circle on TFT -------------------------

# from bombs import bomber
# t.rotation(2)
# b = bomber(t)
# b.run()

# Accelerometer display ----------------------------------

# import Balance
# Balance.main()

# Carpenter level display using accelerometer ------------

# from level import Level
# l = Level(t)
# l.run()

# PIR motion sensor --------------------------------------

# import motion
# m = motion.motion(t)
# # m.run()

# Cat Treat Thrower --------------------------------------

# import TreatThrower
# tt = TreatThrower.TreatThrower(m)
# tt.run()

# L2082 Motor control ------------------------------------

# from L298N import Motor
# m1 = Motor('Y1', 'Y2', ('Y3', 4))
# m2 = Motor('Y5', 'Y6', ('Y4', 4))

# IR or SR04 distance display ----------------------------

# from IRDistance import IRDistance
# r = IRDistance("X12")

# from SR04Distance import SR04Distance
# r = SR04Distance("Y2", "Y1")

# t.rotation(2)
# from DistanceDisplay import Display
# d = Display(t, r)
# d.run()

# Bluetooth board ----------------------------------------

# from JYMCU import JYMCU

# u = JYMCU(6, 57600)
# u.write("Testing.")
# u.readline()
# u.setrepl()

# from pyb import ExtInt

# x = 0
# def cb(line):
#   global x
#   x += 1
#   print(x)

# f = ExtInt("Y2", ExtInt.IRQ_RISING, pyb.Pin.PULL_UP, cb)

from ESP8266 import WIFI

v = WIFI(6)

from pyb import Pin
p = Pin("X11", Pin.IN, Pin.PULL_DOWN)
def v(): return p.value()
