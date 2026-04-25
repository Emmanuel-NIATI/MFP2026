#!/usr/bin/env python3

from RPi import GPIO
from time import sleep


"""

     ---A---             ---A---             ---A---             ---A---
    |       |           |       |           |       |           |       |
    | F     | B         | F     | B         | F     | B         | F     | B
    |       |           |       |     O     |       |           |       |
     ---G---             ---G---             ---G---             ---G---
    |       |           |       |     O     |       |           |       |
    | E     | C         | E     | C         | E     | C         | E     | C
    |       |           |       |           |       |           |       |
     ---D---    O        ---D---    O        ---D---    O        ---D---    O

    data[i] = 0b0GFEDCBA

"""

class TM1637_02:

    COMMAND_DATA = 0x40         # command data
    COMMAND_ADDRESS = 0xC0      # command address
    COMMAND_DISPLAY_CTRL = 0x80 # command display control

    TM1637_DSP_ON = 0x08        # display on
    TM1637_DSP_OFF = 0x00       # display off

    NUMBER_TO_HEX = {

        -1: 0x00,
        0: 0x3f,
        1: 0x06,
        2: 0x5b,
        3: 0x4f,
        4: 0x66,
        5: 0x6d,
        6: 0x7d,
        7: 0x07,
        8: 0x7f,
        9: 0x6f,

    }

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
        0b00111111,  # 0
        0b00000110,  # 1
        0b01011011,  # 2
        0b01001111,  # 3
        0b01100110,  # 4
        0b01101101,  # 5
        0b01111101,  # 6
        0b00000111,  # 7
        0b01111111,  # 8
        0b01101111,  # 9
        0b01110111,  # A
        0b01111100,  # b
        0b00111001,  # C
        0b01011110,  # d
        0b01111001,  # E
        0b01110001   # F
    ]

    NONE_SEGMENT = 0x00
    DIGIT_SPACE = ' '
    NUMBER_NULL = -1

    DATA_CLEAR = (NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT, NONE_SEGMENT)

    def __init__(self, clk, dio, brightnes, is_show_double_point, pin_mode):

        assert 0 <= brightnes <= 7

        self.clk = clk
        self.dio = dio
        self.brightnes = brightnes
        self.is_show_double_point = is_show_double_point

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


    def refresh(self):

        self.show_data(self.current_data)


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

            sleep(0.001)

            if GPIO.input(self.dio):
                GPIO.setup(self.dio, GPIO.OUT)
                GPIO.output(self.dio, GPIO.LOW)
                GPIO.setup(self.dio, GPIO.IN)

        GPIO.setup(self.dio, GPIO.OUT)


    def show_data(self, data):

        self.current_data = tuple(data)
        
        self.start()
        self.write_byte(self.COMMAND_DATA)
        self.stop()

        self.start()
        self.write_byte(self.COMMAND_ADDRESS)

        for i in range(6):
            self.write_byte(data[i])
        
        self.stop()

        self.start()
        self.write_byte(self.COMMAND_DISPLAY_CTRL | self.TM1637_DSP_ON | self.brightnes)
        self.stop()


    def show_double_point(self):

        double_point_data = 0b10000000
        self.is_show_double_point = True
        self.current_data = (   self.current_data[0],
                                self.current_data[1] | double_point_data,
                                self.current_data[2],
                                self.current_data[3],
                                self.current_data[4],
                                self.current_data[5])
        self.refresh()


    def hide_double_point(self):
        
        double_point_data = 0b01111111
        self.is_show_double_point = False
        self.current_data = (   self.current_data[0],
                                self.current_data[1] & double_point_data,
                                self.current_data[2],
                                self.current_data[3],
                                self.current_data[4],
                                self.current_data[5])
        self.refresh()


    def show_digit(self, data):

        data_0 = ' '
        data_1 = ' '
        data_2 = ' '
        data_3 = ' '
        data_4 = ' '
        data_5 = ' '

        if data[0] in self.DIGIT_TO_HEX:
            data_0 = data[0]

        if data[1] in self.DIGIT_TO_HEX:
            data_1 = data[1]

        if data[2] in self.DIGIT_TO_HEX:
            data_2 = data[2]

        if data[3] in self.DIGIT_TO_HEX:
            data_3 = data[3]

        encoded_data = (    self.DIGIT_TO_HEX[data_0],
                            self.DIGIT_TO_HEX[data_1],
                            self.DIGIT_TO_HEX[data_2],
                            self.DIGIT_TO_HEX[data_3],
                            self.DIGIT_TO_HEX[data_4],
                            self.DIGIT_TO_HEX[data_5] )

        self.show_data(encoded_data)


    def clear(self):

        self.show_digit(self.DATA_CLEAR)


    def scroll_digit(self, data, delay):

        str_data = str(data)
        k = len(str_data)


    def show_number(self, data):

        data_0 = -1
        data_1 = -1
        data_2 = -1
        data_3 = -1
        data_4 = -1
        data_5 = -1

        if data[0] in self.NUMBER_TO_HEX:
            data_0 = data[0]

        if data[1] in self.NUMBER_TO_HEX:
            data_1 = data[1]

        if data[2] in self.NUMBER_TO_HEX:
            data_2 = data[2]

        if data[3] in self.NUMBER_TO_HEX:
            data_3 = data[3]

        encoded_data = (    self.NUMBER_TO_HEX[data_0],
                            self.NUMBER_TO_HEX[data_1],
                            self.NUMBER_TO_HEX[data_2],
                            self.NUMBER_TO_HEX[data_3],
                            self.NUMBER_TO_HEX[data_4],
                            self.NUMBER_TO_HEX[data_5] )

        self.show_data(encoded_data)


    def show_binary(self, data):

        data_0 = 0b00000000
        data_1 = 0b00000000
        data_2 = 0b00000000
        data_3 = 0b00000000
        data_4 = 0b00000000
        data_5 = 0b00000000

        data_0 = data[0]
        data_1 = data[1]
        data_2 = data[2]
        data_3 = data[3]
        data_4 = data[4]
        data_5 = data[5]

        encoded_data = (    data_0,
                            data_1,
                            data_2,
                            data_3,
                            data_4,
                            data_5 )

        self.show_data(encoded_data)
