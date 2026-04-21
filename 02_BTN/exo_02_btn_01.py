#!/usr/bin/env python3

from gpiozero import LED, Button
from signal import pause
from time import sleep

led_red = LED(12)
button_red = Button(5, pull_up=False)

def setup():
    print("Exercice 02 - Les boutons - Partie 01")

def loop():
    button_red.when_pressed = led_red.on
    pause()

try:
    setup()
    while True:
        loop()

finally:
    led_red.close()

# END
