#!/usr/bin/env python

import gpiod as GPIO
from SimpleMFRC522 import SimpleMFRC522

chip = GPIO.Chip('gpiochip4')
RST = chip.get_line(14)
reader = SimpleMFRC522()

try:
        id, text = reader.read()
        print(id)
        print(text)
finally:
        RST.release()