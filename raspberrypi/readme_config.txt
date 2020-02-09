This code can do the following:
1- Initialize serial communication with XBee.
2- Send clean(or decoded) messages to and receive them from Arduino (received messages must start with !!! and end with ???)
3- Stores connected device addresses to text file and loops through them (multi-device communication) until stopped by interrupting kernel
4-  Able to add new devices by adding their addresses to text file.
5- Can view and set local XBee parameters including PAN ID, scan channel, channel verification, coordinator enable and destination address.
6- Copies read data along with address of device data was received from onto a text file.
7 - Includes UI to select what to do

For proper operation, code must be modified to set baud rate, serial port and  paths of address text file and data text file.
Need to run start() only to enter UI. This can be running start once can let you start data tracking mode, view settings, change settings and add new devices. To remove devices, address text file must be modified. running start once will let you run any of these operations once, however we will stay in data tracking mode until kernel is interrupted, using KeyboardInterrupt or other.

The accompanying arduino serial traceiver code provides a template to ping the end device and receive a response. This is used to test the codes functionality.
