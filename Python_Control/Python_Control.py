"""
This script will run on the main control computer.
"""

__version__ = '0.1'
__author__ = 'MINT@GESS'

#Imports
import logging
import sys
from time import sleep

import pygame
import serial
import serial.tools.list_ports

import Comm
import GUI
import JoystickState
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

MAX_NUM_OF_ITERATIONS = 300     #If this threshold is overshot, we can count the
                                # connection as lost

#Variables
ser = None                                          #The serial port
j = None                                            #The joystick
screen = None                                       #The window for display
textPrint = None                                    #The method for drawing text
clock = None                                        #The method for controlling the display
status = StatusReport.StatusReport()                #The status of the MagnusFlieger
iterations_since_last_status_recieved = 0           #The number of iterations since the last
                                                    # status message was recieved
is_xbee_communication_alive = False                 #Is a connection established
                                                    # (in other words: was the last status not
                                                    #  too long ago)
recieved = None                                     #Bytes recieved via XBee

# The current settings we have on this controller
currentSettings = Settings.Settings(SPEED_MIN, LR_HALF, UD_HALF, FRONT_MIN, BACK_MIN)

# The settings of the previous iteration
lastSettings = Settings.Settings.EmptySettings()

# The settings reported by the MagnusFlieger
arduinoSettings = currentSettings.copy()

# The current button state we have on this controller
# This is used to detect when exactly a button has been pressed and lifted
j_state = JoystickState.JoystickState.empty_state()

# The settings of the previous iteration
previous_j_state = JoystickState.JoystickState.empty_state()

def get_com_port():
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

    global j_state
    global previous_j_state

    global recieved

    global status
    global is_xbee_communication_alive
    global iterations_since_last_status_recieved

    #Read from serial
    recieved = ser.read_all()
    status_recieved = False
    for read in recieved:
        # What does the byte signal?
        # Status reports
        if StatusReport.StatusReport.is_status_char(read):
            status.parse_char(read)
            iterations_since_last_status_recieved = 0
            status_recieved = True

        # Confirmation messages
        if read == Comm.R_STABILIZING_ON_CONFIRM:
            # Only set Stabilizing on if we really requested that stabilizing be turned on
            if currentSettings.stabilizing == Settings.BooleanSettingStates.on_but_awaiting_confirmation:
                currentSettings.stabilizing == Settings.BooleanSettingStates.on
        
        elif read == Comm.R_STABILIZING_OFF_CONFIRM:
            # Only set Stabilizing off if we really requested that
            if currentSettings.stabilizing == Settings.BooleanSettingStates.off_but_awaiting_confirmation:
                currentSettings.stabilizing = Settings.BooleanSettingStates.off

        elif read == Comm.R_SENSORS_ON_CONFIRM:
            # Only set Sensors to on if we really requested that
            if currentSettings.sensor == Settings.BooleanSettingStates.on_but_awaiting_confirmation:
                currentSettings.sensor = Settings.BooleanSettingStates.on

        elif read == Comm.R_SENSORS_OFF_CONFIRM:
            # Only set Sensors to off if we really requested that
            if currentSettings.sensor == Settings.BooleanSettingStates.off_but_awaiting_confirmation:
                currentSettings.sensor = Settings.BooleanSettingStates.off

    #Process status further
    if status_recieved:
        is_xbee_communication_alive = True
    else:
        iterations_since_last_status_recieved += 1
        # If the number of iterations since the last status was recieved
        # exceeds the threshold, the connection is not alive anymore.
        if iterations_since_last_status_recieved > MAX_NUM_OF_ITERATIONS:
            is_xbee_communication_alive = False
    
    #Get values from joystick
    deltaSpeed = 0          #Change in speed
    deltaLeftRight = 0      #Change in Left-Right
    deltaUpDown = 0         #Change in Up-Down

    pygame.event.pump()

    #Get the values from the axes
    deltaSpeed = j.get_axis(2)      #LT and RT
    deltaLeftRight = j.get_axis(4)  #x-axis of right axis
    deltaUpDown = j.get_axis(3)     #y-axis of right axis

    #Get the values from the buttons
    j_state = JoystickState.JoystickState.from_joystick(j)

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

    # Send commands
    # Loop through all newly pressed buttons
    for button in j_state.get_pressed_buttons(previous_j_state):
        if button == JoystickState.JoystickState.Buttons.start:
            logging.info("START pressed")
            # Send a reset command
            ser.write(Comm.S_RESET_COMMAND)

        if button == JoystickState.JoystickState.Buttons.back:
            logging.info("BACK pressed")
            # Toggle self-stabilizing
            # If stabilizing is currently off, toggle it to on (but wait for confirmation)
            if currentSettings.stabilizing == Settings.BooleanSettingStates.off:
                ser.write(Comm.S_STABILIZING_ON_COMMAND)
                currentSettings.stabilizing = Settings.BooleanSettingStates.on_but_awaiting_confirmation
            # If stabilizing is currently on, toggle it to off (but wait for confirmation)
            if currentSettings.stabilizing == Settings.BooleanSettingStates.on:
                ser.write(Comm.S_STABILIZING_OFF_COMMAND)
                currentSettings.stabilizing = Settings.BooleanSettingStates.off_but_awaiting_confirmation

        if button == JoystickState.JoystickState.Buttons.y:
            logging.info("Y pressed")
            # Toggle Gyro-Sensor
            # If sensor is currently off, toggle it to on (but wait for confirmation)
            if currentSettings.sensor == Settings.BooleanSettingStates.off:
                ser.write(Comm.S_SENSORS_ON_COMMAND)
                currentSettings.sensor = Settings.BooleanSettingStates.on_but_awaiting_confirmation
            # If sensor is currently on, toggle it to off (but wait for confirmation)
            if currentSettings.sensor == Settings.BooleanSettingStates.on:
                ser.write(Comm.S_SENSORS_OFF_COMMAND)
                currentSettings.sensor = Settings.BooleanSettingStates.off_but_awaiting_confirmation

        if button == JoystickState.JoystickState.Buttons.x:
            logging.info("X pressed")
            # Toggle Flight recorder
            # If flight recorder is currently off, toggle it to on (but wait for confirmation)
            if currentSettings.flight_recorder == Settings.BooleanSettingStates.off:
                ser.write(Comm.S_FLIGHT_REC_ON_COMMAND)
                currentSettings.flight_recorder = Settings.BooleanSettingStates.on_but_awaiting_confirmation
            # If flight recorder is currently on, toggle it to off (but wait for confirmation)
            if currentSettings.flight_recorder == Settings.BooleanSettingStates.on:
                ser.write(Comm.S_FLIGHT_REC_OFF_COMMAND)
                currentSettings.flight_recorder = Settings.BooleanSettingStates.off_but_awaiting_confirmation

        if button == JoystickState.JoystickState.Buttons.a:
            logging.info("A pressed")
        if button == JoystickState.JoystickState.Buttons.b:
            logging.info("B pressed")
            # Send an emergency command
            ser.write(Comm.S_EMERGENCY_COMMAND)
        if button == JoystickState.JoystickState.Buttons.lb:
            logging.info("LB pressed")
        if button == JoystickState.JoystickState.Buttons.rb:
            logging.info("RB pressed")

    # Calibrate values so they fit into the 0-180 range
    # We create a final Settings that will be sent directly to the Arduino
    outSettings = Settings.Settings(int(float(currentSettings.speed) * 1.8),
                                    currentSettings.leftRight + 90,
                                    currentSettings.upDown + 90,
                                    0,
                                    0)
    
    # If there are differences in the settings last sent 
    # and the current out settings, then send
    if not outSettings == lastSettings:
        bys = outSettings.deltaBytes(lastSettings)
        ser.write(bys)

    #ITERATION OFFICIALLY ENDS HERE
    #Write to the settings of the previous iteration
    lastSettings = outSettings.copy()
    previous_j_state = j_state.copy()

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

    textPrint.drawBooleanBox(screen, "Connection", is_xbee_communication_alive,
                             bg_color_true=GUI.GREEN, bg_color_false=GUI.DA_GRAY)
    textPrint.indent_box()
    textPrint.drawBooleanBox(screen, "Master", status.everything_ok,
                             bg_color_true=GUI.GREEN, bg_color_false=GUI.RED)
    textPrint.unindent_box()
    textPrint.add_spacing(GUI.BOOL_BOX_HEIGHT)

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

    if is_xbee_communication_alive:
        textPrint.printLine(screen, "Connection alive")
    else:
        textPrint.printLine(screen, "Connection dead", GUI.RED)
    textPrint.printLine(screen, "Iterations since last status report" +
                        str(iterations_since_last_status_recieved))
    textPrint.printLine(screen, "Recieved via serial: " + str(recieved))

    textPrint.printEmptyLine(screen)
    textPrint.printLine(screen, "DIAGNOSTICS", GUI.BLUE)

    textPrint.printEmptyLine(screen)
    textPrint.printLine(screen, "Press START to reset and initialize everything")
    textPrint.printLine(screen, "Press BACK to toggle self-stabilizing mecanism")
    textPrint.printLine(screen, "Press Y to toggle Gyro-Sensor", GUI.YELLOW)
    textPrint.printLine(screen, "Press X to toggle Flight recorder", GUI.BLUE)
    textPrint.printLine(screen, "Press A to ", GUI.GREEN)
    textPrint.printLine(screen, "Press B in case of emergency", GUI.RED)

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

    logging.info("PythonControl started!")

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
        serialport = get_com_port()
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
