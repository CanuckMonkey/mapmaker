#!/usr/bin/env python

""" Map Creation Tool

    This tool is designed with an initial focus on Bard's Tale-style maps.

    Maps are built on a cartesian grid.  Each cell in the grid defines its own contents as well as the contents of the four bounding walls.

"""

try:
    import os
    import sys
    import pygame
except ImportError, err:
    print "Could not load module: %s" % (err)
    sys.exit(2)

if not pygame.font: print "Warning: fonts disabled."

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
