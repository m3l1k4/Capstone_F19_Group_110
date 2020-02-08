This code can do the following:
1- Initialize serial communication with XBee.
2- Form XBee local commands to configure XBee.
3- Send clean(or decoded) messages to and receive them from Arduino (messages must start and end with !!!)
4- Stores connected device addresses to text file and loops through them (multi-device communication) until stopped by interrupting kernel
5-  Able to add new devices by adding their addresses to text file.
6- Can view and set local XBee parameters including PAN ID, scan channel, channel verification, coordinator enable and destination address.
7- Copies read data along with address of device data was received from onto a text file.
8 - Includes UI to select what to do

For proper operation, code must be modified to include paths of address text file and data text file.
Only two functions need to be called:
1. initialize(baud rate, serial port) ;both parameters must be entered as strings
2. start() ; this enters UI which can only be exited by interrupting kernel like KeyboardInterrupt