# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Terrain Configuration
###############################################################################

Dummy = {
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
'flags': ['WALL']
}

WoodWall = {
'char': '#',
'color': libtcod.darkest_orange,
'name': 'wooden wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL']
}

IceWall = {
'char': '#',
'color': libtcod.dark_cyan,
'name': 'ice wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL']
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
'flags': ['GROUND']
}

IceFloor = {
'char': '.',
'color': libtcod.cyan,
'name': 'ice floor',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'SLIDE']
}

# Doors:
WoodDoor = {
'char': '+',
'color': libtcod.darkest_orange,
'name': 'wooden door',
'BlockMove': True,
'BlockSight': True,
'flags': ['DOOR', 'CAN_BE_OPENED']
}

OpenDoor = {
'char': '\'',
'color': libtcod.darkest_orange,
'name': 'open door',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'CAN_BE_CLOSED']
}

# Decorations:
Vines = {
'char': '|',
'color': libtcod.dark_green,
'name': 'hanging vines',
'BlockMove': False,
'BlockSight': True,
}

RockPile = {
'char': '*',
'color': libtcod.darker_grey,
'name': 'rock pile',
'BlockMove': False,
'BlockSight': False,
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
