# Fingerprint Sensor R307

The **fingerprint sensor R307** is Serial communication based fingerprint
sensor. It has Facility to *Enroll, Verify and Delete* the enrolled fingerprints.
It has Built-In memory to store the fingerprint data.

## Precaution to take
While interfacing with Raspberry Pi, make sure that **Serial Port** is *Enabled* and 
**Serial Console** is *Disabled* from **Raspberry-Pi Configuration Utility or 
by using command line utility **raspi-config**.

## Connections wit Raspberry Pi

|Raspberry Pi|Fingerprint Module|
|------------|------------------|
|	 SV5	 | J2 (LCD_Data)	|
|	 SV6	 | J1 (LCD_CMD)		|
|	 SV7	 | J3 (Fingerprint) |