import curses
import pygame
from random import choice
from utils import cons_print, play_music, roll_dice
from potion import Potion
from offhand import Arrow
from weapon import *
from frame import Frame

def clear_area(stdscr, y1, x1, y2, x2):
    for y in range(y1, y2+1):
        stdscr.move(y, x1)
        for x in range(x1, x2+1):
            stdscr.addch(' ')  # Remplace le caractère à la position actuelle par un espace
    stdscr.refresh()  # Met à jour l'écran avec les changements

def draw_diagonal(stdscr, height=24, width=62):
    for i in range(min(height, width)):
        y = i +1
        x = int(i * 2.58333333) + 2
        stdscr.addch(y, x, '*')
    stdscr.refresh()

def center_text(stdscr, text, height=24, width=62):
    lines = text.split('\n')
    top_margin = (height - len(lines)) // 2 +1
    for i, line in enumerate(lines):
        left_margin = (width - len(line)) // 2 +1
        stdscr.addstr(top_margin + i, left_margin, line, curses.A_BLINK | curses.color_pair(6))
    stdscr.refresh()

def bars_refresh(stdscr, enemy=None, player=None):
        if enemy != None:
            if enemy.name == "Wolf":
                enemy.health_bar.draw_mini(stdscr, 48, 6)
                enemy.mana_bar.draw_mini(stdscr, 48, 7)
                stdscr.addstr(1,45, f"    {enemy.name} lvl {enemy.level}", curses.color_pair(1))
            elif enemy.name == "Skeleton":
                enemy.health_bar.draw_mini(stdscr, 47, 9)
                enemy.mana_bar.draw_mini(stdscr, 47, 10)
                stdscr.addstr(1,42, f"    {enemy.name} lvl {enemy.level}", curses.color_pair(1))
            elif enemy.name == "Zombie":
                enemy.health_bar.draw_mini(stdscr, 45, 8)
                enemy.mana_bar.draw_mini(stdscr, 45, 9)
                stdscr.addstr(1,41, f"    {enemy.name} lvl {enemy.level}", curses.color_pair(1))
            elif enemy.name == "Boss":
                enemy.health_bar.draw_mini(stdscr, 45, 7)
                enemy.mana_bar.draw_mini(stdscr, 45, 8)
                stdscr.addstr(1,42, f"    {enemy.name} lvl {enemy.level}", curses.color_pair(1))
        if player != None:
            player.health_bar.draw_mini(stdscr, 2, 23)
            player.mana_bar.draw_mini(stdscr, 2, 24)
            player.health_bar.draw(stdscr, 90, 1)
            player.mana_bar.draw(stdscr, 90, 2)

        character_frame = Frame(18,4,64,0, title="Character", body_color=29, body=[(f"Name: {player.name}"), ("Class: "), (f"Level: {player.level}")])
        attribute_frame = Frame(18,14,64,5, title="Attributes", body=[(f"Strenght: {player.strength}"), (f"Dexterity: {player.dexterity}"), (f"Magic: {player.magic}"), (f"Vitality: {player.vitality}"), (f"Luck: {player.luck}"), (""), (f"Damage: {player.damage}"), (f"% Crit: {player.critical}"), (""), (f"Armor: {player.armor + player.temporary_effects.get('armor', 0)}"), (f"% Block: {player.block}"), (f"Res. Magic: {player.resist_magic + player.temporary_effects.get('resist_magic', 0)}")])
        equipment_frame = Frame(32,14,82,5, title="Equipment", body=[(f"Weapon:  {player.weapon.name}"), (f"         {player.weapon.description}"), (f"Offhand: {player.offhand.name}"), (f"         {player.offhand.description}"), (f"{player.helmet.name}: {player.helmet.description}"), (f"{player.body_armor.name}: {player.body_armor.description}"), (f"{player.gloves.name}: {player.gloves.description}"), (f"{player.belt.name}: {player.belt.description}"), (f"{player.boots.name}: {player.boots.description}"), (""), (f"Gold: {player.gold}")])
        spells_frame = Frame(50,5,64,20, title="Spells", body=player.spell_book)
        character_frame.draw(stdscr)
        attribute_frame.draw(stdscr)        
        equipment_frame.draw(stdscr)        
        spells_frame.draw(stdscr)
        stdscr.refresh()

def frame_player(stdscr, player, enemy):
    x=1
    y=1
    width=16
    width2=22
    height=8
    height2=len(player.spell_book)+2
    height3 = sum(isinstance(key, Potion) for key in player.inventory.keys()) + 2 + sum(isinstance(key, Arrow) for key in player.inventory.keys())
    x2 = x + width
    selected = [1,1]
    stdscr.addstr(y, x, "┌" + "─" * (width-2) + "┐", curses.color_pair(26))
    for i in range(height-2):
        stdscr.addstr(y+i+1, x, "│" + " " * (width-2) + "│", curses.color_pair(26))
    stdscr.addstr(y+height-1, x, "└" + "─" * (width-2) + "┘", curses.color_pair(26))
    stdscr.addstr(y,x, "Your Turn", curses.A_BOLD | curses.color_pair(29))
    while True:
        if selected == [1,1]:stdscr.addstr(y+1,x+2, "Attack", curses.A_BOLD | curses.color_pair(29) | curses.A_REVERSE)
        else: stdscr.addstr(y+1,x+2, "Attack", curses.A_BOLD | curses.color_pair(29))
        if selected == [1,2]:stdscr.addstr(y+2,x+2, "Magic", curses.A_BOLD | curses.color_pair(29) | curses.A_REVERSE)
        else: stdscr.addstr(y+2,x+2, "Magic", curses.A_BOLD | curses.color_pair(29))
        if selected == [1,3]:stdscr.addstr(y+3,x+2, "Items", curses.A_BOLD | curses.color_pair(29) | curses.A_REVERSE)
        else: stdscr.addstr(y+3,x+2, "Items", curses.A_BOLD | curses.color_pair(29))
        if selected == [1,4]:stdscr.addstr(y+4,x+2, "Run", curses.A_BOLD | curses.color_pair(29) | curses.A_REVERSE)
        else: stdscr.addstr(y+4,x+2, "Run", curses.A_BOLD | curses.color_pair(29))
        if selected[0] == 2:
            stdscr.addstr(y+1, x2, "┌" + "─" * (width2-2) + "┐" + "        ", curses.color_pair(26))
            for i in range(height2-2):
                stdscr.addstr(y+i+1+1, x2, "│" + " " * (width2-2) + "│" + "       ", curses.color_pair(26))
            stdscr.addstr(y+height2-1+1, x2, "└" + "─" * (width2-2) + "┘" + "       ", curses.color_pair(26))
            stdscr.addstr(y+height2-1+2, x2, " " + " " * (width2-2) + " " + "       ", curses.color_pair(26))
            for i, content, in enumerate(player.spell_book):
                stdscr.addstr(y+i+2, x2+2, f"{content.name} {content.level} {content.mana_cost}", curses.A_BOLD | curses.color_pair(29))
                if selected[1] == i+2:
                    stdscr.addstr(y+i+2, x2+2, f"{content.name} {content.level} {content.mana_cost}", curses.A_BOLD | curses.color_pair(29) | curses.A_REVERSE)
                if content.mana_cost > player.mana:
                    stdscr.addstr(y+i+2, x2+2, f"{content.name}    ", curses.A_BOLD | curses.color_pair(27))
                    if selected[1] == i+2:
                        stdscr.addstr(y+i+2, x2+2, f"{content.name} {content.level} {content.mana_cost}", curses.A_BOLD | curses.color_pair(27) | curses.A_REVERSE)

        elif selected[0] == 3:
            stdscr.addstr(y+1, x2, " " + " " * (width2) + " ", curses.color_pair(26))
            stdscr.addstr(y+2, x2, "┌" + "─" * (width2) + "┐", curses.color_pair(26))
            for i in range(height3-2):
                stdscr.addstr(y+i+1+2, x2, "│" + " " * (width2) + "│", curses.color_pair(26))
            stdscr.addstr(y+height3-1+2, x2, "└" + "─" * (width2) + "┘", curses.color_pair(26))
            i=0
            for key, value in player.inventory.items():
                if isinstance(key, Potion) or isinstance(key, Arrow):
                    stdscr.addstr(y+i+3, x2+2, f"{key.name} x{value}", curses.A_BOLD | curses.color_pair(29))
                    i += 1
                    if selected[1] == i+2:
                        stdscr.addstr(y+i+2, x2+2, f"{key.name} x{value}", curses.A_BOLD | curses.color_pair(29) | curses.A_REVERSE)
        else:
            stdscr.addstr(y+1, x2, " " + " " * (width2) + " ", curses.color_pair(26))
            for i in range(height):
                stdscr.addstr(y+i+1+1, x2, " " + " " * (width2) + " ", curses.color_pair(26))
            stdscr.addstr(y+height-1+2, x2, " " + " " * (width2) + " ", curses.color_pair(26))

        stdscr.refresh()
        key = stdscr.getch()
        if key == curses.KEY_UP:
            pygame.mixer.Sound('Sounds/select.wav').play()
            selected[1] -= 1
            if selected[0] == 1 and selected[1] < 1: selected[1] = 4
            elif selected[0] == 2 and selected[1] < 2: selected[1] = len(player.spell_book)+1
            elif selected[0] == 3 and selected[1] < 3: selected[1] = sum(isinstance(key, Potion) for key in player.inventory.keys())+2
        elif key == curses.KEY_DOWN: 
            pygame.mixer.Sound('Sounds/select.wav').play()
            selected[1] += 1
            if selected[0] == 1 and selected[1] > 4: selected[1] = 1
            elif selected[0] == 2 and selected[1] > len(player.spell_book)+1: selected[1] = 2
            elif selected[0] == 3 and selected[1] > height3: selected[1] = 3
        elif key == curses.KEY_LEFT and selected[0] > 1:
            pygame.mixer.Sound('Sounds/select.wav').play()
            if selected[0] == 2: 
                selected = [1,2]
            elif selected[0] == 3: 
                selected = [1,3]
            else: selected[0] -= 1
        elif key == curses.KEY_RIGHT and selected[0] < 3:
            pygame.mixer.Sound('Sounds/select.wav').play()
            if selected == [1,3]:
                selected[0] += 2
            elif selected == [1,1] or selected == [1,4]:
                pass
            elif selected[0] == 2: 
                pass
            else: selected[0] += 1
        elif (key == curses.KEY_ENTER or key == ord('\n')):
            if selected == [1,1]:
                player.attack(stdscr, enemy, enemy, player)
                # bars_refresh(stdscr, enemy, player)
                # stdscr.refresh()
                return True
            elif selected == [1,2]:
                selected[0] = 2
            elif selected == [1,3]:
                selected[0] = 3
            elif selected == [1,4]:
                if roll_dice(100, 40, player.luck):
                    player.temporary_effects.clear()
                    enemy.temporary_effects.clear()
                    cons_print(stdscr, "You run away...", color=10, bold=True)
                    return False
                else:
                    cons_print(stdscr, "You failed to run away...", color=4, bold=True)
                    return True
            elif selected[0] == 2:
                number_of_spells = len(player.spell_book)
                for i in range(number_of_spells):
                    if i+2 == selected[1]:
                        spell_to_cast = list(player.spell_book.items())[i]
                        player.cast_spell(stdscr, enemy, spell_to_cast[0], enemy, player)
                        return True
            elif selected[0] == 3:
                filtered_inventory = {key: value for key, value in player.inventory.items() if isinstance(key, (Arrow, Potion))}
                number_of_items = len(filtered_inventory)
                for i in range(number_of_items):
                    if i+3 == selected[1]:
                        item = list(filtered_inventory.keys())[i]
                        if isinstance(item, Potion):
                            player.use(stdscr, item)
                            bars_refresh(stdscr, enemy, player)
                            pygame.time.delay(750)
                            return True
                        elif isinstance(item, Arrow):
                            player.equip(stdscr, item)
                            player.put_out_inventory(stdscr, item)
                            bars_refresh(stdscr, enemy, player)
                            pygame.time.delay(750)
                            return True
                            



    

def fight_screen(stdscr, player, enemy):
    inventory_names = [item.name for item in enemy.inventory.keys()]
    cons_print(stdscr, f"DEBUG: gold: {enemy.gold} inventory: {inventory_names} "
        f"Stuff: "
        f"{'' if enemy.helmet.description == 'Empty' else enemy.helmet.name}"
        f"{'' if enemy.body_armor.description == 'Empty' else enemy.body_armor.name}"
        f"{'' if enemy.gloves.description == 'Empty' else enemy.gloves.name}"
        f"{'' if enemy.belt.description == 'Empty' else enemy.belt.name}"
        f"{'' if enemy.boots.description == 'Empty' else enemy.boots.name}"
        f"{'' if enemy.weapon.name == 'Hands' else enemy.weapon.name}"
        f"{'' if enemy.offhand.description == 'Empty' else enemy.offhand.name}", color=29, bold=True)
    cons_print(stdscr, f"DEBUG: Stats: S:{enemy.strength} D:{enemy.dexterity} M:{enemy.magic} V:{enemy.vitality} L:{enemy.luck} A:{enemy.armor} MA:{enemy.resist_magic} B:{enemy.block} C:{enemy.critical} HP:{enemy.health} MP:{enemy.mana}", color=29, bold=True)
    play_music(choice(['fight.wav', 'fight2.wav']))
    clear_area(stdscr, 1, 1, 24, 62)
    # draw_diagonal(stdscr)
    text = """
▄▄   █▀▀ █ █▀▀ █░█ ▀█▀   ▄▄
░░   █▀░ █ █▄█ █▀█ ░█░   ░░"""
    center_text(stdscr, text)


    # stdscr.addstr(12,5, f"{player1.name}", curses.A_BOLD | curses.color_pair(9))
    # stdscr.addstr(13,5, f"Level: {player1.level}", curses.A_BOLD | curses.color_pair(9)

    if isinstance(player.weapon, Bow):
        stdscr.addstr(18,1, f"     ▄▄ ", curses.color_pair(26))
        stdscr.addstr(19,1, f"     ̳█▒ ❚\\", curses.color_pair(26))
        stdscr.addstr(20,1, f"    ██)-❚-|>", curses.color_pair(26))
        stdscr.addstr(21,1, f"   (██▀▀❚/", curses.color_pair(26))
        stdscr.addstr(22,1, f"    █▄", curses.color_pair(26))
    elif isinstance(player.weapon, Weapon):
        if player.weapon.name != "Hands":
            stdscr.addstr(18,1, f"     ▄▄ ⏶", curses.color_pair(26))
            stdscr.addstr(19,1, f"     ̳█▒ ❚", curses.color_pair(26))
            stdscr.addstr(20,1, f"    ██)_❚_", curses.color_pair(26))
            stdscr.addstr(21,1, f"   (██▀▀❚", curses.color_pair(26))
            stdscr.addstr(22,1, f"    █▄", curses.color_pair(26))
        else:
            stdscr.addstr(18,1, f"     ▄▄ ", curses.color_pair(26))
            stdscr.addstr(19,1, f"     ̳█▒ ", curses.color_pair(26))
            stdscr.addstr(20,1, f"    ██)", curses.color_pair(26))
            stdscr.addstr(21,1, f"   (██▀▀", curses.color_pair(26))
            stdscr.addstr(22,1, f"    █▄", curses.color_pair(26))

    if enemy.name == "Wolf":
        stdscr.addstr(2,45, f"|\_/|▒▄▄▄^▄^▄▄▀▀", curses.color_pair(26))
        stdscr.addstr(3,45, f"(.▒.)█▒█▒█▒█▒)", curses.color_pair(26))
        stdscr.addstr(4,45, f" \-/\▄/▀▀▀▀\\\\", curses.color_pair(26))
        stdscr.addstr(5,45, f"   _//    _//", curses.color_pair(26))
        # stdscr.addstr(12,50, f"{enemy.name}", curses.A_BOLD | curses.color_pair(1))
        # stdscr.addstr(13,50, f"Level: {enemy.level}", curses.A_BOLD | curses.color_pair(1))

    elif enemy.name == "Skeleton":
        stdscr.addstr(2,45, f"     ▄≡▄", curses.color_pair(26))
        stdscr.addstr(3,45, f"    █▄ȸ▄█  ⏶", curses.color_pair(26))
        stdscr.addstr(4,45, f"     █▄█   █", curses.color_pair(26))
        stdscr.addstr(5,45, f" ▄▄ ▄ ̳¥ ̳▄ ▄█▄", curses.color_pair(26))
        stdscr.addstr(6,45, f"█()█▀)‡(▀▀▀█", curses.color_pair(26))
        stdscr.addstr(7,45, f" ▀▀  ▄±▄", curses.color_pair(26))
        stdscr.addstr(8,45, f"    ▄█ █▄", curses.color_pair(26))
    
    elif enemy.name == "Zombie":
        stdscr.addstr(2,45, f"   ▄\\▄ ", curses.color_pair(26))  
        stdscr.addstr(3,45, f"  ❚°,º❚ ", curses.color_pair(26))
        stdscr.addstr(4,45, f"   ▀▄▀",  curses.color_pair(26))
        stdscr.addstr(5,45, f"❚▀❚▀‡▀", curses.color_pair(26))
        stdscr.addstr(6,45, f"   (≡", curses.color_pair(26))
        stdscr.addstr(7,45, f"   ❚█", curses.color_pair(26))

    elif enemy.name == "Boss":
        stdscr.addstr(2,45, f"   ����", curses.color_pair(20))
        stdscr.addstr(3,45, f"  �BOSS�", curses.color_pair(20))
        stdscr.addstr(4,45, f"  ������", curses.color_pair(20))
        stdscr.addstr(5,45, f"   ����", curses.color_pair(20))


    # stdscr.refresh()
    pygame.time.delay(2000)
    # Clear fight intro
    # stdscr.addstr(12, 5, " " * len(player.name))
    # stdscr.addstr(13, 5, " " * len(f"Level: {player.level}"))
    # stdscr.addstr(12, 50, " " * len(enemy.name))
    # stdscr.addstr(13, 50, " " * len(f"Level: {enemy.level}"))
    text = """
                            
                            """

    center_text(stdscr, text)

    stdscr.addstr(17,1, f"   {player.name}", curses.color_pair(9))
    bars_refresh(stdscr, enemy, player)

    while player.is_alive(stdscr) and enemy.is_alive(stdscr): 
        if frame_player(stdscr, player, enemy) == False:  
            play_music('the_forest.wav')
            break
        if not enemy.is_alive(stdscr):
            play_music('the_forest.wav')
            break
        if not player.is_alive(stdscr):
            player.game_over(stdscr)
        if enemy.name != "Boss":
            enemy.attack(stdscr, player, enemy, player)
        else:
            if enemy.health < enemy.health_max * 0.33:
                spell_to_cast = list(enemy.spell_book.items())[2]
                if enemy.cast_spell(stdscr, player, spell_to_cast[0], enemy, player):
                    continue
                else:
                    enemy.attack(stdscr, player, enemy, player)
            else:
                    enemy.attack(stdscr, player, enemy, player)
    