#Imports
import sys
from time import sleep

import pygame
import serial
import serial.tools.list_ports

import GUI

#CONSTANTS
SPEED_MIN = 0
SPEED_MAX = 100
SPEED_FACTOR = 5
SERVO_MIN = 0
SERVO_MAX = 180
LR_MIN = -90
LR_MAX = 90
LR_HALF = 0
LR_FACTOR = 5
UD_MIN = -90
UD_MAX = 90
UD_HALF = 0
UD_FACTOR = 5

#Variables
ports = list(serial.tools.list_ports.comports())
serialport = ""

#Speed setting: SPEED_MIN - SPEED_MAX
currentSpeedSetting = SPEED_MIN
currentLeftRightSetting = LR_HALF
currentUpDownSetting = UD_HALF

def getCOM():
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
    while not done:
        update()
        updateGUI()
        sleep(0.1)


def update():
    global currentSpeedSetting
    global currentLeftRightSetting
    global currentUpDownSetting

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
    deltaSpeed = int(deltaSpeed * SPEED_FACTOR)
    deltaLeftRight = int(deltaLeftRight * LR_FACTOR)
    deltaUpDown = int(deltaUpDown * UD_FACTOR)

    #Calculate new current settings
    currentSpeedSetting = currentSpeedSetting + deltaSpeed
    if currentSpeedSetting < SPEED_MIN:
        currentSpeedSetting = SPEED_MIN
    if currentSpeedSetting > SPEED_MAX:
        currentSpeedSetting = SPEED_MAX
    currentLeftRightSetting = currentLeftRightSetting + deltaLeftRight
    if currentLeftRightSetting < LR_MIN:
        currentLeftRightSetting = LR_MIN
    if currentLeftRightSetting > LR_MAX:
        currentLeftRightSetting = LR_MAX
    currentUpDownSetting = currentUpDownSetting + deltaUpDown
    if currentUpDownSetting < UD_MIN:
        currentUpDownSetting = UD_MIN
    if currentUpDownSetting > UD_MAX:
        currentUpDownSetting = UD_MAX

    #Write to serial
    #Calibrate values so they fit into the 0-180 range
    outSpeedSetting = currentSpeedSetting
    outLeftRightSetting = currentLeftRightSetting + 90
    outUpDownSetting = currentUpDownSetting + 90

    ser.write(bytes([outSpeedSetting]))


def updateGUI():
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(GUI.WHITE)
    textPrint.reset()

    # Get count of joysticks
    textPrint.print(screen, "CONTROL PANEL")

    textPrint.print(screen, "Speed")
    textPrint.indent()
    textPrint.drawProgressBar(screen, (currentSpeedSetting / 100))
    textPrint.unindent()

    textPrint.print(screen, "Left-Right")
    textPrint.indent()
    textPrint.drawProgressBar(screen, (currentLeftRightSetting / 180 + 0.50))
    textPrint.unindent()

    textPrint.print(screen, "Up-Down")
    textPrint.indent()
    textPrint.drawProgressBar(screen, (currentUpDownSetting / 180 + 0.50))
    textPrint.unindent()

    textPrint.print(screen, "Current speed setting: " + str(currentSpeedSetting))
    textPrint.print(screen, "Current left right setting: "+ str(currentLeftRightSetting))
    textPrint.print(screen, "Current up down setting: " + str(currentUpDownSetting))

    textPrint.printEmptyLine(screen)
    textPrint.print(screen, "MAGNUSFLIEGER STATUS")
    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

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
    serialport = getCOM()
    print("Establishing connection to: %s" % serialport)
    ser = serial.Serial(serialport, 9600, timeout=1)
except:
    print("Error establishing connection to serial port. Exiting now")
    exit()

#Set up GUI
# Set the width and height of the screen [width,height]
size = [500, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Control")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Get ready to print
textPrint = GUI.TextPrint()

#Setting up finished, now loop
if __name__ == "__main__":
    loop()

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit ()
