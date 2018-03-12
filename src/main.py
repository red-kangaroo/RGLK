# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import ai
import dungeon
import entity
import var

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(var.ScreenWidth, var.ScreenHeight, 'RGLK', False)

# Player must be defined here, we work with him shortly.
Player = entity.Mob(1, 1, '@', libtcod.white, 'Player', 2, 2, 4)
var.Entities.append(Player)
Player.flags.append('AVATAR')

###############################################################################
#  Main Loop
###############################################################################

Dungeon = dungeon.Builder()
Dungeon.makeMap(True)
Player.recalculateFOV()

while not libtcod.console_is_window_closed():
    # Heartbeat
    for i in var.Entities:
        i.Be()

    # Mob turns, including player
    for i in var.Entities:
        while i.AP >= 1:
            if i.hasFlag('AVATAR'):
                # Redraw screen with each of the player's turns.
                # Draw screen:
                var.render_all(i)
                # Print screen:
                libtcod.console_flush()

            ai.getAICommand(i)

            if var.WizModeNewMap:
                Dungeon.makeMap(False)
                var.WizModeNewMap = False

            # This looks ugly...
            # Maybe soemthing like sys.exit?
            if var.ExitGame:
                break
        if var.ExitGame:
            break
    if var.ExitGame:
        break
