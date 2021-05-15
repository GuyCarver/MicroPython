#Driver for DFPlayer mini, MP3 player with SD card slot, using serial communication.

#See documentation at:
#  https://www.dfrobot.com/wiki/index.php/DFPlayer_Mini_SKU:DFR0299

#0 Each command starts with byte 0x7E
#1 Version # (set to 0xFF)
#2 The number of bytes which follow (6, Not including checksum and termination)
#3 The command to execute
#4 Feedback indicator (0: no, 1: yes)
#5 Argument high byte
#6 Argument low byte
#7-8 2 byte checksum
#9 Termination byte 0xEF

#Commands
#The next and prev commands wrap when they hit the end of the list.
#0x01   next
#0x02   prev
#0x03   Track # 0-2999
#0x04   volume +
#0x05   volume -
#0x06   volume #0-30
#0x07   equalizer 0-5 (Normal, Pop, Rock, Jazz, Classical, Base)
#0x08   playback mode 0-3 (Repeat, folder repeat, single repeat, random)
#0x09   playback source 0-3 (U, TF, AUX, SLEEP, FLASH)
#0x0A   sleep mode
#0x0B   Normal mode
#0x0C   reset
#0x0D   play/resume
#0x0E   pause
#0x0F   specify folder 1-10
#0x10   volume adjust (High byte = Open volume adjust, Low byte = volume gain 0-31)
#0x11   repeat 0 = stop, 1 = repeat.

#Query commands
#0x3F   Send init parameters 0-0x0F.
#0x41   Reply.  The command byte is set to this on a reply read from the dfplayer as a reply if
#                 the the feedback indicator was set on the command.  Not very useful.
#0x42   status
#0x43   volume
#0x44   eq
#0x45   playback mode
#0x46   software version
#0x47   # of TF card files
#0x48   # of SD card files
#0x49   # of flash files
#0x4A   Keep on ?
#0x4B   Current TF card track
#0x4C   Current SD card track
#0x4D   Current flash track

#Results - These are sent as replies to certain commands.
#0x3D   Result of play, next, prev (param hi/lo is current file index)

#  Folders are named 01, 02..99.  Files 001, 002 ... 999.

from machine import UART
from time import sleep_ms

class dfplayer(UART) :

  _WAIT = const(10)

  '''Initialize dfplayer at given UART 0-2'''
  def __init__(self, aUART, aBaud = 9600) :
    super(dfplayer, self).__init__(aUART, aBaud)
    self._buffer = bytearray(10)
    self._buffer[0] = 0x7E  #commands always start with these bytes.
    self._buffer[1] = 0xFF  #Version #
    self._buffer[2] = 6     #Commands are always 6 bytes
    self._buffer[4] = 0     #We never want results returned. (0x41)  This is just an ack we don't use.
    self._buffer[9] = 0xEF  #Command terminator.
    self._readbuffer = bytearray(20)

  def _clear( self ) :
    while self.any() :
      self.readinto(self._readbuffer)

  def _cmd( self, aCommand, aArg = 0 ) :
    '''Send aCommand to hc05 with given argument.'''
    self._buffer[3] = aCommand
    self._buffer[5] = aArg >> 8
    self._buffer[6] = aArg

    cs = 0
    for i in range(1, 7) :
      cs -= self._buffer[i]

    #Set the checksum.
    self._buffer[7] = cs >> 8
    self._buffer[8] = cs

    self._clear()  #Make sure return buffer is empty.
    self.write(self._buffer)

  @property
  def readbuffer( self ):
    return self._readbuffer

  def result( self  ) :
    '''Wait for result and return # of bytes read.  Result is in _readbuffer.'''
    for i in range(1, 100) :
      if self.any() :
        return self.readinto(self._readbuffer)
      sleep_ms(_WAIT)

    return 0

  def resultnum( self ) :
    '''Read result, then pull 16 bit # from it.'''
    res = self.result()
    if res >= 10 :
      return (self._readbuffer[5] << 8 | self._readbuffer[6])
    return 0

  def printres( self ) :
    '''Print result as string of hex values.'''
    b = self.result()
    for i in range(0, b) :
      print(str(hex(self._readbuffer[i])) + ',', end='')
    print('/')

  def next( self ) :
    '''Play next song.'''
    self._cmd(1)

  def prev( self ) :
    '''Play previous song.'''
    self._cmd(2)

  def play( self, aIndex ) :
    '''Play song at given index.'''
    self._cmd(3, aIndex)

  def volume( self, aLevel ) :
    '''Set volume to absolute value.'''
    self._cmd(6, aLevel & 0x1E)

  def qvolume( self ) :
    self._cmd(0x43)
    return self.resultnum()

  def equalizer( self, aArg ) :
    '''Set equalizer type. (Normal, Pop, Rock, Jazz, Classical, Base)'''
    self._cmd(7, aArg)

  def qequalizer( self ) :
    self._cmd(0x44)
    return self.resultnum()

  def qsdfiles( self ) :
    '''return # of files on sd card.'''
    self._cmd(0x48)
    return self.resultnum()

  def qsdtrack( self ) :
    '''return current sd card track #.'''
    self._cmd(0x4C)
    return self.resultnum()

  def qflashfiles( self ) :
    '''return # of files in flash memory.'''
    self._cmd(0x49)
    return self.resultnum()

  def qflashtrack( self ) :
    '''return current flash track #.'''
    self._cmd(0x4D)
    return self.resultnum()

  def sleep( self, abSleep ) :
    '''Set/clear low power mode.'''
    self._cmd(0xA if abSleep else 0xB)

  def reset( self ) :
    '''Reset the device.'''
    self._cmd(0x0C)

  def pause( self, abTF ) :
    '''Pause or resume play.'''
    p = 0x0E if abTF else 0x0D
    self._cmd(0x0E)

  def folder( self, aDir ) :
    '''Specify folder.'''
    self._cmd(0x0F, aDir)

  def folderandfile( self, aFolder, aFile ) :
    '''Play specified file in specified folder.'''
    self._cmd(0x12, (aFolder << 8) | aFile)

  def playback( self, aMode ) :
    '''Set playback mode: 0-Repeat, 1-Folder repeat, 2-Single repeat, 3-Random'''
    self._cmd(8, aMode)

  def source( self, aSource ) :
    '''Set play source, 0-SD, 1-TF, 2-AUX, 3-SLEEP, 4-FLASH.
    I don't know what TF, AUX or SLEEP are.'''
    self._cmd(9, aSource)

