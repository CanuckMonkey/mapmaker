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
        self.coord_display = COORD_DISPLAY['both']
        self.cell_width = 32
        self.cell_height = 32
        self.wraparound_repeat = 1
        self.wall_thickness = 0.05
        self.gridline_thickness = 0.02
        self.wall_rect_thickness = 0.2
        self.bgcolours = {'default': COLORS['dkgrey'],
                          'seen': COLORS['yellow'],
                          'visited': COLORS['white'],
                          }
        self.num_cells_x = 22
        self.num_cells_y = 22


