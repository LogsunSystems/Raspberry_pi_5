import gpiod
import time
LED_PINs=[25,24,23,22,27,18,17,4,26,16,19,13,12,6,5,7]
led_pin= []
chip = gpiod.Chip('/dev/gpiochip4')
i = 0

for x in LED_PINs:
    led_pin.append(chip.get_line(x))
    led_pin[i].request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
    i=i+1

try:
   
   while True:
    for l in range (0,len(LED_PINs)):
        led_pin[l].set_value(1)
        time.sleep(0.08)
    
        led_pin[l].set_value(0)
        time.sleep(0.05)
finally:
    for l in range (0,len(LED_PINs)):
        led_pin[l].release()
