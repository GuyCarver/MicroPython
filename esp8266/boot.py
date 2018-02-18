# This file is executed on every boot (including wake-boot from deepsleep)

import esp
import gc
import webrepl

esp.osdebug(None)

webrepl.start()
gc.collect()

from main import *



