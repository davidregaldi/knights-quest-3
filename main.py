import curses
import pygame
import time
from tile import init_colors_extend
from character import Character, Hero, Enemy
from frame import Frame
from map import Map
from weapon import *
from offhand import *
from helmet import *
from body_armor import *
from gloves import *
from belt import *
from boots import *
from potion import *
from spell import *
from utils import *
from combat import *

first_start=True
def main(stdscr):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.25)
    stdscr.clear()
    init_colors_extend(stdscr)
    game_map = Map(62, 24, "The Forest 8")
    game_loop = True
    player1 = Hero(name="Eidknab")
    player1.spawn(stdscr, game_map)
    player1.put_in_inventory(stdscr, short_sword, 1)
    player1.put_in_inventory(stdscr, small_life_potion, 3)
    player1.put_in_inventory(stdscr, small_mana_potion, 1)
    player1.learn_spell(stdscr, firebolt)
    player1.learn_spell(stdscr, icearmor)
    player1.learn_spell(stdscr, heal)

    while game_loop:
        map_frame = Frame(64,25,0,0, title=f"Knight Quest III: {game_map.name}")
        character_frame = Frame(18,4,64,0, title="Character", body_color=29, body=[(f"Name: {player1.name}"), ("Class: "), (f"Level: {player1.level}")])
        bars_frame = Frame(32,4,82,0, title="Bars", body=[(f"Health {player1.health}/{player1.health_max}"), (f"Mana  {player1.mana}/{player1.mana_max}"), (f"Exp.   {player1.xp}/{player1.xp_max}")])
        attribute_frame = Frame(18,14,64,5, title="Attributes", body=[(f"Strenght: {player1.strength}"), (f"Dexterity: {player1.dexterity}"), (f"Magic: {player1.magic}"), (f"Vitality: {player1.vitality}"), (f"Luck: {player1.luck}"), (""), (f"Damage: {player1.damage}"), (f"% Crit: {player1.critical}"), (""), (f"Armor: {player1.armor}"), (f"% Block: {player1.block}"), (f"Res. Magic: {player1.resist_magic}")])
        equipment_frame = Frame(32,14,82,5, title="Equipment", body=[(f"Weapon:  {player1.weapon.name}"), (f"         {player1.weapon.description}"), (f"Offhand: {player1.offhand.name}"), (f"         {player1.offhand.description}"), (f"{player1.helmet.name}: {player1.helmet.description}"), (f"{player1.body_armor.name}: {player1.body_armor.description}"), (f"{player1.gloves.name}: {player1.gloves.description}"), (f"{player1.belt.name}: {player1.belt.description}"), (f"{player1.boots.name}: {player1.boots.description}"), (""), (f"Gold: {player1.gold}")])
        spells_frame = Frame(50,5,64,20, title="Spells", body=player1.spell_book)

        map_frame.draw(stdscr)
        character_frame.draw(stdscr)
        bars_frame.draw(stdscr)
        attribute_frame.draw(stdscr)        
        equipment_frame.draw(stdscr)        
        spells_frame.draw(stdscr)
        game_map.draw_map(stdscr)
        player1.health_bar.draw(stdscr, 90, 1)
        player1.mana_bar.draw(stdscr, 90, 2)
        player1.xp_bar.draw(stdscr, 90, 3)
        global first_start
        boss_frame = Frame(1,1,9,10, title="", body=["", "Knight !?", "A valley appeared in the mountains !", "Find the treasure but... Be careful", ""], body_color=4, body_bold=True, movable=True, actions=["quit_menu"], foot="'Enter' to Continue")
        game_map.generate_boss(stdscr, frame=boss_frame)
        if first_start:
            help_frame = Frame(37,2,13,4, title="Help", body=["   Welcome to Knight Quest III   ", "", "Press '←↑↓→' to Move ", "Press 'H' to Show Help", "Press 'I' to Show Inventory", "Press 'M' to Mute Music", "Press 'Space' to Clean Console", "Press 'Q' to Quit Game", "", "'@' = Player", "'S''W''Z'= Skeleton,Wolf,Zombie", "'B' = Boss", "'8' = Trees", "'^' = Mountains", "'$' = Chests", "'~' = Water,Lava", "'=' = Bridges" ], movable=True, actions=["quit_menu", "quit_menu", "quit_menu", "quit_menu", "quit_menu"], foot="'Enter' to Continue")
            help_frame.draw(stdscr)
            game_map.draw_map(stdscr)
            starting_frame = Frame(1,1,9,10, title="", body=["", "Knight !?", "Equip your sword and explore the forest !", ""], body_color=4, body_bold=True, movable=True, actions=["quit_menu"], foot="'Enter' to Continue")
            cons_print(stdscr, "Knight !? Equip your sword and explore the forest !", 4)
            starting_frame.draw(stdscr)
        else:
            select = stdscr.getch()
            if select == ord('q') or select == ord('Q'):
                confirm_frame = Frame(24,3,19,10, title="Quit The Game ?", body=["         Yes         ", "         No          "], movable=True, actions=["quit_game", "quit_menu"])
                if confirm_frame.draw(stdscr):
                    game_loop = False
                    break
            elif select == ord(' '):
                cons_clean(stdscr)
            elif select == ord('i') or select == ord('I'):
                player1.show_inventory(stdscr)
            elif select == ord('h') or select == ord('H'):
                help_frame = Frame(37,2,13,4, title="Help", body=["   Welcome to Knight Quest III   ", "", "Press '←↑↓→' to Move ", "Press 'H' to Show Help", "Press 'I' to Show Inventory", "Press 'M' to Mute Music", "Press 'Space' to Clean Console", "Press 'Q' to Quit Game", "", "'@' = Player", "'S''W''Z'= Skeleton,Wolf,Zombie", "'B' = Boss", "'8' = Trees", "'^' = Mountains", "'$' = Chests", "'~' = Water,Lava", "'=' = Bridges" ], movable=True, actions=["quit_menu", "quit_menu", "quit_menu", "quit_menu", "quit_menu"], foot="'Enter' to Continue")
                help_frame.draw(stdscr)
            elif select == ord('m') or select == ord('M'):
                pygame.mixer.music.stop()
            elif select == curses.KEY_UP:game_loop = player1.move(stdscr, player1, game_map, 0, -1)
            elif select == curses.KEY_DOWN:game_loop = player1.move(stdscr, player1, game_map, 0, 1)
            elif select == curses.KEY_LEFT:game_loop = player1.move(stdscr, player1, game_map, -1, 0)
            elif select == curses.KEY_RIGHT:game_loop = player1.move(stdscr, player1, game_map, 1, 0)
        if player1.health <= 0:
            player1.inventory.clear()
            game_loop = False
            first_start= True
            main(stdscr)

        first_start=False

curses.wrapper(main)
print("Quitting...")
pygame.mixer.Sound('Sounds/quit.wav').play()
time.sleep(1.5)