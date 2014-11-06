# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
from ST7735 import *

#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('CDC+MSC') # act as a serial and a storage device
#pyb.usb_mode('CDC+HID') # act as a serial device and a mouse
