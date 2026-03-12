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
        if state_led_red:
            led_red.on()
        else:
            led_red.off()
        state_led_red = not(state_led_red)

def setup():
    print("Exercice 02 - Les boutons 02")

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










import RPi.GPIO as GPIO
from time import sleep

LED = 5
BTN = 6

TIME = 0.1

TIME_HIGHT=0.5
TIME_LOW=0.5

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(LED ,GPIO.LOW)


def loop():
    sleep(TIME)
    b = GPIO.input(BTN)
    if b:
        print("BTN still pressed with LED off")
        GPIO.output(LED ,GPIO.LOW)
    else:
        print("BTN still released with LED on")
        GPIO.output(LED ,GPIO.HIGH)

try:
    setup()
    while True:
        loop()

finally:
    GPIO.cleanup()

# END

