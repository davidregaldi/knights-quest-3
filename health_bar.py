# Imports
from utils import *
import curses

# Class Setup
class HealthBar:
    symbol_remaining: str = "█"
    symbol_remaining_mini: str = "▄"
    symbol_lost: str = "▒"
    symbol_lost_mini: str = "_"
    barrier: str = "│"
    color: int = 9 
    def __init__(self,
                 entity,
                 length: int = 21,
                 mini_length: int = 8,
                 color: int = 8,
                 ) -> None:
        self.entity = entity
        self.length = length
        self.mini_length = mini_length
        self.color = color
        self.max_value = entity.health_max
        self.current_value = entity.health
        self.memory = 0

    def update(self):
        if self.entity.health < 0: self.memory = self.entity.health; self.entity.health = 0
        self.current_value = self.entity.health
        self.max_value = self.entity.health_max
        return self

    def draw(self,stdscr, x, y):
        self.update()
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        # stdscr.addstr(y, x+self.length+1, "Health", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(y, x, self.barrier, curses.color_pair(self.color))
        stdscr.addstr(y, x+1, 
                      f"{remaining_bars * self.symbol_remaining}"
                      f"{lost_bars * self.symbol_lost}", curses.color_pair(self.color))
        stdscr.addstr(y, x+1+remaining_bars+lost_bars, self.barrier, curses.color_pair(self.color))
        if len(str(self.entity.health)) > 1:
            stdscr.addstr(y, x+1+remaining_bars-len(str(self.entity.health)), f"{self.entity.health}", curses.A_BOLD | curses.color_pair(31))
        elif self.entity.health <= 0:
            stdscr.addstr(y, x+1, f"{lost_bars * self.symbol_lost}", curses.A_BOLD | curses.color_pair(1))
            stdscr.addstr(y, x+1, f"{self.memory}", curses.A_BOLD | curses.color_pair(34))
            stdscr.addstr(y, x+9, f"DEAD", curses.A_BOLD | curses.color_pair(34))
        else:
            stdscr.addstr(y, x+1, 
                          f"{remaining_bars * self.symbol_remaining}"
                          f"{lost_bars * self.symbol_lost}", curses.A_BOLD | curses.color_pair(1))
            stdscr.addstr(y, x+1, f"{lost_bars * self.symbol_lost}", curses.A_BOLD | curses.color_pair(1))
            stdscr.addstr(y, x+1, f"{self.entity.health}", curses.A_BOLD | curses.color_pair(34))
        return self
    
    def draw_mini(self,stdscr, x, y):
        self.update()
        remaining_bars = round(self.current_value / self.max_value * self.mini_length)
        lost_bars = self.mini_length - remaining_bars
        # stdscr.addstr(y, x+self.length+1, "Health", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(y, x, '', curses.color_pair(self.color))
        stdscr.addstr(y, x+1, f"{remaining_bars * self.symbol_remaining_mini}", curses.color_pair(self.color))
        stdscr.addstr(y, x+1+remaining_bars, f"{lost_bars * self.symbol_lost_mini}", curses.color_pair(1))
        stdscr.addstr(y, x+1+remaining_bars+lost_bars, '', curses.color_pair(self.color))
        return self

