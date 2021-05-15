
from machine import UART, Pin, PWM
from utime import sleep_ms
import _thread
import math

#angle data.
# distance = 14 bits - Distance or error code (invalid flag set)
# strength = 1 bit - Flag indicating signal strength was lower than expected.
# invalid = 1 bit - Set when distance couldn't be calculated
# uint16_t signal strength

#frame data
# uint8_t start = 0xFA
# uint8_t index = index - 0xA0 * 4 is the angle for the readings array
# uint16_t speed = divide by 64 to get speed in rpm
# 16 bytes - angledata[4] = angle data for 4 consecutive angles
# uint16_t checksum
# Total size = 22 bytes

#invalid data codes.
#   XV11LIDAR_CRC_FAILURE = 0x66 the frame had incorrect CRC, don't use the data
#   XV11LIDAR_ERROR1 = 0x02
#   XV11LIDAR_ERROR2 = 0x03
#   XV11LIDAR_ERROR3 = 0x21
#   XV11LIDAR_ERROR4 = 0x25
#   XV11LIDAR_ERROR5 = 0x35
#   XV11LIDAR_ERROR6 = 0x50

#--------------------------------------------------------
#Constants for lidar driver
_FRAMESIZE = const(22)                          # See frame data below
_FRAMESTART = const(0xFA)                       # Each frame starts with this tag
_FRAMEINDEX = const(0xA0)                       # Indexes are 0xA0 + 0-90
_ANGLESPERFRAME = const(4)
_FRAMESPERROT = const(90)
_ANGLESPERROT = const(_FRAMESPERROT * _ANGLESPERFRAME) # We get 90 frames with 4 angles per frame
_FRAMESPERREAD = const(90)                      # Up this to read more data per attempt
_INVALID = const(1 << 15)                       # Bit set in destance word of angle data indicating invalid data
_BUFFERSIZE = const(_FRAMESIZE * _FRAMESPERREAD)
_MOTORSPEED = const(32)
_MOTORSPEEDMIN = const(20)
_MOTORSPEEDMAX = const(40)
_MAXDISTANCE = const(16383)

#--------------------------------------------------------
# def printit( aBuffer ):
#   ''' Print bytearray data as hex. '''
#   for v in aBuffer:
#     print(hex(v), end=',')
#
#   print('')

#--------------------------------------------------------
class lidar(object):
  ''' xv11 lidar driver. Reads data into an angles buffer as well as keep track of rpm.
      Attempts to maintain ~245 rpm. '''

  def __init__( self ):
    super(lidar, self).__init__()

    #rx pin is connected to the orange wire. tx isn't necessary but we have to
    # supply a pin.
    self._uart = UART(1, tx = 13, rx = 15, baudrate = 115200, buffer_size = 8192)
    self._motor = PWM(Pin(17), freq = 100)
    self._speed = _MOTORSPEED
    self._speedcheck = 0
    self._motor.duty(self._speed)

    self._rpm = 0
    self._buffer = bytearray(_BUFFERSIZE)
    self._inbuffer = bytearray(_BUFFERSIZE)
    self._angles = [0] * _ANGLESPERROT    # Storage for angles
    self._insync = False
    self._good = 0

  #--------------------------------------------------------
  def _sync( self ):
    ''' sync up the serial data read with the start of frame. '''
#     print('syncing')

    #Function to return true if the start tag is found at the desired location
    def isstart( aOffset ):
      return self._buffer[aOffset] == _FRAMESTART

    while not self._insync:
      self._fillbuffer()
      offset = -1
      #Loop for up to 4 frames worth of data.  If we didn't find a tag by then we probably won't
      for x in range(_FRAMESIZE * 4):
        #If start tag is found in 3 consecutive frames then this is probably a real frame start
        if isstart(x) and isstart(x + _FRAMESIZE) and isstart(x + (_FRAMESIZE * 2)):
          offset = x
          break

      #If we found an start tag then let's try and use it
      if offset != -1:
        #If the tag is at the beginning of the buffer, don't need to move data
        if offset > 0:
          tomove = len(self._buffer) - offset
          #Move data so frame start is at the beginning
          for x in range(tomove):
            self._buffer[x] = self._buffer[offset + x]
#           printit(self._buffer[:_FRAMESIZE])
          toread = offset
          #Now read in data to fill in the rest of the buffer
          while toread:
            cnt = self._uart.readinto(self._inbuffer, toread)
            for y in range(cnt):
              self._buffer[offset + y] = self._inbuffer[0]
            offset += cnt
            toread -= cnt

        #Process the buffer data
        self._process()
        #If we got enough good values then we are synced
        # This is half the number of angles read
        if self._good > _FRAMESPERREAD * 2:
          print('sync good')
          self._insync = True

  #--------------------------------------------------------
  @property
  def speed( self ):
    return self._speed

  #--------------------------------------------------------
  @speed.setter
  def speed( self, aValue ):
    self._speed = aValue
    self._motor.duty(aValue)

  #--------------------------------------------------------
  def _getrpm( self, aIndex ):
    ''' Get the rpm value. '''
    return (self._buffer[aIndex + 2] | (self._buffer[aIndex + 3] << 8)) >> 6

  #--------------------------------------------------------
  def _adjustrpm( self ):
    '''  '''
    if self._speedcheck >= 0:
      if self._rpm < 240:
        self.speed = min(self.speed + 1, _MOTORSPEEDMAX)
      elif self._rpm > 248:
        self.speed = max(self.speed - 1, _MOTORSPEEDMIN)
      self._speedcheck = -20
    else:
      self._speedcheck += 1

  #--------------------------------------------------------
  def _checksum( self, aIndex = 0 ):
    ''' Calculate the checksum and return true if matched. '''
    chk = 0
    crc = self._buffer[aIndex + 20] | (self._buffer[aIndex + 21] << 8)
    for i in range(aIndex, aIndex + 20, 2):
      w = self._buffer[i] + (self._buffer[i + 1] << 8)
      chk = (chk << 1) + w

    chk = (chk & 0x7FFF) + (chk >> 15)
    return (chk & 0x7FFF) == crc

  #--------------------------------------------------------
  def _fillbuffer( self ):
    ''' Fill the buffer with serial data '''
    read = self._uart.readinto(self._buffer, _BUFFERSIZE)
    #Read until the buffer is full
    while read < _BUFFERSIZE:
      #Read into temp buffer then append to _buffer
      cnt = self._uart.readinto(self._inbuffer, _BUFFERSIZE - read)
      if cnt:
        for x in range(cnt):
          self._buffer[read + x] = self._inbuffer[x]
        read += cnt

  #--------------------------------------------------------
  def _process( self ):
    ''' Process buffer data and return number of good values read. '''

    self._good = 0
    #Loop for each frame in the buffer
    for x in range(0, _BUFFERSIZE, _FRAMESIZE):
#       if x == 0:
#         printit(self._buffer[x:x + _FRAMESIZE])
      #Make sure buffer starts with start tag
      if self._buffer[x] == _FRAMESTART:
        #Make sure checksum is good
        if self._checksum(x):
          #Average rpm value.
          self._rpm = self._getrpm(x) #(self._rpm + self._getrpm(x)) >> 1
          angle = (self._buffer[x + 1] - 0xA0) << 2
          a = x + 4 #Point to angle data array
          #Process 4 angle values
          for y in range(a, a + 16, 4): #4 angle entries of 4 bytes each
            dist = self._buffer[y] | (self._buffer[y + 1] << 8)
            #If invalid flag set then clear distance
            if dist & _INVALID:
              dist = _MAXDISTANCE
            else:
              self._good += 1
            self._angles[angle] = dist
            angle += 1
          #todo: May want to keep track of bad checksums and frames and report them
#         else:
#           print('checksum bad')
#       else:
#         self._insync = False
#       else:
#         print('bad frame')

  #--------------------------------------------------------
  def update( self ):
    ''' Update lidar data '''
    if self._insync:
      self._fillbuffer()                        # Read new data
      self._process()                           # Process the data
      self._adjustrpm()                         # Try and maintain 240-250 rpm
    else:
      insync = self._sync()

  #--------------------------------------------------------
  def output( self ):
    '''  '''
    a = self._angles[0]
    b = self._angles[90]
    c = self._angles[180]
    d = self._angles[270]
    print('rpm:', self._rpm, a, b, c, d, self._good, '        ', end='\r')

#--------------------------------------------------------
# Constants for lidardisplay
_DISPLAYPERFRAME = const(90)
_MAXDISPLAYDISTANCE = const(68)
_DADJ = const(2048 // _MAXDISPLAYDISTANCE)
_CX = const(120)
_CY = const(67)

#--------------------------------------------------------
class lidardisplay(object):
  ''' Display lidar data on TFT '''

  #--------------------------------------------------------
  def __init__( self, aLidar, aDisplay ):
    ''' Setup display for give aLidar using tft aDisplay. '''

    super(lidardisplay, self).__init__()
    self._lidar = aLidar
    self._tft = aDisplay
    self._clear = 0xFFFFFF - self._tft.BLACK
    self._draw = 0xFFFFFF - self._tft.YELLOW
    self._tft.set_bg(self._clear)
    self._tft.clearwin()
    self._tft.pixel(_CX, _CY, 0xFFFFFF - self._tft.DARKGREY)
    self._angles = [-1] * len(aLidar._angles)
    self._angle = 0
    self._rpm = 0

  #--------------------------------------------------------
  def update( self ):
    ''' Update give number of angles per call. Clears old displayed line
         and draws a new line if distance has changed. '''
    a0 = self._angle
    plotted = 0

    #Loop for number of angles we wish to update this frame
    for i in range(360):
      d = min(self._lidar._angles[a0] // _DADJ, _MAXDISPLAYDISTANCE)
      od = self._angles[a0]
      a1 = (a0 + 1) % 360

      #if line has changed since last update
      if d != od:
        plotted += 1

        a0r = math.radians(a0)
        a1r = math.radians(a1)
        x0 = math.sin(a0r)
        y0 = math.cos(a0r)
        x1 = math.sin(a1r)
        y1 = math.cos(a1r)

        #Only clear if we drew something before.
        oldx0 = int(x0 * od) + _CX
        oldx1 = int(x1 * od) + _CX
        oldy0 = int(y0 * od) + _CY
        oldy1 = int(y1 * od) + _CY
#         print('erase:', oldx0, oldy0, oldx1, oldy1)
        if (abs(oldx0 - oldx1) + abs(oldy0 - oldy1)) < 2:
          self._tft.pixel(oldx0, oldy0, self._clear)
        else:
          self._tft.line(oldx0, oldy0, oldx1, oldy1, self._clear)

        self._angles[a0] = d

        #Only draw new line if distance is not negative.
        x0 = int(x0 * d) + _CX
        x1 = int(x1 * d) + _CX
        y0 = int(y0 * d) + _CY
        y1 = int(y1 * d) + _CY
#         print('plot:', x0, y0, x1, y1)
        if (abs(x0 - x1) + abs(y0 - y1)) < 2:
          self._tft.pixel(x0, y0, self._draw)
        else:
          self._tft.line(x0, y0, x1, y1, self._draw)

      if plotted >= _DISPLAYPERFRAME:
        break;

      a0 = a1

    self._angle = a0

    if self._rpm != self._lidar._rpm:
      self._rpm = self._lidar._rpm
      self._tft.rect(0, 0, 35, 15, self._clear, self._clear)
      self._tft.text(0, 0, str(self._rpm), self._draw)
#       self._tft.text(0, 15, str(self.speed), self._draw)

#--------------------------------------------------------
def displayloop( aLidar, aTFT ):
  ''' Run display loop in background thread. '''
  d = lidardisplay(aLidar, aTFT)

  while True:
    if aLidar._insync:
      d.update()
    sleep_ms(33)
    n = _thread.getnotification()
    if n == _thread.EXIT:
      break

#--------------------------------------------------------
def run( aTFT ):
  l = lidar()
  displaythread = _thread.start_new_thread('display', displayloop, (l, aTFT))

  while True:
    l.update()
    #todo: Sleep?
