#!/usr/bin/env python3

from tm1637_library_00 import TM1637_00
from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep

unTM1637 = TM1637_00(17, 27)  

def setup():

    print("Exercice 04 - Les afficheurs 7 segments - Partie 00")
        
    unTM1637.set_brightness(1)

    unTM1637.set_values([0b1111111,0b1111111,0b1111111,0b1111111])
    sleep(1)

    unTM1637.set_values(['A', 'B', 'b', 'C'])
    sleep(0.5)

    unTM1637.set_values(['c', 'D', 'd', 'E'])
    sleep(0.5)

    unTM1637.set_values(['F', 'G', 'H', 'h'])
    sleep(0.5)

    unTM1637.set_values(['I', 'J', 'K', 'L'])
    sleep(0.5)

    unTM1637.set_values(['l', 'n', 'O', 'o'])
    sleep(0.5)

    unTM1637.set_values(['P', 'r', 'S', 'U'])
    sleep(0.5)

    unTM1637.set_values(['Y', 'Z', ' ', ' '])
    sleep(0.5)

    unTM1637.set_values(['T1', 'T2', 'W1', 'W2'])
    sleep(0.5)

    unTM1637.set_value('M1', 0)
    sleep(0.5)

    unTM1637.set_value('M2', 1)
    sleep(0.5)

    unTM1637.set_values(range(4))
    sleep(0.5)

    unTM1637.set_values(range(4, 8))
    sleep(0.5)

    unTM1637.set_values(range(6, 10))
    sleep(0.5)

    unTM1637.clear()

    unTM1637.cleanup()

#def loop():

#   pause()

try:
    setup()
    #while True:
    #    loop()

finally:
    print("...")

# END
