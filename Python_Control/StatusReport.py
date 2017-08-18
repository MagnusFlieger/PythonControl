"""
This module provides the class StatusReport
"""
class StatusReport:
    """
    Stores all necessary information regarding the status of the MagnusFlieger
    """
    def __init__(self, everythingOK=True, motorOK=True, servosOK=True, arduinoOK=True):
        self.everythingOK = everythingOK
        self.motorOK = motorOK
        self.servosOK = servosOK
        self.arduinoOK = arduinoOK
