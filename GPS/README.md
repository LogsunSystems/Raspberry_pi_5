# Global Positioning System (GPS) [NEO-6] 

The GPS sensor **NEO-6** is Serial communication based GPS
sensor. You need to connect external Antenna with *UFL Connector* to the GPS sensor
for communicating with GPS satellites.

After connecting the antenna and Powering ON the GPS module it will take around 5-15 minutes 
of time to get connected with satellites. The waiting time can get extended up-to 30 minutes 
in worst situations.

Once the GPS module gets established communication with GPS satellites the **LED** on the 
module starts *blinking*. Don't execute the program on the module before GPS module gets
connected to GPS satellites.


## Precaution to take
While interfacing with Raspberry Pi, make sure that **Serial Port** is *Enabled* and 
**Serial Console** is *Disabled* from **Raspberry-Pi Configuration Utility or 
by using command line utility **raspi-config**.

## Connections wit Raspberry Pi

|Raspberry Pi|     GPS Module   |
|:----------:|:----------------:|
|	 SV5	 | J2 (LCD_Data)	|
|	 SV6	 | J1 (LCD_CMD)		|
|	 SV8	 | J3 (GPS  Sensor) |
