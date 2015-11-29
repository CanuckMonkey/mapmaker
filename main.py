#!/usr/bin/env python

""" Map Creation Tool

This tool is designed with an initial focus on Bard's Tale-style maps.

Maps are built on a cartesian grid.  Each cell in the grid defines its
own contents as well as the contents of the four bounding walls.
"""

# Yes, I am aware of https://www.python.org/dev/peps/pep-0008/.
# I *hate* lower_case_with_underscores and *love* mixedCase, which I am
# using in spite of the PEP 0008 recommendations.

# A lot of base code copied from my earlier SoC project.

# ??? is a searchable string for later lookup for things I know are
# needed but whose exact use is unclear.

# "coord" and "coordinates" refer to the MapCell coordinates, while
# "top" and "left" and "width" etc. refer to pixel coordinates.

try:
    import os
    import sys
    import pygame as pg

    import options
    from prepare import COLORS, COORD_DISPLAY, DIRS, WALL_TYPE, DEBUG_TEST, FPS

except ImportError as err:
    print "Could not load module: %s" % (err)
    sys.exit(2)

if not pg.font:
    print "Warning: fonts disabled."


def terminate():
    """End the program cleanly."""
    pg.quit()
    sys.exit(0)

def main():
    """Run the program."""
    opts = options.Options()
    theMap = Map(opts)

    screenWidth = opts.cellWidth * (theMap.numCellsX + opts.wraparoundRepeat
                                    * 2 + opts.coordDisplay)
    screenHeight = opts.cellHeight * (theMap.numCellsY + opts.wraparoundRepeat
                                      * 2 + opts.coordDisplay)

    pg.init()
    screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE, 32)
    pg.display.set_caption("MapMaker BT by CanuckMonkey Games")
    background = pg.Surface(screen.get_size())
    background = background.convert()
    overlay = pg.Surface(screen.get_size())
    overlay = screen.convert_alpha()
    theMap.draw(background)
    screen.blit(background, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()

    running = True

    # Loop while program is running
    while running:
        # Control maximum framrate
        clock.tick(FPS)

        # Process input
        for event in pg.event.get():
            if event.type == pg.QUIT:      #
                terminate()
            #if event.type == pg.KEYUP:
            #    if event.key == pg.K_ESCAPE:
            #        terminate()

        # Update program state

        # Draw/render
        overlay.fill((0, 0, 0, 0))
        theMap.draw(overlay)
        screen.blit(overlay, (0, 0))

        # *After* drawing everything, flip the display
        pg.display.flip()

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
            myRect = pg.draw.rect(surface, COLORS['ltgrey'], self.rect)


class MapCell(object):
    """Define a single cell of the map."""

    def __init__(self, opts, coords, topleft):
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
        self.rect = pg.Rect(self.topleft, (self.width, self.height))
        self.walls = {'n': Wall(self.opts, DIRS['north']),
                      'e': Wall(self.opts, DIRS['east']),
                      's': Wall(self.opts, DIRS['south']),
                      'w': Wall(self.opts, DIRS['west'])
                      }
        for wall in self.walls.itervalues():
            if wall.direction == DIRS['north']:
                wall.rect.width = self.rect.width
                wall.rect.height = self.rect.height * self.opts.wallRectThickness
                wall.rect.midtop = self.rect.midtop
            elif wall.direction == DIRS['south']:
                wall.rect.width = self.rect.width
                wall.rect.height = self.rect.height * self.opts.wallRectThickness
                wall.rect.midbottom = self.rect.midbottom
            elif wall.direction == DIRS['east']:
                wall.rect.width = self.rect.width * self.opts.wallRectThickness
                wall.rect.height = self.rect.height
                wall.rect.midleft = self.rect.midleft
            elif wall.direction == DIRS['west']:
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
            bgcolour = COLORS['black']

        myRect = pg.draw.rect(surface, bgcolour, (left, top, self.width, self.height))
        for wall in self.walls.itervalues():
            wall.draw(surface)

        return myRect

class Map(object):
    """Define one complete map."""

    def __init__(self, opts):
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
