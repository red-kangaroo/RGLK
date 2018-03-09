# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

import dungeon

###############################################################################
#  Functions
###############################################################################

# Let's hope I didn't mess up the chances...
def rand_chance(percent):
    if libtcod.random_get_int(0, 1, 100) > percent:
        return False
    else:
        return True

# Call it from here, or BAD THINGS (tm) happen.
# This is slow... TODO?
def calculateFOVMap():
    for i in Entities:
        for y in range(MapHeight):
            for x in range(MapWight):
                libtcod.map_set_properties(i.FOVMap, x, y, not dungeon.map[x][y].BlockSight,
                                           not dungeon.map[x][y].BlockMove)

def changeFOVMap(x, y):
    for i in Entities:
        libtcod.map_set_properties(i.FOVMap, x, y, not dungeon.map[x][y].BlockSight,
                                   not dungeon.map[x][y].BlockMove)

###############################################################################
#  Global Variables
###############################################################################

# TODO: Most of this should be in a script file.

ScreenWidth = 100
ScreenHeight = 55
MapWight = 80
MapHeight = 50

RoomMinSize = 5
RoomMaxSize = 10
RoomMaxNumber = 99
DrunkenSteps = 5000

MonsterMaxNumber = 30 # Should depend on dungeon level.

PlayerIsDead = False
ExitGame = False

WizModeNoClip = False
WizModeTrueSight = False
WizModeNewMap = False

Entities = []

# Base console:
Con = libtcod.console_new(ScreenWidth, ScreenHeight)
