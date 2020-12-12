'''
bitarray.py

    An example using map_bitarray_to_rgb565 to draw sprites on the
    M5Stack Core Display.

'''

import time
import random
from machine import Pin, SPI
import ili9342c

SPRITES = 100

SPRITE_WIDTH = 16
SPRITE_HEIGHT = 16
SPRITE_STEPS = 3
SPRITE_BITMAPS = [
    bytearray([
        0b00000000, 0b00000000,
        0b00000001, 0b11110000,
        0b00000111, 0b11110000,
        0b00001111, 0b11100000,
        0b00001111, 0b11000000,
        0b00011111, 0b10000000,
        0b00011111, 0b00000000,
        0b00011110, 0b00000000,
        0b00011111, 0b00000000,
        0b00011111, 0b10000000,
        0b00001111, 0b11000000,
        0b00001111, 0b11100000,
        0b00000111, 0b11110000,
        0b00000001, 0b11110000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000]),

    bytearray([
        0b00000000, 0b00000000,
        0b00000011, 0b11100000,
        0b00001111, 0b11111000,
        0b00011111, 0b11111100,
        0b00011111, 0b11111100,
        0b00111111, 0b11110000,
        0b00111111, 0b10000000,
        0b00111100, 0b00000000,
        0b00111111, 0b10000000,
        0b00111111, 0b11110000,
        0b00011111, 0b11111100,
        0b00011111, 0b11111100,
        0b00001111, 0b11111000,
        0b00000011, 0b11100000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000]),

    bytearray([
        0b00000000, 0b00000000,
        0b00000111, 0b11000000,
        0b00011111, 0b11110000,
        0b00111111, 0b11111000,
        0b00111111, 0b11111000,
        0b01111111, 0b11111100,
        0b01111111, 0b11111100,
        0b01111111, 0b11111100,
        0b01111111, 0b11111100,
        0b01111111, 0b11111100,
        0b00111111, 0b11111000,
        0b00111111, 0b11111000,
        0b00011111, 0b11110000,
        0b00000111, 0b11000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000]),

    bytearray([
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000,
        0b00000000, 0b00000000])]


class pacman():
    '''
    pacman class to keep track of a sprites locaton and step
    '''
    def __init__(self, x, y, step):
        self.x = x
        self.y = y
        self.step = step

    def move(self):
        self.step += 1
        self.step %= SPRITE_STEPS
        self.x += 1
        if self.x == 302:
            self.step = SPRITE_STEPS

        self.x %= 303

def main():
    '''
    Draw on screen using map_bitarray_to_rgb565
    '''
    try:

        # initialize display

        tft = ili9342c.ILI9342C(
            SPI(2, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(23)),
            320,
            240,
            reset=Pin(33, Pin.OUT),
            cs=Pin(14, Pin.OUT),
            dc=Pin(27, Pin.OUT),
            backlight=Pin(32, Pin.OUT),
            rotation=0)

        # enable display and clear screen
        tft.init()
        tft.fill(ili9342c.BLACK)
        time.sleep(3)

        sprite = bytearray(512)

        # create pacman spites in random positions
        sprites = []
        for man in range(SPRITES):
            sprites.append(
                pacman(
                    random.randint(0, tft.width()-SPRITE_WIDTH),
                    random.randint(0, tft.height()-SPRITE_HEIGHT),
                    random.randint(0, SPRITE_STEPS-1)
                )
            )

        # move and draw sprites
        while True:
            for man in sprites:
                # move the sprite
                man.move()

                # convert bitmap into rgb565 blitable buffer
                tft.map_bitarray_to_rgb565(
                    SPRITE_BITMAPS[man.step],
                    sprite,
                    SPRITE_WIDTH,
                    ili9342c.YELLOW,
                    ili9342c.BLACK)

                # blit the buffer to the display
                tft.blit_buffer(
                    sprite,
                    man.x,
                    man.y,
                    SPRITE_WIDTH,
                    SPRITE_HEIGHT)

            time.sleep(0.1)

    finally:
        # shutdown spi
        if 'spi' in locals():
            spi.deinit()

main()