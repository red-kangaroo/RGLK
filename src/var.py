# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

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

def rand_dice(DiceNumber, DiceValue, Bonus):
    result = 0

    while DiceNumber > 0:
        result += libtcod.random_get_int(0, 1, DiceValue)
        DiceNumber -= 1

    result += Bonus

    return result

def rand_gaussian_d20(rerolls = 0):
    rollResult = 0
    rollNo = 0

    if rerolls >= 0:
        while rollNo < rerolls + 1:
            roll1 = libtcod.random_get_int(0, 1, 20)
            roll2 = libtcod.random_get_int(0, 1, 20)
            result = (roll1 + roll2) / 2

            if result > rollResult:
                rollResult = result
            rollNo += 1
    else:
        while rollNo < abs(rerolls) + 1:
            roll1 = libtcod.random_get_int(0, 1, 20)
            roll2 = libtcod.random_get_int(0, 1, 20)
            result = (roll1 + roll2) / 2

            if rollNo == 0:
                rollResult = result
            elif result < rollResult:
                rollResult = result
            rollNo += 1

    return rollResult

def rand_int_from_float(number):
    # Returns integer from a float, with a chance of higher integer based on decimal
    # part of the float. Ie. 5.5 will return as 6 50 % of time.
    (decimal, base) = math.modf(number)

    if random.random() < decimal:
        if base >= 0:
            base += 1
        else:
            base -= 1

    return int(base)

# FOV:
# ----
# Call it from here, or BAD THINGS (tm) happen.
def calculateFOVMap():
    for y in range(MapHeight):
        for x in range(MapWidth):
            libtcod.map_set_properties(FOVMap, x, y, not Maps[DungeonLevel][x][y].BlockSight,
                                       not Maps[DungeonLevel][x][y].BlockMove)

def changeFOVMap(x, y):
    libtcod.map_set_properties(FOVMap, x, y, not Maps[DungeonLevel][x][y].BlockSight,
                               not Maps[DungeonLevel][x][y].BlockMove)

# Find functions:
# ---------------
def findNearestFreeSpot(x, y):
    pass

def findNearestCreature(x, y, attitude = None):
    pass

# General:
# --------

def beRude():
    pass

def bePolite():
    pass

###############################################################################
#  Global Variables
###############################################################################

# TODO: Most of this should be in a script file.

ScreenWidth = 100
ScreenHeight = 60
MapWidth = 80
MapHeight = 50
PanelWidth = 20
PanelHeight = 10
MenuWidth = 70
MenuHeight = 30
MainWidth = 40
MainHeight = 12

# Dungeon generation:
RoomMinSize = 5
RoomMaxSize = 10
RoomMaxNumber = 99
BSPMaxDepth = 10
BSPMinSize = 4
DrunkenSteps = 5000
FloorMaxNumber = 25 # Depths of the dungeon.

# TODO: Should depend on dungeon level.
MonsterMaxNumber = 10
ItemMaxNumber = 20

TurnCount = 0
DungeonLevel = 1 # Starting level of the player.

WizModeActivated = True # For now.
WizModeNoClip = False
WizModeTrueSight = False
WizModeNewMap = False

Maps = []
Entities = []
MessageHistory = []

TextColor = libtcod.white
GameName = "Recondite Gaol of the Lachrymose Knights"
# Once this was "Realm of the Glorious Lich King"

# FOV map:
FOVMap = libtcod.map_new(MapWidth, MapHeight)
# Consoles:
MapConsole = libtcod.console_new(MapWidth, MapHeight)
UIPanel = libtcod.console_new(PanelWidth, ScreenHeight)
MessagePanel = libtcod.console_new(ScreenWidth - PanelWidth, PanelHeight)
MenuPanel = libtcod.console_new(MenuWidth, MenuHeight)
MainMenu = libtcod.console_new(MainWidth, MainHeight)
