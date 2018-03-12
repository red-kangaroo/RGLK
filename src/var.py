# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

import dungeon

###############################################################################
#  General Functions
###############################################################################

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

def render_all(Player):
    # Draw map.
    for y in range(MapHeight):
        for x in range(MapWight):
            tile = dungeon.map[x][y]
            tile.draw(x, y, Player)
    # Draw first features, then items, then mobs.
    for i in Entities:
        if i.hasFlag('FEATURE'):
            i.draw(Player)
    for i in Entities:
        if i.hasFlag('ITEM'):
            i.draw(Player)
    for i in Entities:
        if i.hasFlag('MOB'):
            i.draw(Player)
    # Draw player last, over everything else.
    Player.draw(Player)

    # Hack in primitive GUI:
    libtcod.console_print_ex(MapConsole, ScreenWidth - 19, 1, libtcod.BKGND_NONE, libtcod.LEFT,
                             Player.displayHP())

    libtcod.console_blit(MapConsole, 0, 0, ScreenWidth, ScreenHeight, 0, 0, 0)

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

MonsterMaxNumber = 10 # Should depend on dungeon level.

ExitGame = False

WizModeActivated = False
WizModeNoClip = False
WizModeTrueSight = False
WizModeNewMap = False

Entities = []

# Base console:
MapConsole = libtcod.console_new(ScreenWidth, ScreenHeight)
