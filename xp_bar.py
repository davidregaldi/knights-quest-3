# Imports
from utils import *
import curses

# Class Setup
class XpBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "▒"
    barrier: str = "│"
    color: int = 5 
    def __init__(self,
                 entity,
                 length: int = 22,
                 color: int = 5,
                 ) -> None:
        self.entity = entity
        self.length = length
        self.color = color
        self.max_value = entity.xp_max
        self.current_value = entity.xp

    def update(self):
        self.current_value = self.entity.xp
        self.max_value = self.entity.xp_max
        return self

    def draw(self,stdscr, x, y):
        self.update()
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        stdscr.addstr(y, x, self.barrier, curses.color_pair(self.color))
        stdscr.addstr(y, x+1, 
                      f"{remaining_bars * self.symbol_remaining}"
                      f"{lost_bars * self.symbol_lost}", curses.color_pair(self.color))
        stdscr.addstr(y, x+remaining_bars+lost_bars, self.barrier, curses.color_pair(self.color))
        if len(str(self.entity.xp)) > 1:
            stdscr.addstr(y, x+remaining_bars-len(str(self.entity.xp)), f"{self.entity.xp}", curses.A_BOLD | curses.color_pair(33))
        else:
            stdscr.addstr(y, x+1, f"{self.entity.xp}", curses.A_BOLD | curses.color_pair(33))
        return self