#Imports
import pygame
import serial
import sys
from time import sleep
import serial.tools.list_ports

#CONSTANTS
SPEED_MIN = 0
SPEED_MAX = 100
SERVO_MIN = 0
SERVO_MAX = 180
LR_MIN = -90
LR_MAX = 90
UD_MIN = -90
UD_MAX = 90

#Variables
ports = list(serial.tools.list_ports.comports())
serialport = ""

#Speed setting: SPEED_MIN - SPEED_MAX
currentSpeedSetting = SPEED_MIN
currentLeftRightSetting = 0
currentUpDownSetting = 0


def getcom():
    #Is list ports empty?
    if not ports:
        print("No Serial Ports found! Exiting now")
        exit()
    #If there is only one port available, automatically use that one
    if len(ports) == 1:
        return ports[0].device

    #Display all available ports if there are more than one available
    print("Available Ports: ")
    for port in ports:
        print(port)
    return input("Enter Xbee Serialport: ")

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
    deltaSpeed = 0
    deltaLeftRight = 0
    deltaUpDown = 0

    pygame.event.pump()

    #Get the values from the axes
    deltaSpeed = j.get_axis(2)
    deltaLeftRight = j.get_axis(4)
    deltaUpDown = j.get_axis(3)
    
    #Figure out delta values
    #out = (out * 90.0) + 90.0
    deltaSpeed = int(deltaSpeed * 5)

    print("DeltaSpeed: " + str(deltaSpeed))
    print("DeltaLeftRight: " + str(deltaLeftRight))
    print("DeltaUpDown: " + str(deltaUpDown))

    #Calculate new current settings
    currentSpeedSetting = currentSpeedSetting + deltaSpeed
    if currentSpeedSetting < SPEED_MIN:
        currentSpeedSetting = SPEED_MIN
    if currentSpeedSetting > SPEED_MAX:
        currentSpeedSetting = SPEED_MAX

    print("Current speed setting: " + str(currentSpeedSetting))
    print("Current left right setting: "+ str(currentLeftRightSetting))
    print("Current up down setting: " + str(currentUpDownSetting))

    #Write to serial
    #inputFromUser = input("Enter value: ")

    #valueToWrite = inputFromUser.encode('utf-8')
        
    #ser.write(valueToWrite)

    #Calibrate values so they fit into the 0-180 range


    ser.write(bytes([currentSpeedSetting]))

    print(ser.read_all())

#Setting up joystick
pygame.init()

try:
    j = pygame.joystick.Joystick(0)
except:
    print("Error initializing joystick. Exiting now")
    exit()

j.init()
print('Initialized Joystick : %s' % j.get_name())

#Setting up XBee Serial

try:
    serialport = getcom()
    print("Establishing connection to: %s" % serialport)
    ser = serial.Serial(serialport, 9600, timeout=1)
except:
    print("Error establishing connection to serial port. Exiting now")
    exit()

#Setting up finished, now loop
if __name__ == "__main__":
    loop()
