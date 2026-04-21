#!/usr/bin/env python3

from gpiozero import LED, Button, Buzzer
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

bzz = Buzzer(4)

COLOR_R = "red"
COLOR_G = "green"
COLOR_B = "blue"
COLOR_W = "white"

TIME_HIGH_SPEED_01 = 0.1
TIME_LOW_SPEED_01 = 0.1

TIME_HIGH_SPEED_02 = 0.25
TIME_LOW_SPEED_02 = 0.25

TIME_HIGH_SPEED_03 = 0.5
TIME_LOW_SPEED_03 = 0.5

TIME_HIGH_SPEED_04 = 1
TIME_LOW_SPEED_04 = 1


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
        bzz.beep(TIME_HIGH_SPEED_01,TIME_LOW_SPEED_01, True)
    elif color == COLOR_G:
        bzz.beep(TIME_HIGH_SPEED_02,TIME_LOW_SPEED_02, True)
    elif color == COLOR_B:
        bzz.beep(TIME_HIGH_SPEED_03,TIME_LOW_SPEED_03, True)
    elif color == COLOR_W:
        bzz.beep(TIME_HIGH_SPEED_04,TIME_LOW_SPEED_04, True)
        

def setup():
    print("Exercice 03 - Les buzzers - Partie 02")

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
