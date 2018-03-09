# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import entity
import var

###############################################################################
#  AI
###############################################################################

def getAICommand(Mob):
    if Mob.isAvatar == True:
        handle_keys(Mob)
    else:
        # Check for enemies:
        for enemy in var.Entities:
            if (enemy.isAvatar == True and libtcod.map_is_in_fov(self.FOVMap, enemy.x, enemy.y)):
                if Mob.range(enemy) > 1:
                    aiMove(Mob, enemy)
                    return
                elif Mob.range(enemy) == 1:
                    dx = enemy.x - Mob.x
                    dy = enemy.y - Mob.y

                    Mob.actionAttack(dx, dy, enemy)
                    return

        if Mob.goal != None:
            aiMove(Mob, goal)
        Mob.actionWait()
        return

# Player input
def handle_keys(Player):

    Key = libtcod.console_wait_for_keypress(True)

    # Alt+Enter goes fullscreen
    if Key.vk == libtcod.KEY_ENTER and Key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # Exit game with Ctrl + Q
    if (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('q'))):
        var.ExitGame = True


    # WIZARD MODE:
    # Walk through walls
    if Key.vk == libtcod.KEY_F1:
        var.WizModeNoClip = not var.WizModeNoClip

    if Key.vk == libtcod.KEY_F2:
        var.WizModeTrueSight = not var.WizModeTrueSight

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                libtcod.console_put_char_ex(var.Con, x, y, ' ', libtcod.black, libtcod.black)

        var.WizModeNewMap = True


    # MOVEMENT:
    if not var.PlayerIsDead:
        if ((Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
            Player.actionWait()
            return

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

# Monster Actions
def aiMove(Me, Target):
    # Create a FOV map that has the dimensions of the map.
    MoveMap = libtcod.map_new(var.MapWight, var.MapHeight)

    # Set non-walkable spaces:
    for y in range(var.MapHeight):
        for x in range(var.MapWight):
            libtcod.map_set_properties(MoveMap, x, y, not dungeon.map[x][y].BlockSight,
                                       not dungeon.map[x][y].BlockMove)
    for i in var.Entities:
        if i.BlockMove and i != Me and i != Target:
            libtcod.map_set_properties(MoveMap, i.x, i.y, True, not i.BlockMove)

    path = libtcod.path_new_using_map(MoveMap, 1.41)
    libtcod.path_compute(path, Me.x, Me.y, Target.x, Target.y)

    # Check if the path exists, and in this case, also the path is shorter than 25 tiles.
    # The path size matters for alternative longer paths (for example through other rooms
    # if the player is in a corridor).
    if not libtcod.path_is_empty(path) and libtcod.path_size(path) < 50:
        x, y = libtcod.path_walk(path, True)

        if x or y:
            dx = x - Me.x
            dy = y - Me.y

            Me.actionWalk(dx, dy)