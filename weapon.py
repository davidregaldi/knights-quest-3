# Class Setup
class Weapon:
    def __init__(self,
                 name: str,
                 damage: int=2,
                 value: int=0,
                 description: str=""
                 ) -> None:
        self.name = name
        self.damage = damage
        self.value = value
        self.description = description
        
# Items Creation
hands = Weapon(name="Hands",
               damage=2,
               value=0)

short_sword = Weapon(name="Short Sword",
                     damage=5,
                     value=5,
                     description=f"+5dmg")
long_sword = Weapon(name="Long Sword",
                    damage=8,
                    value=25,
                    description=f"+8dmg")
broad_sword = Weapon(name="Broad Sword",
                     damage=12,
                     value=120,
                     description=f"+12dmg")
claymore = Weapon(name="Claymore",
                  damage=15,
                  value=480)
great_sword = Weapon(name="Great Sword",
                     damage=20,
                     value=1800,
                     description=f"+20dmg")

class Bow(Weapon):
    def __init__(self,
                 name: str,
                 damage: int=5,
                 value: int=0,
                 description: str=""
                 ) -> None:
        super().__init__(name, damage, value, description)

# Sub Items Creation
short_bow = Bow(name="Short Bow",
                damage=5,
                value=5,
                description=f"+5dmg")
long_bow = Bow(name="Long Bow",
               damage=10,
               value=55,
               description=f"+10dmg")
battle_bow = Bow(name="Battle Bow",
                 damage=15,
                 value=240,
                 description=f"+15dmg")
war_bow = Bow(name="War Bow",
              damage=20,
              value=2000,
              description=f"+20dmg")