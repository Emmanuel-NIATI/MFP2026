#!/usr/bin/env python3

from tm1637_library_02 import TM1637_02
from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep

display = TM1637_02(clk=17, dio=27, brightnes=1, is_show_double_point=False, pin_mode="BCM")

def setup():

    print("Exercice 04 - Les afficheurs 7 segments - Partie 02")

    display.set_brightnes(1)
    sleep(0.5)

    display.show_double_point()
    sleep(0.5)

    display.set_brightnes(2)
    sleep(0.5)

    display.hide_double_point()
    sleep(0.5)

    display.show_digit([ 'A', 'B', 'C', 'd'])
    sleep(0.5)

    display.show_digit([ '1', '2', '3', '4'])
    sleep(0.5)

    display.show_digit([ 'A', '1', TM1637_02.DIGIT_SPACE, TM1637_02.DIGIT_SPACE])
    sleep(0.5)

    display.show_number([ 4, 3, 2, 1])
    sleep(0.5)

    display.show_number([ 9, 8, TM1637_02.NUMBER_NULL, TM1637_02.NUMBER_NULL])
    sleep(0.5)

    display.show_binary([ 0b00000110, 0b01011011,  0b01001111,  0b01100110, 0b00000000, 0b00000000,])
    sleep(0.5)

    display.clear()


#def loop():

#   pause()

try:
    setup()
    #while True:
    #    loop()

finally:
    print("...")

# END



