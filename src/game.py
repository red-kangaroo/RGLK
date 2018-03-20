# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import shelve
import sys

import ai
import dungeon
import entity
import raw
import ui
import var

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(var.ScreenWidth, var.ScreenHeight, 'RGLK', False)
#libtcod.sys_set_fps(30)

###############################################################################
#  Functions
##############################################################################

def initialize():
    global Player, Dungeon

    # Player must be defined here, we work with him shortly.
    Player = entity.spawn(0, 0, raw.Player)
    var.Entities.append(Player)

    Dungeon = dungeon.Builder()
    Dungeon.makeMap(True)
    ui.message("Welcome to the %s!" % var.GameName, libtcod.dark_violet)
    # TODO: Better welcoming message.

def main_loop():
    global Player

    while not libtcod.console_is_window_closed():
        var.TurnCount += 1

        # Heartbeat of all entities.
        for i in var.Entities:
            i.Be()

        # Mob turns, including the player.
        for i in var.Entities:
            while i.AP >= 1:
                # Calculate FOV for the current actor.
                i.recalculateFOV()

                if i.hasFlag('AVATAR'):
                    # Redraw screen with each of the player's turns.
                    # Draw screen:
                    ui.render_all(i)

                # Now get the command, keyboard for player and AI for monsters.
                ai.getAICommand(i)

                # Some wizard mode handling:
                if var.WizModeNewMap:
                    Dungeon.makeMap(False)
                    var.WizModeNewMap = False
                    ui.message("You call upon the great powers of wizard mode to create a whole new dungeon level!")

        # This is a stupid way of doing this, but eh...
        if Player.hasFlag('DEAD'):
            ui.render_all(Player)
            ai.getAICommand(Player)

def play():
    what = ui.main_menu()

    if what == 0: # Quick Start
        initialize()
        main_loop()
    elif what == 1: # Create Character
        sys.exit("This function is unfortunately not yet supported!")
    if what == 2: # Load
        try:
            load()
        except:
            sys.exit("No savefile detected!")

        main_loop()
    if what == 3: # Tutorial
        sys.exit("This function is unfortunately not yet supported!")
    if what == 4: # Options
        sys.exit("This function is unfortunately not yet supported!")
    else: # Quit
        sys.exit("Goodbye!")

def save():
    global Player, Dungeon
    file = shelve.open('savegame', 'n')

    file["dungeon"] = Dungeon
    file["map"] = dungeon.map
    #file["map"] = var.Maps
    file["entity"] = var.Entities
    file["wizard"] = var.WizModeActivated
    file["message"] = var.MessageHistory
    file["turn"] = var.TurnCount
    file["player"] = var.Entities.index(Player) # Index of player in Entities list, to prevent doubling on load.
    file.close()

def load():
    global Player, Dungeon
    file = shelve.open('savegame', 'r')

    Dungeon = file["dungeon"]
    dungeon.map = file["map"]
    #file["map"] = var.Maps
    var.Entities = file["entity"]
    var.WizModeActivated = file["wizard"]
    var.MessageHistory = file["message"]
    var.TurnCount = file["turn"]
    Player = var.Entities[file["player"]]
    file.close()

    var.calculateFOVMap()
