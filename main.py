# main.py -- put your code here!

# from seriffont import *
#from sysfont import *
# from terminalfont import *
import gc
from time import sleep_ms

print(gc.mem_free())

def reboot(  ) : pyb.hard_reset()
#pyt = 0
#if pyt :
#  from st7735 import makeg
#  t = makeg()
#else:
#  t = pyb.TFT("x", "X1", "X2")
#  t.initg()
#
#t.fill(0)
#
#print(gc.mem_free())

# import tft
# tft.run(t)

# Display animated circle on tft -------------------------

#from bombs import bomber
#t.rotation(2)
#b = bomber(t)
#b.run()

# Accelerometer display ----------------------------------

# import balance
# balance.main()

# Carpenter level display using accelerometer ------------

# from level import Level
# l = Level(t)
# l.run()

# pir motion sensor --------------------------------------

# import motion
# m = motion.motion(t)
# # m.run()

# Cat Treat Thrower --------------------------------------

# import TreatThrower
# tt = TreatThrower.TreatThrower(m)
# tt.run()

# l2082 Motor control ------------------------------------

#from l298n import motor
#m1 = motor('Y1', 'Y2', ('Y3', 4))
# m2 = motor('Y5', 'Y6', ('Y4', 4))

# IR or SR04 distance display ----------------------------

# from irdistance import IRDistance
# r = IRDistance("X12")

# from sr04distance import sr04distance
# r = sr04distance("Y2", "Y1")

# t.rotation(2)
# from distancedisplay import display
# d = display(t, r)
# d.run()

# Bluetooth board ----------------------------------------

# from jymcu import jymcu

# u = jymcu(6, 57600)
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

# WIFI board ----------------------------------------

# from esp8266 import wifi

# v = wifi(6)

# from pyb import Pin
# p = Pin("X11", Pin.IN, Pin.PULL_DOWN)
# def v(): return p.value()

# Accelerometer board ----------------------------------------

#from gy521 import accel
#
print(gc.mem_free())
#
#a = accel(1)
#def d(): return a.acceltemprot
#
#print(gc.mem_free())

#import gyreport
#
#print(gc.mem_free())
#
#m = gyreport.motion(1, t)
#
#print(gc.mem_free())
#
#m.run()
#
#print(gc.mem_free())

#def do( ) :
#  return pyb.MPU6050('x', 0)

#def prnt( dev, font ) :
#  dev.text((10, 10), "Hello!", 1, font, 1)
#  dev.text((10, 30), "Hi Again?", 1, font, 3)

from apds9960 import *
a = apds9960(1)

from oled import oled
from terminalfont import *

o = oled(2)

def check():
  empty = (0,0,0,0)
  while True:
    cr = a.colordataready
    c = a.colordata() if cr else empty
    p = a.proximity()
    v = a.gesturedata()
    g = a.readgesture()
    if v == None :
      v = empty

    o.clear()
    o.text((0, 10), "{:3}".format(p), 1, terminalfont)
#    o.text((0, 20), "{:3}".format(g), 1, terminalfont)
    o.text((0, 20), "{:3} {:3} {:3} {:3}".format(*v), 1, terminalfont)
    o.text((0, 30), "{:3} {:3} {:3} {:3}".format(*c), 1, terminalfont)
    o.display()
    sleep_ms(100)

check()

#b = bytearray(4)
#b[0] = 0x66
#b[1] = 0x66
#b[2] = 0x02
#b[3] = 0x56
#
#u = pyb.UART(1, 115200)
#
#def rd( aData ) :
#  v = u.read(aData)
#  print("-----")
#  for e in v :
#    print("{:02x}".format(e))

#from cjmcu import *
#u = cjmcu(1)
