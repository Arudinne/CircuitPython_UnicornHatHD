# Unicorn-Hat-HD-Arduino

The goal of this library is to allow the Unicorn Hat HD to be controlled as if it were a 16x16 of NeoPixel or DotStar LEDs (or as if were a 256 LED strand).

Pixel 0 is in the top right corner below the Unicorn Hat HD silkscreen. Pixel 255 is in the bottom right corner. 

Tested on an Particle Xenon (NRF52840) running CircuitPython 4.0.1, but in theory it should work on other CircuitPython boards.

This is intended to be a CircuitPython port of my Arduino Library: https://github.com/Arudinne/Unicorn-Hat-HD-Arduino which itself is based on this Gist: https://gist.github.com/emoryy/24899c8dee7112d62e4adfbdaaa4826a and the Adafruit NeoPixel Library: https://github.com/adafruit/Adafruit_NeoPixel.
