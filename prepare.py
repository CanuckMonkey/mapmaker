import os

import pygame as pg

import tools
import options
import map


opts = options.Options()
theMap = map.Map(opts)

screenWidth = opts.cellWidth * (theMap.numCellsX + opts.wraparoundRepeat
                                * 2 + opts.coordDisplay)
screenHeight = opts.cellHeight * (theMap.numCellsY + opts.wraparoundRepeat
                                    * 2 + opts.coordDisplay)

pg.init()
screen = pg.display.set_mode((screenWidth, screenHeight), pg.RESIZABLE, 32)
pg.display.set_caption("MapMaker BT by CanuckMonkey Games")


GFX = tools.load_all_gfx(os.path.join("asset", "image"))
SFX = tools.load_all_sfx(os.path.join("asset", "sound"))
FONTS = tools.load_all_fonts(os.path.join("asset", "font"))
MUSIC = tools.load_all_music(os.path.join("asset", "music"))

background = pg.Surface(screen.get_size())
background = background.convert()
overlay = pg.Surface(screen.get_size())
overlay = screen.convert_alpha()
theMap.draw(background)
screen.blit(background, (0, 0))
pg.display.flip()





