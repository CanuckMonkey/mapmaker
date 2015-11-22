#!/usr/bin/env python

""" Map Creation Tool

This tool is designed with an initial focus on Bard's Tale-style maps.

Maps are built on a cartesian grid.  Each cell in the grid defines its
own contents as well as the contents of the four bounding walls.
"""

# A lot of base code copied from my earlier SoC project.
# ??? is a searchable string for later lookup for things I know are
# needed but whose exact use is unclear.
# "coord" and "coordinates" refer to the MapCell coordinates, while
# "top" and "left" and "width" etc. refer to pixel coordinates.

try:
    import os
    import sys
    import pygame
    from pygame.locals import QUIT, KEYUP, K_ESCAPE, RESIZABLE
    #from pygame.locals import *     # Bad form, should import only needed items for clarity
except ImportError as err:
    print "Could not load module: %s" % (err)
    sys.exit(2)

if not pygame.font:
    print "Warning: fonts disabled."

DEBUGTEST = True

# Define useful colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
LTGRAY = (191, 191, 191)
DKGRAY = (63, 63, 63)
RED = (255, 0, 0)
DKRED = (191, 0, 0)
BLUE = (0, 0, 255)
DKBLUE = (0, 0, 191)
ORANGE = (255, 127, 0)
GREEN = (0, 127, 0)
LTGRN = (63, 191, 63)
DKGRN = (0, 95, 0)
YELLOW = (191, 191, 0)
GOLD = (127, 127, 0)
BROWN = (191, 63, 63)
LTBROWN = (255, 207, 71)

NONE = 0
SINGLE = 1
BOTH = 2

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

WALL = 1
DOOR = 2

FPS = 24

def terminate():
    """End the program cleanly."""
    pygame.quit()
    sys.exit(0)

def main():
    """Run the program."""
    opts = Options()
    theMap = Map(opts)

    screenWidth = opts.cellWidth * (theMap.numCellsX + opts.wraparoundRepeat
                                    * 2 + opts.coordDisplay)
    screenHeight = opts.cellHeight * (theMap.numCellsY + opts.wraparoundRepeat
                                      * 2 + opts.coordDisplay)

    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight), RESIZABLE, 32)
    pygame.display.set_caption("MapMaker BT by CanuckMonkey Games")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    overlay = pygame.Surface(screen.get_size())
    overlay = screen.convert_alpha()
    theMap.draw(background)
    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    running = True

    # Loop while program is running
    while running:
        # Control maximum framrate
        clock.tick(FPS)

        # Process input
        for event in pygame.event.get():
            if event.type == QUIT:      #
                terminate()
            #if event.type == KEYUP:
            #    if event.key == K_ESCAPE:
            #        terminate()

        # Update program state

        # Draw/render
        overlay.fill((0, 0, 0, 0))
        theMap.draw(overlay)
        screen.blit(overlay, (0, 0))

        # *After* drawing everything, flip the display
        pygame.display.flip()

class Options(object):
    """Define the options in use for this map."""

    def __init__(self):
        self.wraparound = True
        self.coordDisplay = BOTH
        self.cellWidth = 32
        self.cellHeight = 32
        self.wraparoundRepeat = 1
        self.wallThickness = 0.05
        self.gridlineThickness = 0.02
        self.wallRectThickness = 0.2
        self.bgcolours = {'default': DKGRAY, 'seen': YELLOW, 'visited': WHITE}
        self.numCellsX = 22
        self.numCellsY = 22

class Wall(object):
    """Define a wall bounding a MapCell()."""

    def __init__(self, opts=Options(), direction=NORTH, data=None):
        self.direction = direction
        self.data = data
        self.rect = pygame.Rect(0, 0, 0, 0)

    def draw(self, surface, left=(), top=()):
        """Draw the wall to surface."""
        if not left:
            left = self.rect.left
        if not top:
            top = self.rect.top
        if self.data == DOOR:
            pass
        else:
            pass
        if DEBUGTEST:
            myRect = pygame.draw.rect(surface, LTGRAY, self.rect)


class MapCell(object):
    """Define a single cell of the map."""

    def __init__(self, opts=Options(), coords=(0, 0), topleft=(0, 0)):
        self.opts = opts
        self.coords = coords
        self.topleft = topleft
        self.darkness = False
        self.spinner = False
        self.antiMagic = False
        self.odd = False
        self.special = False
        self.encounter = False
        self.explored = False
        self.width = opts.cellWidth
        self.height = opts.cellHeight
        self.rect = pygame.Rect(self.topleft, (self.width, self.height))
        self.walls = {'n': Wall(self.opts, NORTH), 'e': Wall(self.opts, EAST),
                      's': Wall(self.opts, SOUTH), 'w': Wall(self.opts, WEST)}
        for wall in self.walls.itervalues():
            if wall.direction == NORTH:
                wall.rect.width = self.rect.width
                wall.rect.height = self.rect.height * self.opts.wallRectThickness
                wall.rect.midtop = self.rect.midtop
            elif wall.direction == SOUTH:
                wall.rect.width = self.rect.width
                wall.rect.height = self.rect.height * self.opts.wallRectThickness
                wall.rect.midbottom = self.rect.midbottom
            elif wall.direction == EAST:
                wall.rect.width = self.rect.width * self.opts.wallRectThickness
                wall.rect.height = self.rect.height
                wall.rect.midleft = self.rect.midleft
            elif wall.direction == WEST:
                wall.rect.width = self.rect.width * self.opts.wallRectThickness
                wall.rect.height = self.rect.height
                wall.rect.midright = self.rect.midright

    def draw(self, surface, left=(), top=()):
        """Draw the MapCell onto the surface."""
        if not left:
            left = self.rect.left
        if not top:
            top = self.rect.top
        if self.explored == False:
            bgcolour = self.opts.bgcolours['default']
        else:
            bgcolour = BLACK

        myRect = pygame.draw.rect(surface, bgcolour, (left, top, self.width, self.height))
        for wall in self.walls.itervalues():
            wall.draw(surface)

        return myRect

class Map(object):
    """Define one complete map."""

    def __init__(self, opts=Options()):
        self.opts = opts
        self.numCellsX = opts.numCellsX
        self.numCellsY = opts.numCellsY
        self.map = [None] * self.numCellsX
        self.offsetTop = opts.coordDisplay ** 0 * opts.cellHeight
        self.offsetLeft = opts.coordDisplay ** 0 * opts.cellWidth
        if self.opts.wraparound == True:
            self.offsetTop += opts.wraparoundRepeat * opts.cellHeight
            self.offsetLeft += opts.wraparoundRepeat * opts.cellWidth

        #for i in range(self.numCellsX):
        #    self.map[i] = [None] * self.numCellsY
        self.map = []
        for x in range(self.numCellsX):
            self.map.append([])
            for y in range(self.numCellsY):
                locX = self.offsetLeft + x * opts.cellWidth
                locY = self.offsetTop + y * opts.cellHeight
                self.map[x].append(MapCell(self.opts, coords=(x, y), topleft=(locX, locY)))

    def draw(self, surface):
        """Draw the entire map."""
        offsetTop = self.opts.coordDisplay ** 0 * self.opts.cellHeight
        offsetLeft = self.opts.coordDisplay ** 0 * self.opts.cellWidth
        if self.opts.wraparound == True:
            self.offsetTop += self.opts.wraparoundRepeat * self.opts.cellHeight
            self.offsetLeft += self.opts.wraparoundRepeat * self.opts.cellWidth
        for x in range(self.numCellsX):
            for y in range(self.numCellsY):
                self.map[x][y].draw(surface)
                #self.map[x][y].draw(surface, left=(self.offsetLeft + x *
                #                                   self.opts.cellWidth),
                #                    top=(self.offsetTop + y *
                #                         self.opts.cellHeight))

if __name__ == "__main__":      # Do not run this if called from some other module???
    main()
