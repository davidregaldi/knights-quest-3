from tile import Tile, grass, forest, water, player, bridge, mountains, zombie, wolf, skeleton, chest, boss, super_chest
from random import randint, choice
from utils import play_music, cons_print
import curses
import pygame
import os

class Map:
    def __init__(self, 
                 width: int=64,
                 height: int=24,
                 name: str="",
                )->None:
        self.width = width
        self.height = height
        self.name = name
        self.map_data = list[list[Tile]]
        self.generate_map()
        if self.name == "The Forest 8":
            self.generate_patch(forest, 12, 6, 6, 2)
            self.generate_patch(mountains, 1, 12, 7, 0)
            self.generate_river(water)
            self.generate_bridge(3, water)
            self.generate_entities(type=wolf, quantity=8)
            self.generate_entities(type=zombie, quantity=4)
            self.generate_entities(type=skeleton, quantity=4)
            self.generate_entities(type=chest,quantity=6)
            play_music("the_forest.wav")
    
    def generate_map(self)->None:
        self.map_data = [[grass for x in range(self.width)] for y in range(self.height)]
    
    def generate_entities(self, type: Tile, quantity: int)->None:
        i = 0
        while i < quantity:
            x = randint(1, self.width - 2)
            y = randint(1, self.height - 2)
            if self.map_data[y][x] == grass:
                self.map_data[y][x] = type
                i += 1
            else:
                continue

    def generate_patch(self, 
                    tile: Tile, 
                    num_patches: int, 
                    wsize: int, 
                    hsize: int,
                    variation: int=2,
                    irregular: bool=True,
                    )->None:
        for _ in range(num_patches):    
            width = randint(wsize-variation, wsize+variation)
            height = randint(hsize-variation, hsize+variation)
            start_x = randint(1, self.width - width - 1)
            start_y = randint(1, self.height - height - 1)
            if irregular:
                init_start_x = randint(3, self.width - wsize)
            for y in range(height):
                if irregular:
                    width = randint(int(0.7 * wsize), wsize)
                    start_x = init_start_x - randint(1, 2)
                for x in range(width):
                    self.map_data[start_y + y][start_x + x] = tile
    
    def generate_river(self, tile: Tile) -> None:
        is_horizontal = bool(randint(0, 1))
        if is_horizontal:
            y = randint(1, self.height - 2)
            for x in range(self.width):
                self.map_data[y][x] = tile
                if choice([True, False]):
                    y = max(1, min(y + choice([-1, 1]), self.height - 2))
        else:
            x = randint(1, self.width - 2)
            for y in range(self.height):
                self.map_data[y][x] = tile
                if choice([True, False]):
                    x = max(1, min(x + choice([-1, 1]), self.width - 2))

    def generate_bridge(self, number: int=3, tile: Tile=water) -> None:
        bridge_count = 0
        while bridge_count < 3:
            for y in range(1, self.height - 1):
                for x in range(1, self.width - 1):
                    if self.map_data[y][x] == tile and bridge_count < 3:
                        self.map_data[y][x] = bridge
                        bridge_count += 1
                        break
                if bridge_count >= number:
                    break

    def generate_boss(self, stdscr, frame, mountain_tile: Tile=mountains, boss_tile: Tile=boss, z_tile: Tile=zombie, s_tile: Tile=skeleton, w_tile: Tile=wolf, g_tile: Tile=grass, sc_tile: Tile=super_chest) -> None:
        if any(tile in row for row in self.map_data for tile in [z_tile, s_tile, w_tile, boss_tile]):
            return
        
        mountain_coords = [(x, y) for y, row in enumerate(self.map_data) for x, tile in enumerate(row) if tile == mountain_tile]
        if not mountain_coords:
            return
        
        center_x = sum(x for x, y in mountain_coords) // len(mountain_coords)
        center_y = sum(y for x, y in mountain_coords) // len(mountain_coords)

        self.map_data[center_y][center_x] = boss_tile
        self.map_data[center_y +1][center_x] = sc_tile
        self.map_data[center_y][center_x - 1] = g_tile
        self.map_data[center_y][center_x - 2] = g_tile
        self.map_data[center_y][center_x - 3] = g_tile
        self.map_data[center_y][center_x - 4] = g_tile
        self.map_data[center_y][center_x - 5] = g_tile

        frame.draw(stdscr)      
        
    def draw_map(self, stdscr):
        for y, row in enumerate(self.map_data):
            for x, tile in enumerate(row):
                stdscr.attron(curses.color_pair(tile.color))
                if tile.bold:stdscr.attron(curses.A_BOLD)
                stdscr.addch(y+1, x+1, tile.char)
                if tile.bold:stdscr.attroff(curses.A_BOLD)
                stdscr.attroff(curses.color_pair(tile.color))
            
    