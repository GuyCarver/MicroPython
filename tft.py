#testing code for pyb.TFT

import pyb
from sysfont import sysfont
from seriffont import seriffont
from terminalfont import terminalfont

def randcolor(  ) :
  r = pyb.rng() & 0xFF
  g = pyb.rng() & 0xFF
  b = pyb.rng() & 0xFF
  return pyb.TFT.color(r, g, b)

def testpixel( display ) :
  print('testing pixels')
  displaysize = display.size()
  r = 255
  x = -10
  g = 0
  b = 0
  for y in range(-10, displaysize[1] + 10) :
      display.pixel((x, y), pyb.TFT.color(r, g, b))
      x += 1
      g += 2
      b += 1
  for i in range(100):
    x = pyb.rng() % displaysize[0]
    y = pyb.rng() % displaysize[1]
    display.pixel((x,y), randcolor())
  pyb.delay(2000)

def testline( display ) :
  print('testing line')
  displaysize = display.size()
  start = (int(displaysize[0] / 2), int(displaysize[1] / 2))
  px = 0
  py = 0

  def draw(x, y) :
    display.line(start, (x, y), randcolor())

  for x in range(displaysize[0]) :
    draw(px, py)
    px += 1

  for y in range(displaysize[1]) :
    draw(px, py)
    py += 1

  for x in range(displaysize[0]) :
    draw(px, py)
    px -= 1

  for y in range(displaysize[1]) :
    draw(px, py)
    py -= 1
  pyb.delay(2000)

def testrect( display ) :
  print('testing rect')
  displaysize = display.size()
  size = (20, 10)
  p0 = (0, 0)
  p1 = (displaysize[0] - size[0], p0[1])
  p2 = (p1[0], displaysize[1] - size[1])
  p3 = (p0[0], p2[1])
  #fillrect at center, top left and bottom right
  display.fillrect(p0, size, display.BLUE)
  display.fillrect(p1, size, display.GRAY)
  display.fillrect(p2, size, display.PURPLE)
  display.fillrect(p3, size, display.NAVY)

  #now do border rect as well
  display.rect(p0, size, display.CYAN)
  display.rect(p1, size, display.WHITE)
  display.rect(p2, size, display.YELLOW)
  display.rect(p3, size, display.FOREST)

  #try negative sizes
  size = (-10, -10)
  center = (int((displaysize[0] / 2) - (size[0] / 2)), int((displaysize[1] / 2) - (size[1] / 2)))
  display.fillrect(center, size, display.WHITE)
  pyb.delay(1000)
  display.rect(center, size, display.RED)
  pyb.delay(1000)
  size = (displaysize[0] * 2, 50)
  pos = (-displaysize[0], center[1])
  display.fillrect(pos, size, display.GREEN)
  display.rect(pos, size, display.WHITE)
  pyb.delay(2000)

def testcircle( display ) :
  print('testing circle')
  displaysize = display.size()
  radius = 20
  p0 = (radius, radius)
  p1 = (displaysize[0] - radius, p0[1])
  p2 = (p1[0], displaysize[1] - radius)
  p3 = (p0[0], p2[1])
  #draw filled circle win upper right, center and lower left
  display.fillcircle(p0, radius, display.BLUE)
  display.fillcircle(p1, radius, display.GRAY)
  display.fillcircle(p2, radius, display.PURPLE)
  display.fillcircle(p3, radius, display.NAVY)
  #Now do border.
  display.circle(p0, radius, display.CYAN)
  display.circle(p1, radius, display.MAROON)
  display.circle(p2, radius, display.YELLOW)
  display.circle(p3, radius, display.FOREST)
  pyb.delay(2000)
  center = ((displaysize[0] >> 1), (displaysize[1] >> 1))
  #try negative radius
  display.fillcircle(center, -radius, display.WHITE)
  pyb.delay(2000)
  display.circle(center, -radius, display.GREEN)
  #tedt big circle.
  display.fillcircle(center, 90, display.WHITE)
  pyb.delay(2000)
  display.circle(center, 90, display.GREEN)
  display.fill(0)
  #draw near edge to test clipping.
  pos = (center[0], 0)
  display.fillcircle(pos, 30, display.RED)
  display.circle(pos, 30, display.PURPLE)
  pos = (center[0], displaysize[1] - 1)
  display.fillcircle(pos, 30, display.RED)
  display.circle(pos, 30, display.PURPLE)
  pos = (0, center[1])
  display.fillcircle(pos, 30, display.RED)
  display.circle(pos, 30, display.PURPLE)
  pos = (displaysize[0] - 1, center[1])
  display.fillcircle(pos, 30, display.RED)
  display.circle(pos, 30, display.PURPLE)
  pyb.delay(2000)

def testtext( display ) :
  print('testing text')
  displaysize = display.size()
  txt = "Testing Text"
  fontA = [None, sysfont, seriffont, terminalfont]

  def draw(  ) :
    x = 0
    f = 0
    for y in range(0, display.size()[1], 10) :
      display.text((x, y), txt, pyb.TFT.CYAN, fontA[f])
      x += 2
      f = (f + 1) % len(fontA)

  #draw text
  draw()
  pyb.delay(2000)
  display.rotation(1)
  display.fill(0)
  draw()
  pyb.delay(2000)

  #try passing bogus font dict
  bogus = { "Hello": 1, "Width": 8 }
  try:
    display.text((0, 0), txt, pyb.TFT.GREEN, bogus)
  except Exception as e :
    print("Bogus font failed with:")
    print(e)

  pyb.delay(2000)
  display.fill(0)
  display.rotation(3)
  #try different scales
  display.text((0, 0), txt, pyb.TFT.GREEN, fontA[0], 2)
  display.text((0, 20), txt, pyb.TFT.BLUE, fontA[1], (2, 1))
  display.text((0, 30), txt, pyb.TFT.PURPLE, fontA[2], (1, 2))

  display.rotation(2)

  #try negative scales
  display.text((50, 50), txt, pyb.TFT.YELLOW, fontA[1], -1)

  display.rotation(0)
  pyb.delay(2000)

def testfill( display ) :
  print("testing fill")
  display.fill(pyb.TFT.GREEN)
  pyb.delay(2000)
  display.rotation(1)
  display.fill(pyb.TFT.RED)
  pyb.delay(2000)
  display.rotation(2)
  display.fill(pyb.TFT.BLACK)
  #left at rotation 2.

def testrgb( display ) :
  print("bgr")
  display.rgb(False) #bgr
  pyb.delay(2000)
  print("rgb")
  display.rgb(True) #rgb
  pyb.delay(1000)

def testinvert( display ) :
  print("Invert Color")
  display.invertcolor(True)  #invert color
  pyb.delay(2000)
  display.invertcolor(False)
  pyb.delay(2000)

def testonoff( display ) :
  print("Display on/off")
  display.on(False)
  pyb.delay(2000)
  display.on(True)
  pyb.delay(2000)

def run( display ) :
  testdisplay = display
  #inits?
#  display.initg()
  displaysize = display.size()
  #draw pixels all over, try out of range values as well.
  testpixel(display)
  #draw lines in 360 deg at center, top left and bottom right
  testline(display)
  #fill using difference colors and different rotations.
  testfill(display)
  testtext(display)
  display.fill(0)
  testrect(display)
  testcircle(display)
  testinvert(display)
  testrgb(display)
  #off/on
  testonoff(display)
  print("Test Done")
