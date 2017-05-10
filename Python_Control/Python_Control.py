import pygame
import serial
import time
import sys

import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
def getcom():
    for port in ports:
        print(port)

if __name__ == "__main__":
    print("Available ports")
    print(getcom())
