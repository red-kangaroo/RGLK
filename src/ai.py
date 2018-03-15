# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import sys

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
        sys.exit("You cowardly quit the game.")
        return # Not that it's needed here...


    # WIZARD MODE:
    # Walk through walls
    if Key.vk == libtcod.KEY_F1:
        var.WizModeNoClip = not var.WizModeNoClip

        if var.WizModeNoClip == True:
            ui.message("Walking through walls activated.")
        else:
            ui.message("Walking through walls deactivated.")
        return

    if Key.vk == libtcod.KEY_F2:
        var.WizModeTrueSight = not var.WizModeTrueSight

        if var.WizModeNoClip == True:
            ui.message("True sight activated.")
        else:
            ui.message("True sight deactivated.")
        return


    if Key.vk == libtcod.KEY_F3:
        for i in var.Entities:
            if not i.hasFlag('AVATAR'):
                i.receiveDamage(i.maxHP)
        return

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                libtcod.console_put_char_ex(var.MapConsole, x, y, ' ', libtcod.black, libtcod.black)

        var.WizModeNewMap = True
        return


    # You can do some stuff even when dead:
    # Wait
    if ((Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')) or
        libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
        Player.actionWait()
        return

    # Look
    if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('l'))):
        examined = askForTarget(Player, "Look around.")
        if examined != None:
            # TODO: Descriptions.
            pass
        return

    # Following actions can only be performed by living player:
    if not Player.hasFlag('DEAD'):
        # GENERAL ACTIONS:
        # Interact
        if Key.vk == libtcod.KEY_SPACE:
            where = askForDirection(Player)
            if where != None:
                Player.actionInteract(where)
            else:
                # This should not take a turn.
                ui.message("Never mind.")
            return

        # Close
        if Key.vk == libtcod.KEY_CHAR and Key.c == ord('c'):
            where = askForDirection(Player)
            if where != None:
                x = Player.x + where[0]
                y = Player.y + where[1]

                Player.actionClose(x, y)
            else:
                ui.message("Never mind.")
            return

        # Jump
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('j'))):
            where = askForDirection(Player)
            if where != None:
                Player.actionJump(where)
            else:
                # This should not take a turn.
                ui.message("You decide not to jump.")
            return # We need to return here, or we fall through to vi keys...

        # Open
        if Key.vk == libtcod.KEY_CHAR and Key.c == ord('o'):
            where = askForDirection(Player)
            if where != None:
                x = Player.x + where[0]
                y = Player.y + where[1]

                Player.actionOpen(x, y)
            else:
                ui.message("Never mind.")
            return

        # Swap places
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('x'))):
            where = askForDirection(Player)
            if where != None:
                x = Player.x + where[0]
                y = Player.y + where[1]

                for i in var.Entities:
                    if i.x == x and i.y == y and i.hasFlag('MOB'):
                        Player.actionSwap(i)
                        return
                ui.message("There is no one to swap with.")
            else:
                # This should not take a turn.
                ui.message("You decide not to swap with anyone.")
            return

        # MOVEMENT:
        dx = 0
        dy = 0

        if (libtcod.console_is_key_pressed(libtcod.KEY_UP) or
            (Key.vk == libtcod.KEY_CHAR and Key.c == ord('k')) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP8)):
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('j')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP2)):
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('h')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP4)):
            dx -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('l')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP6)):
            dx += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP7) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('y'))):
            dx -= 1
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP9) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('u'))):
            dx += 1
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP1) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('b'))):
            dx -= 1
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP3) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('n'))):
            dx += 1
            dy += 1

        if (dx != 0 or dy != 0):
            Player.actionBump(dx, dy)
            return

def askForDirection(Player):
    ui.message("Select a direction. [dir keys, Esc to exit]")
    ui.render_all(Player)
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
            (Key.vk == libtcod.KEY_CHAR and Key.c == ord('k')) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP8)):
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('j')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP2)):
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('h')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP4)):
            dx -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('l')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP6)):
            dx += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP7) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('y'))):
            dx -= 1
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP9) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('u'))):
            dx += 1
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP1) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('b'))):
            dx -= 1
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP3) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('n'))):
            dx += 1
            dy += 1
        # TODO: Up and down.

        if (dx != 0 or dy != 0 or dz != 0):
            return [dx, dy, dz]

def askForConfirmation(Player, prompt = "Really?"):
    ui.message(prompt + " [Y/n]")
    ui.render_all(Player)
    while True:
        Key = libtcod.console_wait_for_keypress(True)

        if (Key.vk == libtcod.KEY_ESCAPE or
            (Key.vk == libtcod.KEY_CHAR and Key.c == ord('n'))):
            return False

        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('y'))):
            # Requires capital Y to avoid fat-fingering with vi keys.
            return True

def askForTarget(Player, prompt = "Select a target."):
    ui.message(prompt + " [dir keys, Enter or . to confirm, Esc to exit]")
    ui.render_all(Player)

    x = Player.x
    y = Player.y

    origBack = libtcod.console_get_char_background(var.MapConsole, x, y)

    while True:
        Key = libtcod.console_wait_for_keypress(True)

        dx = 0
        dy = 0

        if (libtcod.console_is_key_pressed(libtcod.KEY_UP) or
            (Key.vk == libtcod.KEY_CHAR and Key.c == ord('k')) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP8)):
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('j')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP2)):
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('h')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP4)):
            dx -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('l')) or
              libtcod.console_is_key_pressed(libtcod.KEY_KP6)):
            dx += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP7) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('y'))):
            dx -= 1
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP9) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('u'))):
            dx += 1
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP1) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('b'))):
            dx -= 1
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_KP3) or
              (Key.vk == libtcod.KEY_CHAR and Key.c == ord('n'))):
            dx += 1
            dy += 1

        if (dx != 0 or dy != 0):
            # Move the colored cursor:
            if (x + dx > 0 or x + dx < var.MapWidth - 1 or
                y + dy > 0 or y + dy < var.MapHeight - 1):
                x = x + dx
                y = y + dy

            libtcod.console_set_char_background(var.MapConsole, x, y, libtcod.light_grey,
                                                libtcod.BKGND_SET)

            # Print what's there:
            if dungeon.map[x][y].explored == True:
                square = dungeon.map[x][y].name
            else:
                square = None

            mob = None
            stuff = []

            for i in var.Entities:
                if i.hasFlag('MOB') and i.hasFlag('SEEN') and i.x == x and i.y == y:
                    mob = i.name
                elif i.hasFlag('ITEM') and i.x == x and i.y == y:
                    stuff.append(i.name)

            if len(stuff) < 1:
                names = None
            elif len(stuff) == 1:
                names = stuff[0]
            elif len(stuff) < 3:
                names = ', '.join(stuff)
            else:
                names = 'many items'

            describeTile = ""
            describeMob = ""
            describeItems = ""

            if libtcod.map_is_in_fov(var.FOVMap, x, y):
                describeTile = "You see here %s. " % square
            elif square != None:
                describeTile = "You remember here %s. " % square

            if mob != None:
                describeMob = "There is a %s. " % mob

            if names != None:
                if libtcod.map_is_in_fov(var.FOVMap, x, y):
                    describeItems = "You see here %s." % names
                else:
                    describeItems = "You remember here %s." % names

            if square != None or mob != None or names != None:
                ui.message(describeTile + describeMob + describeItems)

            # And draw it:
            ui.render_all(Player)

        libtcod.console_set_char_background(var.MapConsole, x, y, libtcod.black,
                                            libtcod.BKGND_SET)

        if Key.vk == libtcod.KEY_ESCAPE:
            return None
        elif (Key.vk == libtcod.KEY_ENTER or
            (Key.vk == libtcod.KEY_CHAR and Key.c == ord('.'))):
            return [x, y]

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
