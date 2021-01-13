"""
fonts.py

    Pages through all characters of four fonts on the M5Stack Display.

"""
import utime
import random
from machine import Pin, SPI
import ili9342c

import vga1_8x8 as font1
import vga1_8x16 as font2
import vga1_bold_16x16 as font3
import vga1_bold_16x32 as font4

def main():
    tft = ili9342c.ILI9342C(
        SPI(2, baudrate=40000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(23)),
        320,
        240,
        reset=Pin(33, Pin.OUT),
        cs=Pin(14, Pin.OUT),
        dc=Pin(27, Pin.OUT),
        backlight=Pin(32, Pin.OUT),
        rotation=0,
        buffer_size=16*32*2)

    tft.init()
    tft.fill(ili9342c.BLACK)
    utime.sleep(1)

    while True:
        for font in (font1, font2, font3, font4):
            tft.fill(ili9342c.BLUE)
            line = 0
            col = 0
            for char in range(font.FIRST, font.LAST):
                tft.text(font, chr(char), col, line, ili9342c.WHITE, ili9342c.BLUE)
                col += font.WIDTH
                if col > tft.width() - font.WIDTH:
                    col = 0
                    line += font.HEIGHT

                    if line > tft.height()-font.HEIGHT:
                        utime.sleep(3)
                        tft.fill(ili9342c.BLUE)
                        line = 0
                        col = 0

            utime.sleep(3)
main()
