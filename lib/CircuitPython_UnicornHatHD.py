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
import digitalio
import board
import busio
import time
import struct

hatheight = 16 # Height of hat's display
hatwidth = 16 # Width of hat's display
black = 0x000000
sofbyte = b'\x72' #Required byte to be sent prior to data per Pimoroni's documentation
grid=[] # generate a list of coordinates for the pixel_color function to use
for x in range(16):
    for y in range(16):
        grid.append((y,x))

class UnicornHatHD:
    # Configure the hat
    def __init__(self,cs_pin,sck_pin=None,mosi_pin=None):
        self.cs_pin = digitalio.DigitalInOut(cs_pin)
        self.cs_pin.direction = digitalio.Direction.OUTPUT
        self.cs_pin.value = True
        if sck_pin is None:
            self.sck = board.SCK
        else:
            self.sck = sck_pin
        if mosi_pin is None:
            self.mosi = board.MOSI
        else:
            self.mosi = mosi_pin
        self.height = hatheight
        self.width = hatwidth
        self.blank = black
        self.sof = sofbyte
        self.buffer = [[self.blank for y in range(self.width)] for z in range(self.height)]
    
    # Clear the hat (set all pixels to black)
    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.buffer[i][j] = 0x000000
    # Specify a color to fill the whole hat.
    def fill(self,color):
        for i in range(self.height):
            for j in range(self.width):
                self.buffer[i][j] = (int(color))

    # Specify a pixel using a number and a color using a hex value. Valid options are 0-255 for the pixel number. 0x000000 thru 0xffffff for the color
    def set_pixel_color(self, n, color):
        self.grid = grid
        self.buffer[self.grid[n][0]][self.grid[n][1]] = (int(color))

    # Specify a pixel using X/Y grid and a color using a hex value. Valid options are 0-15 for x and y coordinates. 0x000000 thru 0xffffff for the color
    def set_xypixel_color(self,x,y,color):
        self.buffer[x][y] = (int(color))

    # Write data to the hat
    def show(self):
        spi = busio.SPI(self.sck, MOSI=self.mosi)
        while not spi.try_lock():
            pass
        try:
            spi.configure(baudrate=12000000)
            self.cs_pin.value = False
            spi.write(self.sof)
            for i in range(self.height):
                for j in range(self.width):
                    spi.write(struct.pack('>i',(self.buffer[i][j]))[1:])
            self.cs_pin.value = True
        finally:
            spi.unlock()
            spi.deinit() # Required for multiple hats. You can uncomment this line if you use multiple SPI buses for multiple hats or are only using one hat. Not sure if it will play well with other devices using the SPI bus.
