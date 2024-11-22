class Spell:
    def __init__(self, 
                 name: str,
                 level: int,
                 mana_cost: int,
                 effects: list={
                     'magic_damage': 0,
                     'resist_magic': 0,
                     'damage': 0,
                     'armor': 0,
                     'heal': 0,
                 },
                 ):
        self.name = name
        self.level = level
        self.mana_cost = mana_cost
        self.effects = effects

    def __str__(self):
        effects_str = ', '.join(
            f'{k.replace("magic_", "Mag.").replace("damage", "Dmg").replace("resist_", "Res.").replace("armor", "Arm")}: {v}' 
            for k, v in self.effects.items()
        )
        return (f'{self.name} lvl: {self.level} Cost: {self.mana_cost} {effects_str}')

# Spells Creation
firebolt = Spell(name="Firebolt",
                    level=1,
                    mana_cost=15,
                    effects={
                        'magic_damage': 40,
                    }
                )
icearmor = Spell(name="Ice Armor",
                    level=1,
                    mana_cost=15,
                    effects={
                        'resist_magic': 4,
                        'armor': 2,
                    }
                )
heal = Spell(name="Heal",
                    level=1,
                    mana_cost=15,
                    effects={
                        'heal': 40,
                    }
                )


        