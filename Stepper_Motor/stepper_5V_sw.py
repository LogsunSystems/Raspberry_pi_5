###########################################################
#Stepper Motor interface with Raspberry pi-3
#Compony Name- Logsun Systems
###########################################################

import gpiod as GPIO
from time import sleep

#assign GPIO pins for motor
EN1 = 17
EN2 = 24
IP1 = 4
IP2 = 18
IP3 = 27
IP4 = 23

START = 7
REV   = 5
STOP  = 13

sw_arr=[0,0,0,0,0,0,0,0,0,0]
i=0


Flag_Start = False
Flag_Clockwise = True



chip = GPIO.Chip('gpiochip4')

EN1_line = chip.get_line(EN1)
EN1_line.request(consumer="EN1",type = GPIO.LINE_REQ_DIR_OUT)

EN2_line = chip.get_line(EN2)
EN2_line.request(consumer = "EN2", type = GPIO.LINE_REQ_DIR_OUT)

IP1_line = chip.get_line(IP1)
IP1_line.request(consumer = "IP1", type = GPIO.LINE_REQ_DIR_OUT)

IP2_line = chip.get_line(IP2)
IP2_line.request(consumer="IP2", type = GPIO.LINE_REQ_DIR_OUT)

IP3_line = chip.get_line(IP3)
IP3_line.request(consumer = "IP3", type = GPIO.LINE_REQ_DIR_OUT)

IP4_line = chip.get_line(IP4)
IP4_line.request(consumer = "IP4", type = GPIO.LINE_REQ_DIR_OUT)

STR_line = chip.get_line(START)
STR_line.request(consumer = "START" , type = GPIO.LINE_REQ_DIR_IN)

REV_line = chip.get_line(REV)
REV_line.request(consumer = "REV", type = GPIO.LINE_REQ_DIR_IN)

STOP_line = chip.get_line(STOP)
STOP_line.request(consumer = "STOP", type = GPIO.LINE_REQ_DIR_IN)




#infinite Loop:
try:
    while(True):
    
        if not (STR_line.get_value()):
            #print('Start Button Pressed')
            Flag_Start = True
            sleep(0.35)
        if not (REV_line.get_value()):
            Flag_Clockwise = not Flag_Clockwise
            sleep(0.35)
        if not (STOP_line.get_value()):
            Flag_Start = False
            sleep(0.35)
    
        if (Flag_Start):
            #print('Run Mode')
            EN1_line.set_value(1)
            EN2_line.set_value(1)
        
            if(Flag_Clockwise):
                #print('Clock-wise')
                IP1_line.set_value(1)
                IP2_line.set_value(0)
                IP3_line.set_value(0)
                IP4_line.set_value(1)
                sleep(0.01)
            
                IP1_line.set_value(0)
                IP2_line.set_value(0)
                IP3_line.set_value(1)
                IP4_line.set_value(1)
                sleep(0.01)
            
                IP1_line.set_value(0)
                IP2_line.set_value(1)
                IP3_line.set_value(1)
                IP4_line.set_value(0)
                sleep(0.01)
            
                IP1_line.set_value(1)
                IP2_line.set_value(1)
                IP3_line.set_value(0)
                IP4_line.set_value(0)
                sleep(0.01)
            else:
                #print('Anit Clock-wise')
                IP1_line.set_value(1)
                IP2_line.set_value(0)
                IP3_line.set_value(0)
                IP4_line.set_value(1)
                sleep(0.01)
            
                IP1_line.set_value(1)
                IP2_line.set_value(1)
                IP3_line.set_value(0)
                IP4_line.set_value(0)
                sleep(0.01)
            
                IP1_line.set_value(0)
                IP2_line.set_value(1)
                IP3_line.set_value(1)
                IP4_line.set_value(0)
                sleep(0.01)
            
                IP1_line.set_value(0)
                IP2_line.set_value(0)
                IP3_line.set_value(1)
                IP4_line.set_value(1)
                sleep(0.01)

        if not (Flag_Start):
            #print('Stop')
            EN1_line.set_value(0)
            EN2_line.set_value(0)
            
            IP1_line.set_value(0)
            IP2_line.set_value(0)
            IP3_line.set_value(0)
            IP4_line.set_value(0)
        
finally:
    EN1_line.release()
    EN2_line.release()
    IP1_line.release()
    IP2_line.release()
    IP3_line.release()
    IP4_line.release()
        
