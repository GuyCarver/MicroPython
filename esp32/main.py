
import esp
import network

def connect():
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected() :
    print('Connecting to Carvers')
    sta_if.active(True)
    sta_if.connect('Carvers', 'gruntbuggly')
    while not sta_if.isconnected():
      pass
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid="ESP32-1")
  print('network ip: ', sta_if.ifconfig()[0])
  print('{} access point: {}'.format(ap_if.config('essid'), ap_if.ifconfig()[0]))

def no_debug():
  # this can be run from the REPL as well
  esp.osdebug(None)
