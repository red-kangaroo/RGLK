# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random
import sys

import entity
import game
import ui
import var

###############################################################################
#  AI Handling
###############################################################################

def getAICommand(Mob):
    if Mob.hasFlag('AVATAR'):
        if Mob.target != None:
            if not libtcod.map_is_in_fov(var.FOVMap, Mob.target.x, Mob.target.y):
                Mob.target = None

        handleKeys(Mob)
        return # D'oh, and I was wondering where the player's AP were leaking...
    elif Mob.hasFlag('MOB'):
        if Mob.hasFlag('DEAD'):
            print "BUG: %s is too dead to do anything." % Mob.name
            Mob.AP -= 100
            return

        if var.rand_chance(1):
            # This prevents hang-ups when I screw up some AI loop. ;)
            Mob.target = None
            Mob.goal = None
            Mob.actionWait()
            return

        if (len(Mob.inventory) > Mob.carry):
            Mob.actionDrop()
            return

        if (Mob.SP <= 0 or Mob.HP <= (Mob.maxHP / 10)):
            Mob.flags.append('AI_FLEE')
            print "%s flees." % Mob.name

        if (Mob.hasFlag('AI_FLEE') and Mob.SP >= (Mob.maxSP / 2) and
              Mob.HP >= (Mob.maxHP / 2)):
            Mob.flags.remove('AI_FLEE')
            print "%s no longer flees." % Mob.name

        Target = None

        if Mob.target != None:
            #for i in var.Entities[var.DungeonLevel]:
            #    if i.target == Mob.target:
            #        Mob.target = None
            #        break

            if (not libtcod.map_is_in_fov(var.FOVMap, Mob.target.x, Mob.target.y) and
                var.rand_chance(15)):
                Mob.target == None
                return

            # This prevents looking for target that was picked up or something:
            for i in var.Entities[var.DungeonLevel]:
                if i == Mob.target:
                    Target = Mob.target
                    break

            if Target == None:
                Mob.target = None

        if Target == None:
            # Check for enemies:
            for i in var.Entities[var.DungeonLevel]:
                if i.hasFlag('MOB') and libtcod.map_is_in_fov(var.FOVMap, i.x, i.y):
                    if Mob.getRelation(i) < 1 and not i.hasFlag('DEAD'):
                        Target = i
                        Mob.goal = [i.x, i.y]
                        Mob.target = Target
                        break
                elif i.hasFlag('ITEM') and libtcod.map_is_in_fov(var.FOVMap, i.x, i.y):
                    if Mob.hasFlag('AI_SCAVENGER') and not (len(Mob.inventory) >= Mob.carry):
                        Target = i
                        Mob.goal = [i.x, i.y]
                        Mob.target = Target
                        break

        if Target != None:
            if Mob.hasFlag('AI_FLEE'):
                if aiFlee(Mob, Target) == True:
                    return

            # TODO: ranged attacks

            if Mob.range(Target) > 1:
                if Mob.hasFlag('AI_KITE'):
                    if aiKite(Mob, Target) == True:
                        return

                if aiMove(Mob, Target) == True:
                    return

            if Target.hasFlag('MOB') and Mob.range(Target) < 2:
                if Mob.getRelation(Target) < 1:
                    if Mob.hasFlag('AI_KITE') and var.rand_chance(50):
                        if aiKite(Mob, Target) == True:
                            return

                    dx = Target.x - Mob.x
                    dy = Target.y - Mob.y

                    # We want to sometimes sidestep player to allow others to join us.
                    friends = False

                    for i in var.Entities[var.DungeonLevel]:
                        if (i != Mob and i != Target and i.range(Mob) < 2 and
                            i.getRelation(Target) < 1):
                            friends = True
                            break

                    if friends == True and var.rand_chance(20):
                        for y in range(Mob.y - 1, Mob.y + 2):
                            for x in range(Mob.x - 1, Mob.x + 2):
                                if (x in range(0, var.MapWidth - 1) and
                                    y in range(0, var.MapHeight - 1)):
                                    if var.Maps[var.DungeonLevel][x][y].BlockMove == False:
                                        if Target.distance(x, y) < 2:
                                            dx = x - Mob.x
                                            dy = y - Mob.y
                                            break
                        Mob.actionBump(dx, dy)
                        return

                    # Exterminate! Exterminate! Exterminate!
                    Mob.actionAttack(dx, dy, Target)
                    return
                else:
                    Target = None
                    Mob.target = None
                    return

            if Target.hasFlag('ITEM') and Mob.hasFlag('AI_SCAVENGER'):
                if Mob.x == Target.x and Mob.y == Target.y:
                    Mob.actionPickUp(Mob.x, Mob.y, True)

                    for i in var.Entities[var.DungeonLevel]:
                        if i.target == Target:
                            i.target = None

                    Target = None
                    return
                else:
                    if aiMoveBase(Mob, Target.x, Target.y) == False:
                        Mob.actionWait()
                    return

            # We can't seem to be able to do anything, so find other target.
            aiWander(Mob)
            Mob.actionWait()
            return

        if Mob.goal != None:
            if aiMoveBase(Mob, Mob.goal[0], Mob.goal[1]) == True:
                return
            elif var.rand_chance(2):
                aiWander(Mob)
            else:
                Mob.actionWait()
                return
        else:
            if var.rand_chance(50):
                # Close doors, chat with friends...
                for y in range(Mob.y - 1, Mob.y + 2):
                    for x in range(Mob.x - 1, Mob.x + 2):
                        where = [Mob.x - x, Mob.y - y]

                        if Mob.actionInteract(where) == True:
                            return
            else:
                aiWander(Mob)
                Mob.actionWait()
                return

    # Even some items and features will be able to take turns, but not now.
    Mob.AP -= 1

###############################################################################
#  Player Input
###############################################################################
def handleKeys(Player):

    Key = libtcod.console_wait_for_keypress(True)


    # NON-TURN ACTIONS:
    # Escape for main menu
    if Key.vk == libtcod.KEY_ESCAPE:
        what = ui.main_menu(Player)

        if what == 0: # Save
            game.save()
            sys.exit("Game saved.")
            return
        elif what == 1: # Options
            ui.message("This function is unfortunately not yet supported!", libtcod.yellow)
            return
        if what == 2: # Quit
            sys.exit("You cowardly quit the game.")
            return
        else:
            return

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
        for i in var.Entities[var.DungeonLevel]:
            if not i.hasFlag('AVATAR'):
                i.receiveDamage(i.maxHP)
        return

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        var.WizModeNewMap = True
        return


    # You can do some stuff even when dead:
    # Wait
    if ((not Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')) or
        libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
        Player.actionWait()
        return

    # Inventory
    if (Key.vk == libtcod.KEY_CHAR and Key.c == ord('i')):
        Player.actionInventory()
        return

    # Look
    if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('l'))):
        examined = askForTarget(Player, "Looking around.")
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

        # Climb up and down
        if Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord(','):
            Player.actionClimb(1)
            return

        if Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord('.'):
            Player.actionClimb(-1)
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

        # Drop
        if Key.vk == libtcod.KEY_CHAR and Key.c == ord('d'):
            while Player.actionDrop() == True:
                pass # Return to menu if something remains to drop.
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

        # Jump
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('m'))):
            ui.text_menu("Message history:", var.MessageHistory)
            return

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

        # Pick all
        # Must be before non-modified key!!!
        if ((Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('g'))) or
            (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord(',')))):
            Player.actionPickUp(Player.x, Player.y, pickAll = True)
            return

        # Pick up
        if ((Key.vk == libtcod.KEY_CHAR and Key.c == ord('g')) or
            (Key.vk == libtcod.KEY_CHAR and Key.c == ord(','))):
            while Player.actionPickUp(Player.x, Player.y) == True:
                pass # Return to menu if something remains to pick up.
            return

        # Save game
        if (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('s'))):
            ui.message("Saving...", libtcod.yellow)
            waitForMore(Player)
            game.save()
            sys.exit("Game saved.")
            return

        # Swap places
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('x'))):
            where = askForDirection(Player)
            if where != None:
                x = Player.x + where[0]
                y = Player.y + where[1]

                for i in var.Entities[var.DungeonLevel]:
                    if (i.x == x and i.y == y and (i.hasFlag('MOB') or
                       (i.BlockMove == True and i.hasFlag('ITEM'))) and
                        not i == Player):
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
    ui.message("Select a direction. [dir keys; Esc to exit]")
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
        elif (Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord(',')):
            dz += 1
        elif (Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')):
            dz -= 1

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

def askForTarget(Player, prompt = "Select a target.", Range = None):
    ui.message(prompt + " [dir keys; Enter or . to confirm; Esc to exit]")
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
                if Range != None:
                    if Player.distance(x + dx, y + dy) <= Range:
                        x = x + dx
                        y = y + dy
                    else:
                        ui.message("Out of range!")
                        ui.render_all(Player)
                        continue
                else:
                    x = x + dx
                    y = y + dy

            libtcod.console_set_char_background(var.MapConsole, x, y, libtcod.light_grey,
                                                libtcod.BKGND_SET)

            # Print what's there:
            if var.Maps[var.DungeonLevel][x][y].explored == True:
                square = var.Maps[var.DungeonLevel][x][y].name
            else:
                square = None

            mob = None
            stuff = []

            for i in var.Entities[var.DungeonLevel]:
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

def waitForMore(Player):
    ui.message("Press Enter, Space or Esc for more.", color = libtcod.yellow)
    ui.render_all(Player)

    while True:
        Key = libtcod.console_wait_for_keypress(True)

        if (Key.vk == libtcod.KEY_ESCAPE or Key.vk == libtcod.KEY_ENTER or
            Key.vk == libtcod.KEY_SPACE):
            return

###############################################################################
#  Monster Actions
###############################################################################
def aiFlee(Me, Target):
    if not Me.hasFlag('AI_FLEE'):
        return False
    elif Target == None or not libtcod.map_is_in_fov(var.FOVMap, Target.x, Target.y):
        Me.actionWait()
        return True
    else:
        if aiKite(Me, Target) == True:
            return True

        # We failed to move away, so find a friendly target and run for help.
        fails = 0
        Other = None

        while fails < 100:
            Other = random.choice(var.Entities[var.DungeonLevel])

            if Other.hasFlag('MOB'):
                if Me.getRelation(Other) == 1:
                    Me.target = Other
                    break

        if Me.target != None and Me.target != Target:
            if aiMove(Me, Me.target) == True:
                return True

        ui.message("%s screams like a girl." % (str.capitalize(Me.name)), actor = Me)
        Me.actionWait()
        return False

def aiKite(Me, Target):
    if Me.range(Target) >= Me.FOVRadius:
        return False

    distance = Me.range(Target)
    goal = None

    for y in range(Me.y - 1, Me.y + 2):
        for x in range(Me.x - 1, Me.x + 2):
            if x in range(0, var.MapWidth - 1) and y in range(0, var.MapHeight - 1):
                if var.Maps[var.DungeonLevel][x][y].BlockMove == False:
                    if Target.distance(x, y) > distance:
                        distance = Target.distance(x, y)
                        goal = [x, y]

    if goal != None:
        Me.goal = goal
        if aiMoveBase(Me, goal[0], goal[1]) == True:
            return True

    return False

def aiMove(Me, Target):
    # Create a map that has the dimensions of the map.
    MoveMap = libtcod.map_new(var.MapWidth, var.MapHeight)

    # Set non-walkable spaces:
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            libtcod.map_set_properties(MoveMap, x, y, not var.Maps[var.DungeonLevel][x][y].BlockSight,
                    (not var.Maps[var.DungeonLevel][x][y].BlockMove or var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_OPENED')))
    for i in var.Entities[var.DungeonLevel]:
        if i.BlockMove and i != Me and i != Target:
            libtcod.map_set_properties(MoveMap, i.x, i.y, True, not i.BlockMove)

    if Me.hasFlag('AI_DIJKSTRA'):
        if aiMoveDijkstra(Me, Target, MoveMap) == True:
            return True
    if Me.Wit > -3:
        if aiMoveAStar(Me, Target, MoveMap) == True:
            return True

    if Me.hasFlag('AI_FLEE'):
        flee = True
    else:
        flee = False

    aiMoveBase(Me, Target.x, Target.y, flee)

def aiMoveAStar(Me, Target, MoveMap):
    path = libtcod.path_new_using_map(MoveMap, 1.41)
    libtcod.path_compute(path, Me.x, Me.y, Target.x, Target.y)

    # Check if the path exists, and in this case, also the path is shorter than 25 tiles.
    # The path size matters for alternative longer paths (for example through other rooms
    # if the player is in a corridor).
    moved = False
    if (not libtcod.path_is_empty(path) and libtcod.path_size(path) < 25 and
        libtcod.path_size(path) > 1):
        x, y = libtcod.path_walk(path, True)

        if x or y:
            dx = x - Me.x
            dy = y - Me.y

            if Me.actionBump(dx, dy) == True:
                moved = True

    elif aiMoveBase(Me, Target.x, Target.y) == True:
        moved = True

    libtcod.path_delete(path)
    return moved

def aiMoveBase(Me, x, y, flee = False):
    if (Me.x == x and Me.y == y):
        Me.target = None
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

        if flee == True:
            dx = -dx
            dy = -dy

        if Me.actionBump(dx, dy) == False:
            Me.actionWait()
            Me.target = None
            Me.goal = None
            return False
        else:
            return True

def aiMoveDijkstra(Me, Target, MoveMap):
    path = libtcod.dijkstra_new(MoveMap, 1.41)
    libtcod.dijkstra_compute(path, Me.x, Me.y)
    libtcod.dijkstra_path_set(path, Target.x, Target.y)

    # Check if the path exists and walk it:
    moved = False
    if (not libtcod.dijkstra_is_empty(path) and libtcod.dijkstra_size(path) < 25 and
        libtcod.dijkstra_size(path) > 1):
        x, y = libtcod.dijkstra_path_walk(path)

        if x or y:
            dx = x - Me.x
            dy = y - Me.y

            if Me.actionBump(dx, dy) == True:
                moved = True

    elif aiMoveBase(Me, Target.x, Target.y) == True:
        moved = True

    libtcod.dijkstra_delete(path)
    return moved

def aiSpite(Me, Enemy):
    pass
    # break weapon, spit at Enemy etc.

def aiSuicide(Me, Enemy):
    pass

def aiWander(Me):
    Me.target = None
    Me.goal = None

    x = 0
    y = 0

    while Me.isBlocked(x, y) == True:
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

    Me.goal = [x, y]
