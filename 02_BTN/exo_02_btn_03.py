#!/usr/bin/env python3

from gpiozero import LED, Button
from signal import pause
from time import sleep

led_red = LED(12)
button_red = Button(5, pull_up=False)

state_led_red = 0
state_led_green = 0
state_led_blue = 0
state_led_white = 0

def ctrl_led_red():
    ctrl_led("red")

def ctrl_led(color: str):
    if color == "red":
        global state_led_red
        state_led_red = not(state_led_red)
        if state_led_red:
            led_red.blink(0.5, 0.5, None, True)
        else:
            led_red.off()

def setup():
    print("Exercice 02 - Les boutons 03")

def loop():
    button_red.when_pressed = ctrl_led_red
    pause()

try:
    setup()
    while True:
        loop()

finally:
    led_red.close()

# END
