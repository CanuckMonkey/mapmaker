import os

import pygame as pg

import tools
import options
import map_tools

ORIGINAL_CAPTION = "MapMaker BT by CanuckMonkey Games"

opts = options.Options()
all_sprites = pg.sprite.LayeredDirty()
the_map = map_tools.Map(opts, all_sprites)

screen_width = opts.cell_width * (the_map.num_cells_x + opts.wraparound_repeat *
                                 2 + opts.coord_display)
screen_height = opts.cell_height * (the_map.num_cells_y + opts.wraparound_repeat *
                                   2 + opts.coord_display)

pg.init()
screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE, 32)
pg.display.set_caption(ORIGINAL_CAPTION)


GFX = tools.load_all_gfx(os.path.join("asset", "image"))
SFX = tools.load_all_sfx(os.path.join("asset", "sound"))
FONTS = tools.load_all_fonts(os.path.join("asset", "font"))
MUSIC = tools.load_all_music(os.path.join("asset", "music"))

background = pg.Surface(screen.get_size())
background = background.convert()
overlay = pg.Surface(screen.get_size())
overlay = screen.convert_alpha()
the_map.draw(background)
screen.blit(background, (0, 0))
pg.display.flip()

