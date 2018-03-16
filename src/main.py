# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import ai
import dungeon
import entity
import monster as mon
import ui
import var

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(var.ScreenWidth, var.ScreenHeight, 'RGLK', False)
#libtcod.sys_set_fps(30)

# Player must be defined here, we work with him shortly.
Player = entity.spawn(0, 0, mon.Player)
var.Entities.append(Player)

###############################################################################
#  Main Loop
###############################################################################

Dungeon = dungeon.Builder()
Dungeon.makeMap(True)
ui.message("Welcome to the Realm of the Lich King!", libtcod.dark_violet)
# TODO: Better welcoming message.

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
