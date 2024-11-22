class BodyArmor:
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
no_body_armor = BodyArmor(name="Body",
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
cloak_armor = BodyArmor(name="Cloak",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 1,
                    'damage': 0,
                    'critical': 0,
                    'armor': 0,
                    'block': 0,
                    'resist_magic': 1,
                    },
                value=5,
                description=f"+1vit +1r.mag")

leather_armor = BodyArmor(name="Leather Armor",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 1,
                    'damage': 0,
                    'critical': 0,
                    'armor': 1,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=20,
                description=f"1vit +1arm")

chain_mail = BodyArmor(name="Chain Mail",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 1,
                    'damage': 0,
                    'critical': 0,
                    'armor': 2,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=80,
                description=f"+2vit +2arm")

plates_armor = BodyArmor(name="Plates Armor",
                effects={
                    'strength': 0,
                    'dexterity': 0,
                    'magic': 0,
                    'vitality': 3,
                    'damage': 0,
                    'critical': 0,
                    'armor': 3,
                    'block': 0,
                    'resist_magic': 0,
                    },
                value=240,
                description=f"+3vit +3arm")