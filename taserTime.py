###HID interfacing with mouse to ensure pain :) I hate myself
import time
import serial
import serial.tools.list_ports

def openR(s):
    s.open()
    s.write(b'\xa0\x01\x01\xa2')
    s.close()

def closeR(s):
    s.open()
    s.write(b'\xa0\x01\x00\xa1')
    s.close()

def hurt(sec):
    #device setup
    ports = [comport.device for comport in serial.tools.list_ports.comports()]
    s = serial.Serial()
    if len(ports) > 0:
        s.port = ports[0]
    else:
        print('no serial connections found')
        return
    s.baudrate=9600
    openR(s)
    time.sleep(sec)
    closeR(s)

c = 0

hurt(0.75)
