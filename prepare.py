import os

import pygame as pg

import tools

DEBUG_TEST = False

GFX = tools.load_all_gfx(os.path.join("asset", "image"))
SFX = tools.load_all_sfx(os.path.join("asset", "sound"))
FONTS = tools.load_all_fonts(os.path.join("asset", "font"))
MUSIC = tools.load_all_music(os.path.join("asset", "music"))


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

