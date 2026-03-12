#!/usr/bin/env python3

from gpiozero import LED, Button
from signal import pause
from time import sleep

led_red = LED(12)
led_green = LED(16)
led_blue = LED(20)
led_white = LED(21)

button_red = Button(5, pull_up=False)
button_green = Button(6, pull_up=False)
button_blue = Button(13, pull_up=False)
button_white = Button(19, pull_up=False)

state_led_red = 0
state_led_green = 0
state_led_blue = 0
state_led_white = 0

COLOR_R = "red"
COLOR_G = "green"
COLOR_B = "blue"
COLOR_W = "white"

TIME_HIGH_SLOW = 1
TIME_LOW_SLOW = 1

TIME_HIGH_MEDIUM = 0.5
TIME_LOW_MEDIUM = 0.5

TIME_HIGH_FAST = 0.2
TIME_LOW_FAST = 0.2

def ctrl_led_red():
    ctrl_led(COLOR_R)

def ctrl_led_green():
    ctrl_led(COLOR_G)

def ctrl_led_blue():
    ctrl_led(COLOR_B)

def ctrl_led_white():
    ctrl_led(COLOR_W)

def ctrl_led(color: str):
    if color == COLOR_R:
        global state_led_red
        state_led_red = not(state_led_red)
        if state_led_red:
            led_red.blink(TIME_HIGH_SLOW,TIME_LOW_SLOW , None, True)
        else:
            led_red.off()
    elif color == COLOR_G:
        global state_led_green
        state_led_green = not(state_led_green)
        if state_led_green:
            led_green.blink(TIME_HIGH_MEDIUM, TIME_LOW_MEDIUM, None, True)
        else:
            led_green.off()
    if color == COLOR_B:
        global state_led_blue
        state_led_blue = not(state_led_blue)
        if state_led_blue:
            led_blue.blink(TIME_HIGH_FAST,TIME_LOW_FAST, None, True)
        else:
            led_blue.off()
    elif color == COLOR_W:
        global state_led_white
        state_led_white = not(state_led_white)
        if state_led_white:
            led_white.blink(TIME_HIGH_SLOW,TIME_LOW_FAST, None, True)
        else:
            led_white.off()

def setup():
    print("Exercice 02 - Les boutons 05")

def loop():
    button_red.when_pressed = ctrl_led_red
    button_green.when_pressed = ctrl_led_green
    button_blue.when_pressed = ctrl_led_blue
    button_white.when_pressed = ctrl_led_white
    pause()

try:
    setup()
    while True:
        loop()

finally:
    led_red.close()

# END
