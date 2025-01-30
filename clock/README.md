
# 7 Segment Display [TM1637]

As Name indicates, the 7 Segment Display have seven different segments.  Additionally it have Decimal points 
and Colon to in case of clock application. Each seggmetn have asociated a LED behind it. We need to Control each
LED to display diffrent numbers. If we coonect each segment to differnet GPIO it will eangage lot 
of GPIOs of the Raspberry PI.

Thanks to TM1637 Driver which controls the 4 digit 7 segment display by using only 4 pins

## Connection with Raspberry Pi

|RPI Connector|7-Segment|
|:-----------:|:-------:|
|	SV8		  |	  J1    |
