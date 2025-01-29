import serial              
from time import sleep
import sys
import gpiod as GPIO


# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 6
LCD_RW = 5
LCD_D4 = 22
LCD_D5 = 23
LCD_D6 = 24
LCD_D7 = 25


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



ser = serial.Serial ('/dev/ttyAMA0')
gpgga_info = '$GPGGA,'
GPGGA_buffer = 0
NMEA_buff = 0

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



def convert_to_degrees(raw_value):
    decimal_value = raw_value/100.00
    degrees = int(decimal_value)
    mm_mmmm = (decimal_value - int(decimal_value))/0.6
    position = degrees + mm_mmmm
    position = '%.4f' %(position)
    return position


RW_line.set_value(0)
lcd_init()

try:
    while True:
        received_data = (str)(ser.readline()) #read NMEA string received
        GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGA string                
        if (GPGGA_data_available>0):
            GPGGA_buffer = received_data.split('$GPGGA,',1)[1]  #store data coming after “$GPGGA,” string
            NMEA_buff = (GPGGA_buffer.split(','))
            nmea_time = []
            nmea_latitude = []
            nmea_longitude = []
            nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
            nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
            nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
            print('NMEA Time: ', nmea_time,'\n')
            lat = (float)(nmea_latitude)
            lat = convert_to_degrees(lat)
            LAT = 'LAT:   ' + str(lat)
            lcd_string(LAT,LCD_LINE_1)
            longi = (float)(nmea_longitude)
            longi = convert_to_degrees(longi)
            LONGI = 'LONG:  ' + str(longi)
            lcd_string(LONGI,LCD_LINE_2)
            
            print ('NMEA Latitude:', lat,'NMEA Longitude:', longi,'\n')           

except KeyboardInterrupt:
    RS_line.release()
    EN_line.release()
    D4_line.release()
    D5_line.release()
    D6_line.release()
    D7_line.release()
    sys.exit(0)