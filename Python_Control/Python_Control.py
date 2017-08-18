"""
This script will run on the main control computer.
"""

__version__ = '0.1'
__author__ = 'MINT@GESS'

#Imports
import sys
from time import sleep
import logging

import pygame
import serial
import serial.tools.list_ports

import GUI
import Settings
import StatusReport

#CONSTANTS
SPEED_MIN = 0       #Minimum speed value
SPEED_MAX = 100     #Maximum speed value
SPEED_FACTOR = 5    #Factor by which the joystick value is multiplied
SERVO_MIN = 0       #Minimum value to send to a servo
SERVO_MAX = 180     #Maxium value to send to a servo
LR_MIN = -90        #Minimum left-right value
LR_MAX = 90         #Maximum left-right value
LR_HALF = 0         #Middle of left-right
LR_FACTOR = 6       #Factor by which the joystick value is multiplied
UD_MIN = -90        #Minimum up-down value
UD_MAX = 90         #Maximum up-down value
UD_HALF = 0         #Middle of up-down
UD_FACTOR = 7       #Factor by which the joystick value is multiplied
FRONT_MIN = 0       #Minimum rotating cylinder (front) value
FRONT_MAX = 100     #Maximum rotating cylinder (front) value
FRONT_FACTOR = 5    #Factor by which the joystick value is multiplied
BACK_MIN = 0        #Minimum rotating cylinder (back) value
BACK_MAX = 100      #Maximum rotating cylinder (back) value
BACK_FACTOR = 5     #Factor by which the joystick value is multiplied

BYTES_EXPECTED_TO_RECIEVE = 5   #Number of bytes we should get from the Arduino via Xbee

#Variables
ser = None                                          #The serial port
j = None                                            #The joystick
screen = None                                       #The window for display
textPrint = None                                    #The method for drawing text
clock = None                                        #The method for controlling the display
status = StatusReport.StatusReport()                #The status of the MagnusFlieger
recieved = None                                     #Bytes recieved via XBee

# The current settings we have on this controller
currentSettings = Settings.Settings(SPEED_MIN, LR_HALF, UD_HALF, FRONT_MIN, BACK_MIN)

# The settings of the previous iteration
lastSettings = Settings.Settings.EmptySettings()

# The settings reported by the MagnusFlieger
arduinoSettings = currentSettings.copy()

def getCOM():
    """
    Function that returns the COM port of the XBee (if available)
    """
    ports = list(serial.tools.list_ports.comports())

    #Is list ports empty?
    if not ports:
        logging.critical("No Serial Ports found! Exiting now")
        exit()

    #If there is only one port available, automatically use that one
    if len(ports) == 1:
        return ports[0].device

    #Display all available ports if there are more than one available
    print("Available Ports: ")
    for port in ports:
        print(port)
    return input("Enter Xbee Serialport: ")

def loop():
    """
    Function that runs forever after all is set up
    """

    global done

    while not done:
        update()
        updateGUI()
        sleep(0.1)


def update():
    """
    Function that controls one iteration of the loop() function
    """
    global currentSettings
    global lastSettings

    global recieved

    global status

    #Read from serial
    recieved = ser.read_all()
    if len(recieved) != BYTES_EXPECTED_TO_RECIEVE:
        #Incomplete/insufficient data recieved!
        everythingFine = False
        if not recieved:
            #Nothing recieved!
            errorMessage = "Nothing recieved via serial!"
        else:
            errorMessage = "Wrong amount of data recieved!"
    
    else:
        #Get status report
        # A - everything ok
        # B - battery low
        # C - other battery error
        # D - motor error
        # E - servo error
        # F - sensor error
        # G - other hardware error
        # H - internal Arduino error
        # I - other error
        statusReport = recieved[0]

        if statusReport != 'A':
            pass
        else:
            pass

        #Get other data
        
    #Get values from joystick
    deltaSpeed = 0 #Change in speed
    deltaLeftRight = 0 #Change in Left-Right
    deltaUpDown = 0 #Change in Up-Down

    pygame.event.pump()

    #Get the values from the axes
    deltaSpeed = j.get_axis(2)      #LT and RT
    deltaLeftRight = j.get_axis(4)  #x-axis of right axis
    deltaUpDown = j.get_axis(3)     #y-axis of right axis

    #Get the values from the buttons
    startButton = bool(j.get_button(7)) #Start button: Used for initializing everything
    backButton = bool(j.get_button(6))  #Back button: Used for toggling stabilizing
    XButton = bool(j.get_button(2))     #X: Used for
    YButton = bool(j.get_button(3))     #Y: Used for
    AButton = bool(j.get_button(0))     #A: Used for
    BButton = bool(j.get_button(1))     #B: Used for
    LBButton = bool(j.get_button(4))    #LB: Used for
    RBButton = bool(j.get_button(5))    #RB: Used for

    #Get the values from the hat
    hat = j.get_hat(0)
    deltaFront = hat[0]             #x-axis of the hat
    deltaBack = hat[1]              #y-axis of the hat
    
    #Figure out delta values
    deltaSpeed = int(deltaSpeed * SPEED_FACTOR)
    deltaLeftRight = int(deltaLeftRight * LR_FACTOR)
    deltaUpDown = int(deltaUpDown * UD_FACTOR)
    deltaFront = int(deltaFront * FRONT_FACTOR)
    deltaBack = int(deltaBack * BACK_FACTOR)

    #Calculate new current settings
    currentSettings.speed = Settings.KeepInBoundary(currentSettings.speed + deltaSpeed,
                                                    SPEED_MAX, SPEED_MIN)

    currentSettings.leftRight = Settings.KeepInBoundary(currentSettings.leftRight + deltaLeftRight,
                                                        LR_MAX, LR_MIN)
    
    currentSettings.upDown = Settings.KeepInBoundary(currentSettings.upDown + deltaUpDown,
                                                     UD_MAX, UD_MIN)
    
    currentSettings.front = Settings.KeepInBoundary(currentSettings.front + deltaFront,
                                                    FRONT_MAX, FRONT_MIN)
    
    currentSettings.back = Settings.KeepInBoundary(currentSettings.back + deltaBack,
                                                   BACK_MAX, BACK_MIN)

    #Write to serial
    #Calibrate values so they fit into the 0-180 range
    outSettings = Settings.Settings(int(float(currentSettings.speed) * 1.8),
                                    currentSettings.leftRight + 90,
                                    currentSettings.upDown + 90,
                                    0,
                                    0)
    if not currentSettings == lastSettings:
        ser.write(bytes(outSettings))

    #ITERATION OFFICIALLY ENDS HERE
    #Write to the settings of the previous iteration
    lastSettings = currentSettings.copy()

def updateGUI():
    """
    Function that updates the GUI display (pygame)
    """

    global done
    
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            logging.info("User induced a quit via the close button")
            done = True # Flag that we are done so we exit this loop
        
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(GUI.WHITE)
    textPrint.reset()

    # Now print info
    textPrint.printLine(screen, "CONTROL PANEL", GUI.BLUE)

    textPrint.printLine(screen, "Speed")
    textPrint.indent()
    textPrint.drawProgressBar(screen, (currentSettings.speed / 100))
    textPrint.unindent()

    textPrint.printLine(screen, "Left-Right")
    textPrint.indent()
    textPrint.drawPositiveNegativeProgressBar(screen, (currentSettings.leftRight / 90))
    textPrint.unindent()

    textPrint.printLine(screen, "Up-Down")
    textPrint.indent()
    textPrint.drawPositiveNegativeProgressBar(screen, (currentSettings.upDown / 90))
    textPrint.unindent()

    textPrint.printLine(screen, "Current speed setting: " + str(currentSettings.speed))
    textPrint.printLine(screen, "Current left right setting: "+ str(currentSettings.leftRight))
    textPrint.printLine(screen, "Current up down setting: " + str(currentSettings.upDown))
    textPrint.printLine(screen, "Current front setting: " + str(currentSettings.front))
    textPrint.printLine(screen, "Current back setting: " + str(currentSettings.back))

    textPrint.printEmptyLine(screen)
    textPrint.printLine(screen, "MAGNUSFLIEGER STATUS", GUI.BLUE)

    textPrint.printLine(screen, "Recieved via serial: " + str(recieved))

    textPrint.printEmptyLine(screen)
    textPrint.printLine(screen, "DIAGNOSTICS", GUI.BLUE)

    textPrint.printEmptyLine(screen)
    textPrint.printLine(screen, "Press START for ")
    textPrint.printLine(screen, "Press BACK for")
    textPrint.printLine(screen, "Press Y for ", GUI.YELLOW)
    textPrint.printLine(screen, "Press X for ", GUI.BLUE)
    textPrint.printLine(screen, "Press A for ", GUI.GREEN)
    textPrint.printLine(screen, "Press B for ", GUI.RED)

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

def init():
    """
    This function initailizes all of PythonControl
    """
    global done
    global ser
    global j
    global screen
    global textPrint
    global clock
    # PROGRAM STARTS HERE

    # Set up logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                        level=logging.DEBUG,
                        filename='PythonControl.log')

    logging.info("PythonControl started")

    #Setting up joystick
    pygame.init()

    try:
        j = pygame.joystick.Joystick(0)
    except:
        logging.critical("Error initializing joystick. Exiting now")
        exit()

    j.init()
    logging.info('Initialized Joystick: ' + str(j.get_name()))

    #Setting up XBee Serial

    try:
        serialport = getCOM()
        logging.info("Establishing connection to: " + str(serialport))
        ser = serial.Serial(serialport, 9600, timeout=1)
    except:
        logging.critical("Error establishing connection to serial port. Exiting now")
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

if __name__ == "__main__":
    init()

    loop()

    #CODE AFTER THIS LINE IS CLEAN UP AFTER EXIT
    #Close serial

    logging.info("Closing serial...")
    ser.close()
    # Close the window and quit.

    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    logging.info("Terminating Pygame...")
    pygame.quit()
    logging.info("PythonControl terminated")
