# Raspberry Pi Camera Module 
**Raspberry Pi** has build in connector to connect Ribbon camera.
The camera libraries are pre-built in raspbean OS.


## Camera Cable
**Raspberry Pi 5** hace two connectora for connecting camera and ddisplay. Both the connectors are compatible with both camera and 
Display. The cables for Camera and Display are diffrent.

Also, for Raspberry Pi 5 the regular camera cable is not compatible, as\connector on Raspberry pi 5 is not same the connector 
on *Raspberry Ppi 4*. So if you have RPI-4 Camera module with cable, you need to purchase new cable.

Whille purchasing the new cable , select the cable carefully, as camera cable and display cable for
Raspberry pi 5 are looks exact same. It's printed on themwhther its camera cable or dislay cable. 

## Connections
The new camera cable have different size at both the ends, one is small andanother is slightly bigger.
Connect the small end at Raspberry pi 5 connector and bigger end to Camera Module. Make sure that the 
Raspberyy Pi is not powered ON while connecting the camera to it to avoid any potential damage to either device.


## Usage

To test the camera open the terminal by pressing `CTRL+ALT+T`

To test the Software, use follwing command

```
libcamera-hello
```

To Capture Image

```
libcamera-jpeg -o Test.jpeg
```

To Capture a Video

```
libcamera-vid -t 10s -o Test.mp4
```

