import pygame
import serial
import sys
from time import sleep

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

def move():
    while True:
        out = 0
        pygame.event.pump()
        out = j.get_axis(1)
        print('GetAxisY')
        out = (out * 90.0) + 90.0
        print(out)
        out = int(out)
        move(out)



if __name__== "__main__":
    getcom()
    connections()
    move()
