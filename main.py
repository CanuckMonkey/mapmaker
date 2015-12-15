#!/usr/bin/env python

""" Map Creation Tool

This tool is designed with an initial focus on Bard's Tale-style maps.

Maps are built on a cartesian grid.  Each cell in the grid defines its
own contents as well as the contents of the four bounding walls.
"""

# A lot of base code copied from my earlier SoC project.

# ??? is a searchable string for later lookup for things I know are
# needed but whose exact use is unclear.

# "coord" and "coordinates" refer to the MapCell coordinates, while
# "top" and "left" and "width" etc. refer to pixel coordinates.

import os
import sys

try:
    import pygame as pg

    import prepare
    import map_tools
    import options
    from options import COLORS, COORD_DISPLAY, DIRS, WALL_TYPE, FPS

except ImportError as err:
    print "Could not load module: %s" % (err)
    sys.exit(2)

if not pg.font:
    print "Warning: fonts disabled."


#def terminate():
#    """End the program cleanly."""
#    pg.quit()
#    sys.exit(0)


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
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    running = False

        # Update program state

        # Draw/render
        prepare.overlay.fill((0, 0, 0, 0))
        prepare.the_map.draw(prepare.overlay)
        prepare.screen.blit(prepare.overlay, (0, 0))

        ## *After* drawing everything, flip the display
        #pg.display.flip()

        # *After* drawing everything, update the display
        pg.display.update()

        pg.display.set_caption(prepare.ORIGINAL_CAPTION+
                               "     FPS: {}".format(clock.get_fps()))

    pg.quit()
    return 0


#if __name__ == "__main__":      # Do not run this if called from some other module???
#    main()

if __name__ == "__main__":
    sys.exit(int(main() or 0))
