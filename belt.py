class Belt:
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
no_belt = Belt(name="Belt",
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

sash = Belt(name="Sash",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 1,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 0,
                    'armor': 0,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=5,
                description=f"+1mag")

spiderweb_sash = Belt(name="Spiderweb Sash",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 3,
                    'vitality': 0,
                    'damage': 0,
                    'critical': 0,
                    'armor': 1,
                    'block': 0,
                    'resist_magic': 2,
                    },
                value=5,
                description=f"+3mag +1arm +2r.mag")

leather_belt = Belt(name="Leather Belt",
                effects={
                    'strength': 1,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 1,
                    'damage': 0,
                    'critical': 0,
                    'armor': 1,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=5,
                description=f"+1str +1vit")

goldwrap = Belt(name="Goldwrap",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 2,
                    'damage': 0,
                    'critical': 0,
                    'armor': 0,
                    'block': 0,
                    'resist_magic': 0,
                    'luck': 2,
                    },
                value=25,
                description=f"+2vit +2luck")