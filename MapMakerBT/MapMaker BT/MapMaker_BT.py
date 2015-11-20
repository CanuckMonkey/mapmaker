#!/usr/bin/env python

""" Map Creation Tool

This tool is designed with an initial focus on Bard's Tale-style maps.

Maps are built on a cartesian grid.  Each cell in the grid defines its own contents as well as the contents of the four bounding walls.
"""

# A lot of base code copied from my earlier SoC project.  When I know something is needed but exact use is unclear, I have used ??? as a searchable string for later lookup.

try:
    import os
    import sys
    import pygame
    #from pygame.locals import *     # Bad form, should import only needed items for clarity
except ImportError as err:
    print "Could not load module: %s" % (err)
    sys.exit(2)

if not pygame.font: print "Warning: fonts disabled."

def main():
    pygame.init()

    while True:     # Loop while program is running
        clock.tick(60)      # Where does clock come from and what does this do???

class Options():
    """Define the options in use for this map."""

    def __init__(self):
        self.wraparound = True
        self.coordDisplay = True
        

class MapSpace():
    """Define a single cell of the map."""

    def __init__(self, coords=(0, 0)):
        self.coords = coords
        self.darkness = False
        self.spinner = False
        self.antiMagic = False
        self.odd = False
        self.special = False
        self.encounter = False

class Map():
    """Define one complete map."""

    def __init__(self, width=22, height=22):
        self.width = width
        self.height = height
        for x in range(width):
            for y in range(height):
                self.map[x][y] = MapSpace(coords=(x, y))

if __name__ == "__main__":      # Do not run this if called from some other module, I think???
    main()