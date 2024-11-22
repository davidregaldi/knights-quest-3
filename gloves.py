class Gloves:
    def __init__(self,
                 name: str,
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
no_gloves = Gloves(name="Gloves",
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
silk_gloves = Gloves(name="Silk Gloves",
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
                value=50,
                description=f"+1mag +1r.mag")

leather_gloves = Gloves(name="Leather Gloves",
                effects={
                    'strength': 0,
                    'dexterity': 1,
                    'magic': 0,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 1,
                    'armor': 1,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=50,
                description=f"+1dex +1%Crit +1arm")

chain_gloves = Gloves(name="Chain Gloves",
                effects={
                    'strength': 1,
                    'dexterity': 1,
                    'magic': 0,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 0,
                    'armor': 2,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=50,
                description=f"+1str +1dex +2arm")

gauntlets = Gloves(name="Gauntlets",
                effects={
                    'strength': 2,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 1,
                    'damage': 0,
                    'critical': 0,
                    'armor': 3,
                    'block': 1,
                    'resist_magic': 0,
                    },
                value=50,
                description=f"+2str +1vit +3arm +1blk")