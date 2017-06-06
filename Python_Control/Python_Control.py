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
    #Is list ports empty?
    if not ports:
        print("No Serial Ports found!")
        exit()
    #If there is only one port available, automatically use that one
    if len(ports) == 1:
        return ports[0].device

    #Display all available ports if there are more than one available
    for port in ports:
        print(port)
    print("Available Ports: ")
    return

#Send the position out to the servo
def move(angle):
    ser.write(angle)

#Function that runs forever after all is set up
def loop():
    while True:
        update()
        sleep(0.1)


def update():
    #Read from serial
    #TODO: Is everything ok on the Arduino?
        
    #Get values from joystick
    out = 0
    pygame.event.pump()
    out = j.get_axis(1)
    print('GetAxisY')
    out = (out * 90.0) + 90.0
    out = int(out)
    out = bytes([out])
    print(out)

    #Write to serial
    #inputFromUser = input("Enter value: ")

    #valueToWrite = inputFromUser.encode('utf-8')
        
    #ser.write(valueToWrite)

    ser.write(out)

    print(ser.read_all())

#Setting up joystick
pygame.init()

try:
    j = pygame.joystick.Joystick(0)
except:
    print("Error initializing joystick. ")
    exit()

j.init()
print('Initialized Joystick : %s' % j.get_name())

#Setting up XBee Serial
resultFromGetCom = getcom()

if resultFromGetCom != "":
    serialport = resultFromGetCom
else:
    serialport = input("Enter Xbee Serialport: ")

print("Establishing connection to: %s" % serialport)
ser = serial.Serial(serialport, 9600, timeout=1)

#Setting up finished, now loop
if __name__ == "__main__":
    loop()
