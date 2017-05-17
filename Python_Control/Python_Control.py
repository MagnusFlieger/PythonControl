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

def move(angle):
    ser.write(angle)

def forward():
    while True:
        out = 0
        pygame.event.pump()
        out = j.get_axis(1)
        print('GetAxisY')
        out = (out * 90.0) + 90.0
        out = int(out)
        print(out)
        move(out)
        sleep(0.3)




pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print('Initialized Joystick : %s' % j.get_name())

getcom()
serialport = input("Enter Xbee Serialport: ")
print("Establishing connection to: %s" % serialport)
ser = serial.Serial(serialport, 9600, timeout=1)

def getcom():
    for port in ports:
        print(port)
    print("Available Ports")

def move(angle):
    ser.write(angle)

def forward():
    while True:
        out = 0
        pygame.event.pump()
        out = j.get_axis(1)
        print('GetAxisY')
        out = (out * 90.0) + 90.0
        out = int(out)
        print(out)
        move(out)
        sleep(0.3)



if __name__== "__main__":
    forward()
