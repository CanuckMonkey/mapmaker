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

    import prepare
    import map
    import options
    from options import COLORS, COORD_DISPLAY, DIRS, WALL_TYPE, DEBUG_TEST, FPS

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
        prepare.overlay.fill((0, 0, 0, 0))
        prepare.theMap.draw(prepare.overlay)
        prepare.screen.blit(prepare.overlay, (0, 0))

        # *After* drawing everything, flip the display
        pg.display.flip()


if __name__ == "__main__":      # Do not run this if called from some other module???
    main()
