# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import dungeon
import entity
import ui
import var

###############################################################################
#  AI Handling
###############################################################################

def getAICommand(Mob):
    if Mob.hasFlag('AVATAR'):
        handleKeys(Mob)
    elif Mob.hasFlag('MOB'):
        if Mob.hasFlag('DEAD'):
            # TODO
            print "BUG: %s is too dead to do anything." % Mob.name
            Mob.AP -= 100
            return

        Target = None
        # Check for enemies:
        for enemy in var.Entities:
            if (Mob.getRelation(enemy) < 1 and (not enemy.hasFlag('DEAD')) and
                libtcod.map_is_in_fov(var.FOVMap, enemy.x, enemy.y)):
                Target = enemy
                Mob.goal = [enemy.x, enemy.y]
                break

        if Target != None:
            if Mob.range(Target) > 1:
                if aiMoveAStar(Mob, Target):
                    return
            elif Mob.range(Target) < 2:
                dx = Target.x - Mob.x
                dy = Target.y - Mob.y

                Mob.actionAttack(dx, dy, enemy)
                return
        elif Mob.goal != None:
            if aiMoveBase(Mob, Mob.goal[0], Mob.goal[1]):
                return
            else:
                Mob.actionWait()
        else:
            aiWander(Mob)
    else:
        # Even some items and features will be able to take turns, but not now.
        Mob.AP -= 1

###############################################################################
#  Player Input
###############################################################################
def handleKeys(Player):

    Key = libtcod.console_wait_for_keypress(True)


    # NON-TURN ACTIONS:
    # Alt+Enter goes fullscreen
    if Key.vk == libtcod.KEY_ENTER and Key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        return

    # Exit game with Ctrl + Q
    if (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('q'))):
        var.ExitGame = True
        return


    # WIZARD MODE:
    # Walk through walls
    if Key.vk == libtcod.KEY_F1:
        var.WizModeNoClip = not var.WizModeNoClip

        if var.WizModeNoClip == True:
            ui.message("Walking through walls activated.", actor = Player)
        else:
            ui.message("Walking through walls deactivated.", actor = Player)
        return

    if Key.vk == libtcod.KEY_F2:
        var.WizModeTrueSight = not var.WizModeTrueSight

        if var.WizModeNoClip == True:
            ui.message("True sight activated.", actor = Player)
        else:
            ui.message("True sight deactivated.", actor = Player)
        return

    # TODO: Instakill all.
    #if Key.vk == libtcod.KEY_F3:
    #    for i in var.Entities:
    #        if not i.hasFlag('AVATAR'):
    #            del i
    #    return

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                libtcod.console_put_char_ex(var.MapConsole, x, y, ' ', libtcod.black, libtcod.black)

        var.WizModeNewMap = True
        return


    # You can wait even when dead:
    if ((Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')) or
        libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
        Player.actionWait()
        return

    # Following actions can only be performed by living player:
    if not Player.hasFlag('DEAD'):
        # GENERAL ACTIONS:
        # Jump
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('j'))):
            where = askForDirection()
            if where != None:
                Player.actionJump(where)
                return
            else:
                # This should not take a turn.
                ui.message("You decide not to jump.", actor = Player)

        # Swap places
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('x'))):
            where = askForDirection()
            if where != None:
                x = Player.x + where[0]
                y = Player.y + where[1]

                for i in var.Entities:
                    if i.x == x and i.y == y and i.hasFlag('MOB'):
                        Player.actionSwap(i)
                        return
                ui.message("There is no one to swap with.", actor = Player)
            else:
                # This should not take a turn.
                ui.message("You decide not to swap with anyone.", actor = Player)

        # MOVEMENT:
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
            return

def askForDirection():
    ui.message("Select a direction. [dir keys]", actor = Player)
    while True:
        Key = libtcod.console_wait_for_keypress(True)

        if Key.vk == libtcod.KEY_ESCAPE:
            return None

        #if ((Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')) or
        #    libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
        #    return self TODO

        dx = 0
        dy = 0
        dz = 0

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
        # TODO: Up and down.

        if (dx != 0 or dy != 0 or dz != 0):
            return [dx, dy, dz]

###############################################################################
#  Monster Actions
###############################################################################
def aiMoveAStar(Me, Target):
    # Create a FOV map that has the dimensions of the map.
    MoveMap = libtcod.map_new(var.MapWidth, var.MapHeight)

    # Set non-walkable spaces:
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
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
    moved = False
    if not libtcod.path_is_empty(path) and libtcod.path_size(path) < 50:
        x, y = libtcod.path_walk(path, True)

        if x or y:
            dx = x - Me.x
            dy = y - Me.y

            if Me.actionBump(dx, dy):
                moved = True

    elif aiMoveBase(Me, Target.x, Target.y):
        moved = True

    libtcod.path_delete(path)
    return moved

def aiMoveBase(Me, x, y):
    if (Me.x == x and Me.y == y):
        Me.goal = None
        return False
    else:
        dx = x - Me.x
        dy = y - Me.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize it to length 1 (preserving direction), then round it and
        # convert to integer.
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not Me.actionBump(dx, dy):
            Me.goal = None
            return False
        else:
            return True

def aiSpite(Me, Enemy):
    pass
    # break weapon, spit at Enemy

def aiSuicide(Me, Enemy):
    pass

def aiWander(Me):
    x = 0
    y = 0

    while Me.isBlocked(x, y):
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

    Me.goal = [x, y]
