"""
This module provides the class Settings
"""

import Comm

class BooleanSettingStates:
    """
    The possible states of a boolean here
    """
    off = 0
    off_but_awaiting_confirmation = 1
    on = 2
    on_but_awaiting_confirmation = 3
    unknown = 4

class Settings:
    """
    Stores all settings which are necessary for the Arudino
    """

    def __init__(self, speedSetting, leftRightSetting, upDownSetting,
                 frontSetting, backSetting, stabilizing=BooleanSettingStates.off,
                 sensor=BooleanSettingStates.off,
                 flight_recorder=BooleanSettingStates.off):
        self.speed = speedSetting
        self.leftRight = leftRightSetting
        self.upDown = upDownSetting
        self.front = frontSetting
        self.back = backSetting
        self.stabilizing = stabilizing
        self.sensor = sensor
        self.flight_recorder = flight_recorder

    def __str__(self):
        return str(self.speed) + str(self.leftRight) + str(self.upDown) + str(self.front) + str(self.back)

    def __bytes__(self):
        return bytes([self.speed,
                      self.leftRight,
                      self.upDown,
                      self.front,
                      self.back])

    def copy(self):
        """
        Creates an identical copy of these settings
        """
        return Settings(self.speed, self.leftRight, self.upDown,
                        self.front, self.back, self.stabilizing,
                        self.sensor, self.flight_recorder)

    def __eq__(self, comparison):
        """
        Checks if these settings exactly match the comparison
        """
        if not isinstance(comparison, Settings):
            return False
        if self.speed != comparison.speed:
            return False
        if self.leftRight != comparison.leftRight:
            return False
        if self.upDown != comparison.upDown:
            return False
        if self.front != comparison.front:
            return False
        if self.back != comparison.back:
            return False
        return True

    def deltaBytes(self, comparison):
        """
        Returns the settings which are different with their prefixes.
        The values from these Settings will be used, not from the
        comparison.
        """
        output = bytes()
        if self.speed != comparison.speed:
            output += Comm.S_SPEED_PREFIX
            output += bytes([self.speed])
        if self.leftRight != comparison.leftRight:
            output += Comm.S_LR_PREFIX
            output += bytes([self.leftRight])
        if self.upDown != comparison.upDown:
            output += Comm.S_UD_PREFIX
            output += bytes([self.upDown])
        if self.front != comparison.front:
            output += Comm.S_FRONT_PREFIX
            output += bytes([self.front])
        if self.back != comparison.back:
            output += Comm.S_BACK_PREFIX
            output += bytes([self.back])
        return output

    @staticmethod
    def GetDeltaSettings(original, comparison):
        """
        Returns the difference between these settings and the comparison
        """
        return Settings(comparison.speed - original.speed,
                        comparison.leftRight - original.leftRight,
                        comparison.upDown - original.upDown,
                        comparison.front - original.front,
                        comparison.back - original.back)

    @staticmethod
    def EmptySettings():
        """
        Returns empty settings
        """
        return Settings(0, 0, 0, 0, 0, False, False, False)


def KeepInBoundary(val, upper_bound, under_bound=0):
    """
    Automatically keep the value between upperBound and underBound
    """
    if val > upper_bound:
        return upper_bound
    if val < under_bound:
        return under_bound
    return val
