## 27 January 2020
##
## The following sample code uses the PySerial package to connect to
## a serial device and reads data from the serial device until user
## inputs -1.
##
## For our purposes, we are using an XBee antenna and receiving data
## from another XBee antenna.

import serial

## /dev/ttyUSB0 is the USB port for the XBee antenna.
device = serial.Serial('/dev/ttyUSB0')
device.baudrate = 9600

## Looks like while the program is blocked the input(),
## the device continues to buffer the incoming data.
##
## e.g. If the user stalls a "long time" before continuing,
## the data will be printed instantly rather than waiting for
## new data line by line.
while input("Read next 10 lines?") != -1:
    for i in range(10):
        print(device.readline())
    
try:
    device.close()
    print("Device connection closed successfully.")
except:
    print("Error: Device connection did not close successfully.")

## The digi.xbee library/package has issues with the method
## .open()
## The program stalls at the line and does not finish unless user
## explicitly stops program.
##
##from digi.xbee.devices import XBeeDevice
##
##device = XBeeDevice("/dev/ttyUSB0", 9600)
##print("device instantiated")
##device.open()
##print("device open")
##device.close()