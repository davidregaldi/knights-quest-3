# Imports
from random import randint, choice
from weapon import *
from offhand import *
from helmet import *
from body_armor import *
from gloves import *
from belt import *
from boots import *
from potion import *
from spell import *
from health_bar import HealthBar
from mana_bar import ManaBar
from xp_bar import XpBar
from tile import player, grass, forest, water, bridge, mountains, zombie, wolf, skeleton, chest, boss, super_chest
from utils import *
from frame import Frame
from combat import *
import curses
import pygame
import time

# Parent Class Setup
class Character:
    def __init__(self, 
                 name: str, 
                 position: list[int, int]=[0,0], #x, y
                 level: int=1,
                 level_max: int=50,
                 xp: int=0,
                 xp_max: int=100,
                 strength: int=30,
                 dexterity: int=20,
                 magic: int=10,
                 vitality: int=20,
                 luck: int=0,
                 weapon: object=None, #object of weapon class
                 offhand: object=None, #object of offhand class
                 helmet: object=None, 
                 body_armor: object=None,
                 gloves: object=None,
                 belt: object=None,
                 boots: object=None,
                 gold: int=0,
                 inventory: dict={}, #dict of items and their quantity
                 spell_book: dict={}, #dict of spells and their level
                 temporary_effects: dict={}, #dict of temporary effects and value
                ) -> None:
        self.name = name
        self.position = position
        self.level = level
        self.level_max = level_max
        self.xp = xp
        self.xp_max = xp_max
        if self.level > 1: self.xp_max = self.xp_max * (1.5 * (self.level-1)) #+50% xp_max per level
        self.strength = strength + level-1 #+1 str per level
        self.dexterity = dexterity + level-1 #+1 dex per level
        self.magic = magic + level-1 #+1 mag per level
        self.vitality = vitality + level-1 #+1 vit per level
        self.luck = luck
        self.armor = level // 5 + dexterity // 10 #+1 arm per 5 levels + 1% every 10 dex points
        self.resist_magic = 0 + magic // 10 #+1 res per 10 mag points
        self.critical = 3 + dexterity // 10 #3% + 1% crit every 10 dex points
        self.block = 0
        self.health = round(vitality * 5 + (vitality * 0.25 * (level - 1))) #+5 per vitality + //4 per level
        self.health_max = self.health
        self.mana = round(magic * 5 + (magic * 0.25 * (level - 1))) #+5 per magic + //4 per level
        self.mana_max = self.mana
        self.weapon = weapon
        self.offhand = offhand
        self.helmet = helmet
        self.body_armor = body_armor
        self.gloves = gloves
        self.belt = belt
        self.boots = boots
        self.gold = gold
        self.inventory = inventory
        self.spell_book = spell_book
        self.temporary_effects = temporary_effects
        self.damage = self.strength + self.weapon.damage

    def learn_spell(self, stdscr, spell) -> None:
        if spell in self.spell_book:
            cons_print(stdscr, f"{self.name} already knows {spell.name} !")
        else:
            self.spell_book[spell] = 0  # Ajoutez cette ligne
        self.spell_book[spell] += 1
        cons_print(stdscr, f"{self.name} has learned {spell.name} !", 14)
        return self
    
    def forget_spell(self, stdscr, spell) -> None:
        if spell in self.spell_book:
            if self.spell_book[spell] >= 1:self.spell_book[spell] -= 1
            if self.spell_book[spell] <= 0:del self.spell_book[spell]
            cons_print(stdscr, f"{self.name} has forgotten {spell.name} !")
        return self
    
    def spell_level_up(self, stdscr, spell) -> None:
        if spell in self.spell_book:
            self.spell_book[spell] += 1
            spell.level += 1
            spell.mana_cost *= 1.5
            spell.mana_cost = round(spell.mana_cost)
            for effect, value in spell.effects.items():
                spell.effects[effect] *= 1.5
                spell.effects[effect] = round(spell.effects[effect])
            cons_print(stdscr, f"{self.name} has leveled up {spell.name} !")
        else:
            self.learn_spell(stdscr, spell)
    
    def cast_spell(self, stdscr, target, spell, br1, br2) -> None:
        if spell.name == "Firebolt" and self.mana >= spell.mana_cost:
            cons_print(stdscr, f"{self.name} casted {spell.name} level {spell.level} !", 14)
        elif spell.name == "Ice Armor" and self.mana >= spell.mana_cost:
            cons_print(stdscr, f"{self.name} casted {spell.name} level {spell.level} !", 14)
        elif spell.name == "Heal" and self.mana >= spell.mana_cost:
            cons_print(stdscr, f"{self.name} casted {spell.name} level {spell.level} !", 14)
        else:
            pygame.mixer.Sound('Sounds/error.wav').play()
            cons_print(stdscr, f"{self.name} doesn't have enough mana to cast {spell.name} !", 9)
            return False
        self.mana -= spell.mana_cost
        cons_print(stdscr, f"{self.name} has {self.mana} mana left !", 14)
        bars_refresh(stdscr, br1, br2)
        for k, v in spell.effects.items():
            if k == 'magic_damage':
                damage = randint(int(v*0.85), int(v*1.15)) + self.magic
                damage = damage * (1 + ((self.level - target.level) * 0.05))
                damage = damage * (1 - 0.05 * self.resist_magic)
                if "resist_magic" in target.temporary_effects:
                    damage = damage * (1 - 0.05 * target.temporary_effects['resist_magic'])
                target.health -= round(damage)
                bars_refresh(stdscr, br1, br2)
                cons_print(stdscr, f"{self.name} did {round(damage)} magic damage to {target.name}.", 14)
                play_hit()
            if k == 'damage':
                damage = randint(int(v*0.85), int(v*1.15)) + self.magic
                damage = damage * (1 + ((self.level - target.level) * 0.05))
                damage = damage - target.armor
                if "armor" in target.temporary_effects:
                    damage = damage - target.temporary_effects['armor']
                target.health -= round(damage)
                bars_refresh(stdscr, br1, br2)
                cons_print(stdscr, f"{self.name} did {round(damage)} plysical damage to {target.name}.", 14)
            if k == 'resist_magic':
                self.temporary_effects['resist_magic'] = v + round(self.magic * 0.10)
                cons_print(stdscr, f"{self.name} got +{v} resist magic until the end of the fight !", 14)
            if k == 'armor':
                self.temporary_effects['armor'] = v + round(self.vitality * 0.10)
                cons_print(stdscr, f"{self.name} got +{v} armor until the end of the fight !", 14)
            if k == 'heal':
                v = randint(int(v*0.85), int(v*1.15))
                v = v + self.magic
                self.health += v
                if self.health > self.health_max:self.health = self.health_max
                cons_print(stdscr, f"{self.name} healed himself for {v} health !", 14)
        bars_refresh(stdscr, br1, br2)
        pygame.time.delay(750)
        if target.is_alive(stdscr) == False:
            cons_clean(stdscr)
            cons_print(stdscr, f"{target.name} is dead !", bold=True, reverse=True)
            pygame.mixer.Sound('Sounds/dead.wav').play()
            self.temporary_effects.clear()
            target.temporary_effects.clear()
            pygame.time.delay(500)
            if isinstance(target, Enemy):    
                target.give_xp(stdscr, self)
                target.drop(stdscr, self)
            elif isinstance(target, Hero):
                cons_print(stdscr, f"Game Over !", bold=True, reverse=True)
                pygame.mixer_music.stop()
                target.game_over(stdscr)  
                return False  
        return True


    def attack(self, stdscr, target, brefresh1, brefresh2) -> None: 
        damage = 0
        if isinstance(self.weapon, Bow):
            if self.name != 'Eidknab':
                pass
            else:
                try:
                    if self.offhand.quantity > 0:
                        self.offhand.quantity -= 1
                        cons_print(stdscr, f"{self.name} shot an arrow ! {self.offhand.quantity} arrows left")
                    else:
                        cons_print(stdscr, f"{self.name} has no arrows left, you have to fight with your hands !")
                        self.unequip(stdscr, self.weapon)
                        self.offhand = no_offhand
                except:
                    cons_print(stdscr, f"{self.name} has no arrows left, you have to fight with your hands !")
                    self.unequip(stdscr, self.weapon)
                    self.offhand = no_offhand
        if isinstance(target.offhand, Shield) or target.block > 0: #shield block
            if randint(1, 100) <= (target.block - (self.level-target.level)*2):
                cons_print(stdscr, f"{target.name} blocked the attack !", color=9)
                pygame.mixer.Sound('Sounds/block.wav').play()
                damage = 0
                pygame.time.delay(750)
                return
        damage = damage * (1 + ((self.level - target.level) * 0.05)) #+- 5% damage per level difference
        if randint(1, 100) <= (self.critical + (self.level-target.level)*5): #critical hit
            cons_print(stdscr, f"{self.name} did a Critical Hit !", color=5)
            damage *= 1.33 #+33% damage
        damage = randint(int(self.damage*0.85), int(self.damage*1.15))
        damage = damage - target.armor #armor reduction
        if "armor" in self.temporary_effects:
            damage = damage - self.temporary_effects['armor']
        target.health -= round(damage) #apply damage
        target.health = max(target.health, 0) #health cannot be negative
        bars_refresh(stdscr, brefresh1, brefresh2)
        cons_print(stdscr, f"{self.name} did {round(damage)} damage to {target.name}.")
        play_hit()
        pygame.time.delay(750)
        if target.is_alive(stdscr) == False:
            cons_clean(stdscr)
            cons_print(stdscr, f"{target.name} is dead !", bold=True, reverse=True)
            pygame.mixer.Sound('Sounds/dead.wav').play()
            self.temporary_effects.clear()
            target.temporary_effects.clear()
            pygame.time.delay(500)
            if isinstance(target, Enemy):    
                target.give_xp(stdscr, self)
                target.drop(stdscr, self)
            elif isinstance(target, Hero):
                cons_print(stdscr, f"Game Over !", bold=True, reverse=True)
                pygame.mixer_music.stop()
                target.game_over(stdscr)  
                return False          
        
    def is_alive(self, stdscr) -> bool:
        if self.health > 0:
            return True
        else:
            return False
        
    def equip(self, stdscr, item) -> None:
        if isinstance(item, Weapon):
            if self.weapon == hands:
                self.damage -= 2
            if self.weapon != hands:
                self.unequip(stdscr, self.weapon)
            self.weapon = item
            self.damage += self.weapon.damage
            cons_print(stdscr, f"{self.name} has equipped {self.weapon.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        elif isinstance(item, Offhand):
            if self.offhand != no_offhand:
                self.unequip(stdscr, self.offhand)
            self.offhand = item
            if isinstance(self.offhand, Shield):
                self.armor += self.offhand.armor
                self.block += self.offhand.block
            if isinstance(self.offhand, Arrow):
                self.damage += self.offhand.damage
            cons_print(stdscr, f"{self.name} has equipped {self.offhand.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        elif isinstance(item, Helmet):
            self.helmet = item
            for effect, value in self.helmet.effects.items():
                if hasattr(self, effect):
                    setattr(self, effect, getattr(self, effect) + value)
            cons_print(stdscr, f"{self.name} has equipped {self.helmet.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        elif isinstance(item, BodyArmor):
            self.body_armor = item
            for effect, value in self.body_armor.effects.items():
                if hasattr(self, effect):
                    setattr(self, effect, getattr(self, effect) + value)
            cons_print(stdscr, f"{self.name} has equipped {self.body_armor.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        elif isinstance(item, Gloves):
            self.gloves = item
            for effect, value in self.gloves.effects.items():
                if hasattr(self, effect):
                    setattr(self, effect, getattr(self, effect) + value)
            cons_print(stdscr, f"{self.name} has equipped {self.gloves.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        elif isinstance(item, Belt):
            self.belt = item
            for effect, value in self.belt.effects.items():
                if hasattr(self, effect):
                    setattr(self, effect, getattr(self, effect) + value)
            cons_print(stdscr, f"{self.name} has equipped {self.belt.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        elif isinstance(item, Boots):
            self.boots = item
            for effect, value in self.boots.effects.items():
                if hasattr(self, effect):
                    setattr(self, effect, getattr(self, effect) + value)
            cons_print(stdscr, f"{self.name} has equipped {self.boots.name} !", bold=True)
            pygame.mixer.Sound('Sounds/equip.wav').play()
        self.health_max = round(self.vitality * 5 + (self.vitality * 0.25 * (self.level - 1)))
        self.mana_max = round(self.magic * 5 + (self.magic * 0.25 * (self.level - 1)))
        self.health_bar.draw(stdscr, 90, 1)
        self.mana_bar.draw(stdscr, 90, 2)
        return self
    
    def unequip(self, stdscr, item) -> None:
        if isinstance(item, Weapon):
            if self.weapon == hands:
                cons_print(stdscr, f"{self.name} has no weapon to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.weapon.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                self.damage -= self.weapon.damage
                self.weapon = hands
                self.damage += self.weapon.damage
                self.put_in_inventory(stdscr, item)         
        if isinstance(item, Offhand):
            if self.offhand == no_offhand:
                cons_print(stdscr, f"{self.name} has no offhand to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.offhand.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                if isinstance(self.offhand, Shield):
                    self.armor -= self.offhand.armor
                    self.block -= self.offhand.block
                if isinstance(self.offhand, Arrow):
                    self.damage -= self.offhand.damage
                self.offhand = no_offhand
                self.put_in_inventory(stdscr, item)
        if isinstance(item, Helmet):
            if self.helmet == no_helmet:
                cons_print(stdscr, f"{self.name} has no helmet to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.helmet.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                for effect, value in self.helmet.effects.items():
                    if hasattr(self, effect):
                        setattr(self, effect, getattr(self, effect) - value)
                self.helmet = no_helmet
                self.put_in_inventory(stdscr, item)
        if isinstance(item, BodyArmor):
            if self.body_armor == no_body_armor:
                cons_print(stdscr, f"{self.name} has no body armor to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.body_armor.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                for effect, value in self.body_armor.effects.items():
                    if hasattr(self, effect):
                        setattr(self, effect, getattr(self, effect) - value)
                self.body_armor = no_body_armor
                self.put_in_inventory(stdscr, item)
        if isinstance(item, Gloves):
            if self.gloves == no_gloves:
                cons_print(stdscr, f"{self.name} has no gloves to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.gloves.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                for effect, value in self.gloves.effects.items():
                    if hasattr(self, effect):
                        setattr(self, effect, getattr(self, effect) - value)
                self.gloves = no_gloves
                self.put_in_inventory(stdscr, item)
        if isinstance(item, Belt):
            if self.belt == no_belt:
                cons_print(stdscr, f"{self.name} has no belt to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.belt.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                for effect, value in self.belt.effects.items():
                    if hasattr(self, effect):
                        setattr(self, effect, getattr(self, effect) - value)
                self.belt = no_belt
                self.put_in_inventory(stdscr, item)
        if isinstance(item, Boots):
            if self.boots == no_boots:
                cons_print(stdscr, f"{self.name} has no boots to unequip !")
                pygame.mixer.Sound('Sounds/error.wav').play()
            else:
                cons_print(stdscr, f"{self.name} has unequipped {self.boots.name} !")
                pygame.mixer.Sound('Sounds/unequip.wav').play()
                for effect, value in self.boots.effects.items():
                    if hasattr(self, effect):
                        setattr(self, effect, getattr(self, effect) - value)
                self.boots = no_boots
                self.put_in_inventory(stdscr, item)
        return self
                
    def equip_display(self, stdscr) -> None:
        print(f"{self.name}'s equipment:")
        if self.weapon != None: cons_print(stdscr, f"Weapon: {self.weapon.name}")
        if self.offhand != None: cons_print(stdscr, f"Offhand: {self.offhand.name}")
        if self.helmet != None: cons_print(stdscr, f"Helmet: {self.helmet.name}")
        if self.body_armor != None: cons_print(stdscr, f"Body Armor: {self.body_armor.name}")
        if self.gloves != None: cons_print(stdscr, f"Gloves: {self.gloves.name}")
        if self.belt != None: cons_print(stdscr, f"Belt: {self.belt.name}")
        if self.boots != None: cons_print(stdscr, f"Boots: {self.boots.name}")
        return self

    def put_in_inventory(self, stdscr, item, quantity=1) -> None:
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        cons_print(stdscr, f"{self.name} has put x{quantity} {item.name} in his inventory !", 28)
        return self
        
    def put_out_inventory(self, stdscr, item) -> None:
        if item in self.inventory:
            if self.inventory[item] >= 1:self.inventory[item] -= 1
            if self.inventory[item] <= 0:del self.inventory[item]
            cons_print(stdscr, f"{self.name} has put out {item.name} from his inventory !", 28)
        return self

    def show_inventory(self, stdscr) -> None:
        width = 31
        height = 12
        stdscr.addstr(1, 1, "┌" + "─" * (width-2) + "┐" + "┌" + "─" * (width-2) + "┐", curses.color_pair(29))
        for i in range(1, height):
            stdscr.addstr(i+1, 1, "│" + " " * (width-2) + "│", curses.color_pair(29))
        for i in range(1, height):
            stdscr.addstr(i+1, width+1, "│" + " " * (width-2) + "│", curses.color_pair(29))
        stdscr.addstr(12,1, "└" + "─" * (width-2) + "┘" + "└" + "─" * (width-2) + "┘", curses.color_pair(29))
        stdscr.addstr(1, width//2-len("Inventory")//2+1, "Inventory", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(1, width+width//2-len("Equiped")//2+1, "Equiped", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(height+1, 4, "┌─────────Help─────────┐",curses.color_pair(28))
        stdscr.addstr(height+2, 4, "│ '←↑↓→' to Navigate   │",curses.color_pair(28))
        stdscr.addstr(height+3, 4, "│ 'd' to Drop          │",curses.color_pair(28))
        stdscr.addstr(height+4, 4, "│ 'Enter' to Equip/Use │",curses.color_pair(28))
        stdscr.addstr(height+5, 4, "└──────────────────────┘",curses.color_pair(28))

        stdscr.addstr(2, width, " →", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(3, width, "← ", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(2, width+3, f"{self.weapon.name} +{self.weapon.damage}dmg", curses.color_pair(29))
        stdscr.addstr(3, width+3, f"{self.offhand.name} {self.offhand.description}", curses.color_pair(29))
        stdscr.addstr(4, width+3, f"{self.helmet.name} {self.helmet.description}", curses.color_pair(29))
        stdscr.addstr(5, width+3, f"{self.body_armor.name} {self.body_armor.description}", curses.color_pair(29))
        stdscr.addstr(6, width+3, f"{self.gloves.name} {self.gloves.description}", curses.color_pair(29))
        stdscr.addstr(7, width+3, f"{self.belt.name} {self.belt.description}", curses.color_pair(29))
        stdscr.addstr(8, width+3, f"{self.boots.name} {self.boots.description}", curses.color_pair(29))
        select = [0,0]
        refresh = True
        while True:
            if refresh:
                for y in range(2, height):
                    stdscr.addstr(y, 3, " " * (width-3), curses.color_pair(29))
                    stdscr.addstr(y, width+3, " " * (width-3), curses.color_pair(29))
                inventory_list = [f"{item.name} x{quantity}" for item, quantity in self.inventory.items()]
                refresh = False
                # select[0] = 0
                attribute_frame = Frame(18,14,64,5, title="Attributes", body=[(f"Strenght: {self.strength}"), (f"Dexterity: {self.dexterity}"), (f"Magic: {self.magic}"), (f"Vitality: {self.vitality}"),  (f"Luck: {self.luck}"), (""), (f"Damage: {self.damage}"), (f"% Crit: {self.critical}"), (""), (f"Armor: {self.armor}"), (f"% Block: {self.block}"), (f"Res. Magic: {self.resist_magic}")])
                attribute_frame.draw(stdscr)   
                equipment_frame = Frame(32,14,82,5, title="Equipment", body=[(f"Weapon:  {self.weapon.name}"), (f"         {self.weapon.description}"), (f"Offhand: {self.offhand.name}"), (f"         {self.offhand.description}"), (f"{self.helmet.name}: {self.helmet.description}"), (f"{self.body_armor.name}: {self.body_armor.description}"), (f"{self.gloves.name}: {self.gloves.description}"), (f"{self.belt.name}: {self.belt.description}"), (f"{self.boots.name}: {self.boots.description}"), (""), (f"Gold: {self.gold}")])
                equipment_frame.draw(stdscr)
            for i, content in enumerate(inventory_list):
                stdscr.addstr(i+2, 3, str(content), curses.color_pair(29))
                if select == [i,0]:stdscr.addstr(i+2, 3, str(inventory_list[i]), curses.color_pair(29) | curses.A_REVERSE)
            if select != [0,1]:stdscr.addstr(2, width+3, f"{self.weapon.name} +{self.weapon.damage}dmg", curses.color_pair(29))
            else:stdscr.addstr(2, width+3, f"{self.weapon.name} +{self.weapon.damage}dmg", curses.color_pair(29) | curses.A_REVERSE)
            if select != [1,1]:stdscr.addstr(3, width+3, f"{self.offhand.name} {self.offhand.description}", curses.color_pair(29))
            else:stdscr.addstr(3, width+3, f"{self.offhand.name} {self.offhand.description}", curses.color_pair(29) | curses.A_REVERSE)
            if select != [2,1]:stdscr.addstr(4, width+3, f"{self.helmet.name} {self.helmet.description}", curses.color_pair(29))
            else:stdscr.addstr(4, width+3, f"{self.helmet.name} {self.helmet.description}", curses.color_pair(29) | curses.A_REVERSE)
            if select != [3,1]:stdscr.addstr(5, width+3, f"{self.body_armor.name} {self.body_armor.description}", curses.color_pair(29))
            else:stdscr.addstr(5, width+3, f"{self.body_armor.name} {self.body_armor.description}", curses.color_pair(29) | curses.A_REVERSE)
            if select != [4,1]:stdscr.addstr(6, width+3, f"{self.gloves.name} {self.gloves.description}", curses.color_pair(29))
            else:stdscr.addstr(6, width+3, f"{self.gloves.name} {self.gloves.description}", curses.color_pair(29) | curses.A_REVERSE)
            if select != [5,1]:stdscr.addstr(7, width+3, f"{self.belt.name} {self.belt.description}", curses.color_pair(29))
            else:stdscr.addstr(7, width+3, f"{self.belt.name} {self.belt.description}", curses.color_pair(29) | curses.A_REVERSE)
            if select != [6,1]:stdscr.addstr(8, width+3, f"{self.boots.name} {self.boots.description}", curses.color_pair(29))
            else:stdscr.addstr(8, width+3, f"{self.boots.name} {self.boots.description}", curses.color_pair(29) | curses.A_REVERSE)

            key = stdscr.getch()
            if key == curses.KEY_UP and select[0]>0:select[0] -= 1; pygame.mixer.Sound('Sounds/select.wav').play()
            elif key == curses.KEY_DOWN and select[0]<len(inventory_list)-1 and select[1] == 0:select[0] += 1; pygame.mixer.Sound('Sounds/select.wav').play()
            elif key == curses.KEY_DOWN and select[1]==1 and select[0]<6:select[0] += 1; pygame.mixer.Sound('Sounds/select.wav').play()
            elif key == curses.KEY_LEFT and select[1]>0 and select[0]<len(inventory_list):select[1] -= 1; pygame.mixer.Sound('Sounds/select.wav').play()
            elif key == curses.KEY_RIGHT and select[1]<1 and select[0]<7:select[1] += 1; pygame.mixer.Sound('Sounds/select.wav').play()

            elif key == ord("i") or key == ord('I'):return
            elif key == ord('q') or key == ord('Q'):return
            elif key == curses.KEY_ENTER or key == ord('\n'):
                if select == [0,1]:self.unequip(stdscr, self.weapon);refresh=True; select = [1,1]
                elif select == [1,1]:self.unequip(stdscr, self.offhand);refresh=True; select = [2,1]
                elif select == [2,1]:self.unequip(stdscr, self.helmet);refresh=True ; select = [3,1]
                elif select == [3,1]:self.unequip(stdscr, self.body_armor);refresh=True ; select = [4,1]
                elif select == [4,1]:self.unequip(stdscr, self.gloves);refresh=True ; select = [5,1]
                elif select == [5,1]:self.unequip(stdscr, self.belt);refresh=True ; select = [6,1]
                elif select == [6,1]:self.unequip(stdscr, self.boots);refresh=True ; select = [0,1]

                for i, item in enumerate(inventory_list):
                    if select == [i,0]:self.use(stdscr, list(self.inventory.keys())[i]);refresh=True
            elif key == ord('d') or key == ord('D'):
                for i, item in enumerate(inventory_list):
                    if select == [i,0]:self.drop(stdscr, list(self.inventory.keys())[i]);refresh=True
            elif key == ord(' '):
                cons_clean(stdscr)

    def use(self, stdscr, item) -> None:
        if isinstance(item, Potion):
            if self.inventory[item] >= 1:
                self.inventory[item] -= 1
                self.health += item.health_restore
                if self.health > self.health_max:self.health = self.health_max
                self.mana += item.mana_restore
                if self.mana > self.mana_max:self.mana = self.mana_max
                cons_print(stdscr, f"{self.name} has used {item.name} !", )
                pygame.mixer.Sound('Sounds/equip.wav').play()
            if self.inventory[item] <= 0 :del self.inventory[item]
        elif isinstance(item, Weapon):
            if item != self.weapon:
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.weapon:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        elif isinstance(item, Offhand):
            if item != self.offhand:
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.offhand:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        elif isinstance(item, Helmet):
            if item != self.helmet:
                if self.helmet != no_helmet:
                    self.unequip(stdscr, self.helmet)
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.helmet:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        elif isinstance(item, BodyArmor):
            if item != self.body_armor:
                if self.body_armor != no_body_armor:
                    self.unequip(stdscr, self.body_armor)
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.body_armor:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        elif isinstance(item, Gloves):
            if item != self.gloves:
                if self.gloves != no_gloves:
                    self.unequip(stdscr, self.gloves)
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.gloves:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        elif isinstance(item, Belt):
            if item != self.belt:
                if self.belt != no_belt:
                    self.unequip(stdscr, self.belt)
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.belt:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        elif isinstance(item, Boots):
            if item != self.boots:
                if self.boots != no_boots:
                    self.unequip(stdscr, self.boots)
                self.put_out_inventory(stdscr, item)
                self.equip(stdscr, item)
            elif item == self.boots:
                cons_print(stdscr, f"{self.name} has already equipped {item.name} !")
                pygame.mixer.Sound('Sounds/error.wav').play()
        self.health_bar.draw(stdscr, 90, 1)
        self.mana_bar.draw(stdscr, 90, 2)

# Sub Class Setup
class Hero(Character):
    def __init__(self, 
                 name: str="Player", 
                 position: list[int, int]=[0,0],
                 level: int=1,
                 level_max: int=50,
                 xp: int=0,
                 xp_max: int=100,
                 strength: int=30,
                 dexterity: int=20,
                 magic: int=10,
                 vitality: int=20,
                 luck: int=1,
                 weapon: object=hands,
                 offhand: object=no_offhand,
                 helmet: object=no_helmet,
                 body_armor: object=no_body_armor,
                 gloves: object=no_gloves,
                 belt: object=no_belt,
                 boots: object=no_boots,
                 gold: int=100,
                 is_caster: bool=True,
                 inventory: dict={}, #dict of items and their quantity
                 spell_book: dict={}, #dict of spells and their level
                 temporary_effects: dict={} #dict of temporary effects and their duration
                ) -> None:
        super().__init__(name, position, level, level_max, xp, xp_max, strength, dexterity, magic, vitality, luck, weapon, offhand, helmet, body_armor, gloves, belt, boots, gold, inventory, spell_book, temporary_effects)
        self.is_caster = is_caster
        self.health_bar = HealthBar(self)
        self.mana_bar = ManaBar(self)
        self.xp_bar = XpBar(self,)

    def spawn(self, stdscr, game_map):
        cons_print(stdscr, f"{self.name} level {self.level} has spawned !", 19)
        game_map.map_data[self.position[1]][self.position[0]] = player

    def game_over(self, stdscr):
        clear_area(stdscr, 1, 1, 24, 62)
        stdscr.addstr(7,22, f"         ┌───┐", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(8,22, f"    '-.  │ ▀ │  .-'", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(9,22, f"     ┌───┘ + └───┐", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(10,22, f"     │+   RIP   +│", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(11,22, f"     └───┐   ┌───┘", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(12,22, f"         │   │", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(13,22, f"         │   │", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(14,22, f"         │▒ ▒│", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(15,22, f"      _.-│▒▄▒│-._", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(16,22, f"  .-'`  G A M E  `'-.", curses.A_BOLD | curses.color_pair(29))
        stdscr.addstr(17,22, f".'      O V E R      '.", curses.A_BOLD | curses.color_pair(29))
        select = stdscr.getch()
        return False

    def move(self, stdscr, player1, game_map, x, y):
        global memory
        try:memory
        except:memory = grass;game_map.map_data[self.position[1]][self.position[0]] = memory

        if 0 <= self.position[1]+y < game_map.height and 0 <= self.position[0]+x < game_map.width:
            game_map.map_data[self.position[1]][self.position[0]] = memory
            if game_map.map_data[self.position[1]+y][self.position[0]+x] == grass:
                memory = grass
                pygame.mixer.Sound('Sounds/grass.wav').play()
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == forest:
                memory = forest
                pygame.mixer.Sound('Sounds/forest.wav').play()
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == bridge:
                memory = bridge
                pygame.mixer.Sound('Sounds/bridge.wav').play()
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == chest:
                memory = grass
                cons_clean(stdscr)
                cons_print(stdscr, f"{self.name} has found a chest !", 7, bold=True)
                self.find_chest(stdscr, roll_number=(2+self.luck))
                pygame.mixer.Sound('Sounds/gold.wav').play()
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == super_chest:
                memory = grass
                cons_clean(stdscr)
                cons_print(stdscr, f"{self.name} has found a super chest !", 20, bold=True)
                self.find_chest(stdscr, roll_number=(3+self.luck*2))
                pygame.mixer.Sound('Sounds/gold.wav').play()
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == zombie:
                memory = grass
                monster = Enemy(name="Zombie", level=max(1, self.level + choice([-2, 2])), strength=20, dexterity=20, magic=1, vitality=20)
                monster.drop_maker(stdscr, 1+player1.luck)
                monster.gold += monster.gold * player1.luck // 10
                cons_clean(stdscr)
                cons_print(stdscr, f"A 'Zombie' is heading in your direction ! Hurgh...", 12, bold=True)
                fight_screen(stdscr, player1, monster)
                if monster.is_alive(stdscr) == True:
                    memory = zombie
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == wolf:
                memory = grass
                monster = Enemy(name="Wolf", level=max(1, self.level + choice([-2, 2])), strength=20, dexterity=25, magic=1, vitality=20)
                monster.drop_maker(stdscr, 1+player1.luck)
                monster.gold += monster.gold * player1.luck // 10
                cons_clean(stdscr)
                cons_print(stdscr, f"A 'wolf' level {monster.level} is running at you ! Ghrrr...", 2, bold=True)
                fight_screen(stdscr, player1, monster)
                if monster.is_alive(stdscr) == True:
                    memory = wolf
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == skeleton:
                memory = grass
                monster = Enemy(name="Skeleton", level=max(1, self.level + choice([-2, 2])), strength=15, dexterity=20, magic=1, vitality=20)
                monster.block = 20
                monster.drop_maker(stdscr, 1+player1.luck)
                monster.gold += monster.gold * player1.luck // 10
                cons_clean(stdscr)
                cons_print(stdscr, f"A 'Skeleton' comes out of the ground ! ", 25, bold=True)
                fight_screen(stdscr, player1, monster)
                if monster.is_alive(stdscr) == True:
                    memory = skeleton
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == boss:
                memory = grass
                monster = Enemy(name="Boss", level=8, strength=30, dexterity=30, magic=10, vitality=30, is_caster=True)
                monster.equip(stdscr, great_sword)
                monster.equip(stdscr, tower_shield)
                monster.equip(stdscr, goldwrap)
                monster.drop_maker(stdscr, 2+player1.luck)
                monster.gold += monster.gold * player1.luck // 10
                monster.health = monster.health_max
                monster.health = 10
                monster.mana = monster.mana_max
                monster.learn_spell(stdscr, firebolt)
                monster.learn_spell(stdscr, icearmor)
                monster.learn_spell(stdscr, heal)
                cons_clean(stdscr)
                cons_print(stdscr, f"The Master of the mountain is rushing at you ! ", 20, bold=True)
                fight_screen(stdscr, player1, monster)
                if monster.is_alive(stdscr) == True:
                    memory = boss
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == water:
                cons_print(stdscr, f"I should find a bridge, the river seems dangerous to cross...", 8)
                game_map.map_data[self.position[1]][self.position[0]] = player
                pygame.mixer.Sound('Sounds/water.wav').play()
                return True
            elif game_map.map_data[self.position[1]+y][self.position[0]+x] == mountains:
                cons_print(stdscr, f"There is nothing to do in the mountains right now...", 8)
                game_map.map_data[self.position[1]][self.position[0]] = player
                return True
            else:
                game_map.map_data[self.position[1]][self.position[0]] = player
                return True
            game_map.map_data[self.position[1]+y][self.position[0]+x] = player
            self.position[0] += x
            self.position[1] += y
            return True
        return True
                                 
    def drop(self, stdscr, item) -> None:
        if item in self.inventory:
            if self.inventory[item] >= 1:self.inventory[item] -= 1
            if self.inventory[item] <= 0:del self.inventory[item]; pygame.mixer.Sound('Sounds/dead.wav').play()

            cons_print(stdscr, f"{self.name} has drop {item.name} from his inventory !", 28)
        return self


    def level_up(self, stdscr) -> bool:
        if self.level < self.level_max and self.xp >= self.xp_max:
            pygame.mixer.Sound('Sounds/level_up.wav').play()
            self.level += 1
            self.xp_max = self.xp_max * (1.5 * (self.level-1))
            self.xp_max = round(self.xp_max)
            self.xp = 0
            self.strength = self.strength + self.level-1 #+1 str per level
            self.dexterity = self.dexterity + self.level-1 #+1 dex per level
            self.magic = self.magic + self.level-1 #+1 mag per level
            self.vitality = self.vitality + self.level-1 #+1 vit per level
            self.armor = self.level // 5 + self.dexterity // 10 #+1 arm per 5 levels + 1% every 10 dex points
            self.critical = 3 + self.dexterity // 10 #5% + 1% crit every 10 dex points
            self.health = round(self.vitality * 5 + (self.vitality * 0.25 * (self.level - 1))) #+5 per vitality + //4 per level
            self.health_max = self.health
            self.mana = round(self.magic * 5 + (self.magic * 0.25 * (self.level - 1))) #+5 per magic + //4 per level
            self.mana_max = self.mana
            self.health_bar.update()
            self.mana_bar.update()
            self.xp_bar.update()
            cons_print(stdscr, f"{self.name} has leveled up !", color=18)
            return True
        else: return False

    def find_chest(self, stdscr, roll_number=2) ->None:
        common_list = [short_sword, long_sword, small_shield, short_bow, sandals, silk_gloves, leather_gloves, cap, cloak_armor, leather_armor, sash, spiderweb_sash] #list of common items
        rare_list = [chain_mail, plates_armor, leather_boots, heavy_boots, chain_gloves, gauntlets, skull_cap, medium_shield, tower_shield, broad_sword, claymore, long_bow, battle_bow, leather_belt] #rare items
        epic_list = [great_sword, war_bow, goldwrap] #epic items
        consomable_list = [small_life_potion, small_mana_potion, arrow] #list of consomable items
        better_consomable_list = [medium_life_potion, medium_life_potion, medium_mana_potion, large_life_potion, large_mana_potion] #list of better consomable items
        spell_list = [firebolt, icearmor, heal]

        i = 0
        gold_finded = 0
        while i < roll_number:
            i += 1
            if roll_dice(100, 100, self.luck):
                item = choice(epic_list)
                cons_print(stdscr, f"{self.name} has found {item.name}, it's an epic item !", color=18, bold=True)
                self.put_in_inventory(stdscr, item, 1)
            elif roll_dice(100, 98, self.luck):
                item = choice(spell_list)
                self.spell_level_up(stdscr, item)
            elif roll_dice(100, 96, self.luck):
                item = choice(rare_list)
                cons_print(stdscr, f"{self.name} has found {item.name}, it's a rare item !", color=4, bold=True)
                self.put_in_inventory(stdscr, item, 1)
            elif roll_dice(100, 90, self.luck):
                item = choice(better_consomable_list)
                cons_print(stdscr, f"{self.name} has found {item.name} !", color=11)
                self.put_in_inventory(stdscr, item, 1)
            elif roll_dice(100, 85, self.luck):
                item = choice(common_list)
                cons_print(stdscr, f"{self.name} has found {item.name} !", color=11)
                self.put_in_inventory(stdscr, item, 1)
            elif roll_dice(100, 75, self.luck):
                item = choice(consomable_list)
                cons_print(stdscr, f"{self.name} has found {item.name} !", color=11)
                self.put_in_inventory(stdscr, item, 1)
            elif roll_dice(100, 40, self.luck):
                gold_finded += randint(1, (20*self.level))
            elif roll_dice(100, 20, self.luck):
                if i < 2:
                    cons_print(stdscr, f"The chest is empty !", color=29, reverse=True)
                i = roll_number
            elif roll_dice(100, 10, self.luck):
                cons_print(stdscr, f"A mechanical trap has been triggered !", color=1, bold=True)
                damage = randint(1, (10*self.level))
                self.health -= damage
                cons_print(stdscr, f"{self.name} has lost {damage} health !", color=1)
                self.health_bar.update()
                i = roll_number
        if gold_finded > 0:
                self.gold += gold_finded
                cons_print(stdscr, f"{self.name} has found {gold_finded} gold !", color=6)
            
            
class Enemy(Character):
    def __init__(self, 
                 name : str="Enemy", 
                 position : list[int, int]=[0,0],
                 level : int=1,
                 level_max : int=50,
                 xp : int=0,
                 xp_max : int=100,
                 strength : int=30,
                 dexterity : int=20,
                 magic : int=10,
                 vitality : int=20,
                 luck: int=0,
                 weapon : object=hands,
                 offhand : object=no_offhand,
                 helmet : object=no_helmet,
                 body_armor : object=no_body_armor,
                 gloves: object=no_gloves,
                 belt: object=no_belt,
                 boots: object=no_boots,
                 gold : int=randint(0, 9),
                 is_caster : bool=False, #False = will not cast spells and not have mana bar
                 inventory : dict={}, #dict of items and their quantity
                 spell_book : dict={}, #dict of spells and their level
                 temporary_effects : dict={} #dict of temporary effects and their duration
                ) -> None:
        super().__init__(name, position, level, level_max, xp, xp_max, strength, dexterity, magic, vitality, luck, weapon, offhand, helmet, body_armor, gloves, belt, boots, gold, inventory, spell_book, temporary_effects)
        self.gold = gold + (gold * level)
        self.is_caster = is_caster
        self.health_bar = HealthBar(self, color=1)
        self.mana_bar = ManaBar(self)
        
    def drop(self, stdscr, target) -> None:
        if self.gold > 0:
            cons_print(stdscr, f"{target.name} has gained {self.gold} gold !", color=6)
            target.gold += self.gold
            self.gold = 0
            pygame.mixer.Sound('Sounds/gold.wav').play()
        if self.weapon != hands:
            cons_print(stdscr, f"{self.name} has dropped {self.weapon.name} !")
            target.put_in_inventory(stdscr, self.weapon)
            self.weapon = hands
        if self.offhand != no_offhand:
            cons_print(stdscr, f"{self.name} has dropped {self.offhand.name} !")
            target.put_in_inventory(stdscr, self.offhand)
            self.offhand = no_offhand
        if self.helmet != no_helmet:
            cons_print(stdscr, f"{self.name} has dropped {self.helmet.name} !")
            target.put_in_inventory(stdscr, self.helmet)
            self.helmet = no_helmet
        if self.body_armor != no_body_armor:
            cons_print(stdscr, f"{self.name} has dropped {self.body_armor.name} !")
            target.put_in_inventory(stdscr, self.body_armor)
            self.body_armor = no_body_armor
        if self.gloves != no_gloves:
            cons_print(stdscr, f"{self.name} has dropped {self.gloves.name} !")
            target.put_in_inventory(stdscr, self.gloves)
            self.gloves = no_gloves
        if self.belt != no_belt:
            cons_print(stdscr, f"{self.name} has dropped {self.belt.name} !")
            target.put_in_inventory(stdscr, self.belt)
            self.belt = no_belt
        if self.boots != no_boots:
            cons_print(stdscr, f"{self.name} has dropped {self.boots.name} !")
            target.put_in_inventory(stdscr, self.boots)
            self.boots = no_boots
        for items in list(self.inventory.keys()):
            cons_print(stdscr, f"{self.name} has dropped {items.name} !")
            target.put_in_inventory(stdscr, items)
            del self.inventory[items]
            
    def give_xp(self, stdscr, target) -> None:
        xp_gained = self.xp_max * randint(15, 25) // 100
        xp_gained = xp_gained * (1 + ((self.level - target.level) * 0.25)) #+ 25% xp per level difference
        xp_gained = round(xp_gained)
        cons_print(stdscr, f"{target.name} has gained {xp_gained} experience !", color=5)
        target.xp += xp_gained
        target.xp_bar.update()
        if target.xp >= target.xp_max: 
            target.xp = target.xp_max
            pygame.time.delay(500)
            target.level_up(stdscr)

    def drop_maker(self, stdscr, roll_number=1) ->None:
        common_list = [short_sword, long_sword, small_shield, short_bow, sandals, silk_gloves, leather_gloves, cap, cloak_armor, leather_armor, sash, spiderweb_sash] #list of common items
        rare_list = [chain_mail, plates_armor, leather_boots, heavy_boots, chain_gloves, gauntlets, skull_cap, medium_shield, tower_shield, broad_sword, claymore, long_bow, battle_bow, leather_belt] #rare items
        epic_list = [great_sword, war_bow, goldwrap] #epic items
        consomable_list = [small_life_potion, small_life_potion, small_mana_potion, arrow] #list of consomable items
        better_consomable_list = [medium_life_potion, medium_life_potion, medium_mana_potion, large_life_potion, large_mana_potion] #list of better consomable items

        i = 0
        while i < roll_number:
            i += 1
            if roll_dice(100, 100):
                item = choice(epic_list)
                self.inventory={}
                if roll_dice(100, 50):
                    self.put_in_inventory(stdscr, item, 1)
                else:
                    self.equip(stdscr, item)
            elif roll_dice(100, 95):
                item = choice(rare_list)
                self.inventory={}
                if roll_dice(100, 50):
                    self.put_in_inventory(stdscr, item, 1)
                else:
                    self.equip(stdscr, item)
            elif roll_dice(100, 90):
                item = choice(better_consomable_list)
                self.put_in_inventory(stdscr, item, 1)
            elif roll_dice(100, 85):
                item = choice(common_list)
                self.inventory={}
                if roll_dice(100, 50):
                    self.put_in_inventory(stdscr, item, 1)
                else:
                    self.equip(stdscr, item)
            elif roll_dice(100, 75):
                item = choice(consomable_list)
                self.put_in_inventory(stdscr, item, 1)