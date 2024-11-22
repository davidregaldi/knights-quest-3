from os import system, name
from random import choice
import curses
import pygame

def cls():
    _ = system('cls') if name == 'nt' else system('clear')

def init_clock():
    clock = pygame.time.Clock()
    return clock

global cons_line
cons_line = 26

def cons_print(stdscr, message, color=29, bold=False, reverse=False, blink=False):
    global cons_line
    if cons_line > 37:
        cons_line = 26
        stdscr.addstr(cons_line, 1 , " "*64, curses.color_pair(0)) 
    stdscr.addstr(cons_line, 1, message, curses.color_pair(color))
    if bold:
        stdscr.addstr(cons_line, 1, message, curses.A_BOLD | curses.color_pair(color))
    if reverse:
        stdscr.addstr(cons_line, 1, message, curses.A_REVERSE | curses.color_pair(color))
    if blink:
        stdscr.addstr(cons_line, 1, message, curses.A_BLINK | curses.color_pair(color))
    if bold and reverse:
        stdscr.addstr(cons_line, 1, message, curses.A_REVERSE | curses.A_BOLD | curses.color_pair(color))
    if bold and blink:
        stdscr.addstr(cons_line, 1, message, curses.A_BLINK | curses.A_BOLD | curses.color_pair(color))
    if reverse and blink:
        stdscr.addstr(cons_line, 1, message, curses.A_BLINK | curses.A_REVERSE | curses.color_pair(color))
    if bold and reverse and blink:
        stdscr.addstr(cons_line, 1, message, curses.A_BLINK | curses.A_REVERSE | curses.A_BOLD | curses.color_pair(color))
    stdscr.addstr(cons_line+1, 1 , " "*64, curses.color_pair(0))
    cons_line += 1
    stdscr.refresh()

def cons_clean(stdscr):
    global cons_line
    for i in range(26,38):
        stdscr.addstr(i, 1, " "*128, curses.color_pair(0))
    cons_line = 26
        
def play_music(file):
    play_music = pygame.mixer.music.load(f'Sounds/{file}')
    pygame.mixer.music.play(-1)

def play_hit():
    sound = choice(['hit1.wav', 'hit2.wav'])
    pygame.mixer.Sound(f'Sounds/{sound}').play()

def roll_dice(dice=100, needed=50, luck=0):
    roll = choice(range(1,dice+1))
    if (roll+luck) >= needed:
        return True
    else:
        return False

