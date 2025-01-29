import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#Connect the module to SV7 of  the RPI GPIO PRotection Board
 
 # Please make sure that I2C interface of Raspberry Pi
 # is enables from 'Raspberyy PI Configuration' 
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA) #Create I2C Object
time.sleep(1)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
time.sleep(1)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0) #Select Channel 0 of ADC
 
# Loop to read the analog input continuously
while True:
    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)    # Display the ADC readings on terminal
    time.sleep(1)
