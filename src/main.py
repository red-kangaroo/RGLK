# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import ai
import dungeon
import entity
import var

###############################################################################
#  Objects
###############################################################################


###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(var.ScreenWidth, var.ScreenHeight, 'RGLK', False)

# Player must be defined here, we work with him shortly.
Player = entity.Mob(1, 1, '@', libtcod.white, 'Player', 0, 0, 0, 1.0, 6, True)
var.Entities.append(Player)

###############################################################################
#  Functions
###############################################################################

def render_all():
    for y in range(var.MapHeight):
        for x in range(var.MapWight):
            tile = dungeon.map[x][y]
            tile.draw(x, y)

    for mob in var.Entities:
        if mob != Player:
            mob.draw()
    # Draw player last, over everything else.
    Player.draw()

    libtcod.console_blit(var.Con, 0, 0, var.ScreenWidth, var.ScreenHeight, 0, 0, 0)

###############################################################################
#  Main Loop
###############################################################################

Dungeon = dungeon.Builder()
Dungeon.makeMap(True)
Player.recalculateFOV()

while not libtcod.console_is_window_closed():
    # Heartbeat
    for i in var.Entities:
        # How else to check if entity has a speed variable?
        try:
            i.AP += i.speed
        except:
            i.AP += 1

    # Mob turns, including player
    for i in var.Entities:
        while i.AP >= 1:
            if i == Player:
                # Redraw screen with each of the player's turns.
                # Draw screen:
                render_all()
                # Print screen:
                libtcod.console_flush()

            ai.getAICommand(i)

            if var.WizModeNewMap:
                Dungeon.makeMap(False)
                var.WizModeNewMap = False

            # This looks ugly...
            if var.ExitGame:
                break
        if var.ExitGame:
            break
    if var.ExitGame:
        break
