"""
This module provides all functions necessary for displaying the GUI
control window
"""
import pygame

# Color constants
BLACK   =   (   0,   0,   0)
WHITE   =   ( 255, 255, 255)
GRAY    =   ( 128, 128, 128)
LI_GRAY =   ( 204, 204, 224)
DA_GRAY =   (  77,  77,  77)
BLUE    =   (   0,   0, 255)
GREEN   =   (   0, 255,   0)
RED     =   ( 255,   0,   0)
YELLOW  =   ( 200, 200,   0)

# Drawing constants
FONT_SIZE = 20
LINE_HEIGHT = 15
INDENT_SIZE = 10

# Progress bar constants
PROGRESSBAR_WIDTH = 300
PROGRESSBAR_HEIGHT = 30

# Boolean box constants
BOOL_BOX_WIDTH = 100
BOOL_BOX_HEIGHT = 30

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    """
    The main control window
    """
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, FONT_SIZE)

    def print(self, screen, textString, color=BLACK, bg_color=None):
        """
        Prints some text to the screen
        ATTENTION: This doesn't move x and y positions, so your
        text might end up dirty
        """
        textBitmap = self.font.render(textString, True, color, bg_color)
        screen.blit(textBitmap, [self.x, self.y])

    def printLine(self, screen, textString, color=BLACK, bg_color=None):
        """
        Prints some text to the screen and shifts the
        next text a line below the current text.
        """
        textBitmap = self.font.render(textString, True, color, bg_color)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += LINE_HEIGHT

    def printEmptyLine(self, screen):
        """
        Shifts the current drawing pointer one line down
        """
        self.y += LINE_HEIGHT

    def drawProgressBar(self, screen, progress, color=BLACK):
        """
        Draws a simple progress bar. Progress must be between 0 and 1.
        """
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, PROGRESSBAR_WIDTH,PROGRESSBAR_HEIGHT), 1)
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, PROGRESSBAR_WIDTH*progress,PROGRESSBAR_HEIGHT))
        self.y += PROGRESSBAR_HEIGHT

    def drawPositiveNegativeProgressBar(self, screen, progress, color=BLACK):
        """
        Draws a progress bar that can go positive and negative.
        Progress must be between -1 and 1.
        """
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, PROGRESSBAR_WIDTH, PROGRESSBAR_HEIGHT), 1)
        pygame.draw.rect(screen, color, pygame.Rect(self.x + PROGRESSBAR_WIDTH/2, self.y, PROGRESSBAR_WIDTH/2*progress, PROGRESSBAR_HEIGHT))
        self.y += PROGRESSBAR_HEIGHT

    def drawBooleanBox(self, screen, text, boolean_expr, bg_color_true=WHITE, bg_color_false=GRAY, fg_color=BLACK):
        """
        Draws a box that displays a status according
        to the color given
        """
        if boolean_expr:
            bg_color = bg_color_true
        else:
            bg_color = bg_color_false
        pygame.draw.rect(screen, fg_color, pygame.Rect(self.x, self.y, BOOL_BOX_WIDTH, BOOL_BOX_HEIGHT), 1)
        pygame.draw.rect(screen, bg_color, pygame.Rect(self.x, self.y, BOOL_BOX_WIDTH, BOOL_BOX_HEIGHT))
        textBitmap = self.font.render(text, True, fg_color, bg_color)
        text_rect = textBitmap.get_rect(center=(self.x+BOOL_BOX_WIDTH/2, self.y+BOOL_BOX_HEIGHT/2))
        screen.blit(textBitmap, text_rect)

    def reset(self):
        """
        Resets the x and y values to start from the top
        """
        self.x = 10
        self.y = 10

    def indent(self, number_of_indents=1):
        """
        Adds indentations at the current position
        """
        self.x += number_of_indents * INDENT_SIZE

    def unindent(self, number_of_indents=1):
        """
        Removes indentations at the current position
        """
        self.indent(-1 * number_of_indents)

    def indent_box(self, number_of_indents=1):
        """
        Adds an indentation at the current position
        """
        self.x += number_of_indents * BOOL_BOX_WIDTH

    def unindent_box(self, number_of_indents=1):
        """
        Removes an indentation at the current position
        """
        self.indent_box(-1 * number_of_indents)

    def add_spacing(self, length):
        self.y += length

if __name__ == "__main__":

    pygame.init()

    # Set the width and height of the screen [width,height]
    size = [500, 500]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Control")

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Get ready to print
    textPrint = TextPrint()

    # -------- Main Program Loop -----------

    while not done:
        # EVENT PROCESSING STEP
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

        # DRAWING STEP
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        screen.fill(WHITE)
        textPrint.reset()

        # Get count of joysticks
        textPrint.printLine(screen, "Hello")
        textPrint.printLine(screen, "World")

        textPrint.indent()
        textPrint.drawProgressBar(screen, 0.3)
        textPrint.unindent()

        textPrint.drawBooleanBox(screen, "Status good", True, fg_color=WHITE, bg_color_true=GREEN)
        textPrint.indent_box()
        textPrint.drawBooleanBox(screen, "Status bad", True, fg_color=WHITE, bg_color_true=RED)
        textPrint.unindent_box()

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)

    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit()
