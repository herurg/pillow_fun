import serial
import serial.tools.list_ports


def get_ports():
    ports = serial.tools.list_ports.comports()
    if ports:
        return str(ports[0]).split(' ')[0]
    else:
        return 'NO PORTS'


serial_on=True
'''
ports = serial.tools.list_ports.comports()
if ports:
    print(ports[0])
else:
    serial_on=False
    





for port in ports:
    print(port)
serial_on = True
'''

if get_ports()!='NO CONTROLLER':
    ser = serial.Serial(get_ports(),115200)
else:
    serial_on = False


while True:
    if (serial_on):
        dt = str(ser.readline())
        if "P1" in dt:
            print("Player 1")
        if "P2" in dt:
            print("Player 2")
        
    else:
        print("No serial")
