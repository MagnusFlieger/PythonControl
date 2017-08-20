"""
This module provides the class JoystickState
"""
# IMPORTS
import pygame

class JoystickState:
    """
    This class stores all button states of a joystick for easy comparison
    """
    def __init__(self, start_button, back_button, a_button, b_button, x_button, y_button,
                 lb_button, rb_button):
        self.start_button = start_button
        self.back_button = back_button
        self.a_button = a_button
        self.b_button = b_button
        self.x_button = x_button
        self.y_button = y_button
        self.lb_button = lb_button
        self.rb_button = rb_button

    def copy(self):
        """
        Returns an exact copy of the state
        """
        return JoystickState(self.start_button,
                             self.back_button,
                             self.a_button,
                             self.b_button,
                             self.x_button,
                             self.y_button,
                             self.lb_button,
                             self.rb_button)

    @staticmethod
    def empty_state():
        """
        Returns an empty class
        """
        return JoystickState(False, False, False, False, False, False, False, False)
    
    @staticmethod
    def from_joystick(j):
        """
        Returns a complete JoystickState instance with the corresponding buttons
        """
        return JoystickState(j.get_button(7),
                             j.get_button(6),
                             j.get_button(0),
                             j.get_button(1),
                             j.get_button(2),
                             j.get_button(3),
                             j.get_button(4),
                             j.get_button(5))
