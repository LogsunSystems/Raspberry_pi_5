import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
time.sleep(1)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
time.sleep(1)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)
 
# Loop to read the analog input continuously
while True:
    print("Analog Value: ", channel.value, "Voltage: ", channel.voltage)
    time.sleep(1)