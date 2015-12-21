﻿""" Create maps and define their cells and walls.

Map(): ???

"""

import math

import pygame as pg

from options import COLORS, COORD_DISPLAY, DIRS, WALL_TYPE, TEST_FLAGS, FPS

DATA_DUMP = False


class Wall(pg.sprite.DirtySprite):
    """Define a wall bounding a MapCell()."""

    def __init__(self, opts, direction, data=WALL_TYPE['none'], *groups):
        super(Wall, self).__init__(*groups)
        self.direction = direction
        self.data = data
        self.rect = pg.Rect(0, 0, 0, 0)
        self.image = pg.Surface((self.rect.w, self.rect.h))
        self.image.fill((0, 0, 0, 0))
        self.opts = opts
        self.layer = 1

    def hover(self, surface):
        #highlight = pg.Surface((self.rect.w, self.rect.h))
        #highlight.fill((255, 255, 255, 127))
        self.dirty = 1
        #pg.draw.rect(self.image, (255, 255, 255, 63), self.rect)
        pg.draw.rect(surface, (222, 222, 222, 32), self.rect)
        #print('Hovering')
        #surface.blit(self.image, self.rect)
        return self.rect
        #rect = surface.blit(highlight, self.rect)
        #return rect
    
    def draw(self, surface, left=(), top=()):
        """Draw the wall to surface."""
        if not left:
            left = self.rect.left
        if not top:
            top = self.rect.top

        temp_surf = pg.Surface((self.opts.cell_width,
                                self.opts.cell_height *
                                self.opts.wall_rect_thickness), 0, surface)
        temp_surf.fill((0, 0, 0, 0))

        if self.data == WALL_TYPE['door']:
            door_points = [(0, 0),
                           (math.ceil(self.opts.cell_width * 0.25), 0),
                           (math.ceil(self.opts.cell_width * 0.25),
                            self.opts.wall_rect_thickness * self.opts.cell_height * 0.7),
                           (math.floor(self.opts.cell_width * 0.75) - 1,
                            self.opts.wall_rect_thickness * self.opts.cell_height * 0.7),
                           (math.floor(self.opts.cell_width * 0.75) - 1, 0),
                           (self.opts.cell_width, 0)]
            pg.draw.lines(temp_surf, COLORS['black'], False, door_points,
                          max(1, int(self.opts.cell_height *
                                     self.opts.wall_thickness)))
        else:
            pg.draw.line(temp_surf, COLORS['ltgrey'], (0, 0), (self.opts.cell_width, 0),
                         max(1, self.opts.gridline_thickness * self.opts.cell_height))

        temp_surf = pg.transform.rotate(temp_surf, 90 * self.direction)
        if not (self.opts.cell_height == self.opts.cell_width):
            pass # TODO add code to scale size of non-square image
        my_rect = surface.blit(temp_surf, (left, top))
        #my_rect = surface.blit(temp_surf, self.rect)
        self.image = temp_surf

        if self.dirty:
            return my_rect
            self.dirty = False
        else:
            return None

        if TEST_FLAGS['debug']:
            my_rect = pg.draw.rect(surface, COLORS['ltgrey'], self.rect)


class MapCell(pg.sprite.DirtySprite):
    """Define a single cell of the map."""

    def __init__(self, opts, coords, topleft, *groups):
        super(MapCell, self).__init__(*groups)
        self.opts = opts
        self.coords = coords
        self.topleft = topleft
        self.darkness = False
        self.spinner = False
        self.anti_magic = False
        self.odd = False
        self.special = False
        self.encounter = False
        self.explored = 'default'
        self.width = opts.cell_width
        self.height = opts.cell_height
        self.rect = pg.Rect(self.topleft, (self.width, self.height))
        self.image = pg.Surface((self.rect.w, self.rect.h))
        self.image.fill((0, 0, 0, 0))
        self.walls = [Wall(self.opts, DIRS['north'], *groups),
                      Wall(self.opts, DIRS['east'], *groups),
                      Wall(self.opts, DIRS['south'], *groups),
                      Wall(self.opts, DIRS['west'], *groups),
                      ]
        #self.walls = {'n': Wall(self.opts, DIRS['north'], *groups),
        #              'e': Wall(self.opts, DIRS['east'], *groups),
        #              's': Wall(self.opts, DIRS['south'], *groups),
        #              'w': Wall(self.opts, DIRS['west'], *groups),
        #              }
        self.dirty = True
        for wall in self.walls: #.itervalues():
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

        if TEST_FLAGS['doors'] and self.coords == (1, 1):
            self.explored = 'seen'
            #for wall in self.walls.itervalues():
            #    wall.data = WALL_TYPE['door']
            self.walls['n'].data = WALL_TYPE['door']

    def hover(self, surface):
        #print('Cell Hover')
        self.dirty = 1
        pg.draw.rect(surface, (127, 127, 127, 32),
                     self.rect.inflate(-2 * (self.width * self.opts.wall_rect_thickness),
                                       -2 * (self.height * self.opts.wall_rect_thickness))
                     )
        return self.rect

    def draw(self, surface, left=0, top=0):
        """Draw the MapCell onto the surface."""
        if not left:
            left = self.rect.left
        if not top:
            top = self.rect.top
        #if not self.explored:
        #    bgcolour = self.opts.bgcolours['default']
        #else:
        #    bgcolour = self.opts.bgcolours[self.explored]
        bgcolour = self.opts.bgcolours[self.explored]

        #my_rect = pg.draw.rect(surface, bgcolour, (left, top, self.width, self.height))
        self.image = surface.fill(bgcolour, self.rect)
        my_rect = surface.fill(bgcolour, self.rect)
        #pg.draw.rect(surface, COLORS['ltgrey'], my_rect,
        #             max(1, self.opts.gridline_thickness * self.opts.cell_height))
        
        dirty_rects = []
        #for wall in self.walls: #.itervalues():
        #    dirty_rects.append(wall.draw(surface)) #, left=wall.rect.left, top=wall.rect.top))

        if self.dirty:
            dirty_rects.append(my_rect)
            self.dirty = False
        return dirty_rects


class Map(pg.sprite.LayeredDirty):
    """Define one complete map."""

    def __init__(self, opts, *groups, **kwargs):
        super(Map, self).__init__(*groups, **kwargs)
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
                cell = MapCell(self.opts, (x, y), (loc_x, loc_y), self, *groups)
                #self.map[x].append(cell)
                #self.add(cell)
                for wall in cell.walls:
                    self.add(wall)

    def draw(self, surface):
        """Draw the entire map."""
        offset_top = self.opts.coord_display ** 0 * self.opts.cell_height
        offset_left = self.opts.coord_display ** 0 * self.opts.cell_width
        if self.opts.wraparound:
            self.offset_top += self.opts.wraparound_repeat * self.opts.cell_height
            self.offset_left += self.opts.wraparound_repeat * self.opts.cell_width
        #dirty_rects = super(Map, self).draw(surface)
        dirty_rects = []
        for cell in self.sprites():
            dirty_rects.extend(cell.draw(surface))
            #self.map[x][y].draw(surface, left=(self.offsetLeft + x *
            #                                   self.opts.cellWidth),
            #                    top=(self.offsetTop + y *
            #                         self.opts.cellHeight))
            if isinstance(cell, MapCell) and cell.coords[0] == 0 and cell.coords[1] == 0:
                DATA_DUMP = True
            else:
                DATA_DUMP = False
        #for x in range(self.num_cells_x):
        #    for y in range(self.num_cells_y):
        #        dirty_rects.extend(self.map[x][y].draw(surface))
        #        #self.map[x][y].draw(surface, left=(self.offsetLeft + x *
        #        #                                   self.opts.cellWidth),
        #        #                    top=(self.offsetTop + y *
        #        #                         self.opts.cellHeight))
        #        if x == 0 and y == 0:
        #            DATA_DUMP = True
        #        else:
        #            DATA_DUMP = False
        return dirty_rects
