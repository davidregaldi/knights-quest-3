# Imports
from random import randint

# Class Setup
class Potion:
    def __init__(self,
                 name: str,
                 value: int=20,
                 health_restore: int=0,
                 mana_restore: int=0,
                 ) -> None:
        self.name = name
        self.value = value
        self.health_restore = health_restore
        self.mana_restore = mana_restore

        
small_life_potion = Potion(name="Small Life Potion",
                            value=20,
                            health_restore=45,)
medium_life_potion = Potion(name="Medium Life Potion",
                            value=50,
                            health_restore=100,)
large_life_potion = Potion(name="Large Life Potion",
                            value=150,
                            health_restore=190,)
small_mana_potion = Potion(name="Small Mana Potion",
                            value=20,
                            mana_restore=35,)
medium_mana_potion = Potion(name="Medium Mana Potion",
                            value=50,
                            mana_restore=70,)
large_mana_potion = Potion(name="Large Mana Potion",
                            value=150,
                            mana_restore=150,)
