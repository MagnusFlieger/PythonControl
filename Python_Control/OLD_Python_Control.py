"""
OLD VERSION for testing purpose only:
testing for Python 2.7
"""

import pygame
import serial
from time import sleep

usbport = 'COM11'

ser = serial.Serial(usbport, 9600, timeout=1)

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized Joystick : %s' % j.get_name()

"""
Returns a vector of the following form:
[LThumbstickX, LThumbstickY, Unknown Coupled Axis???,
RThumbstickX, RThumbstickY,
Button 1/X, Button 2/A, Button 3/B, Button 4/Y,
Left Bumper, Right Bumper, Left Trigger, Right Triller,
Select, Start, Left Thumb Press, Right Thumb Press]

Note:
No D-Pad.
Triggers are switches, not variable.
Your controller may be different
"""

def move(servo, angle):

    if (0 <= angle <= 180):
        ser.write(chr(255))
        ser.write(chr(servo))
        ser.write(chr(angle))
    else:
        return 'Wrong input'

"""
def get():
    out = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    it = 0 #iterator
    pygame.event.pump()

    #Read input from the two joysticks
    for i in range(0, j.get_numaxes()):
        out[it] = j.get_axis(i)
        it+=1
    #Read input from buttons
    for i in range(0, j.get_numbuttons()):
        out[it] = j.get_button(i)
        it+=1
    return out

"""
def master():
    while True:
        forward()
        left()


def forward():
    while True:
        out = 0
        pygame.event.pump()
        out = j.get_axis(1)
        print 'GetAxisY'
        out = (out * 90.0) + 90.0
        print out
        out = int(out)
        move(1, out)
        sleep(0.3)

def left():
        out = 0
        pygame.event.pump()
        out = j.get_axis(2)
        print 'GetAxisX'
        out = (out * 90.0) + 90.0
        print out
        out = int(out)
        move(2, out)
        sleep(0.3)

def test():
    while True:
        print get()
