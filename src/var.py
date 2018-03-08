# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Functions
###############################################################################

# Let's hope I didn't mess up the chances...
def rand_chance(percent):
    if libtcod.random_get_int(0, 1, 100) > percent:
        return False
    else:
        return True

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

WizModeNoClip = False
WizModeTrueSight = False

Entities = []

# Base console:
Con = libtcod.console_new(ScreenWidth, ScreenHeight)
# Set FOV:
FOVMap = libtcod.map_new(MapWight, MapHeight)
