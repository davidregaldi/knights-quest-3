# Class Setup
class Offhand:
    def __init__(self,
                 name: str,
                 value: int=0,
                 armor: int=0,
                 block: int=0,
                 description: str=""
                 ) -> None:
        self.name = name
        self.value = value
        self.armor = armor
        self.block = block
        self.description = description

        
# Sub Class Setup
class Shield(Offhand):
    def __init__(self,
                 name: str,
                 value: int=0,
                 armor: int=1,
                 block: int=1,
                 description: str="",
                 ) -> None:
        super().__init__(name, value, armor, block, description)

no_offhand = Shield(name="Offhand", value=0, armor=0, block=0, description="Empty")
        
small_shield = Shield(name="Small Shield",
                      value=5,
                      armor=1,
                      block=3,
                      description="+1arm +3blk")
medium_shield = Shield(name="Medium Shield",
                       value=25,
                       armor=2,
                       block=5,
                       description="+2arm +5blk")
tower_shield = Shield(name="Tower Shield",
                      value=120,
                      armor=3,
                      block=7,
                      description="+3arm +7blk")

class Arrow(Offhand):
    def __init__(self,
                 name: str="Arrow",
                 value: int=0,
                 armor: int=0,
                 block: int=0,
                 description: str="",
                 damage: int=3,
                 quantity: int=12,
                 special: str=""
                 ) -> None:
        super().__init__(name, value, armor, block, description)
        self.damage = damage
        self.quantity = quantity
        self.special = special
        
arrow = Arrow(description="3dmg")
fire_arrow = Arrow(name="Fire Arrow",
                     value=5,
                     damage=8,
                     quantity=16,
                     special="Fire")
cold_arrow = Arrow(name="Cold Arrow",
                   value=5,
                   damage=6,
                   quantity=16,
                   special="Cold")
poison_arrow = Arrow(name="Poison Arrow",
                     value=5,
                     damage=4,
                     quantity=16,
                     special="Poison")