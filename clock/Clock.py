import gpiod
import time
from datetime import datetime
from lgstm1637 import TM1637

#Use the SV8 Connector on the RPI Protection Board 
CLK = 14	#Clock Pin Number
DIO = 15	# Data Pin Number
clear = [0,0,0,0]

Display = TM1637(CLK,DIO) #Create Object of the DIaplay Class

Display.write(clear)	#Clear the Display before first use
Display.brightness(0) # can set from 0-7



while True:
    now = datetime.now() #Fetch System Time
    Hour = int(datetime.strftime(now,'%H')) #Extract Hours
    Minute = int(datetime.strftime(now,'%M'))	#Extract Minute
    Second = int(datetime.strftime(now,'%S'))	#Extract Second
    #print (str(Hour)+':'+str(Minute)+':'+str(Second))
    #print((Second%2))
    Display.numbers(Hour, Minute, (Second%2)) # Display Time on 7-segments
    time.sleep(1)	# It's good to take rest !!!
