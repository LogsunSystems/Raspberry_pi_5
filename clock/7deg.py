import lgstm1637
import time
import numpy as np
from datetime import datetime
from gpiozero import CPUTemperature

# Creating 4-digit 7-segment display object
tm = lgstm1637.TM1637(clk=14, dio=15)  # Using GPIO pins 18 and 17
clear = [0, 0, 0, 0]  # Defining values used to clear the display

# Displaying a rolling string
tm.write(clear)
time.sleep(1)
s = 'This is pretty cool'
tm.scroll(s, delay=250)
time.sleep(2)

# Displaying CPU temperautre
tm.write(clear)
time.sleep(1)
cpu = CPUTemperature()
tm.temperature(int(np.round(cpu.temperature)))
time.sleep(2)

# Displaying current time
tm.write(clear)
time.sleep(1)
now = datetime.now()
hh = int(datetime.strftime(now,'%H'))
mm = int(datetime.strftime(now,'%M'))
tm.numbers(hh, mm, colon=True)
time.sleep(2)
tm.write(clear)