
import esp
import network
from time import sleep_ms

def init_ap(  ) :
  ap_if = network.WLAN(network.AP_IF)
  ap_if.active(True)
  ap_if.config(essid="ESP32-2")

  print('{} access point: {}'.format(ap_if.config('essid'), ap_if.ifconfig()[0]))

def connect(  ) :
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected() :
    print('Connecting to Carvers')
    sta_if.active(True)
    sta_if.connect('Carvers', 'gruntbuggly')
    counter = 0
    while not sta_if.isconnected() and counter < 20 :
      sleep_ms(500)
      counter += 1

  print('network ip: ', sta_if.ifconfig()[0])

def no_debug():
  # this can be run from the REPL as well
  esp.osdebug(None)

from machine import PS2

def test(  ):
  ''' '''
  p = PS2(23, 19, 18, 5)

  def cb( ind, status ) :
    inname = p.inputname(ind)
    if status & 2 :
      statname = 'pressed' if status == 3 else 'released'
      print(inname + ': ' + statname)

  p.callback(cb)

  while 1:
    p.update()
    sleep_ms(100)
