import gpiod
import time
LED_PINs=[25,24,23,22,27,18,17,4,26,16,19,13,12,6,5,7,8,11,10,9,2,3,15,14]
led_pin =[]
chip = gpiod.Chip('/dev/gpiochip4') # select the GPIO chip
i = 0

# Set the LED pins to Output
for x in LED_PINs:
    led_pin.append(chip.get_line(x))
    led_pin[i].request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    i=i+1

try:
   
   while True:
    for l in range (0,len(LED_PINs)):
        led_pin[l].set_value(1) #Turn ON LED
        time.sleep(0.04)    # Wait for 80 mSec
    
    time.sleep(5)
    
    for l in range (0,len(LED_PINs)):
        led_pin[l].set_value(0) #Turn OFF LED
        time.sleep(0.04)        #Wait for 50 mSec
finally:
    for l in range (0,len(LED_PINs)):
        led_pin[l].release()        #release the resources of all the LED pins after use
