"""
This module provides the class JoystickState
"""
import enum

# IMPORTS
import pygame


class JoystickState:
    """
    This class stores all button states of a joystick for easy comparison
    """

    class Buttons(enum.Enum):
        """
        Represents all available Buttons on the joysticks
        """
        start = 0
        back = 1
        a = 2
        b = 3
        x = 4
        y = 5
        lb = 6
        rb = 7

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

    def deltaState(self, comparison):
        """
        Returns a list of Buttons which are different
        """
        output = list()
        if self.start_button != comparison.start_button:
            output.append(self.Buttons.start)
        if self.back_button != comparison.back_button:
            output.append(self.Buttons.back)
        if self.a_button != comparison.a_button:
            output.append(self.Buttons.a)
        if self.b_button != comparison.b_button:
            output.append(self.Buttons.b)
        if self.x_button != comparison.x_button:
            output.append(self.Buttons.x)
        if self.y_button != comparison.y_button:
            output.append(self.Buttons.y)
        if self.lb_button != comparison.lb_button:
            output.append(self.Buttons.lb)
        if self.rb_button != comparison.rb_button:
            output.append(self.Buttons.rb)
        return output

    def get_pressed_buttons(self, comparison):
        """
        Returns a list of buttons now pressed, but previously not pressed
        """
        output = list()
        if self.start_button and not comparison.start_button:
            output.append(self.Buttons.start)
        if self.back_button and not comparison.back_button:
            output.append(self.Buttons.back)
        if self.a_button and not comparison.a_button:
            output.append(self.Buttons.a)
        if self.b_button and not comparison.b_button:
            output.append(self.Buttons.b)
        if self.x_button and not comparison.x_button:
            output.append(self.Buttons.x)
        if self.y_button and not comparison.y_button:
            output.append(self.Buttons.y)
        if self.lb_button and not comparison.lb_button:
            output.append(self.Buttons.lb)
        if self.rb_button and not comparison.rb_button:
            output.append(self.Buttons.rb)
        return output

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
