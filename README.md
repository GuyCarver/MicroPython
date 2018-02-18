# My MicroPython repository

## Contents

###lib directory

* apds9960 - Proximity/Motion/Color sensor using I2C interface.  Gesture reporting is not yet complete.
* jcmcu - Temperature sensor using mlx90614 with a serial interface.
* ds3231 - Battery backup clock with I2C interface.  Ties data from ds3231 with pyb.RTC.
* esp8266 - Interface PyBoard with an esp8266 as an external wifi interface with serial connection.  Connection can be a bit flaky.
* gy521 - Driver for gy-521 accelerometer using I2C communication.
* irdistance - Driver for Sharp gp2y0a IR distance sensor using ADC pin.
* joystick - Hilitchi 2pcs Arduino compatible Biaxial Button Joystick Sensor Module.
* jymcu - Driver for JY-MCU Bluetooth board using serial connection.
* l298n - Driver for L298N Dual HBridge Motor Controller.
* mlx90614 - Driver for IR temperature sensor using I2C communication. NOTE: Mine don't work on PyBoard but do on ESP32 and ESP8266.  I suspect the pull up resistors on my mlx90614 breakout are the cause.  A raw mlx90614 would probably work.
* oled - Driver for diymall 9.6 oled display using I2C communication. NOTE: While this works I implemented this in C and included it in the MicroPython OS to improve performance.
* pca9865 - Driver for pca9865 16 servo controller using I2C communication.
* pir - Driver for passive infrared motion detector.
* pwm - wrapper for easier pwm use.
* relay - Driver for my relay board.
* seriffont, sysfont and terminalfont - Fonts used by ST7735 and oled.  NOTE: My C implementations of those drivers use a default petme128_8x8 font included in the OS.
* sr04distance - Driver for the SR04 sonic distance sensor.
* ST7735 - Sainsmart LCD display driver.  While this works, I implemented this in C and included in the MicroPython OS to improve performance.
* tm1637 - Driver for the tm1637 quad 7-segment LED display.

##ESP32
* modules used on ESP32 running MicroPython.

##ESP8266
* modules used on ESP8266 running MicroPython.

##root directory
* bombs - render test for ST7735
* motion - PIR sensor interupt test to display a message on motion detection.
* tft - Tests for ST7735
