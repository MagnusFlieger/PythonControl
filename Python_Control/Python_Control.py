#Imports
import pygame
import serial
import sys
from time import sleep
import serial.tools.list_ports

#Variables
ports = list(serial.tools.list_ports.comports())
serialport = ""


def getcom():
    for port in ports:
        print(port)
    print("Available Ports")

#Send the position out to the servo
def move(angle):
    ser.write(angle)

#Function that runs forever after all is set up
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

#Setting up
pygame.init()

try:
    j = pygame.joystick.Joystick(0)
except:
    print("Error initializing joystick. ")
    exit()

j.init()
print('Initialized Joystick : %s' % j.get_name())

getcom()

serialport = input("Enter Xbee Serialport: ")
print("Establishing connection to: %s" % serialport)
ser = serial.Serial(serialport, 9600, timeout=1)

if __name__== "__main__":
    forward()
