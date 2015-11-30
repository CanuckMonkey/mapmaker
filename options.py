import pygame as pg
#from prepare import *

DEBUG_TEST = False

COLORS = {
    'white':(255, 255, 255),
    'black':(0, 0, 0),
    'gray':(127, 127, 127),
    'ltgrey':(191, 191, 191),
    'dkgrey':(63, 63, 63),
    'red':(255, 0, 0),
    'dkred':(191, 0, 0),
    'blue':(0, 0, 255),
    'dkblue':(0, 0, 191),
    'orange':(255, 127, 0),
    'green':(0, 127, 0),
    'ltgrn':(63, 191, 63),
    'dkgrn':(0, 95, 0),
    'yellow':(191, 191, 0),
    'gold':(127, 127, 0),
    'brown':(191, 63, 63),
    'ltbrown':(255, 207, 71)
    }

COORD_DISPLAY = {
    'none':0,
    'single':1,
    'both':2
    }

DIRS = {
    'north':0,
    'east':1,
    'south':2,
    'west':3
    }

WALL_TYPE = {
    'none':0,
    'wall':1,
    'door':2,
    'secret':3
    }

FPS = 24

class Options(object):
    """Define the options in use for this map."""

    def __init__(self):
        self.wraparound = True
        self.coordDisplay = COORD_DISPLAY['both']
        self.cellWidth = 32
        self.cellHeight = 32
        self.wraparoundRepeat = 1
        self.wallThickness = 0.05
        self.gridlineThickness = 0.02
        self.wallRectThickness = 0.2
        self.bgcolours = {'default': COLORS['dkgrey'],
                          'seen': COLORS['yellow'],
                          'visited': COLORS['white']
                          }
        self.numCellsX = 22
        self.numCellsY = 22


