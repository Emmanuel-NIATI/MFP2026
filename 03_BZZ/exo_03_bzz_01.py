#!/usr/bin/env python3

from gpiozero import LED, Button, Buzzer
from signal import pause
from time import sleep

bzz = Buzzer(4)

def setup():
    i=1
    print("Exercice 03 - Les buzzers 01")
    while(i<5):
        bzz.on()
        sleep(0.5)
        bzz.off()    
        sleep(0.5)
        i+=1

try:
    setup()


finally:
    bzz.off()

# END

