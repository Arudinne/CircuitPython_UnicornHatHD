import time
import board
import busio
import digitalio
import struct
import circuitpython_unicornhathd

display1 = circuitpython_unicornhathd.UnicornHatHD(board.D1) # First Display
display2 = circuitpython_unicornhathd.UnicornHatHD(board.D2) # Second Display
#display2 = circuitpython_unicornhathd.UnicornHatHD(board.D2, Board.D4, Board.D3) # Second Display configured using a separate SPI bus (only tested on the Particle Xenon (NRF52840))

while True:
    display1.fill(0x401010)
    display2.fill(0x104010)
    display1.show()
    display2.show()
    time.sleep(5)
    display1.clear()
    display2.clear()
    display1.show()
    display2.show()
    time.sleep(5)
    display1.set_pixel_color(20,0x303030)
    display2.set_pixel_color(40,0x303030)
    display1.set_xypixel_color(2,2,0x303030)
    display2.set_xypixel_color(4,4,0x303030)
    display1.show()
    display2.show()
    time.sleep(5)
    display1.clear()
    display2.clear()
    display1.show()
    display2.show()
