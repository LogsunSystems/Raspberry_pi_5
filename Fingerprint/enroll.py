import time
import gpiod as GPIO
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2


#*********************************************************************************************
#LCD Routines

def lcd_init():
    # Initialise display
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



#*********************************************************************************************



"""
    This script allow for enrolling of new fingers in the module internal memory.
    The script ask for two finger pressure in order to ensure the quality of finger image.
"""

# Define GPIO to LCD mapping
LCD_RS = 5
LCD_E  = 12
LCD_RW = 6
LCD_D4 = 25
LCD_D5 = 11
LCD_D6 = 8
LCD_D7 = 7

chip = GPIO.Chip('gpiochip4')
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

def main():
    
    
    RW_line.set_value(0)
    time.sleep(0.5)
    # Initialise display
    lcd_init()
    


    ## Tries to initialize the sensor
    try:
        sensor = PyFingerprint('/dev/ttyAMA0', 57600, 0xFFFFFFFF, 0x00000000)

        if ( sensor.verifyPassword() == False ):
            raise ValueError('The fingerprint sensor is protected by password!')
            lcd_string("ERR:  Value",LCD_LINE_1)
            lcd_string("Passwd Protect",LCD_LINE_2)

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: {}'.format(e))
        lcd_string("ERR: Init",LCD_LINE_1)
        lcd_string("FP Init Err",LCD_LINE_2)
        RS_line.release()
        EN_line.release()
        RW_line.release()
        D4_line.release()
        D5_line.release()
        D6_line.release()
        D7_line.release()
        exit(1)

    ## Gets info about how many fingerprint are currently stored
    print('Currently stored fingers: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))

    ## Tries to enroll new finger
    try:
        # We read finger a first time
        print('Waiting for finger...')
        lcd_string(" Waiting for,",LCD_LINE_1)
        lcd_string(" Finger ...",LCD_LINE_2)

        ## Wait for finger to be read as an image
        while sensor.readImage() == False :
            pass

        ## Converts read image to template and stores it in charbuffer 1
        sensor.convertImage(FINGERPRINT_CHARBUFFER1)

        ## Checks if finger is already enrolled to prevent double enroll
        result = sensor.searchTemplate()
        template_position = result[0]

        if template_position >= 0 :
            print('This finger already exists at position #{}'.format(template_position))
            lcd_string("Finger Already",LCD_LINE_1)
            lcd_string("   Exists",LCD_LINE_2)
            RS_line.release()
            EN_line.release()
            RW_line.release()
            D4_line.release()
            D5_line.release()
            D6_line.release()
            D7_line.release()
            exit(0)

        print('Remove finger...')
        #lcd_string("Remove Finger",LCD_LINE_1)
        #lcd_String("From Sensor",LCD_LINE_2)
        time.sleep(2)

        # We read finger a second time to ensure the reading is of good enough quality
        print('Waiting for same finger again...')
        lcd_string("Put Same",LCD_LINE_1)
        lcd_string("finger again !",LCD_LINE_2)

        ## Wait that finger is read again
        while sensor.readImage() == False :
            pass

        ## Converts read image to template and stores it in charbuffer 2
        sensor.convertImage(FINGERPRINT_CHARBUFFER2)

        # Check if the two fingers image match, indicating a good quality of thoses images
        if ( sensor.compareCharacteristics() == 0 ):
            lcd_string("Fingerprint",LCD_LINE_1)
            lcd_string("not matching X",LCD_LINE_2)
            raise Exception('Fingers do not match')
        

        ## Turn our image to a template and save it in reader internal memory
        sensor.createTemplate()
        positionNumber = sensor.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #{}'.format(positionNumber))
        lcd_string("Finger Enrolled",LCD_LINE_1)
        lcd_string("Successfully !!",LCD_LINE_2)

    except Exception as e:
        print('Operation failed!')
        print('Exception message: '.format(e))
        #lcd_string("     ERR: FP",LCD_LINE_1)
        #lcd_string("Operation Failed",LCD_LINE_2)
        RS_line.release()
        EN_line.release()
        RW_line.release()
        D4_line.release()
        D5_line.release()
        D6_line.release()
        D7_line.release()
        exit(1)
    

if __name__ == '__main__':
 
  try:
    main()
  finally:
    #lcd_display(0x01, LCD_CMD)
    RS_line.release()
    EN_line.release()
    RW_line.release()
    D4_line.release()
    D5_line.release()
    D6_line.release()
    D7_line.release()

