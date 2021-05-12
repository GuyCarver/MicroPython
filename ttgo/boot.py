# This file is executed on every boot (including wake-boot from deepsleep)
import sys, network, utime, display
sys.path[1] = '/flash/lib'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('Carvers', 'gruntbuggly')
utime.sleep_ms(4000)
network.telnet.start(user='g', password='g')

#Initialize display in landscape mode at maximum resolution
tft = display.TFT()
tft.init(tft.ST7789, bgr=False, rot=tft.LANDSCAPE, miso=17, backl_pin=4, backl_on=1, mosi=19, clk=18, cs=5, dc=16)
tft.setwin(40, 52, 320, 240)

# import lidar
# lidar.run(tft)

