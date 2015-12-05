""" Create maps and define their cells and walls.

Map(): ???

"""

import pygame as pg

from options import COLORS, COORD_DISPLAY, DIRS, WALL_TYPE, DEBUG_TEST, FPS


class Wall(object):
    """Define a wall bounding a MapCell()."""

    def __init__(self, opts, direction, data=None):
        self.direction = direction
        self.data = data
        self.rect = pg.Rect(0, 0, 0, 0)

    def draw(self, surface, left=(), top=()):
        """Draw the wall to surface."""
        if not left:
            left = self.rect.left
        if not top:
            top = self.rect.top
        if self.data == WALL_TYPE['door']:
            pass
        else:
            pass
        if DEBUG_TEST:
            my_rect = pg.draw.rect(surface, COLORS['ltgrey'], self.rect)


class MapCell(object):
    """Define a single cell of the map."""

    def __init__(self, opts, coords, topleft):
        self.opts = opts
        self.coords = coords
        self.topleft = topleft
        self.darkness = False
        self.spinner = False
        self.anti_magic = False
        self.odd = False
        self.special = False
        self.encounter = False
        self.explored = False
        self.width = opts.cell_width
        self.height = opts.cell_height
        self.rect = pg.Rect(self.topleft, (self.width, self.height))
        self.walls = {'n': Wall(self.opts, DIRS['north']),
                      'e': Wall(self.opts, DIRS['east']),
                      's': Wall(self.opts, DIRS['south']),
                      'w': Wall(self.opts, DIRS['west']),
                      }
        for wall in self.walls.itervalues():
            if wall.direction == DIRS['north']:
                wall.rect.width = self.rect.width
                wall.rect.height = self.rect.height * self.opts.wall_rect_thickness
                wall.rect.midtop = self.rect.midtop
            elif wall.direction == DIRS['south']:
                wall.rect.width = self.rect.width
                wall.rect.height = self.rect.height * self.opts.wall_rect_thickness
                wall.rect.midbottom = self.rect.midbottom
            elif wall.direction == DIRS['east']:
                wall.rect.width = self.rect.width * self.opts.wall_rect_thickness
                wall.rect.height = self.rect.height
                wall.rect.midleft = self.rect.midleft
            elif wall.direction == DIRS['west']:
                wall.rect.width = self.rect.width * self.opts.wall_rect_thickness
                wall.rect.height = self.rect.height
                wall.rect.midright = self.rect.midright

    def draw(self, surface, left=(), top=()):
        """Draw the MapCell onto the surface."""
        if not left:
            left = self.rect.left
        if not top:
            top = self.rect.top
        if not self.explored:
            bgcolour = self.opts.bgcolours['default']
        else:
            bgcolour = COLORS['black']

        my_rect = pg.draw.rect(surface, bgcolour, (left, top, self.width, self.height))
        pg.draw.rect(surface, COLORS['ltgrey'], my_rect, 1)
        for wall in self.walls.itervalues():
            wall.draw(surface)

        return my_rect


class Map(object):
    """Define one complete map."""

    def __init__(self, opts):
        self.opts = opts
        self.num_cells_x = opts.num_cells_x
        self.num_cells_y = opts.num_cells_y
        self.map = [None] * self.num_cells_x
        self.offset_top = opts.coord_display ** 0 * opts.cell_height
        self.offset_left = opts.coord_display ** 0 * opts.cell_width
        if self.opts.wraparound == True:
            self.offset_top += opts.wraparound_repeat * opts.cell_height
            self.offset_left += opts.wraparound_repeat * opts.cell_width

        #for i in range(self.numCellsX):
        #    self.map[i] = [None] * self.numCellsY
        self.map = []
        for x in range(self.num_cells_x):
            self.map.append([])
            for y in range(self.num_cells_y):
                loc_x = self.offset_left + x * opts.cell_width
                loc_y = self.offset_top + y * opts.cell_height
                self.map[x].append(MapCell(self.opts, coords=(x, y), topleft=(loc_x, loc_y)))

    def draw(self, surface):
        """Draw the entire map."""
        offset_top = self.opts.coord_display ** 0 * self.opts.cell_height
        offset_left = self.opts.coord_display ** 0 * self.opts.cell_width
        if self.opts.wraparound:
            self.offset_top += self.opts.wraparound_repeat * self.opts.cell_height
            self.offset_left += self.opts.wraparound_repeat * self.opts.cell_width
        for x in range(self.num_cells_x):
            for y in range(self.num_cells_y):
                self.map[x][y].draw(surface)
                #self.map[x][y].draw(surface, left=(self.offsetLeft + x *
                #                                   self.opts.cellWidth),
                #                    top=(self.offsetTop + y *
                #                         self.opts.cellHeight))
