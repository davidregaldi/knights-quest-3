# Imports
from utils import *
import curses

# Class Setup
class ManaBar:
    symbol_remaining: str = "█"
    symbol_remaining_mini: str = "▀"
    symbol_lost: str = "▒"
    symbol_lost_mini: str = "_"
    barrier: str = "│"
    color: int = 14 
    def __init__(self,
                 entity,
                 length: int = 21,
                 mini_length: int = 8,
                 color: int = 14,
                 ) -> None:
        self.entity = entity
        self.length = length
        self.mini_length = mini_length
        self.color = color
        self.max_value = entity.mana_max
        self.current_value = entity.mana
        self.memory = 0

    def update(self):
        if self.entity.mana < 0: self.memory = self.entity.mana; self.entity.mana = 0
        self.current_value = self.entity.mana
        self.max_value = self.entity.mana_max
        return self

    def draw(self,stdscr, x, y):
        self.update()
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        # stdscr.addstr(y, x-4, "Mana", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(y, x, self.barrier, curses.color_pair(self.color))
        stdscr.addstr(y, x+1,
                      f"{remaining_bars * self.symbol_remaining}"
                      f"{lost_bars * self.symbol_lost}", curses.color_pair(self.color))
        stdscr.addstr(y, x+remaining_bars+lost_bars, self.barrier, curses.color_pair(self.color))
        if len(str(self.entity.mana)) > 1:
            stdscr.addstr(y, x+remaining_bars-len(str(self.entity.mana)), f"{self.entity.mana}", curses.A_BOLD | curses.color_pair(32))
        elif self.entity.mana <= 0:
            stdscr.addstr(y, x+1, f"{self.memory}", curses.A_BOLD | curses.color_pair(14))
        else:
            stdscr.addstr(y, x+1, f"{self.entity.mana}", curses.A_BOLD | curses.color_pair(32))
        return self
    
    def draw_mini(self,stdscr, x, y):
        self.update()
        remaining_bars = round(self.current_value / self.max_value * self.mini_length)
        lost_bars = self.mini_length - remaining_bars
        stdscr.addstr(y, x, '', curses.color_pair(self.color))
        stdscr.addstr(y, x+1,
                      f"{remaining_bars * self.symbol_remaining_mini}"
                      f"{lost_bars * self.symbol_lost_mini}", curses.color_pair(self.color))
        if self.entity.is_caster == False:
            stdscr.addstr(y, x+1, '▀'+'‾'*(self.mini_length-1), curses.color_pair(self.color))
        stdscr.addstr(y, x+remaining_bars+lost_bars, '', curses.color_pair(self.color))
        return self