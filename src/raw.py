# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Attack Types
###############################################################################

DummyAttack = {
'verb': 'BUG: dummy attack',
'ToHitBonus': 0,
'DiceNumber': 1,
'DiceValue': 1,
'DamageBonus': 0,
'DamageType': 'BLUNT',
'range': 1,
'flags': []
}

# TODO:
#  special effects
#  ranged
#  explosions / clouds
#
#  peck, lick, touch, slap

# Natural attacks:
Slam = {
'verb': 'slam&S',
'ToHitBonus': -2,
'DiceNumber': 1,
'DiceValue': 3,
'flags': ['NATURAL']
}

Punch = {
'verb': 'punch&ES',
'DiceNumber': 1,
'DiceValue': 2,
'flags': ['UNARMED', 'NATURAL']
}

Claw = {
'verb': 'claw&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH',
'flags': ['NATURAL']
}

LargeClaw = {
'verb': 'claw&S',
'DiceNumber': 2,
'DiceValue': 3,
'DamageType': 'SLASH',
'flags': ['NATURAL']
}

Bite = {
'verb': 'bite&S',
'DiceNumber': 1,
'DiceValue': 4,
'DamageType': 'PIERCE',
'flags': ['NATURAL']
}

Kick = {
'verb': 'kick&S',
'DiceNumber': 1,
'DiceValue': 5,
'flags': ['NATURAL']
}

Buffet = {
'verb': 'buffet&S',
'ToHitBonus': -1,
'DiceNumber': 2,
'DiceValue': 2,
'flags': ['NATURAL']
}

# Weapon attacks:
NonWeapon = {
'verb': 'bash&S',
'ToHitBonus': -2,
'DiceNumber': 1,
'DiceValue': 2
}

Club = {
'verb': 'club&S',
'DiceNumber': 1,
'DiceValue': 4,
'DamageBonus': 1
}

MaceAttack = {
'verb': 'smash&ES',
'DiceNumber': 2,
'DiceValue': 4
}

Hammer = {
'verb': 'crush&ES',
'DiceNumber': 3,
'DiceValue': 4
}

WoodStaff = {
'verb': 'strike&S',
'DiceNumber': 2,
'DiceValue': 2
}

KnifeAttack = {
'verb': 'jab&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH'
}

DaggerAttack = {
'verb': 'stab&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 4,
'DamageType': 'PIERCE'
}

SmallSword = {
'verb': 'slash&ES',
'DiceNumber': 1,
'DiceValue': 6,
'DamageType': 'SLASH'
}

MediumSword = {
'verb': 'slash&ES',
'DiceNumber': 1,
'DiceValue': 8,
'DamageType': 'SLASH'
}

LargeSword = {
'verb': 'slash&ES',
'DiceNumber': 2,
'DiceValue': 5,
'DamageType': 'SLASH'
}

HugeSword = {
'verb': 'slash&ES',
'DiceNumber': 2,
'DiceValue': 5,
'DamageBonus': 2,
'DamageType': 'SLASH'
}

SmallShield = {
'verb': 'bash&ES',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 3
}

MediumShield = {
'verb': 'bash&ES',
'ToHitBonus': 1,
'DiceNumber': 2,
'DiceValue': 3
}

LargeShield = {
'verb': 'bash&ES',
'ToHitBonus': 1,
'DiceNumber': 3,
'DiceValue': 3
}

HugeShield = {
'verb': 'bash&ES',
'DiceNumber': 4,
'DiceValue': 3
}

WhipAttack = {
'verb': 'whip&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 5,
'DamageType': 'SLASH'
}

BoulderRoll = {
'verb': 'crush&ES',
'ToHitBonus': -4,
'DiceNumber': 2,
'DiceValue': 10
}

# Ranged attacks:
MisThrown = {
'verb': 'hit&S',
'ToHitBonus': -4,
'DiceNumber': 1,
'DiceValue': 2,
'range': 2,
'flags': ['RANGED']
}

ClubThrown = {
'verb': 'strike&S',
'DiceNumber': 1,
'DiceValue': 4,
'range': 4,
'flags': ['RANGED']
}

KnifeThrown = {
'verb': 'stab&S',
'ToHitBonus': 3,
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 2,
'range': 6,
'DamageType': 'PIERCE',
'flags': ['RANGED']
}

DaggerThrown = {
'verb': 'stab&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 4,
'range': 5,
'DamageType': 'PIERCE',
'flags': ['RANGED']
}

###############################################################################
#  Items
###############################################################################

# Must be defined before monsters to allow for generating inventories.

DummyItem = {
'char': '?',
'color': libtcod.white,
'name': 'BUG: dummy item',
'BlockMove': False,
'material': 'STONE',
'size': 0,
'attack': NonWeapon,
'ranged': MisThrown,
'accuracy': 0,             # This is not normal to hit, but a general bonus.
'StrScaling': 'F',
'DexScaling': 'F',
'DV': 0,
'PV': 0,
'intrinsics': [],
'flags': [],
'coolness': 0,
'frequency': 100
}

# Weapons:
Cudgel = {
'char': '\\',
'color': libtcod.darkest_orange,
'name': 'cudgel',
'material': 'WOOD',
'size': -1,
'StrScaling': 'B',
'DexScaling': 'C',
'attack': Club,
'ranged': ClubThrown,
'flags': ['MELEE', 'WEAPON']
}

Mace = {
'char': '\\',
'color': libtcod.silver,
'name': 'mace',
'material': 'IRON',
'size': 0,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': MaceAttack,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF']
}

WarHammer = {
'char': '\\',
'color': libtcod.dark_grey,
'name': 'war hammer',
'material': 'IRON',
'size': 1,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': Hammer,
'flags': ['MELEE', 'WEAPON']
}

QuarterStaff = {
'char': '|',
'color': libtcod.darker_orange,
'name': 'quarterstaff',
'material': 'WOOD',
'size': 1,
'DV': 1,
'StrScaling': 'B',
'DexScaling': 'B',
'attack': WoodStaff,
'flags': ['MELEE', 'WEAPON', 'ENCHANT_DODGE'],
'frequency': 20
}

Knife = {
'char': ')',
'color': libtcod.dark_grey,
'name': 'knife',
'material': 'IRON',
'size': -2,
'StrScaling': 'C',
'DexScaling': 'A',
'attack': KnifeAttack,
'ranged': KnifeThrown,
'flags': ['MELEE', 'WEAPON']
}

Dagger = {
'char': ')',
'color': libtcod.dark_grey,
'name': 'dagger',
'material': 'IRON',
'size': -2,
'StrScaling': 'D',
'DexScaling': 'S',
'attack': DaggerAttack,
'ranged': DaggerThrown,
'flags': ['MELEE', 'WEAPON']
}

ShortSword = {
'char': ')',
'color': libtcod.silver,
'name': 'short sword',
'material': 'IRON',
'size': -1,
'DV': 1,
'StrScaling': 'D',
'DexScaling': 'A',
'attack': SmallSword,
'flags': ['MELEE', 'WEAPON']
}

LongSword = {
'char': ')',
'color': libtcod.silver,
'name': 'long sword',
'material': 'IRON',
'size': 0,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': MediumSword,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF']
}

GreatSword = {
'char': ')',
'color': libtcod.silver,
'name': 'great sword',
'material': 'IRON',
'size': 1,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': LargeSword,
'flags': ['MELEE', 'WEAPON']
}

Scimitar = {
'char': ')',
'color': libtcod.silver,
'name': 'two-handed scimitar',
'material': 'IRON',
'size': 2,
'StrScaling': 'S',
'DexScaling': 'E',
'attack': HugeSword,
'flags': ['MELEE', 'WEAPON'],
'frequency': 30
}

# Shields:
Buckler = {
'char': '[',
'color': libtcod.silver,
'name': 'buckler',
'material': 'IRON',
'size': -1,
'attack': SmallShield,
'StrScaling': 'C',
'DexScaling': 'A',
'flags': ['SHIELD', 'TWO_HAND_OK'],
'frequency': 30
}

RoundShield = {
'char': '[',
'color': libtcod.darker_orange,
'name': 'round shield',
'material': 'WOOD',
'size': -1,
'attack': MediumShield,
'StrScaling': 'B',
'DexScaling': 'B',
'flags': ['SHIELD']
}

KiteShield = {
'char': '[',
'color': libtcod.silver,
'name': 'kite shield',
'material': 'IRON',
'size': 0,
'attack': LargeShield,
'StrScaling': 'A',
'DexScaling': 'C',
'flags': ['SHIELD']
}

TowerShield = {
'char': '[',
'color': libtcod.darker_orange,
'name': 'tower shield',
'material': 'WOOD',
'size': 2,
'attack': HugeShield,
'StrScaling': 'S',
'DexScaling': 'D',
'flags': ['SHIELD'],
'frequency': 70
}

# Headgear:
Bandana = {
'char': '-',
'color': libtcod.dark_green,
'name': 'bandana',
'material': 'CLOTH',
'DV': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

Headband = {
'char': '-',
'color': libtcod.red,
'name': 'headband',
'material': 'CLOTH',
'accuracy': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

Crown = {
'char': '-',
'color': libtcod.yellow,
'name': 'golden crown',
'material': 'GOLD',
'PV': 0,
'DV': 0,
'size': -2,
'flags': ['HEAD', 'ARMOR', 'ENCHANT_DOUBLE'],
'frequency': 20
}

Circlet = {
'char': '-',
'color': libtcod.white,
'name': 'silver circlet',
'material': 'SILVER',
'PV': 0,
'DV': 0,
'size': -2,
'flags': ['HEAD', 'ARMOR', 'ENCHANT_DODGE'],
'frequency': 20
}

Skullcap = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'skullcap',
'material': 'LEATHER',
'PV': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

Helm = {
'char': '-',
'color': libtcod.silver,
'name': 'helmet',
'material': 'IRON',
'PV': 2,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

FullHelm = {
'char': '-',
'color': libtcod.silver,
'name': 'full helmet',
'material': 'IRON',
'DV': -1,
'PV': 3,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 80
}

GreatHelm = {
'char': '-',
'color': libtcod.silver,
'name': 'great helmet',
'material': 'IRON',
'DV': -2,
'PV': 5,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 60
}

# Handwear:
LeatherGlove = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'leather glove',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 1,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 80
}

BlackGlove = {
'char': '(',
'color': libtcod.darker_grey,
'name': 'black glove',
'material': 'CLOTH',
'size': -1,
'accuracy': 1,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 60
}

Gauntlet = {
'char': '(',
'color': libtcod.silver,
'name': 'iron gauntlet',
'material': 'IRON',
'size': -1,
'DV': -1,
'PV': 3,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 70
}

Bracer = {
'char': '(',
'color': libtcod.silver,
'name': 'iron bracer',
'material': 'IRON',
'size': -1,
'DV': -2,
'PV': 5,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 50
}

Bracelet = {
'char': '(',
'color': libtcod.yellow,
'name': 'golden bracelet',
'material': 'GOLD',
'size': -1,
'DV': 0,
'PV': 0,
'flags': ['ARM', 'ARMOR', 'ENCHANT_DOUBLE'],
'frequency': 20
}

ArmGuard = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'leather arm-guard',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 50
}

# Armor:
LeatherArmor = {
'char': ']',
'color': libtcod.darker_orange,
'name': 'boiled leather cuirass',
'material': 'LEATHER',
'size': 0,
'DV': -1,
'PV': 2,
'flags': ['TORSO', 'ARMOR']
}

StuddedArmor = {
'char': ']',
'color': libtcod.darker_orange,
'name': 'studded leather cuirass',
'material': 'IRON',
'size': 0,
'DV': -2,
'PV': 3,
'flags': ['TORSO', 'ARMOR']
}

ChainArmor = {
'char': ']',
'color': libtcod.silver,
'name': 'chain mail',
'material': 'IRON',
'size': 0,
'DV': -3,
'PV': 5,
'flags': ['TORSO', 'ARMOR']
}

ScaleArmor = {
'char': ']',
'color': libtcod.silver,
'name': 'scale mail',
'material': 'IRON',
'size': 0,
'DV': -4,
'PV': 7,
'flags': ['TORSO', 'ARMOR']
}

PlateArmor = {
'char': ']',
'color': libtcod.silver,
'name': 'plate mail',
'material': 'IRON',
'size': 0,
'DV': -5,
'PV': 9,
'flags': ['TORSO', 'ARMOR']
}

CrystalShard = {
'char': ']',
'color': libtcod.cyan,
'name': 'crystal shard mail',
'material': 'GLASS',
'size': 0,
'DV': -4,
'PV': 8,
'flags': ['TORSO', 'ARMOR'],
'frequency': 10
}

CrystalPlate = {
'char': ']',
'color': libtcod.cyan,
'name': 'crystal plate mail',
'material': 'GLASS',
'size': 0,
'DV': -5,
'PV': 10,
'flags': ['TORSO', 'ARMOR'],
'frequency': 10
}

GreenTunic = {
'char': ']',
'color': libtcod.dark_green,
'name': 'green tunic',
'material': 'CLOTH',
'size': 0,
'DV': 1,
'PV': 0,
'flags': ['TORSO', 'ARMOR'],
'frequency': 50
}

RedTunic = {
'char': ']',
'color': libtcod.dark_red,
'name': 'red tunic',
'material': 'CLOTH',
'size': 0,
'accuracy': 2,
'flags': ['TORSO', 'ARMOR'],
'frequency': 50
}

SnakeVest = {
'char': ']',
'color': libtcod.desaturated_green,
'name': 'snakeskin vest',
'material': 'LEATHER',
'size': 0,
'accuracy': 1,
'DV': 1,
'PV': 1,
'flags': ['TORSO', 'ARMOR'],
'frequency': 30
}

BlackRobe = {
'char': ']',
'color': libtcod.darker_grey,
'name': 'black robe',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'flags': ['TORSO', 'ARMOR'],
'frequency': 30
}

BrownRobe = {
'char': ']',
'color': libtcod.darkest_orange,
'name': 'brown robe',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'flags': ['TORSO', 'ARMOR'],
'frequency': 30
}

WhiteRobe = {
'char': ']',
'color': libtcod.white,
'name': 'white robe',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'flags': ['TORSO', 'ARMOR'],
'frequency': 30
}

BlueDress = {
'char': ']',
'color': libtcod.blue,
'name': 'blue dress',
'material': 'CLOTH',
'size': -1,
'DV': 0,
'PV': 0,
'flags': ['TORSO', 'ARMOR'],
'frequency': 10
}

# Belts:
LeatherBelt = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'leather belt',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 1,
'flags': ['GROIN', 'ARMOR'],
'frequency': 80
}

BlackBelt = {
'char': '-',
'color': libtcod.darker_grey,
'name': 'black belt',
'material': 'CLOTH',
'size': -1,
'accuracy': 2,
'flags': ['GROIN', 'ARMOR'],
'frequency': 60
}

Girdle = {
'char': '-',
'color': libtcod.silver,
'name': 'iron girdle',
'material': 'IRON',
'size': -1,
'DV': -1,
'PV': 3,
'flags': ['GROIN', 'ARMOR'],
'frequency': 70
}

PlateSkirt = {
'char': '-',
'color': libtcod.silver,
'name': 'plate skirt',
'material': 'IRON',
'size': -1,
'DV': -2,
'PV': 5,
'flags': ['GROIN', 'ARMOR'],
'frequency': 60
}

Baldric = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'baldric',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['GROIN', 'ARMOR'],
'frequency': 70
}

# Legwear:
Sandal = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'sandal',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['LEG', 'ARMOR', 'PAIRED']
}

SnakeSandal = {
'char': '(',
'color': libtcod.desaturated_green,
'name': 'snakeskin sandal',
'material': 'LEATHER',
'size': -1,
'DV': 2,
'PV': 0,
'flags': ['LEG', 'ARMOR', 'PAIRED'],
'frequency': 30
}

LowBoot = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'low boot',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 1,
'flags': ['LEG', 'ARMOR', 'PAIRED']
}

HighBoot = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'high boot',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 2,
'flags': ['LEG', 'ARMOR', 'PAIRED'],
'frequency': 70
}

Clog = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'clog',
'material': 'WOOD',
'size': -2,
'DV': -1,
'PV': 3,
'flags': ['LEG', 'ARMOR', 'PAIRED']
}

Greave = {
'char': '(',
'color': libtcod.silver,
'name': 'iron greave',
'material': 'IRON',
'size': -2,
'DV': -2,
'PV': 5,
'flags': ['LEG', 'ARMOR', 'PAIRED'],
'frequency': 90
}

Anklet = {
'char': '(',
'color': libtcod.white,
'name': 'silver anklet',
'material': 'SILVER',
'size': -2,
'DV': 0,
'PV': 0,
'flags': ['LEG', 'ARMOR', 'ENCHANT_DODGE'],
'frequency': 20
}

# General:
GoldPiece = {
'char': '$',
'color': libtcod.yellow,
'name': 'gold nugget',
'material': 'GOLD',
'size': -2,
'frequency': 5
}

Berry = {
'char': chr(236),
'color': libtcod.blue,
'name': 'berry',
'material': 'PLANT',
'size': -2,
'flags': ['FOOD'],
'frequency': 30
}

# Furniture, containers and similar:
Boulder = {
'char': '0',
'color': libtcod.dark_grey,
'name': 'boulder',
'BlockMove': True,
'size': 2,
'DV': -10,
'attack': BoulderRoll,
'flags': ['FEATURE'], # TODO: Block sight.
'frequency': 5
}

Chest = {
'char': chr(127),
'color': libtcod.darker_orange,
'name': 'chest',
'material': 'WOOD',
'size': 1,
'DV': -10,
'flags': ['FEATURE', 'CONTAINER', 'CAN_BE_OPENED'],
'frequency': 10
}

Chair = {
'char': chr(249),
'color': libtcod.darker_orange,
'name': 'chair',
'material': 'WOOD',
'size': 0,
'DV': -10,
'flags': ['FEATURE'],
'frequency': 0
}

Table = {
'char': chr(250),
'color': libtcod.darker_orange,
'name': 'table',
'BlockMove': True,
'material': 'WOOD',
'size': 1,
'DV': -10,
'flags': ['FEATURE'],
'frequency': 0
}

Bed = {
'char': chr(251),
'color': libtcod.darker_orange,
'name': 'bed',
'material': 'WOOD',
'size': 1,
'DV': -10,
'flags': ['FEATURE'],
'frequency': 0
}

###############################################################################
#  Monsters
###############################################################################

DummyMonster = {
'char': 'Q', # The question is, what is this strange monster?
'color': libtcod.white,
'name': 'BUG: dummy monster',
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 6,
'material': 'FLESH',
'sex': 'NEUTER',
'size': 0,
'diet': ['FLESH', 'WATER'],
'intrinsics': [],
'inventory': [],
'flags': ['HUMANOID'],
'frequency': 100
}

Player = {
'char': '@',
'color': libtcod.white,
'name': 'Player',
'Str': 2,
'Dex': 2,
'End': 4,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 6,
'sex': 'MOF',
'intrinsics': [],
'inventory': [ShortSword, RoundShield, GreenTunic, LowBoot, LowBoot],
'flags': ['HUMANOID', 'AVATAR'],
'frequency': 0
}

Kobold = {
'char': 'k',
'color': libtcod.red,
'name': 'kobold',
'Str': 0,
'Dex': 3,
'End': -3,
'Wit': 1,
'Ego': 0,
'speed': 1.1,
'sight': 8,
'size': -1,
'sex': 'MOF',
'flags': ['HUMANOID', 'AI_SCAVENGER', 'MUTATION_CLAWS'],
'frequency': 70
}

KoboldWhelp = {
'char': 'k',
'color': libtcod.light_red,
'name': 'kobold whelp',
'Str': 0,
'Dex': 2,
'End': -5,
'Wit': 1,
'Ego': 0,
'speed': 1.1,
'sight': 8,
'size': -2,
'sex': 'MOF',
'flags': ['HUMANOID', 'AI_KITE'],
'frequency': 50
}

Orc = {
'char': 'o',
'color': libtcod.desaturated_green,
'name': 'orc',
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 0,
'Ego': 0,
'sex': 'MOF',
'inventory': [ShortSword, RoundShield, LeatherArmor, LowBoot, LowBoot],
'flags': ['HUMANOID']
}

Troll = {
'char': 'T',
'color': libtcod.dark_green,
'name': 'troll',
'Str': 2,
'Dex': -1,
'End': 3,
'Wit': -1,
'Ego': 0,
'size': 1,
'sex': 'MOF',
'intrinsics': [], # TODO: Regeneration, revival.
'flags': ['HUMANOID', 'USE_HEAD', 'MUTATION_LARGE_CLAWS'],
'frequency': 20
}

###############################################################################
#  Body Parts
###############################################################################

DummyPart = {
'name': 'BUG: dummy body part',
'cover': 100, # Chance of being hit there is based on cover.
'place': 0,   # How high (positive) or low (negative) on the body the part is.
'size': 0,    # How different the size of this part is to main body.
'eyes': 0,
#'breasts': 0,
#'testicles': 0,
'StrScaling': 'B',
'DexScaling': 'B',
'attack': Slam,
'material': 'FLESH',
'flags': []
}

Head = {
'name': 'head',
'cover': 40,
'place': 2,
'size': -2,
'eyes': 2,
'StrScaling': 'C', # No, had is not really that good for attacking.
'DexScaling': 'C',
'attack': Bite,
'flags': ['HEAD', 'VITAL']
}

Torso = {
'name': 'torso',
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

SlimeTorso = {
'name': 'blob',
'eyes': 1,
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER', 'GRASP']
}

AlienTorso = {
'name': 'torso',
'eyes': 3,
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

AnimalTorso = {
'name': 'upper body',
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

Groin = {
'name': 'groin',
'cover': 40,
'place': -1,
'size': -1,
'flags': ['GROIN', 'VITAL', 'CANNOT_SEVER']
}

AnimalGroin = {
'name': 'lower body',
'cover': 50,
'size': -1,
'flags': ['GROIN', 'VITAL', 'CANNOT_SEVER']
}

Tail = {
'name': 'tail',
'cover': 50,
'place': -1,
'size': -1,
'StrScaling': 'A',
'DexScaling': 'C',
'attack': Club,
'flags': ['TAIL']
}

PrehensiveTail = {
'name': 'tail',
'cover': 40,
'place': -1,
'size': -1,
'StrScaling': 'C',
'DexScaling': 'A',
'flags': ['TAIL', 'GRASP']
}

Arm = {
'name': 'arm',
'cover': 70,
'place': 1,
'size': -1,
'flags': ['ARM']
}

TentacleArm = {
'name': 'tentacle',
'cover': 80,
'place': 1,
'attack': WhipAttack,
'flags': ['ARM', 'GRASP']
}

Hand = {
'name': 'hand',
'cover': 40,
'size': -2,
'attack': Punch,
'flags': ['HAND', 'GRASP']
}

SmallClaw = {
'name': 'claw',
'cover': 40,
'size': -2,
'attack': Claw,
'flags': ['HAND', 'GRASP']
}

BigClaw = {
'name': 'claw',
'cover': 60,
'size': -2,
'attack': LargeClaw,
'flags': ['HAND', 'GRASP']
}

Leg = {
'name': 'leg',
'cover': 80,
'place': -2,
'size': -1,
'StrScaling': 'A',
'DexScaling': 'C',
'attack': Kick,
'flags': ['LEG']
}

PegLeg = {
'name': 'peg leg',
'cover': 80,
'place': -2,
'size': -1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': Club,
'material': 'WOOD',
'flags': ['LEG']
}

TentacleLeg = {
'name': 'tentacle',
'cover': 90,
'place': -2,
'attack': Club,
'flags': ['LEG']
}

Paw = {
'name': 'paw',
'cover': 80,
'place': -2,
'size': -1,
'attack': Claw,
'flags': ['LEG']
}

Wing = {
'name': 'wing',
'cover': 90,
'size': -1,
'attack': Buffet,
'flags': ['WING']
}

###############################################################################
#  Clouds
###############################################################################

# TODO:
#  flames
#  frost vapours
#  thick smoke
#  acid smoke
#  toxic smoke

###############################################################################
#  Terrains
###############################################################################

DummyTerrain = {
'char': '.',
'color': libtcod.white,
'name': 'BUG: dummy terrain',
'BlockMove': False,
'BlockSight': False,
'flags': []
}

# Walls:
RockWall = {
'char': '#',
'color': libtcod.dark_grey,
'name': 'rock wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG']
}

BrickWall = {
'char': '#',
'color': libtcod.light_grey,
'name': 'brick wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG']
}

WoodWall = {
'char': '#',
'color': libtcod.darkest_orange,
'name': 'wooden wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG', 'CAN_BE_BURNED']
}

IceWall = {
'char': '#',
'color': libtcod.dark_cyan,
'name': 'ice wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG', 'CAN_BE_MELTED']
}

EarthWall = {
'char': '#',
'color': libtcod.dark_orange,
'name': 'earthen wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG']
}

IronWall = {
'char': '#',
'color': libtcod.silver,
'name': 'iron wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_CORRODED']
}

IronBars = {
'char': chr(240), # Ie. ≡
'color': libtcod.silver,
'name': 'iron bars',
'BlockMove': True,
'BlockSight': False,
'flags': ['WALL', 'CAN_BE_CORRODED']
}

# Floors:
RockFloor = {
'char': '.',
'color': libtcod.light_grey,
'name': 'rock floor',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

WoodFloor = {
'char': '.',
'color': libtcod.darker_orange,
'name': 'parquet',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_BURNED']
}

EarthFloor = {
'char': '.',
'color': libtcod.dark_orange,
'name': 'dirt floor',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

Carpet = {
'char': '.',
'color': libtcod.fuchsia,
'name': 'carpet',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_BURNED']
}

IceFloor = {
'char': '.',
'color': libtcod.cyan,
'name': 'ice floor',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'SLIDE', 'CAN_BE_MELTED']
}

GrassFloor = {
'char': '.',
'color': libtcod.green,
'name': 'grass',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_BURNED']
}

Snow = {
'char': '.',
'color': libtcod.white,
'name': 'snow',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_MELTED']
}

DeepSnow = {
'char': ',',
'color': libtcod.white,
'name': 'deep snow',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_MELTED', 'WADE']
}

Sand = {
'char': '.',
'color': libtcod.light_yellow,
'name': 'sand',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

DeepSand = {
'char': ',',
'color': libtcod.light_yellow,
'name': 'quicksand',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'SWIM']
}

# Doors:
WoodDoor = {
'char': '+',
'color': libtcod.darkest_orange,
'name': 'wooden door',
'BlockMove': True,
'BlockSight': True,
'flags': ['DOOR', 'CAN_BE_OPENED', 'CAN_BE_BURNED', 'CAN_BE_KICKED']
}

SecretDoor = {              # Opened will be revealed and transformed into normal
'char': '#',                # open doors. You need to zap them with invisibility
'color': libtcod.dark_grey, # to make them secret again.
'name': 'rock wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['DOOR', 'CAN_BE_OPENED', 'CAN_BE_BURNED', 'CAN_BE_KICKED', 'SECRET']
}

OpenDoor = {
'char': '\'',
'color': libtcod.darkest_orange,
'name': 'open door',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'CAN_BE_CLOSED', 'CAN_BE_BURNED']
}

BrokenDoor = {
'char': '_',
'color': libtcod.darkest_orange,
'name': 'broken door',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR']
}

ClosedPort = {
'char': '+',
'color': libtcod.white,
'name': 'lowered portcullis',
'BlockMove': True,
'BlockSight': False,
'flags': ['DOOR', 'PORTCULLIS', 'CAN_BE_OPENED']
}

OpenPort = {
'char': '\'',
'color': libtcod.white,
'name': 'raised portcullis',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'PORTCULLIS', 'CAN_BE_CLOSED']
}

Curtain = {
'char': '+',
'color': libtcod.dark_fuchsia,
'name': 'curtain',
'BlockMove': False,
'BlockSight': True,
'flags': ['DOOR']
}

# Plants:
LeafyTree = {
'char': chr(5), # Ie. ♣
'color': libtcod.dark_green,
'name': 'tree',
'BlockMove': True,
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'CAN_BE_CLIMBED', 'PLANT']
}

ConifTree = {   # Coniferous tree
'char': chr(6), # Ie. ♠
'color': libtcod.darker_green,
'name': 'tree',
'BlockMove': True,
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'CAN_BE_CLIMBED', 'PLANT']
}

Vines = {
'char': '|',
'color': libtcod.dark_green,
'name': 'hanging vines',
'BlockMove': False,
'BlockSight': True,
'flags': ['GROUND', 'CAN_BE_BURNED', 'PLANT']
}

TallGrass = {
'char': '\"',
'color': libtcod.dark_green,
'name': 'tall grass',
'BlockMove': False,
'BlockSight': True,
'flags': ['GROUND', 'CAN_BE_BURNED', 'PLANT']
}

# Decorations:
RockPile = {
'char': '*',
'color': libtcod.darker_grey,
'name': 'rock pile',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_KICKED']
}

BonePile = {
'char': '*',
'color': libtcod.white,
'name': 'bone pile',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_KICKED']
}

Grave = {
'char': chr(241), # Ie. ±
'color': libtcod.white,
'name': 'gravestone',
'BlockMove': False,
'BlockSight': False,
'flags': ['CAN_BE_KICKED']
}

# Liquids:
ShallowWater = {
'char': '~',
'color': libtcod.blue,
'name': 'shallow water',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'WADE']
}

DeepWater = {
'char': chr(247),
'color': libtcod.darker_blue,
'name': 'deep water',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'SWIM']
}

Lava = {
'char': chr(247),
'color': libtcod.dark_red,
'name': 'lava',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID']
}

Mud = {
'char': '~',
'color': libtcod.darker_orange,
'name': 'mud',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'STICKY', 'WADE']
}

# Features:
UpStairs = {
'char': '<',
'color': libtcod.white,
'name': 'upward staircase',
'BlockMove': False,
'BlockSight': False,
'flags': ['FEATURE', 'STAIRS_UP']
}

DownStairs = {
'char': '>',
'color': libtcod.white,
'name': 'downward staircase',
'BlockMove': False,
'BlockSight': False,
'flags': ['FEATURE', 'STAIRS_DOWN']
}

BookShelf = {
'char': chr(252),
'color': libtcod.darker_orange,
'name': 'bookshelf',
'BlockMove': True,
'BlockSight': True,
'flags': ['FEATURE', 'CONTAINER', 'CAN_BE_OPENED']
}

'''
# Changing terrain:
ChangedTerrain = {        # Certain actions can change terrain into this, eg. actionOpen on doors.
DummyTerrain: RockFloor,
OpenPort: ClosedPort,
ClosedPort: OpenPort,
WoodDoor: OpenDoor,
SecretDoor: OpenDoor,
OpenDoor: WoodDoor
}

DestroyedTerrain = {      # Damage can change terrain into this.
DummyTerrain: RockFloor,
WoodDoor: BrokenDoor,
OpenDoor: BrokenDoor,
SecretDoor: BrokenDoor,
IceFloor: ShallowWater,
IceWall: IceFloor,
RockWall: RockPile
}
'''
###############################################################################
#  Rooms
##############################################################################

DummyRoom = {
'frequency': 15,
' ': (RockWall, None, None, None),
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None),
'+': (WoodDoor, None, None, None),
'S': (SecretDoor, None, None, None),
'x': (WoodDoor, ['BLOCKED'], None, None),
'$': (RockFloor, None, GoldPiece, None)
}

# Several small cages.
Cage1 = {
'file': 'rooms/cage1',
'width': 9,
'height': 7
}

Cage2 = {
'file': 'rooms/cage2',
'width': 7,
'height': 7,
'1': (RockFloor, None, 'RANDOM_ANY', 'RANDOM_ANY'),
'x': (ClosedPort, ['LOCKED', 'BLOCKED'], None, None),
'X': (IronBars, None, None, None)
}

# Prison cells.
Prison = {
'file': 'rooms/prison',
'width': 10,
'height': 6,
'#': (BrickWall, None, None, None),
'+': (WoodDoor, ['LOCKED'], None, None)
}

# The letters.
LetterX = {
'file': 'rooms/xxx',
'width': 5,
'height': 5
}

LetterS = {
'file': 'rooms/ss',
'width': 6,
'height': 7
}

Curved = {
'file': 'rooms/curved',
'width': 10,
'height': 8
}

Foursome1 = {
'file': 'rooms/foursome1',
'width': 10,
'height': 8
}

Foursome2 = {
'file': 'rooms/foursome2',
'width': 10,
'height': 8
}

# A very secretly hidden rooms.
Secret1 = {
'file': 'rooms/secret1',
'frequency': 5,
'width': 11,
'height': 11,
'#': (WoodWall, None, None, None),
'X': (RockWall, None, None, None),
'.': (WoodFloor, None, None, None),
',': (RockFloor, None, None, None)
}

Secret2 = {
'file': 'rooms/secret2',
'frequency': 10,
'width': 10,
'height': 8
}

Secret3 = {
'file': 'rooms/secret3',
'frequency': 10,
'width': 10,
'height': 8
}

Secret4 = {
'file': 'rooms/secret4',
'frequency': 10,
'width': 10,
'height': 9
}

# Guard stations.
Guard1 = {
'file': 'rooms/guard1',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard2 = {
'file': 'rooms/guard2',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard3 = {
'file': 'rooms/guard3',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard4 = {
'file': 'rooms/guard4',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard5 = {
'file': 'rooms/guard5',
'width': 8,
'height': 7,
'!': (IronBars, None, None, None)
}

# Several rooms in one.
SmallRooms1 = {
'file': 'rooms/smallrooms1',
'width': 10,
'height': 8,
}

SmallRooms2 = {
'file': 'rooms/smallrooms2',
'width': 18, # This may be too much.
'height': 11,
'x': (ClosedPort, None, None, None),
'!': (IronBars, None, None, None)
}

# Why not?
Why1 = {
'file': 'rooms/why1',
'width': 5,
'height': 6,
}

Why2 = {
'file': 'rooms/why2',
'width': 5,
'height': 6,
}

# T-junction.
TJunction = {
'file': 'rooms/tjunction',
'width': 5,
'height': 4,
'0': (RockFloor, None, Boulder, None)
}

# Checkers room!
Checkers = {
'file': 'rooms/checkers',
'width': 9,
'height': 7
}

# A small library.
Library = {
'file': 'rooms/library',
'width': 7,
'height': 7,
'X': (BookShelf, None, None, None)
}

# Pillars in a room.
Pillars1 = {
'file': 'rooms/pillars1',
'width': 11,
'height': 11,
'>': (DownStairs, None, None, None)
}

Pillars2 = {
'file': 'rooms/pillars2',
'width': 9,
'height': 11,
}

Pillars3 = {
'file': 'rooms/pillars3',
'width': 9,
'height': 9,
}

###############################################################################
#  Lists
###############################################################################

# Lists must be last to have all stuff already defined.

# General:
# --------
Sizes = {
2: 'huge',
1: 'large',
0: 'medium',
-1: 'small',
-2: 'tiny'
}

Scaling = {
'S': 2.0,
'A': 1.5,
'B': 1.0,
'C': 0.75,
'D': 0.5,
'E': 0.25,
'F': 0.0
}

MaterialsList = [
'BONE',
'CLOTH',
'FLESH',
'GLASS',
'GOLD',
'IRON',
'LEATHER',
'PLANT',
'SILVER',
'STONE',
'WOOD'
]

DamageTypeList = [
'BLUNT',
'SLASH',
'PIERCE',
'ACID',
'FIRE',
'COLD',
'ELECTRIC',
'NECROTIC',
'POISON'
]

# Items:
# ------
ItemList = [
# Weapons:
Cudgel,
Mace,
QuarterStaff,
WarHammer,
Knife,
Dagger,
ShortSword,
LongSword,
GreatSword,
Scimitar,
# Shields:
Buckler,
RoundShield,
KiteShield,
TowerShield,
# Headgear:
Bandana,
Headband,
Skullcap,
Helm,
FullHelm,
GreatHelm,
Crown,
Circlet,
# Handwear:
LeatherGlove,
BlackGlove,
Gauntlet,
Bracer,
Bracelet,
ArmGuard,
# Body armor:
LeatherArmor,
StuddedArmor,
ChainArmor,
ScaleArmor,
PlateArmor,
CrystalShard,
CrystalPlate,
GreenTunic,
RedTunic,
SnakeVest,
BlackRobe,
BrownRobe,
WhiteRobe,
BlueDress,
# Belts:
LeatherBelt,
BlackBelt,
Girdle,
PlateSkirt,
Baldric,
# Legwear:
Sandal,
SnakeSandal,
LowBoot,
HighBoot,
Clog,
Greave,
Anklet,
# Other:
GoldPiece,
Berry,
Boulder,
Chest,
#Chair,
#Table,
#Bed
]

# Monsters:
# ---------
MobList = [
Kobold,
KoboldWhelp,
Orc,
Troll
]

# Body types:
# -----------
HumanoidList = [
Head,
Torso,
Arm,
Hand,
Arm,
Hand,
Groin,
Leg,
Leg
]

AlienList = [
TentacleArm,
TentacleArm,
TentacleArm,
AlienTorso,
TentacleLeg,
TentacleLeg,
TentacleLeg
]

AnimalList = [
Head,
AnimalTorso,
AnimalGroin,
Paw,
Paw,
Paw,
Paw
]

BirdList = [
Head,
AnimalTorso,
Wing,
Wing,
AnimalGroin,
Paw, # TODO: Talons?
Paw
]

SlimeList = [
SlimeTorso
]

BodyTypes = {
'HUMANOID': HumanoidList,
'ALIEN': AlienList,
'ANIMAL': AnimalList,
'BIRD': BirdList,
'SLIME': SlimeList
}

MutationTypes = [
'MUTATION_CLAWS',
'MUTATION_LARGE_CLAWS'
]

# Prefab rooms:
# -------------
RoomList = [
Cage1,
Cage2,
Checkers,
Curved,
Foursome1,
Foursome2,
Guard1,
Guard2,
Guard3,
Guard4,
Guard5,
LetterS,
LetterX,
Library,
Pillars1,
Pillars2,
Pillars3,
Prison,
Secret1,
Secret2,
Secret3,
Secret4,
SmallRooms1,
SmallRooms2,
TJunction,
Why1,
Why2
]
