# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

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
Player = entity.Mob(1, 1, '@', libtcod.white, 'Player', 0, 0, 0)
var.Entities.append(Player)

###############################################################################
#  Functions
###############################################################################

# Player input
def handle_keys():

    Key = libtcod.console_wait_for_keypress(True)

    # Alt+Enter goes fullscreen
    if Key.vk == libtcod.KEY_ENTER and Key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # Exit game with Ctrl + Q
    if (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('q'))):
        return 'exit'


    # WIZARD MODE:
    # Walk through walls
    if Key.vk == libtcod.KEY_F1:
        var.WizModeNoClip
        var.WizModeNoClip = not var.WizModeNoClip

    if Key.vk == libtcod.KEY_F2:
        var.WizModeTrueSight
        var.WizModeTrueSight = not var.WizModeTrueSight

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                libtcod.console_put_char_ex(var.Con, x, y, ' ', libtcod.black, libtcod.black)
        # Does not work with monster generation, TODO?

        Dungeon.makeMap(False)


    # MOVEMENT:
    if not var.PlayerIsDead:
        dx = 0
        dy = 0

        if (libtcod.console_is_key_pressed(libtcod.KEY_UP) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP8)):
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP2)):
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP4)):
            dx -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP6)):
            dx += 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
            dx -= 1
            dy -= 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
            dx += 1
            dy -= 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
            dx -= 1
            dy += 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
            dx += 1
            dy += 1

        if (dx != 0 or dy != 0):
            Player.actionBump(dx, dy)

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
Player.UpdateFOV()

while not libtcod.console_is_window_closed():
    for i in var.Entities:
        # How else to check if entity has a speed variable?
        try:
            i.AP += i.speed
        except:
            i.AP += 1

    # Player turn
    while Player.AP >= 1:
        # Redraw screen with each of the player's turns.
        # Draw screen:
        render_all()
        # Print screen:
        libtcod.console_flush()
        # Handle player input
        Exit = handle_keys()
        if Exit == 'exit':
            break
    # This looks ugly...
    if Exit == 'exit':
        break

    # Monster turn
    #for i in var.Entities:
    #    while i.AP >= 1:
    #        handle_monsters(i)
