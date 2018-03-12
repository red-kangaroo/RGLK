# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

import dungeon

###############################################################################
#  General Functions
###############################################################################

# Random functions:
# -----------------
# Let's hope I didn't mess up the chances...
def rand_chance(percent):
    if libtcod.random_get_int(0, 1, 100) > percent:
        return False
    else:
        return True

def rand_gaussian_d20():
    roll1 = libtcod.random_get_int(0, 1, 20)
    roll2 = libtcod.random_get_int(0, 1, 20)
    return (roll1 + roll2) / 2


# FOV:
# ----
# Call it from here, or BAD THINGS (tm) happen.
def calculateFOVMap():
    for y in range(MapHeight):
        for x in range(MapWidth):
            libtcod.map_set_properties(FOVMap, x, y, not dungeon.map[x][y].BlockSight,
                                       not dungeon.map[x][y].BlockMove)

def changeFOVMap(x, y):
    libtcod.map_set_properties(FOVMap, x, y, not dungeon.map[x][y].BlockSight,
                               not dungeon.map[x][y].BlockMove)

###############################################################################
#  Global Variables
###############################################################################

# TODO: Most of this should be in a script file.

ScreenWidth = 100
ScreenHeight = 55
MapWidth = 80
MapHeight = 50
PanelWidth = 20
PanelHeight = 5

RoomMinSize = 5
RoomMaxSize = 10
RoomMaxNumber = 99
DrunkenSteps = 5000

MonsterMaxNumber = 10 # Should depend on dungeon level.

WizModeActivated = False
WizModeNoClip = False
WizModeTrueSight = False
WizModeNewMap = False

Entities = []
MessageHistory = []
TurnCount = 0
TextColor = libtcod.white

# FOV map:
FOVMap = libtcod.map_new(MapWidth, MapHeight)
# Consoles:
MapConsole = libtcod.console_new(MapWidth, MapHeight)
UIPanel = libtcod.console_new(PanelWidth, ScreenHeight)
MessagePanel = libtcod.console_new(ScreenWidth - PanelWidth, PanelHeight)
