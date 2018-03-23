# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Attack Types
###############################################################################

DummyAttack = {
'verb': 'BUG: dummy attack',
'ToHitBonus': 0,
'DiceNumber': 0,
'DiceValue': 0,
'DamageBonus': 0,
'DamageType': 'BLUNT',
'flags': []
}

Punch = {
'verb': 'punch',
'DiceNumber': 1,
'DiceValue': 2,
'flags': ['UNARMED', 'NATURAL']
}

Claw = {
'verb': 'claw',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH',
'flags': ['NATURAL']
}

NonWeapon = {
'verb': 'bash',
'ToHitBonus': -2,
'DiceNumber': 1,
'DiceValue': 2
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
'intrinsics': [],
'flags': [],
'frequency': 1000
}

Boulder = {
'char': '0',
'color': libtcod.dark_grey,
'name': 'boulder',
'BlockMove': True,
'size': 2,
'flags': [], # TODO: Block sight.
'frequency': 10
}

# Item list must be last to have all items already defined.
ItemList = [
Boulder
]

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
'BaseAttack': Punch,
'material': 'FLESH',
'size': 0,
'diet': ['FLESH', 'WATER'],
'intrinsics': [],
'flags': [],
'frequency': 1000
}

# Sizes:
# ------
# -2 - tiny
# -1 - small
#  0 - medium
#  1 - large
#  2 - huge

Player = {
'char': '@',
'color': libtcod.white,
'name': 'Player',
'Str': 2,
'Dex': 2,
'End': 4,
'Wit': 0,
'Ego': 0,
'speed': 1.2,
'sight': 6,
'intrinsics': [],
'flags': ['AVATAR'],
'frequency': 0
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
'flags': ['AI_SCAVENGER']
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
'speed': 1.0,
'size': 1,
'intrinsics': [],
'flags': [],
'frequency': 100
}

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
'BlockMove': False, # TODO: Or maybe True?
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'PLANT']
}

ConifTree = {   # Coniferous tree
'char': chr(6), # Ie. ♠
'color': libtcod.dark_green,
'name': 'tree',
'BlockMove': False, # TODO: Or maybe True?
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
'flags': ['LIQUID']
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
'flags': ['LIQUID', 'STICKY']
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
'frequency': 20,
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None),
'+': (WoodDoor, None, None, None),
'S': (SecretDoor, None, None, None)
}

# Several small cages.
Cages = {
'file': 'rooms/cages',
'width': 9,
'height': 7,
'+': (WoodDoor, ['BLOCKED'], None, None)
}

# Prison cells.
Prison = {
'file': 'rooms/prison',
'width': 10,
'height': 6,
'+': (WoodDoor, ['LOCKED'], None, None)
}

# The letter X.
LetterX = {
'file': 'rooms/xxx',
'width': 5,
'height': 5
}

# A very secretly hidden room.
SuperSecret = {
'file': 'rooms/supersecret',
'frequency': 10,
'width': 11,
'height': 11,
'#': (WoodWall, None, None, None),
'X': (RockWall, None, None, None)
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

# Room list must be last to have all rooms already defined.
RoomList = [
Cages,
Checkers,
LetterX,
Pillars1,
Pillars2,
Pillars3,
Prison,
SuperSecret,
TJunction,
Why1,
Why2
]
