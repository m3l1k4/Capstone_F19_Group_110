#import relevant libraries
import serial
import codecs
import copy
import time
import binascii as ba

#this initializes the port and serial communication, both parameters must be strings
ser = serial.Serial() #initializing
ser.baudrate = 9600 #default baud rate
ser.port = 'COM4' #depends on port of RPi/computer
ser.timeout = 0 #sets timeout to 1 second
ser.open() #opens port

#-------------------------------------------------------------------
# below are used modules for local commands
# baud rate and API mode must be pre-set using XCTU
#-------------------------------------------------------------------------
def find_length(s): #finds hex length of string as byte string
    length_int = int(len(s)/2)
    if length_int < 16:
        hex1 = hex(length_int)
        hex1 = hex1[-1:]
        length = '000' + hex1
    elif length_int >= 16 and length_int < 256:
        hex1 = hex(length_int)
        hex1 = hex1[-2:]
        length = '00' + hex1
    elif length_int >= 256 and length_int < 4096:
        hex1 = hex(length_int)
        hex1 = hex1[-3:]
        length = '0' + hex1
    else:
        hex1 = hex(length_int)
        length = hex1[-4:]
    return length

#-------------------------------------------------------------------------
def checksum_value(s): #finds checksum byte of instruction
    base = 0
    f = ""
    j = ""
    l = [s[k:k+2] for k in range (0, len(s), 2)] #this splits list into blocks of 2
    for x in l: #this does interger addition of all bytes in list
        a = int(x, 16)
        base += a
    b = bin(base) #this converts sum into binary of type string
    for c in range(2, len(b)): #this removes 0b from start of string that shows it is binary string
        f += b[c]
    x = list(f) #this splits string into list
    for i in range(0 , len(x)): #this takes 1's complement of binary list
        if x[i] == '1':
            x[i] = '0'
        else:
            x[i] = '1'
    y = "".join(x) #this joins the list into a string
    z = hex(int(y, 2)) #this converts the base-2 string to a hexadecimal string
    for c in range(2, len(z)): #this removes 0x from hexamdecimal string
        j += z[c]
    return j[-2:] #this outputs only last 2 characters that give checksum byte

#--------------------------------------------------------------------------
def set_command(msb, lsb, param): #forms command to set Channel Verification as on or off
    initial = '7e'
    frame_type = '08'
    frame_id = '01'
    string = frame_type + frame_id + msb + lsb + param
    length = find_length(string)
    checksum = checksum_value(string)
    command = initial + length + string + checksum
    command = codecs.decode(command, "hex") #converts into command
    return command

#--------------------------------------------------------------------------
#below are modules used for setting remote commands
#--------------------------------------------------------------------------

#including remote commands is not a requirement, may be added later

#--------------------------------------------------------------------------
#below are modules for sending and receiving data
#--------------------------------------------------------------------------
def ping(addr, msg): #forms command to ping device of addr(str) with msg(str)
    s = msg.encode('utf-8')
    msg = s.hex()
    initial = '7e'
    frame_type = '10'
    frame_id = '00'
    addr16 = 'fffe'
    broadcast_radius = '00'
    options = '00'
    string = frame_type + frame_id + addr + addr16 + broadcast_radius + options + msg
    length = find_length(string)
    checksum = checksum_value(string)
    command = initial + length + string + checksum
    command = codecs.decode(command, "hex") #converts into command
    return command

#----------------------------------------------------------------------------
def receipt(): #this returns address of sender and message sent
    mask = 0
    start_index = 1010
    end_index = 1000
    string = copy.copy(ser.readline())
    a = ba.hexlify(string)
    b = a.decode('utf-8')
    c = [b[k:k+2] for k in range (0, len(b), 2)] #this splits list into blocks of 2
    for i in range(0, len(c) - 2):
        if c[i] == '7e' and mask == 0: #this identifies first start bit
            addr_start_index = i + 4
            addr_end_index = i + 11
            mask = 1;
        if c[i] == '21' and c[i+1] == '21' and c[i+2] == '21': #extracts starting index of message
            start_index = i + 3
        if c[i] == '3f' and c[i+1] == '3f' and c[i+2] == '3f': #extracts ending index of message
            end_index = i - 1
    if start_index >= end_index or start_index == 1010 or end_index == 1000:
        return "Serial Read Failed"
    else:
        d = [c[i] for i in range(start_index, end_index + 1)]
        e = ''.join(d)
        f = [c[i] for i in range(addr_start_index, addr_end_index + 1)]
        addr = ''.join(f)
        msg = codecs.decode(codecs.decode(e,'hex'),'ascii')
        return [addr, msg]

#------------------------------------------------------------------------
# below are modules for different modes of operation
#------------------------------------------------------------------------
def init_comm(): #this initiates communication
    mask = 0;
    addr_file = open("address.txt", "r")
    addr_list = addr_file.readlines() #we read the entire file and place information in a list
    addr_file.close()
    for i in range(0, len(addr_list)):
        temp = addr_list[i]
        temp = temp[:-1]
        addr_l = []
        addr_l.append(temp)
    data_file = open("data.txt", "a")
    print("Start of data tracking! Interrupt kernel to stop")
    try:
        while True:
            for i in range(0, len(addr_l)):
                addr = addr_l[i]
                msg = "code"
                ser.write(ping(addr,msg)) #ping command sent to end device
                time.sleep(3) #wait for data to be sent, processed and then returned
                temp = receipt()
                rec_addr = temp[0]
                if len(rec_addr) != 16:
                    print("Unable to ping: Device-" + str(i))
                    break
                else:
                    print("Ping Successful for Device-" + str(i))
                rec_msg = temp[1]
                data = rec_addr + " , " + rec_msg + "\n"
                data_file.write(data)
    except KeyboardInterrupt:
        data_file.close() #finish writing to data file
        return print("End of communication")

#------------------------------------------------------------------------
def add_new(): #This adds new devices to connected list
    add_more = 'y'
    addr_file = open("address.txt", "a")
    while (add_more == 'y'):
        mac = input("Add new device MAC address: ")
        if len(mac) != 16:
            print("Invalid MAC address")
        else:
            addr_file.write(mac + "\n")
            add_more = input("Do you want to add new devices? press y/n: ")
    print("Finished adding devices")
    addr_file.close()
    return

#-------------------------------------------------------------------------
# below are modules for viewing and changing settings
#-------------------------------------------------------------------------
def set_settings():
    print("\nChoose from one of the following options: ")
    print("1: Change PAN ID")
    print("2: Change Scan channel")
    print("3: Set Coordinator Enable")
    print("4: Set Channel Verification")
    print("5: Set Destination Address- High")
    print("6: Set Destination Address- Low")
    mode = input("Enter your selection: ")
    print("For the following parameters, enter an even number of hex digits or otherwise specified.")
    if mode == "1":
        param = input("Enter new PAN ID (2-16 hex): ")
        if len(param) % 2 == 0:
            cmd = set_command('49', '44', param)
            ser.write(cmd)
        else:
            print("Invalid! Enter even number of hex digits")
    elif mode == '2':
        param = input("Enter new Scan Channel (1- 4 hex): ")
        if len(param) % 2 == 0:
            cmd = set_command('53', '43', param)
            ser.write(cmd)
        else:
            print("Invalid! Enter even number of hex digits")
    elif mode == '3':
        param = input("Enter 00 to disable and 01 to enable: ")
        if len(param) % 2 == 0:
            cmd = set_command('43', '45', param)
            ser.write(cmd)
        else:
            print("Invalid! Enter even number of hex digits")
    elif mode == '4':
        param = input("Enter 00 to disable and 01 to enable: ")
        if len(param) % 2 == 0:
            cmd = set_command('4a', '56', param)
            ser.write(cmd)
        else:
            print("Invalid! Enter even number of hex digits")
    elif mode == '5':
        param = input("Enter new Destination High (8 hex): ")
        if len(param) % 2 == 0:
            cmd = set_command('44', '48', param)
            ser.write(cmd)
        else:
            print("Invalid! Enter even number of hex digits")
    elif mode == '6':
        param = input("Enter new Destination Low (8 hex): ")
        if len(param) % 2 == 0:
            cmd = set_command('44', '4c', param)
            ser.write(cmd)
        else:
            print("Invalid! Enter even number of hex digits")
    else:
        print("Invalid Selection")
    return

#------------------------------------------------------------------------
def view_setting(msb, lsb):
    param = ''
    d = ''
    cmd = set_command(msb, lsb, param) #send empty command
    ser.write(cmd)
    time.sleep(0.2)
    string = copy.copy(ser.readline())
    a = ba.hexlify(string)
    b = a.decode('utf-8')
    c = [b[k:k+2] for k in range (0, len(b), 2)] #this splits list into blocks of 2
    if c[0] == '7e' and c[3] == '88' and c[7] == '00':
        for i in range (8 , len(c) - 1):
            d += c[i]
        return d
    else:
        print("Error in reading parameters. Check connection.")
        return param

#------------------------------------------------------------------------
def view_settings():
    pan_id = view_setting('49', '44')
    sc = view_setting('53', '43')
    jv = view_setting('4a', '56')
    ce = view_setting('43', '45')
    dh = view_setting('44', '48')
    dl = view_setting('44', '4c')
    if jv == '00':
        jv = 'Disabled'
    elif jv == '01':
        jv = 'Enabled'
    if ce == '00':
        ce = 'Disabled'
    elif ce == '01':
        ce = 'Enabled'
    print("\nPAN ID: "+ pan_id)
    print("Scan Channel: " + sc)
    print("Channel Verification: " + jv)
    print("Coordinator Enable: " + ce)
    print("Destination High: " + dh)
    print("Destination Low: " + dl)
    return

#-------------------------------------------------------------------------

def start(): #this is the main program executable
    addr_file = open("address.txt", "r") #open address.txt and print added devices and prints list
    print("Connected devices are: ")
    for addr in addr_file: #this shows existing devices
        print(addr)
    addr_file.close()
    print("\nChoose from one of the following options:")
    print("1: Enter data tracking mode")
    print("2: View local settings")
    print("3: Change local settings")
    print("4: Add new devices")
    mode = input("Enter your selection: ")
    if mode == '1':
        init_comm()
    elif mode == '2':
        view_settings()
    elif mode == '3':
        set_settings()
    elif mode == '4':
        add_new()
    else:
        print("Invalid selection!")
    ser.close()
    return print("Terminated")
        
################################################################################
################################################################################
################################################################################
