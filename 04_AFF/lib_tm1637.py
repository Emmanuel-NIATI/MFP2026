import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

HEXDIGITS = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x07, 0x7f, 0x6f]

HEXLETTERS = {
    'A': 0x77,
    'B': 0x7f,
    'b': 0x7C,
    'C': 0x39,
    'c': 0x58,
    'D': 0x3f,
    'd': 0x5E,
    'E': 0x79,
    'F': 0x71,
    'G': 0x7d,
    'H': 0x76,
    'h': 0x74,
    'I': 0x06,
    'J': 0x1f,
    'K': 0x76,
    'L': 0x38,
    'l': 0x06,
    'n': 0x54,
    'O': 0x3f,
    'o': 0x5c,
    'P': 0x73,
    'r': 0x50,
    'S': 0x6d,
    'U': 0x3e,
    'V': 0x3e,
    'Y': 0x66,
    'Z': 0x5b,
    ' ': 0x00,
    'T1': 0x07,
    'T2': 0x31,
    'M1': 0x33,
    'M2': 0x27,
    'W1': 0x3c,
    'W2': 0x1e,
}

ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xC0
BRIGHT_DARKEST = 0
BRIGHT_DEFAULT = 2
BRIGHT_HIGHEST = 7
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
LOW = GPIO.LOW
HIGH = GPIO.HIGH


class TM1637:
    __doublepoint = False
    __clk_pin = 0
    __data_pin = 0
    __brightness = BRIGHT_DEFAULT
    __current_data = [' ', ' ', ' ', ' ']

    def __init__(self, clock_pin, data_pin, brightness=BRIGHT_DEFAULT):
        self.__clk_pin = clock_pin
        self.__data_pin = data_pin
        self.__brightness = brightness
        GPIO.setup(self.__clk_pin, OUTPUT)
        GPIO.setup(self.__data_pin, OUTPUT)

    def clear(self):
        b = self.__brightness
        point = self.__doublepoint
        self.__brightness = 0
        self.__doublepoint = False
        data = [' ', ' ', ' ', ' ']
        self.set_values(data)
        self.__brightness = b
        self.__doublepoint = point

    def set_values(self, data):
        for i in range(4):
            self.__current_data[i] = data[i]

        self.start()
        self.write_byte(ADDR_AUTO)
        self.stop()
        self.start()
        self.write_byte(STARTADDR)
        for i in range(4):
            self.write_byte(self.encode(data[i]))
        self.stop()
        self.start()
        self.write_byte(0x88 + self.__brightness)
        self.stop()

    def set_value(self, value, index):
        if index not in range(4):
            pass

        self.__current_data[index] = value;

        self.start()
        self.write_byte(ADDR_FIXED)
        self.stop()
        self.start()
        self.write_byte(STARTADDR | index)
        self.write_byte(self.encode(value))
        self.stop()
        self.start()
        self.write_byte(0x88 + self.__brightness)
        self.stop()

    def set_brightness(self, brightness):
        if brightness not in range(8):
            pass

        self.__brightness = brightness
        self.set_values(self.__current_data)

    def set_doublepoint(self, value):
        self.__doublepoint = value
        self.set_values(self.__current_data)

    def encode(self, data):
        point = 0x80 if self.__doublepoint else 0x00;

        if data == 0x7F:
            data = 0
        elif HEXLETTERS.has_key(data):
            data = HEXLETTERS[data] + point
        else:
            data = HEXDIGITS[data] + point
        return data

    def write_byte(self, data):
        for i in range(8):
            GPIO.output(self.__clk_pin, LOW)
            if data & 0x01:
                GPIO.output(self.__data_pin, HIGH)
            else:
                GPIO.output(self.__data_pin, LOW)
            data >>= 1
            GPIO.output(self.__clk_pin, HIGH)

        GPIO.output(self.__clk_pin, LOW)
        GPIO.output(self.__data_pin, HIGH)
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.setup(self.__data_pin, INPUT)

        while GPIO.input(self.__data_pin):
            time.sleep(0.001)
            if GPIO.input(self.__data_pin):
                GPIO.setup(self.__data_pin, OUTPUT)
                GPIO.output(self.__data_pin, LOW)
                GPIO.setup(self.__data_pin, INPUT)
        GPIO.setup(self.__data_pin, OUTPUT)

    def start(self):
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.output(self.__data_pin, HIGH)
        GPIO.output(self.__data_pin, LOW)
        GPIO.output(self.__clk_pin, LOW)

    def stop(self):
        GPIO.output(self.__clk_pin, LOW)
        GPIO.output(self.__data_pin, LOW)
        GPIO.output(self.__clk_pin, HIGH)
        GPIO.output(self.__data_pin, HIGH)

    def cleanup(self):
        GPIO.cleanup(self.__clk_pin)
        GPIO.cleanup(self.__data_pin)




"""
MicroPython TM1637 quad 7-segment LED display driver
https://github.com/mcauser/micropython-tm1637

MIT License
Copyright (c) 2016-2023 Mike Causer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__version__ = '1.3.0'

from micropython import const
from machine import Pin
from time import sleep_us, sleep_ms

TM1637_CMD1 = const(64)  # 0x40 data command
TM1637_CMD2 = const(192) # 0xC0 address command
TM1637_CMD3 = const(128) # 0x80 display control command
TM1637_DSP_ON = const(8) # 0x08 display on
TM1637_DELAY = const(10) # 10us delay between clk/dio pulses
TM1637_MSB = const(128)  # msb is the decimal point or the colon depending on your display

# 0-9, a-z, blank, dash, star
_SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')

class TM1637(object):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver."""
    def __init__(self, clk, dio, brightness=7):
        self.clk = clk
        self.dio = dio

        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness

        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        sleep_us(TM1637_DELAY)

        self._write_data_cmd()
        self._write_dsp_ctrl()

    def _start(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)

    def _stop(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.dio(1)

    def _write_data_cmd(self):
        # automatic address increment, normal mode
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()

    def _write_dsp_ctrl(self):
        # display on, set brightness
        self._start()
        self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | self._brightness)
        self._stop()

    def _write_byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            sleep_us(TM1637_DELAY)
            self.clk(1)
            sleep_us(TM1637_DELAY)
            self.clk(0)
            sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)

    def brightness(self, val=None):
        """Set the display brightness 0-7."""
        # brightness 0 = 1/16th pulse width
        # brightness 7 = 14/16th pulse width
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")

        self._brightness = val
        self._write_data_cmd()
        self._write_dsp_ctrl()

    def write(self, segments, pos=0):
        """Display up to 6 segments moving right from a given position.
        The MSB in the 2nd segment controls the colon between the 2nd
        and 3rd segments."""
        if not 0 <= pos <= 5:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        self._start()

        self._write_byte(TM1637_CMD2 | pos)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._write_dsp_ctrl()

    def encode_digit(self, digit):
        """Convert a character 0-9, a-f to a segment."""
        return _SEGMENTS[digit & 0x0f]

    def encode_string(self, string):
        """Convert an up to 4 character length string containing 0-9, a-z,
        space, dash, star to an array of segments, matching the length of the
        source string."""
        segments = bytearray(len(string))
        for i in range(len(string)):
            segments[i] = self.encode_char(string[i])
        return segments

    def encode_char(self, char):
        """Convert a character 0-9, a-z, space, dash or star to a segment."""
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36] # space
        if o == 42:
            return _SEGMENTS[38] # star/degrees
        if o == 45:
            return _SEGMENTS[37] # dash
        if o >= 65 and o <= 90:
            return _SEGMENTS[o-55] # uppercase A-Z
        if o >= 97 and o <= 122:
            return _SEGMENTS[o-87] # lowercase a-z
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48] # 0-9
        raise ValueError("Character out of range: {:d} '{:s}'".format(o, chr(o)))

    def hex(self, val):
        """Display a hex value 0x0000 through 0xffff, right aligned."""
        string = '{:04x}'.format(val & 0xffff)
        self.write(self.encode_string(string))

    def number(self, num):
        """Display a numeric value -999 through 9999, right aligned."""
        # limit to range -999 to 9999
        num = max(-999, min(num, 9999))
        string = '{0: >4d}'.format(num)
        self.write(self.encode_string(string))

    def numbers(self, num1, num2, colon=True):
        """Display two numeric values -9 through 99, with leading zeros
        and separated by a colon."""
        num1 = max(-9, min(num1, 99))
        num2 = max(-9, min(num2, 99))
        segments = self.encode_string('{0:0>2d}{1:0>2d}'.format(num1, num2))
        if colon:
            segments[1] |= 0x80 # colon on
        self.write(segments)

    def temperature(self, num):
        if num < -9:
            self.show('lo') # low
        elif num > 99:
            self.show('hi') # high
        else:
            string = '{0: >2d}'.format(num)
            self.write(self.encode_string(string))
        self.write([_SEGMENTS[38], _SEGMENTS[12]], 2) # degrees C

    def show(self, string, colon=False):
        segments = self.encode_string(string)
        if len(segments) > 1 and colon:
            segments[1] |= 128
        self.write(segments[:4])

    def scroll(self, string, delay=250):
        segments = string if isinstance(string, list) else self.encode_string(string)
        data = [0] * 8
        data[4:0] = list(segments)
        for i in range(len(segments) + 5):
            self.write(data[0+i:4+i])
            sleep_ms(delay)


class TM1637Decimal(TM1637):
    """Library for quad 7-segment LED modules based on the TM1637 LED driver.

    This class is meant to be used with decimal display modules (modules
    that have a decimal point after each 7-segment LED).
    """

    def encode_string(self, string):
        """Convert a string to LED segments.

        Convert an up to 4 character length string containing 0-9, a-z,
        space, dash, star and '.' to an array of segments, matching the length of
        the source string."""
        segments = bytearray(len(string.replace('.','')))
        j = 0
        for i in range(len(string)):
            if string[i] == '.' and j > 0:
                segments[j-1] |= TM1637_MSB
                continue
            segments[j] = self.encode_char(string[i])
            j += 1
        return segments
