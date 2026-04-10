#!/usr/bin/env python3

from tm1637_library_01 import TM1637_01
from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep

display = TM1637_01(clk=17, dio=27, brightnes=1, is_show_point=False, pin_mode="BCM")

def setup():

    print("Exercice 04 - Les afficheurs 7 segments led 01")

    display.show([1, 2, 3, 4])
    display.clear()

    display.show([1, 2, None, None])

    display.show_point()
    display.close_point()

    display.show([1, 2, 3, 4])

    display.set_brightnes(1)

    display.show([5, 6, 7, 8])

    display.set_brightnes(2)

    display.show_data((0b1111111, 0b1111111, 0b1111111, 0b1000000))

    display.disable()
    display.enable()


#def loop():

#   pause()

try:
    setup()
    #while True:
    #    loop()

finally:
    print("...")

# END



