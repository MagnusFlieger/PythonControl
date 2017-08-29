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

    def to_detailed_string(self):
        """
        Returns a detailed message about the status
        """
        return ""

    def to_short_string(self):
        """
        Returns a short message
        """
        return ""

    @staticmethod
    def empty_statusreport():
        """
        Return an empty status report
        """
        return StatusReport(True, True, True, True)
