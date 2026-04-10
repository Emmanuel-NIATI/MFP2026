#!/usr/bin/env python3

from tm1637_library_01 import TM1637_01
from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep

display = TM1637_01(clk=17, dio=27, brightnes=1, is_show_point=False, pin_mode="BCM")

def setup():

    print("Exercice 04 - Les afficheurs 7 segments led 01")

    display.showSign(['A', 'B', 'C', 'd'])
    sleep(0.5)

    display.showSign(['1', '2', '3', '4'])
    sleep(0.5)

    display.clear()
    sleep(0.5)

    display.showLitteral([1, 2, TM1637_01.TM1637_NONE , TM1637_01.TM1637_NONE])
    sleep(0.5)
    
    display.show_point()
    sleep(0.5)
    
    display.close_point()
    sleep(0.5)
    
    display.showLitteral([1, 2, 3, 4])
    sleep(0.5)
    
    display.set_brightnes(1)
    sleep(0.5)
    
    display.showLitteral([5, 6, 7, 8])
    sleep(0.5)

    display.set_brightnes(2)
    sleep(0.5)

    display.showLitteral((0b1111111, 0b1111111, 0b1111111, 0b1000000))
    sleep(0.5)

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



