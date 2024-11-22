class Helmet:
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
no_helmet = Helmet(name="Head",
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
cap = Helmet(name="Cap",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 0,
                    'armor': 1,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=5,
                description=f"+1arm")

skull_cap = Helmet(name="Skull Cap",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 0,
                    'armor': 2,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=15,
                description=f"+2arm")