import machine
import time
import os
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

# set up the hardware, pen p4 to save RAM
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

# set the display backlight to 50%
display.set_backlight(0.5)

# set up constants for drawing
WIDTH, HEIGHT = display.get_bounds()

# set up positions for counters
coords1 = ((WIDTH - 80), (HEIGHT-50))
coords2 =  (5, 0)

# set up pens
BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)

# set up save file
storeFile = "saved.txt"
maxFileSize = 100

# set up buttons
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# set up counters
counter1 = 0
counter2 = 0

# function to check if there is a saved file
def file_exists(filename):
    try:
        return (os.stat(filename)[0] & 0x4000) == 0
    except OSError:
        return False

# setup for first counter
def displaycounter1(counter):
    display.set_pen(WHITE)
    display.text("Stitches:", coords1[0]-10, coords1[1]-10, scale = 2)
    display.set_pen(CYAN)
    display.text(str(counter), coords1[0], coords1[1], scale=6)
    display.update()
    display.set_pen(BLACK)

# setup for second counter
def displaycounter2(counter):
    display.set_pen(WHITE)
    display.text("Rows:", coords2[0], coords2[1], scale = 2)
    display.set_pen(MAGENTA)
    display.text(str(counter), coords2[0]+10, coords2[1]+10, scale=6)
    display.update()
    display.set_pen(BLACK)
    
# function to draw counters on screen and save the new counter state to file    
def displaycounters(counter1, counter2, storeFile):
    file=open(storeFile, 'w')
    display.clear()
    displaycounter1(counter1)
    displaycounter2(counter2)
    file.write(str(counter1) + " " + str(counter2))
    file.close()

# read file contents if it exists and set counters to either file contents or 0/0 accordingly
if file_exists(storeFile):
    file=open(storeFile, 'r')
    contents = file.read();
    counters = [int(x) for x in contents.split()]
    counter1 = counters[0]
    counter2 = counters[1]
    display.clear()
    displaycounters(counter1, counter2, storeFile)
else:
    counter1 = 0
    counter2 = 0
    display.clear()
    displaycounters(counter1, counter2, storeFile)

# main loop
while True:
    if button_x.read():
        counter1 = counter1 + 1
        displaycounters(counter1, counter2, storeFile)
    if button_y.read():
         counter1 = counter1 - 1
         displaycounters(counter1, counter2, storeFile)
    if button_a.read():
        counter2 = counter2 + 1
        displaycounters(counter1, counter2, storeFile)
    if button_b.read():
        counter2 = counter2 - 1
        displaycounters(counter1, counter2, storeFile)

 