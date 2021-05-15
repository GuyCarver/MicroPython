#Driver for JQ6500 MP3 player, using serial communication.

#See documentation at:
#  https://www.elecfreaks.com/wiki/index.php?title=JQ6500_Mini_MP3_Module
#  http://sparks.gogo.co.nz/jq6500/index.html

#Each command starts with byte 0x7E
#Followed by a byte indicating the number of bytes which follow including the terminating byte (including termination)
#Followed by a byte indicating the command to execute
#Followed by an optional first argument byte
#Followed by an optional second argument byte
#Followed by the byte 0xEF as the termination byte

#The next and prev commands wrap when they hit the end of the list.
#next (play next song)                0x7E 02 01 EF
#prev (play prev song)                0x7E 02 02 EF
#play song at index nn = 1-??         0x7E 04 03 nn nn EF.
#volume+                              0x7E 02 04 EF
#volume-                              0x7E 02 05 EF
#assigned volume nn = 0-30            0x7E 03 06 nn EF
#assigned eq nn (0-5)                 0x7E 03 07 nn EF
#  Eq values are Normal, Pop, Rock, Jazz, Classical, Base
#sleep mode                           0x7E 02 0A EF
#chip reset                           0x7E 02 0C EF
#play                                 0x7E 02 0D EF
#pause                                0x7E 02 0E EF
#next/pref folder 1 = next, 0 = prev  0x7E 03 0F nn EF
#play folder/file (mm,nn)             0x7E 04 12 mm nn EF
#  Folders are named 01, 02..99.  Files 001, 002 ... 999.

from machine import UART

class jq6500(UART):
  '''Initialize jq6500 at given UART 0-2'''
  def __init__(self, aUART, aBaud = 9600):
    super(jq6500, self).__init__(aUART, aBaud)
    self._buffer = bytearray(8)
    self._buffer[0] = 0x7E #commands always start with this.

  def _write( self, *aCommand ) :
    '''Write command bytes to device.'''
    i = 2 #Commands are always at least 2 in length.
    for v in aCommand :
      self._buffer[i] = v
      i += 1

    self._buffer[1] = i - 1 #Set length of command string.
    self._buffer[i] = 0xEF #Put terminator at end of command string.
    self.write(self._buffer)

#  def next( self ) :
#    '''Play next song.'''
#    self._write(01)
#
#  def prev( self ) :
#    '''Play previous song.'''
#    self._write(02)

  def play( self, aIndex ) :
    '''Play song at given index.'''
    self._write(03, aIndex >> 8, aIndex)

#  def volumechange( self, aDir ) :
#    '''Adjust volume up/down by given amount.'''
#    if aDir < 0 :
#      d = 4
#      aDir = -aDir
#    else:
#      d = 5
#    for x in range(0, aDir):
#      self._write(d)

  def volume( self, aLevel ) :
    '''Set volume to absolute value.'''
    self._write(06, aLevel & 0x1E)

  def equalizer( self, aArg ) :
    '''Set equalizer type. (Normal, Pop, Rock, Jazz, Classical, Base)'''
    self._write(07, aArg)

  def sleep( self ) :
    '''Go into low power mode.'''
    self._write(0x0A)

#  def reset( self ) :
#    '''Reset the device.'''
#    self._write(0x0C)
#
#  def pause( self, abTF ) :
#    '''Pause or resume play.'''
#    p = 0x0E if abTF else 0x0D
#    self._write(0x0E)
#
#  def nextfolder( self, aDir ) :
#    '''Next folder.'''
#    self.write(0x0F, 1 if aDir else 0)
#
#  def folderandfile( self, aFolder, aFile ) :
#    '''Play specified file in specified folder.'''
#    self.write(12, aFolder, aFile)

