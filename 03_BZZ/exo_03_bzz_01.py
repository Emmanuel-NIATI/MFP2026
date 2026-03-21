#!/usr/bin/env python3

from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep

bzz = Buzzer(4)

def setup():
    print("Exercice 03 - Les buzzers 01")
    bzz.on()


try:
    setup()


finally:
    bzz.off()

# END

