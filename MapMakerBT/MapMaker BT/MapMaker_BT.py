#!/usr/bin/env python

""" Map Creation Tool

This tool is designed with an initial focus on Bard's Tale-style maps.

Maps are built on a cartesian grid.  Each cell in the grid defines its own contents as well as the contents of the four bounding walls.
"""

# A lot of base code copied from my earlier SoC project.
# ??? is a searchable string for later lookup for things I know are needed but whose exact use is unclear.

try:
    import os
    import sys
    import pygame
    #from pygame.locals import *     # Bad form, should import only needed items for clarity
except ImportError as err:
    print "Could not load module: %s" % (err)
    sys.exit(2)

if not pygame.font: print "Warning: fonts disabled."

""" Colour Constants """

WHITE   = (255, 255, 255)
BLACK   = (  0,   0,   0)
GRAY    = (127, 127, 127)
LTGRAY  = (191, 191, 191)
DKGRAY  = ( 63,  63,  63)
RED     = (255,   0,   0)
DKRED   = (191,   0,   0)
BLUE    = (  0,   0, 255)
DKBLUE  = (  0,   0, 191)
ORANGE  = (255, 127,   0)
GREEN   = (  0, 127,   0)
LTGRN   = ( 63, 191,  63)
DKGRN   = (  0,  95,   0)
YELLOW  = (191, 191,   0)
GOLD    = (127, 127,   0)
BROWN   = (191,  63,  63)
LTBROWN = (255, 207,  71)

def main():
    """Run the program."""
    pygame.init()
    opts = Options()
    theMap = Map(opts)

    screenWidth = opts.cellWidth * (theMap.width + opts.wraparoundRepeat * 2 + opts.coordDisplay)
    screenHeight = opts.cellHeight * (theMap.height + opts.wraparoundRepeat * 2 + opts.coordDisplay)

    screen = pygame.display.set_mode((screenWidth, screenHeight), 0, 32)
    pygame.display.set_caption("MapMaker BT by CanuckMonkey Games")
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    overlay = pygame.Surface(screen.get_size())     # Don't know for sure the purpose of this vs. background???
    overlay = screen.convert_alpha()

    clock = pygame.time.Clock()


    while True:     # Loop while program is running
        clock.tick(60)     # What does this do???

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

class Options():
    """Define the options in use for this map."""

    def __init__(self):
        self.wraparound = True
        self.coordDisplay = 2
        self.cellWidth = 40
        self.cellHeight = 40
        self.wraparoundRepeat = 1
        self.wallThickness = 0.05
        self.gridlineThickness = 0.02
        self.bgcolours = {'default': DKGRAY, 'seen': YELLOW, 'visited': WHITE}
        self.numCellsX = 22
        self.numCellsY = 22

class MapCell():
    """Define a single cell of the map."""

    def __init__(self, opts=Options(), coords=(0, 0)):
        self.coords = coords
        self.darkness = False
        self.spinner = False
        self.antiMagic = False
        self.odd = False
        self.special = False
        self.encounter = False
        self.walls = {'n': None, 'e': None, 's': None, 'w': None}
        self.explored = False
        self.opts = opts
        self.width = opts.cellWidth
        self.height = opts.cellHeight

    def draw(self, surface, left=(), top=()):
        if self.explored == False:
            bgcolour = opts.bgcolours['default']
        pass    # Work in progress


class Map():
    """Define one complete map."""

    def __init__(self, opts=Options()):
        self.opts = opts
        self.numCellsX = opts.numCellsX
        self.numCellsY = opts.numCellsY
        for x in range(numCellsX):
            for y in range(numCellsY):
                self.map[x][y] = MapCell(opts, (x, y))

    def draw(self, surface):
        top = opts.coordDisplay ^ 0 * opts.cellHeight
        left = opts.coordDisplay ^ 0 * opts.cellWidth
        if opts.wraparound == True:
            top += opts.wraparoundRepeat * opts.cellHeight
            left += opts.wraparoundRepeat * opts.cellWidth
        for x in range(numCellsX):
            for y in range(numCellsY):
                map[x][y].draw(surface, left=(left + x * opts.cellWidth), top=(top + y * opts.cellHeight))

if __name__ == "__main__":      # Do not run this if called from some other module, I think???
    main()