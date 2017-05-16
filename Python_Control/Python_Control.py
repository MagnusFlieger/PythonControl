import pygame
import serial
import time
import sys

import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
serialport = ""

def getcom():
    for port in ports:
        print(port)
    print("Available Ports")

def connections():
    serialport = input("Enter Xbee Serialport: ")
    print("Establishing connection to: %s" % serialport)
    ser = serial.Serial(serialport, 9600, timeout=1)

    pygame.init()
    j = pygame.joystick.Joystick(0)
    j.init()
    print('Initialized Joystick : %s' % j.get_name())

if __name__== "__main__":
    getcom()
    connections()
