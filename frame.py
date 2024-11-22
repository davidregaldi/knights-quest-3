import curses
from utils import *

class Frame:
    def __init__(self, width, height, x=0, y=0, frame_color=28, 
                 title=None, title_color=29, 
                 body=None, body_color=29, body_bold=False,
                 movable=False, actions=[],
                 foot=None, foot_color=29,
                 body2=None, body2_color=29):
        self.x = x
        self.y = y
        self.frame_color = frame_color
        self.title = title
        self.title_color = title_color
        self.body = body
        self.body_color = body_color
        self.body_bold = body_bold
        self.width = width
        self.height = height
        self.movable = movable
        self.actions = actions
        self.menu_loop = True
        self.foot = foot
        self.foot_color = foot_color
        self.body2 = body2
        self.body2_color = body2_color

    def draw(self, stdscr):
        if self.body != None and self.height <= len(self.body):
            self.height = len(self.body) +1
        if self.body != None:
            body_as_strings = [str(item) for item in self.body]
            if self.width < len(max(body_as_strings, key=len)):
                self.width = len(max(body_as_strings, key=len)) + 4
        frame_top = "┌" + "─" * (self.width-2) + "┐"
        frame_bottom = "└" + "─" * (self.width-2) + "┘"
        for i in range(1, self.height):
            stdscr.addstr(i+self.y, self.x, "│" + " " * (self.width-2) + "│", curses.color_pair(self.frame_color))
        stdscr.addstr(self.y, self.x, frame_top, curses.color_pair(self.frame_color))
        stdscr.addstr(self.height+self.y, self.x, frame_bottom, curses.color_pair(self.frame_color))
        if self.title != None:
            stdscr.addstr(self.y, self.x + self.width//2-len(self.title)//2, self.title, curses.A_BOLD | curses.color_pair(self.title_color))
        if self.body != None and self.body_bold == False:
            for i, content in enumerate(self.body):
                stdscr.addstr(self.y+i+1, self.x+2, str(content), curses.color_pair(self.body_color))
        if self.body != None and self.body_bold:
            for i, content in enumerate(self.body):
                stdscr.addstr(self.y+i+1, self.x+2, str(content), curses.A_BOLD | curses.color_pair(self.body_color))
        if self.foot != None:
            stdscr.addstr(self.y+self.height, self.width-len(self.foot)+self.x-1, self.foot, curses.A_BOLD | curses.color_pair(self.foot_color))
        if self.title == "Inventory":
            frame_top = "┌" + "─" * (self.width-2) + "┐"
            frame_bottom = "└" + "─" * (self.width-2) + "┘"
            for i in range(1, 12):
                stdscr.addstr(i+self.y, self.x+self.width, "│" + " " * (self.width-2) + "│", curses.color_pair(self.frame_color))
            stdscr.addstr(self.y, self.x+self.width, frame_top, curses.color_pair(self.frame_color))
            stdscr.addstr(13, self.x+self.width, frame_bottom, curses.color_pair(self.frame_color))
            stdscr.addstr(self.y, self.x+self.width+self.width//2-len(self.title)//2, "Equiped", curses.A_BOLD | curses.color_pair(self.title_color))
            for i, content in enumerate(self.body2):
                stdscr.addstr(self.y+i+1, self.x+self.width+2, str(content), curses.color_pair(self.body2_color))

        if self.movable:
            select = 1
            while self.menu_loop:
                for i, content in enumerate(self.body):
                    if i == select - 1:
                        stdscr.addstr(self.y+i+1, self.x+2, content, curses.color_pair(self.body_color) | curses.A_REVERSE)
                    else:
                        stdscr.addstr(self.y+i+1, self.x+2, content, curses.color_pair(self.body_color))
                key = stdscr.getch()
                if key == curses.KEY_UP and select > 1:
                    select -= 1
                elif key == curses.KEY_DOWN and select < len(self.body):
                    select += 1
                elif key == 10:
                    if select - 1 < len(self.actions):
                        if self.actions[select-1] == "quit_menu":self.quit_menu()
                        elif self.actions[select-1] == "quit_game":return True
                elif key == ord('h') or key == ord('H') and self.title == "Help":self.quit_menu()
                elif key == ord('q') or key == ord('Q') or key == 127 or key == 27:self.quit_menu()
                elif key == ord('i') or key == ord('I'):cons_print(stdscr, "Close This Window First.")
                elif key == ord(' '):
                    cons_clean(stdscr)

    def quit_menu(self):
        pygame.mixer.Sound('Sounds/confirm.wav').play()
        self.menu_loop = False
        