# The MIT License (MIT)
#
# Copyright (c) 2019 Brandon C. Allen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`CircuitPython_UnicornHatHD`
====================================================

Driver for the Pimoroni Unicorn Hat HD

* Author(s): Brandon C. Allen

Implementation Notes
--------------------

**Hardware:**
* Unicorn Hat HD:
  https://shop.pimoroni.com/products/unicorn-hat-hd
  
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
  
"""
import time
import board
import busio
import digitalio

#Define the pixel buffer
height = 16
width = 16
depth = 3
buffer = [[[0x0 for x in range(depth)] for y in range(width)] for z in range(height)]

#SPI Stuff
sof = b'\x72'
spi = busio.SPI(board.SCK, MOSI=board.MOSI)
def set_unicorn_matrix(board_pin):
    global cs
    cs = digitalio.DigitalInOut(board_pin)
    cs.direction = digitalio.Direction.OUTPUT
    cs.value = True

#Define the pixel grid so we can set the pixel by number instead of X-Y Coordinates.
grid=[]
for x in range(16):
    for y in range(16):
        grid.append((y,x))

def set_pixel_color(n,r,g,b):
    global buffer
    buffer[grid[n][0]][grid[n][1]][0] = r
    buffer[grid[n][0]][grid[n][1]][1] = g
    buffer[grid[n][0]][grid[n][1]][2] = b

def set_xypixel_color(x,y,r,g,b):
    global buffer
    buffer[x][y][0] = r
    buffer[x][y][1] = g
    buffer[x][y][2] = b

def fill(r,g,b):
    global buffer
    for i in range(height):
        for j in range(width):
                buffer[i][j][0] = r
                buffer[i][j][1] = g
                buffer[i][j][2] = b

def clear():
    global buffer
    for i in range(height):
        for j in range(width):
            for k in range(depth):
                buffer[i][j][k] = 0x00

def show():
    while not spi.try_lock():
        pass

    try:
        spi.configure(baudrate=2000000)
        cs.value = False
        spi.write(sof)
        for i in range(height):
            for j in range(width):
                for k in range(depth): 
                    spi.write(bytes([buffer[i][j][k]]))
        cs.value = True
    finally:
        spi.unlock()

set_unicorn_matrix(board.D1)
set_pixel_color(30,0,0,20)
set_xypixel_color(15,15,20,20,20)
set_pixel_color(31,0,20,0)
set_xypixel_color(12,12,25,25,25)
set_pixel_color(0,0,20,0)
set_pixel_color(75,20,0,0)
show()
time.sleep(5)
clear()
show()
time.sleep(5)
fill(0x20,0x00,0x00)
show()
