# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

# Sizes:
# ------
# -2 - tiny
# -1 - small
#  0 - medium
#  1 - large
#  2 - huge

# Scaling:
# ------
#  S - 200 %
#  A - 150 %
#  B - 100 %
#  C -  75 %
#  D -  50 %
#  E -  25 %
#  F -   0 %

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

Whip = {
'verb': 'whip&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 5,
'DamageType': 'SLASH'
}

BoulderRoll = {
'verb': 'crush&ES',
'ToHitBonus': -4,
'DiceNumber': 1,
'DiceValue': 10,
'DamageBonus': 2
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
'verb': 'hit&S',
'DiceNumber': 1,
'DiceValue': 4,
'range': 4,
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
'size': -1,
'attack': NonWeapon,
'ranged': MisThrown,
'intrinsics': [],
'flags': [],
'frequency': 100
}

# Weapons:
Cudgel = {
'char': ')',
'color': libtcod.darkest_orange,
'name': 'cudgel',
'material': 'WOOD',
'size': -1,
'attack': Club,
'ranged': ClubThrown,
'intrinsics': ['MELEE']
}

# Headgear:
Bandana = {
'char': '-',
'color': libtcod.dark_green,
'name': 'bandana',
'material': 'CLOTH',
'size': -1,
'flags': ['HEAD'],
'frequency': 50
}

# Armor:
BlackRobe = {
'char': ']',
'color': libtcod.darker_grey,
'name': 'black robe',
'material': 'CLOTH',
'size': 0,
'flags': ['TORSO'],
'frequency': 50
}

BrownRobe = {
'char': ']',
'color': libtcod.darkest_orange,
'name': 'brown robe',
'material': 'CLOTH',
'size': 0,
'flags': ['TORSO'],
'frequency': 50
}

WhiteRobe = {
'char': ']',
'color': libtcod.white,
'name': 'white robe',
'material': 'CLOTH',
'size': 0,
'flags': ['TORSO'],
'frequency': 50
}

# Belts:
Belt = {
'char': '-',
'color': libtcod.darkest_orange,
'name': 'leather belt',
'material': 'LEATHER',
'size': 0,
'flags': ['GROIN'],
'frequency': 50
}

# General:
GoldPiece = {
'char': '$',
'color': libtcod.yellow,
'name': 'gold nugget',
'material': 'GOLD',
'size': -2
}

Boulder = {
'char': '0',
'color': libtcod.dark_grey,
'name': 'boulder',
'BlockMove': True,
'size': 2,
'attack': BoulderRoll,
'flags': [], # TODO: Block sight.
'frequency': 5
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
'size': 0,
'diet': ['FLESH', 'WATER'],
'intrinsics': [],
'flags': ['HUMANOID'],
'frequency': 100
}

Player = {
'char': '@',
'color': libtcod.white,
'name': 'Player',
'Str': 2,
'Dex': 0,
'End': 4,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 6,
'intrinsics': [],
'flags': ['HUMANOID', 'AVATAR'],
'frequency': 0
}

Kobold = {
'char': 'k',
'color': libtcod.light_red,
'name': 'kobold',
'Str': 0,
'Dex': 3,
'End': -3,
'Wit': 1,
'Ego': 0,
'speed': 1.1,
'sight': 8,
'size': -1,
'flags': ['HUMANOID', 'AI_SCAVENGER', 'MUTATION_CLAWS']
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
'intrinsics': [],
'flags': ['HUMANOID', 'USE_HEAD', 'MUTATION_LARGE_CLAWS'],
'frequency': 10
}

###############################################################################
#  Body Parts
###############################################################################

DummyPart = {
'name': 'BUG: dummy body part',
'cover': 100, # Chance of being hit there is based on cover.
'eyes': 0,
'attack': Slam,
'flags': []
}

Head = {
'name': 'head',
'cover': 30,
'eyes': 2,
'attack': Bite,
'flags': ['HEAD', 'VITAL']
}

Torso = {
'name': 'torso',
'flags': ['TORSO', 'VITAL']
}

SlimeTorso = {
'name': 'blob',
'eyes': 3,
'flags': ['TORSO', 'VITAL', 'GRASP']
}

AnimalTorso = {
'name': 'upper body',
'flags': ['TORSO', 'VITAL']
}

Groin = {
'name': 'groin',
'cover': 40,
'flags': ['GROIN', 'VITAL']
}

AnimalGroin = {
'name': 'lower body',
'flags': ['GROIN', 'VITAL']
}

Tail = {
'name': 'tail',
'attack': Club,
'flags': ['TAIL']
}

PrehensiveTail = {
'name': 'tail',
'flags': ['TAIL', 'GRASP']
}

Arm = {
'name': 'hand',
'cover': 60,
'attack': Punch,
'flags': ['ARM', 'GRASP']
}

TentacleArm = {
'name': 'tentacle',
'cover': 60,
'attack': Whip,
'flags': ['ARM', 'GRASP']
}

Leg = {
'name': 'leg',
'cover': 70,
'attack': Kick,
'flags': ['LEG']
}

TentacleLeg = {
'name': 'tentacle',
'cover': 70,
'attack': Club,
'flags': ['LEG']
}

Paw = {
'name': 'paw',
'cover': 70,
'attack': Claw,
'flags': ['LEG']
}

Wing = {
'name': 'wing',
'cover': 90,
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
'color': libtcod.dark_orange,
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
'color': libtcod.green,
'name': 'tree',
'BlockMove': True, # TODO: Or maybe False?
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'PLANT']
}

ConifTree = {   # Coniferous tree
'char': chr(6), # Ie. ♠
'color': libtcod.dark_green,
'name': 'tree',
'BlockMove': True, # TODO: Or maybe False?
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'PLANT']
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
'char': '~',
'color': libtcod.darker_blue,
'name': 'deep water',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'SWIM']
}

Lava = {
'char': '~',
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
Cages = {
'file': 'rooms/cages',
'width': 9,
'height': 7
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

ItemList = [
Cudgel,
Bandana,
BlackRobe,
BrownRobe,
WhiteRobe,
Belt,
GoldPiece,
Boulder
]

MobList = [
Kobold,
Orc,
Troll
]

# Body type lists:
HumanoidList = [
Head,
Torso,
Arm,
Arm,
Groin,
Leg,
Leg
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
Paw,
Paw
]

SlimeList = [
SlimeTorso
]

BodyTypes = {
'HUMANOID': HumanoidList,
'ANIMAL': AnimalList,
'BIRD': BirdList,
'SLIME': SlimeList
}

MutationTypes = [
'MUTATION_CLAWS',
'MUTATION_LARGE_CLAWS'
]

RoomList = [
Cages,
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
