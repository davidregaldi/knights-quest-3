class Boots:
    def __init__(self,
                 name: str="Feet",
                 effects: list={
                     'strength': 0,
                     'dexterity': 0,
                     'magic': 0,
                     'vitality': 0,
                     'damage': 0,
                     'critical': 0,
                     'armor': 0,
                     'block': 0,
                     'resist_magic': 0,
                     },
                 value: int=0,
                 description: str=f""
                 ) -> None:
        self.name = name
        self.effects = effects
        self.value = value
        self.description = description
        
# Items Creation
no_boots = Boots(name="Feet",
                     effects={
                          'strength': 0,
                          'dexterity': 0,
                          'magic': 0,
                          'vitality': 0,
                          'damage': 0,
                          'critical': 0,
                          'armor': 0,
                          'block': 0,
                          'resist_magic': 0,
                          },
                     value=0,
                     description=f"Empty"
                     )

sandals = Boots(name="Sandals",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 1,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 0,
                    'armor': 0,
                    'block': 0,
                    'resist_magic': 1,
                    },
                value=5,
                description=f"+1mag +1r.mag")

leather_boots = Boots(name="Leather Boots",
                effects={
                    'strength': 0,
                    'dexterity': 1,
                    'magic': 0,
                    'vitality': 1,
                    'damage': 0,
                    'critical': 0,
                    'armor': 1,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=5,
                description=f"+1dex +1vit")

heavy_boots = Boots(name="Heavy Boots",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 2,
                    'damage': 0,
                    'critical': 0,
                    'armor': 2,
                    'block': 0,
                    'resist_magic': 0,

                    },
                value=25,
                description=f"+2vit +2arm")