#Imports
import pygame
import serial
import sys
from time import sleep
import serial.tools.list_ports

#CONSTANTS
SPEED_MIN = 0
SPEED_MAX = 100

#Variables
ports = list(serial.tools.list_ports.comports())
serialport = ""

#Speed setting: SPEED_MIN - SPEED_MAX
currentSpeedSetting = SPEED_MIN


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
    global currentSpeedSetting

    #Read from serial
    recieved = ser.read_all()
    #TODO: Is everything ok on the Arduino?
        
    #Get values from joystick
    out = 0
    pygame.event.pump()
    out = j.get_axis(2)
    print('GetAxisY')
    #out = (out * 90.0) + 90.0
    out = int(out * 2)
    print(out)
    if out < 0:
        if currentSpeedSetting > SPEED_MIN:
            currentSpeedSetting = currentSpeedSetting + out
    elif out > 0:
        if currentSpeedSetting < SPEED_MAX:
            currentSpeedSetting = currentSpeedSetting + out
    print("Current speed setting: " + str(currentSpeedSetting))

    #Write to serial
    #inputFromUser = input("Enter value: ")

    #valueToWrite = inputFromUser.encode('utf-8')
        
    #ser.write(valueToWrite)

    #ser.write(bytes([currentSpeedSetting]))

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
