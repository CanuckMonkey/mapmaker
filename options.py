from prepare import *

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
        self.bgcolours = {'default': DKGRAY, 'seen': YELLOW, 'visited': WHITE}
        self.numCellsX = 22
        self.numCellsY = 22

