# Driver for ds3231 clock.

import pyb, utime

def bcd2dec(bcd):
  return (((bcd & 0xF0) >> 4) * 10 + (bcd & 0x0F))

def dec2bcd(dec):
  tens, units = divmod(dec, 10)
  return (tens << 4) + units

class ds3231(object):
  _ADDRESS = 0x68
  _SECONDS = const(0)
  _MINUTES = const(1)
  _HOURS = const(2)
  _WEEKDAY = const(3)
  _DAY = const(4)
  _MONTH = const(5)
  _YEAR = const(6)

  def __init__( self, aLoc ) :
    """aLoc I2C pin location is either 1 for 'X' or 2 for 'Y'."""
    self.rtc = pyb.RTC()
    self.i2c = pyb.I2C(aLoc, pyb.I2C.MASTER)
    self._buffer = bytearray(7)
    self.time(True)

  def time( self, Set = False ) :
    if Set:
      data = self.wait()
    else:
      data = self.i2c.mem_read(self._buffer, self._ADDRESS, 0)
    s = bcd2dec(data[_SECONDS])
    m = bcd2dec(data[_MINUTES])
    if data[_HOURS] & 0x40 :
      h = bcd2dec(data[_HOURS] & 0x1F)
      if data[_HOURS] & 0x20:
        h += 12
    else:
      h = bcd2dec(data[_HOURS])
    wd = data[_WEEKDAY]
    day = bcd2dec(data[_DAY])
    month = bcd2dec(data[_MONTH] & 0x1F)
    year = bcd2dec(data[_YEAR])
    #Month value MSB indicates century.
    if data[_MONTH] & 0x80:
      year += 2000
    else:
      year += 1900

    if Set:
      self.rtc.datetime((year, month, day, wd, h, m, s, 0))

    return (year, month, day, h, m, s, wd - 1, 0) # Time from DS3231 in time.time() format (less yday)

  def _set( self, data ) :
    (year, month, day, wday, h, m, s, subsecs) = data
    self.i2c.mem_write(dec2bcd(s), self._ADDRESS, _SECONDS)
    self.i2c.mem_write(dec2bcd(m), self._ADDRESS, _MINUTES)
    self.i2c.mem_write(dec2bcd(h), self._ADDRESS, _HOURS)       # Sets to 24hr mode
    self.i2c.mem_write(dec2bcd(wday), self._ADDRESS, _WEEKDAY)  # 1 == Monday, 7 == Sunday
    self.i2c.mem_write(dec2bcd(day), self._ADDRESS, _DAY)
    if year >= 2000:
      self.i2c.mem_write(dec2bcd(month) | 0b10000000, self._ADDRESS, _MONTH)
      self.i2c.mem_write(dec2bcd(year - 2000), self._ADDRESS, _YEAR)
    else:
      self.i2c.mem_write(dec2bcd(month), self._ADDRESS, _MONTH)
      self.i2c.mem_write(dec2bcd(year - 1900), self._ADDRESS, _YEAR)

  def save( self ) :
    '''Save rtc time to the device.'''
    self._set(self.rtc.datetime())

  def delta( self ) :
    self.wait()
    ms = self.now()
    ut = utime.mktime(self.time())
    return ms - 1000 * ut

  def wait( self ) :
    '''Wait for a 1 second change in time.'''
    data = self.i2c.mem_read(self._buffer, self._ADDRESS, 0)
    s = data[_SECONDS]
    while s == data[_SECONDS]:
      data = self.i2c.mem_read(self._buffer, self._ADDRESS, 0)
    return data

# Get calibration factor for Pyboard RTC. Note that the DS3231 doesn't have millisecond resolution so we
# wait for a seconds transition to emulate it.
# This function returns the required calibration factor for the RTC (approximately the no. of ppm the
# RTC lags the DS3231).
# Delay(min) Outcome (successive runs). Note 1min/yr ~= 2ppm
#   5 173 169 173 173 173
#  10 171 173 171
#  20 172 172 174
#  40 173 172 173 Mean: 172.3
# Note calibration factor is not saved on power down unless an RTC backup battery is used. An option is
# to store the calibration factor on disk and issue rtc.calibration(factor) on boot.

  def getcal( self, minutes = 5 ) :
    self.rtc.calibration(0)                      # Clear existing cal
    self.save()                                 # Set DS3231 from RTC
    self.wait()                                 # Wait for DS3231 to change: on a 1 second boundary
    tus = pyb.micros()
    st = self.rtc.datetime()[7]
    while self.rtc.datetime()[7] == st:         # Wait for RTC to change
      pass
    t1 = pyb.elapsed_micros(tus)                # t1 is duration (uS) between DS and RTC change (start)
    rtcstart = self.nownr()                     # RTC start time in mS
    dsstart = utime.mktime(self.time())         # DS start time in secs
    pyb.delay(minutes * 60000)
    self.wait()                                 # DS second boundary
    tus = pyb.micros()
    st = self.rtc.datetime()[7]
    while self.rtc.datetime()[7] == st:
      pass
    t2 = pyb.elapsed_micros(tus)                # t2 is duration (uS) between DS and RTC change (end)
    rtcend = self.nownr()
    dsend = time.mktime(self.time())
    dsdelta = (dsend - dsstart) * 1000000       # Duration (uS) between DS edges as measured by DS3231
    rtcdelta = (rtcend - rtcstart) * 1000 + t1 -t2 # Duration (uS) between DS edges as measured by RTC and corrected
    ppm = (1000000* (rtcdelta - dsdelta)) / dsdelta
    return int(-ppm / 0.954)

  def calibrate( self, minutes = 5 ) :
    print('Waiting {} minutes to acquire calibration factor...'.format(minutes))
    cal = self.getcal(minutes)
    self.rtc.calibration(cal)
    print('Pyboard RTC is calibrated. Factor is {}.'.format(cal))
    return cal

  def now( self ):  # Return the current time from the RTC in millisecs from year 2000
    secs = utime.time()
    ms = 1000 * (255 - self.rtc.datetime()[7]) >> 8
    if ms < 50:                                 # Might have just rolled over
      secs = utime.time()
    return 1000 * secs + ms

  def nownr( self ):  # Return the current time from the RTC: caller ensures transition has occurred
     return 1000 * utime.time() + (1000 * (255 - self.rtc.datetime()[7]) >> 8)
