#!/usr/bin/python3

from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2
import gpiod as GPIO

"""
    This script allow for deleting a fingerprint from the internal memory.
"""

#---------------------------- [LCD] -----------------------------------------
# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 6
LCD_RW = 5
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25

chip = GPIO.Chip('gpiochip4') #Select the gpiochip
RS_line = chip.get_line(LCD_RS) #Select the GPIO line for RS pin
RS_line.request(consumer = "RS",type=GPIO.LINE_REQ_DIR_OUT) #Set the RS pin as OUTPUT

RW_line = chip.get_line(LCD_RW)
RW_line.request(consumer="RW", type = GPIO.LINE_REQ_DIR_OUT)

EN_line = chip.get_line(LCD_E)
EN_line.request(consumer = "EN",type=GPIO.LINE_REQ_DIR_OUT)

D4_line = chip.get_line(LCD_D4)
D4_line.request(consumer = "D4",type=GPIO.LINE_REQ_DIR_OUT)

D5_line = chip.get_line(LCD_D5)
D5_line.request(consumer = "D5",type=GPIO.LINE_REQ_DIR_OUT)

D6_line = chip.get_line(LCD_D6)
D6_line.request(consumer="D6",type=GPIO.LINE_REQ_DIR_OUT)

D7_line = chip.get_line(LCD_D7)
D7_line.request(consumer = "D6",type=GPIO.LINE_REQ_DIR_OUT)

 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  sleep(E_DELAY)
 
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
  sleep(E_DELAY)
  #GPIO.output(LCD_E, True)
  EN_line.set_value(True)
  sleep(E_PULSE)
  #GPIO.output(LCD_E, False)
  EN_line.set_value(False)
  sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)


RW_line.set_value(0) # set the RS line LOW
lcd_init()	# initialize the LCD before using it
#----------------------------------------------------------------------------

## Tries to initialize the sensor
try:
    sensor = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( sensor.verifyPassword() == False ):
        raise ValueError('The fingerprint sensor is protected by password!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    lcd_string("FP Could not",LCD_LINE_1)
    lcd_string("be initialized",LCD_LINE_2)
    print('Exception message: {}'.format(e))
    exit(1)

## Gets info about how many fingerprint are currently stored
print('Currently stored fingers: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))
Capacity = str(sensor.getStorageCapacity())
Count = str(sensor.getTemplateCount())
FP_CNT = Count + '/' + Capacity
lcd_string("Stored Fingers",LCD_LINE_1)
lcd_string(FP_CNT,LCD_LINE_2)
sleep(4)
lcd_string("Enter FP",LCD_LINE_1)
lcd_string("Index to delet",LCD_LINE_2)
## Tries to enroll new finger
try:
    position = input('Please enter the template position you want to delete: ')
    position = int(position)

    if sensor.deleteTemplate(position) == True :
        print('Fingerprint deleted!')
        lcd_string("Fingerprint",LCD_LINE_1)
        lcd_string("Deleted !!!",LCD_LINE_2)

except Exception as e:
    print('Operation failed!')
    lcd_string("Operation",LCD_LINE_1)
    lcd_string("Failed",LCD_LINE_2)
    print('Exception message: '.format(e))
    exit(1)
