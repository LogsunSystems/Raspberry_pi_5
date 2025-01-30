#!/usr/bin/env python

import gpiod as GPIO
from SimpleMFRC522 import SimpleMFRC522

chip = GPIO.Chip('gpiochip4') #Select the GPI Chip for controlling GPIOs
RST = chip.get_line(14) # Get the GPIO line for RST pin
reader = SimpleMFRC522()  #Create Object of RFID Reader class

try:
        id, text = reader.read() #Read the RFID Card
        print(id)
        print(text)
finally:
        RST.release()
