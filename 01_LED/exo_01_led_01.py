#!/usr/bin/env python3

from gpiozero import LED
from time import sleep

# This library (gpiozero) uses Broadcom (BCM) pin numbering for the GPIO pins
# As opposed to physical (BOARD) numbering. Unlike in the RPi.GPIO library, this is not configurable.
# However, translation from other schemes can be used by providing prefixes to pin numbers (see below).

# Any pin marked “GPIO” in the diagram below can be used as a pin number.
# For example, if an LED was attached to “GPIO17” you would specify the pin number as 17 rather than 11
# For example, if an LED was attached to “GPIO5” you would specify the pin number as 5 rather than 29
# led = LED(5)
# led = LED("GPIO5")
# led = LED("BCM5")

# Specify the pin number as “BOARD29” for GPIO5
# led = LED("BOARD29")

# Specify pins as “header:number”, e.g. “J8:29”
# meaning physical pin 29 on header J8 (the GPIO header on modern Pis)
# led = LED("J8:29")

red = LED(12)

TIME_HIGHT = 0.5
TIME_LOW = 0.5

def blink():
    red.on()
    sleep(TIME_HIGHT)
    red.off()
    sleep(TIME_LOW)

def setup():
    print("Exercice 01 - Les leds")

def loop():
    blink()

try:
    setup()
    while True:
        loop()

finally:
    red.close()

# END
