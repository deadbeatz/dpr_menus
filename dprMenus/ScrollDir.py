from enum import Enum

class ScrollDir(Enum):
    up = 1
    up_block = 2
    down = 3
    down_block = 4
    up_page = 5
    down_page = 6
    home = 7
    end = 8