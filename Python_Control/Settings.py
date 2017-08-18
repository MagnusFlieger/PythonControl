"""
This module provides the class Settings
"""
class Settings:
    """
    Stores all settings which are necessary for the Arudino
    """
    def __init__(self, speedSetting, leftRightSetting, upDownSetting,
                 frontSetting, backSetting):
        self.speed = speedSetting
        self.leftRight = leftRightSetting
        self.upDown = upDownSetting
        self.front = frontSetting
        self.back = backSetting

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
                        self.front, self.back)

    def isSame(self, comparison):
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

    @staticmethod
    def GetDeltaSettings(original, comparison):
        return Settings(comparison.speed - original.speed,
                        comparison.leftRight - original.leftRight,
                        comparison.upDown - original.upDown,
                        comparison.front - original.front,
                        comparison.back - original.back)

    @staticmethod
    def EmptySettings():
        return Settings(0, 0, 0, 0, 0)

    @staticmethod
    def KeepInBoundary(val, upperBound, underBound=0):
        if val > upperBound:
            val = upperBound
        if val < underBound:
            val = underBound
