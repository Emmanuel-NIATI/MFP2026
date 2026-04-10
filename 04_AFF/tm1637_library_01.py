#!/usr/bin/env python3

"""

      A         A
     ---
  F |   | B
     -G-
  E |   | C
     ---    °
      D

"""

import RPi.GPIO as GPIO
import time

class TM1637_01:

    COMMAND_DATA = 0x40         # data command
    COMMAND_ADDRESS = 0xC0      # address command
    COMMAND_CTRL = 0x80         # display control command
    TM1637_DSP_ON = 0x08        # display on
    TM1637_DSP_OFF = 0x00       # display off

    DIGIT_TO_HEX = {

        ' ': 0x00,
        '0': 0x3f,
        '1': 0x06,
        '2': 0x5b,
        '3': 0x4f,
        '4': 0x66,
        '5': 0x6d,
        '6': 0x7d,
        '7': 0x07,
        '8': 0x7f,
        '9': 0x6f,
        'a': 0x77,
        'b': 0x7C,
        'c': 0x58,
        'd': 0x5E,
        'h': 0x74,
        'I': 0x06,
        'l': 0x06,
        'n': 0x54,
        'o': 0x5c,
        'r': 0x50,
        'A': 0x77,
        'B': 0x7f,
        'C': 0x39,
        'D': 0x3f,
        'E': 0x79,
        'F': 0x71,
        'G': 0x7d,
        'H': 0x76,
        'I': 0x06,
        'J': 0x1f,
        'K': 0x76,
        'L': 0x38,
        'n': 0x54,
        'O': 0x3f,
        'P': 0x73,
        'S': 0x6d,
        'T': 0x00,
        'U': 0x3e,
        'V': 0x3e,
        'Y': 0x66,
        'Z': 0x5b,

}

    DIGIT_TO_SEGMENT = [
        0b0111111,  # 0
        0b0000110,  # 1
        0b1011011,  # 2
        0b1001111,  # 3
        0b1100110,  # 4
        0b1101101,  # 5
        0b1111101,  # 6
        0b0000111,  # 7
        0b1111111,  # 8
        0b1101111,  # 9
        0b1110111,  # A
        0b1111100,  # b
        0b0111001,  # C
        0b1011110,  # d
        0b1111001,  # E
        0b1110001   # F
    ]

    NONE_SEGMENT = 0x00

    DATA_CLEAR = (0x00, 0x00, 0x00, 0x00)

    def __init__(self, clk, dio, brightnes, is_show_point, pin_mode):

        assert 0 <= brightnes <= 7

        self.clk = clk
        self.dio = dio
        self.brightnes = brightnes
        self.is_show_point = is_show_point

        if pin_mode == "BCM":
            self.pin_mode = GPIO.BCM
        elif pin_mode == "BOARD":
            self.pin_mode = GPIO.BOARD
        else:
            self.pin_mode = GPIO.BCM
                
        self.display_status = self.TM1637_DSP_ON

        GPIO.setwarnings(False)
        GPIO.setmode(self.pin_mode)
        GPIO.setup(self.clk, GPIO.OUT)
        GPIO.setup(self.dio, GPIO.OUT)

        self.current_data = self.DATA_CLEAR


    def enable(self):

        self.display_status = self.TM1637_DSP_ON
        self.refresh()


    def disable(self):

        self.display_status = self.TM1637_DSP_OFF
        self.refresh()


    def set_brightnes(self, brightnes):

        assert 0 <= brightnes <= 7
        self.brightnes = brightnes
        self.refresh()


    def clear(self):

        self.show_data(self.DATA_CLEAR)


    def show_point(self):

        point_data = 0b10000000
        self.is_show_point = True
        self.current_data = (self.current_data[0],
                             self.current_data[1] | point_data,
                             self.current_data[2],
                             self.current_data[3])
        self.refresh()


    def close_point(self):
        
        point_data = 0b01111111
        self.is_show_point = False
        self.current_data = (self.current_data[0],
                             self.current_data[1] & point_data,
                             self.current_data[2],
                             self.current_data[3])
        self.refresh()


    def show_data(self, data):

        self.current_data = tuple(data)
        self.start()
        self.write_byte(self.COMMAND_DATA)
        self.stop()
        self.start()
        self.write_byte(self.COMMAND_ADDRESS)

        for i in range(4):
            self.write_byte(data[i])
        
        self.stop()
        self.start()
        self.write_byte(self.COMMAND_CTRL | self.display_status | self.brightnes)
        self.stop()
    
    
    def show(self, data):

        if data[1] is None:
            data[1] = self.NONE_SEGMENT
    
        if data[2] is None:
            data[2] = self.NONE_SEGMENT

        if data[3] is None:
            data[3] = self.NONE_SEGMENT

        if data[3] is None:
            data[3] = self.NONE_SEGMENT

        """"
        encoded_data = (
            self.DIGIT_TO_HEX[data[1]],
            self.DIGIT_TO_HEX[data[2]],
            self.DIGIT_TO_HEX[data[3]],
            self.DIGIT_TO_HEX[data[4]]
        )
        """


        encoded_data = (
            self.DIGIT_TO_HEX['1'],
            self.DIGIT_TO_HEX['1'],
            self.DIGIT_TO_HEX['1'],
            self.DIGIT_TO_HEX['1']
        )



        self.show_data(encoded_data)

    def write_byte(self, b):

        for i in range(0, 8):

            GPIO.output(self.clk, GPIO.LOW)

            if b & 0x01:
                GPIO.output(self.dio, GPIO.HIGH)
            else:
                GPIO.output(self.dio, GPIO.LOW)

            b >>= 1
            GPIO.output(self.clk, GPIO.HIGH)

        GPIO.output(self.clk, GPIO.LOW)
        GPIO.output(self.dio, GPIO.HIGH)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.setup(self.dio, GPIO.IN)

        while GPIO.input(self.dio):

            time.sleep(0.001)

            if GPIO.input(self.dio):
                GPIO.setup(self.dio, GPIO.OUT)
                GPIO.output(self.dio, GPIO.LOW)
                GPIO.setup(self.dio, GPIO.IN)

        GPIO.setup(self.dio, GPIO.OUT)


    def refresh(self):

        self.show_data(self.current_data)


    def start(self):

        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.LOW)
        GPIO.output(self.clk, GPIO.LOW)


    def stop(self):

        GPIO.output(self.clk, GPIO.LOW)
        GPIO.output(self.dio, GPIO.LOW)
        GPIO.output(self.clk, GPIO.HIGH)
        GPIO.output(self.dio, GPIO.HIGH)
