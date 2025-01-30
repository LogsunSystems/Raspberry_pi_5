#!/usr/bin/env python

import gpiod as GPIO
import time
from SimpleMFRC522 import SimpleMFRC522

#define the LCD pins
LCD_RS = 5
LCD_E  = 12
LCD_RW = 6
LCD_D4 = 15
LCD_D5 = 17
LCD_D6 = 18
LCD_D7 = 22

chip = GPIO.Chip('gpiochip4') #set the GPIO chip
RST = chip.get_line(14) # Engauge the GPIO line from RST pin
reader = SimpleMFRC522()    #Create the object for RFID Reader

RS_line = chip.get_line(LCD_RS) 
RS_line.request(consumer = "RS",type=GPIO.LINE_REQ_DIR_OUT)

RW_line = chip.get_line(LCD_RW)
RW_line.request(consumer="RW", type = GPIO.LINE_REQ_DIR_OUT)

EN_line = chip.get_line(LCD_E)
EN_line.request(consumer = "EN",type=GPIO.LINE_REQ_DIR_OUT)

D4_line = chip.get_line(LCD_D4)
D4_line.request(consumer = "D4",type=GPIO.LINE_REQ_DIR_OUT)

D5_line = chip.get_line(LCD_D5)
D5_line.request(consumer = "D5",type=GPIO.LINE_REQ_DIR_OUT)

D6_line = chip.get_line(LCD_D6)
D6_line.request(consumer = "D6",type=GPIO.LINE_REQ_DIR_OUT)

D7_line = chip.get_line(LCD_D7)
D7_line.request(consumer = "D7",type=GPIO.LINE_REQ_DIR_OUT)

LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def main():
  # Main program block
  
    RW_line.set_value(0) # Set the RW pin LOW
  # Initialise display
    lcd_init()  # Initialize the LCD prior to use
 
    while True:
 
    # Send some test
        id, text = reader.read() #Read the RFID TAG
        print(id) 
        print(text)
        lcd_string("RFID Reader",LCD_LINE_1)
        lcd_string(id,LCD_LINE_2) #Dsiplay RFID TAG value on LCD
 
        time.sleep(3) # 3 second delay


def lcd_init():
  # Initialise display
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  #GPIO.output(LCD_RS, mode) # RS
    RS_line.set_value(mode)
 
  # High bits
    D4_line.set_value(False)
    D5_line.set_value(False)
    D6_line.set_value(False)
    D7_line.set_value(False)
    if bits&0x10==0x10:
    #GPIO.output(LCD_D4, True)
        D4_line.set_value(True)
    if bits&0x20==0x20:
    #GPIO.output(LCD_D5, True)
        D5_line.set_value(True)
    if bits&0x40==0x40:
    #GPIO.output(LCD_D6, True)
        D6_line.set_value(True)
    if bits&0x80==0x80:
    #GPIO.output(LCD_D7, True)
        D7_line.set_value(True)
 
  # Toggle 'Enable' pin
    lcd_toggle_enable()
 
  # Low bits
    D4_line.set_value(False)
    D5_line.set_value(False)
    D6_line.set_value(False)
    D7_line.set_value(False)
    if bits&0x01==0x01:
    #GPIO.output(LCD_D4, True)
        D4_line.set_value(True)
    if bits&0x02==0x02:
    #GPIO.output(LCD_D5, True)
        D5_line.set_value(True)
    if bits&0x04==0x04:
    #GPIO.output(LCD_D6, True)
        D6_line.set_value(True)
    if bits&0x08==0x08:
    #GPIO.output(LCD_D7, True)
        D7_line.set_value(True)
 
  # Toggle 'Enable' pin
    lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
    time.sleep(E_DELAY)
  #GPIO.output(LCD_E, True)
    EN_line.set_value(True)
    time.sleep(E_PULSE)
  #GPIO.output(LCD_E, False)
    EN_line.set_value(False)
    time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
    message = message.ljust(LCD_WIDTH," ")
 
    lcd_byte(line, LCD_CMD)
 
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
    
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        #Release all the GPIO pins as we have not to do anything more
        RST.release()
        RS_line.release()
        EN_line.release()
        D4_line.release()
        D5_line.release()
        D6_line.release()
        D7_line.release()
