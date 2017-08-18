import pygame

# Define some colors
BLACK   =   (   0,   0,   0)
WHITE   =   ( 255, 255, 255)
BLUE    =   (   0,   0, 255)
GREEN   =   (   0, 255,   0)
RED     =   ( 255,   0,   0)
YELLOW  =   ( 255, 255,   0)

# Progress bar constants
PROGRESSBAR_WIDTH = 300
PROGRESSBAR_HEIGHT = 30

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString, color = BLACK):
        textBitmap = self.font.render(textString, True, color)
        screen.blit(textBitmap, [self.x, self.y])

    def printLine(self, screen, textString, color = BLACK):
        textBitmap = self.font.render(textString, True, color)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def printEmptyLine(self, screen):
        self.y += self.line_height

    def drawProgressBar(self, screen, progress, color = BLACK):
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, PROGRESSBAR_WIDTH,PROGRESSBAR_HEIGHT), 1)
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, PROGRESSBAR_WIDTH*progress,PROGRESSBAR_HEIGHT))
        self.y += PROGRESSBAR_HEIGHT

    def drawPositiveNegativeProgressBar(self, screen, progress, color = BLACK):
        pygame.draw.rect(screen, color, pygame.Rect(self.x, self.y, PROGRESSBAR_WIDTH, PROGRESSBAR_HEIGHT), 1)
        pygame.draw.rect(screen, color, pygame.Rect(self.x + PROGRESSBAR_WIDTH/2, self.y, PROGRESSBAR_WIDTH/2*progress, PROGRESSBAR_HEIGHT))
        self.y += PROGRESSBAR_HEIGHT
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
    
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
        textPrint.print(screen, "Hello")
        textPrint.print(screen, "World")

        textPrint.indent()
        textPrint.drawProgressBar(screen, 0.3)
        textPrint.unindent()

        textPrint.print(screen, "Hi")

    
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 20 frames per second
        clock.tick(20)
    
    # Close the window and quit.
    # If you forget this line, the program will 'hang'
    # on exit if running from IDLE.
    pygame.quit ()