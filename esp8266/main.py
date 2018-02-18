
import network

def report(  ) :
  sta_if = network.WLAN(network.STA_IF)
  if sta_if.isconnected() :
    print('network ip: ', sta_if.ifconfig()[0])
  else:
    print("no network connection.")

  ap_if = network.WLAN(network.AP_IF)
  if ap_if.active() :
    print('{} access point: {}'.format(ap_if.config('essid'), ap_if.ifconfig()[0]))
  else:
    print("Access point not active.")

from mlx90614 import *
m = mlx(14, 12)

from oled import *
from terminalfont import *
o = oled(4, 0)

def display(  ) :
  pos1 = (0, 0)
  pos2 = (0, terminalfont['Height'] + 2)
  while True :
    t1 = c2f(m.temp())
    t2 = c2f(m.objecttemp())
    o.clear()
    s = "amb: {:.2f}".format(t1)
    o.text(pos1, s, 1, terminalfont)
    s = "obj: {:.2f}".format(t2)
    o.text(pos2, s, 1, terminalfont)
    o.display()
    time.sleep_ms(100)

display()
