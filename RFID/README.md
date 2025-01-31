# RFID Reader [MFRC522]

As Name suggesdts, **RFID** is Radio Frequency based identificatin technique.
The RFID reader **MFRC522** is working on **13.2MHz** Frequency. So any RFID
tag of 13.2 MHz frequency can be read by this reader.

The MFRC522 uses SPI communication, which used 4 pins additonal one 
pin is required for **RST** i.e. *Reset* signal.

## Wiring Connections

|Rasoberry pi|RFID Reader |
|:----------:|:----------:|
|	SV5		 |J1(LCD_CMD) |
|	SV6		 |J2(LCD_DATA)|
|	SV7		 |J3(RFID)    |
