"""
This module provides the class StatusReport
"""

import Comm

class StatusReport:
    """
    Stores all necessary information regarding the status of the MagnusFlieger
    """
    def __init__(self, everything_ok=True, motor_ok=True, servos_ok=True, arduino_ok=True,
                 battery_ok=True, sensors_ok=True, flight_rec_ok=True):
        if everything_ok:
            self.everything_ok = True
            self.motor_ok = True
            self.servos_ok = True
            self.arduino_ok = True
            self.battery_ok = True
            self.sensors_ok = True
            self.flight_rec_ok = True
        else:
            self.everything_ok = False
            self.motor_ok = motor_ok
            self.servos_ok = servos_ok
            self.arduino_ok = arduino_ok
            self.battery_ok = battery_ok
            self.sensors_ok = sensors_ok
            self.flight_rec_ok = flight_rec_ok

    def to_detailed_string(self):
        """
        Returns a detailed message about the status
        """
        message = ""

        if self.everything_ok:
            message += "Everything is ok. \n"
        message += str(self.motor_ok)
        message += str(self.servos_ok)
        message += str(self.arduino_ok)

        return message

    def to_short_string(self):
        """
        Returns a short message
        """
        if self.everything_ok:
            return "Everything is ok."
        return "Errors found"

    def parse_char(self, char):
        """
        Will change a status of this status report depending
        on the character
        """
        if char == Comm.R_STATUS_OK:
            self.everything_ok = True
        elif char == Comm.R_STATUS_ARDUINO_FAULT:
            self.arduino_ok = False
        elif char == Comm.R_STATUS_BATTERY_FAULT:
            self.battery_ok = False
        elif char == Comm.R_STATUS_FLIGHT_REC_FAULT:
            self.flight_rec_ok = False
        elif char == Comm.R_STATUS_MOTOR_FAULT:
            self.motor_ok = False
        elif char == Comm.R_STATUS_SENSOR_FAULT:
            self.sensors_ok = False
        elif char == Comm.R_STATUS_UNKNOWN_FAULT:
            pass

    @staticmethod
    def empty_statusreport():
        """
        Return an empty status report
        """
        return StatusReport(True)

    @staticmethod
    def is_status_char(char):
        """
        Returns wheter the given char is a valid status char
        """
        if char in Comm.R_STATUSES:
            return True
        return False
