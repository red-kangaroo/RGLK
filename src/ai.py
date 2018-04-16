# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random
import sys

import dungeon
import entity
import game
import raw
import ui
import var

###############################################################################
#  AI Handling
###############################################################################

def getAICommand(Mob):
    if Mob == None:
        print "Handling keys for None mob, might be a bug!"
        handleKeys(Mob)
        return
    elif Mob.hasFlag('AVATAR'):
        if Mob.target != None:
            if not Mob.canSense(Mob.target):
                Mob.target = None

        handleKeys(Mob)
        return # D'oh, and I was wondering where the player's AP were leaking...
    elif Mob.hasFlag('MOB'):
        if Mob.hasFlag('DEAD'):
            print "BUG: %s is too dead to do anything." % Mob.name
            Mob.AP -= 100
            return

        if var.rand_chance(1):
            aiDoNothing(Mob)
            return

        if Mob.getBurdenState() >= 2:
            Mob.actionDrop()
            return

        aiCheckFlee(Mob)

        Target = aiFindTarget(Mob)

        if Target != None:
            if Mob.hasFlag('AI_FLEE'):
                if aiDoFlee(Mob, Target) == True:
                    return

            # TODO: ranged attacks

            if Mob.range(Target) >= 2:
                if Mob.hasFlag('AI_KITE') and Target.hasFlag('MOB'):
                    if aiKite(Mob, Target) == True:
                        return

                if aiMove(Mob, Target) == True:
                    return

            if Target.hasFlag('MOB') and Mob.range(Target) < 2:
                if Mob.getRelation(Target) < 1:
                    if Mob.hasFlag('AI_KITE') and var.rand_chance(50):
                        if aiKite(Mob, Target) == True:
                            return

                    if aiSidestep(Mob, Target) == True:
                        return

                    dx = Target.x - Mob.x
                    dy = Target.y - Mob.y

                    # Exterminate! Exterminate! Exterminate!
                    Mob.tactics = False
                    Mob.actionAttack(dx, dy, Target)
                    return
                else:
                    Target = None
                    Mob.target = None
                    return

            if Target.hasFlag('ITEM') and aiPickEquipment(Mob, Target):
                if Mob.x == Target.x and Mob.y == Target.y:
                    if Mob.actionPickUp(Mob.x, Mob.y, True) == False:
                        aiWander(Mob)
                    else:
                        for i in var.getEntity():
                            if i.target == Target:
                                i.target = None

                    return
                elif Target.BlockMove:
                    aiWander(Mob)
                else:
                    if aiMoveBase(Mob, Target.x, Target.y) == False:
                        Mob.actionWait()
                    return

        if var.rand_chance(15):
            if aiCheckInventory(Mob):
                return

        aiCheckSquare(Mob)

        if Mob.goal != None:
            if aiMoveBase(Mob, Mob.goal[0], Mob.goal[1]) == True:
                return
            elif var.rand_chance(2):
                aiWander(Mob)
            else:
                Mob.actionWait()
                return
        else:
            if var.rand_chance(30):
                # Close doors, chat with friends...
                for y in range(Mob.y - 1, Mob.y + 2):
                    for x in range(Mob.x - 1, Mob.x + 2):
                        where = [Mob.x - x, Mob.y - y, 0]

                        if Mob.actionInteract(where) == True:
                            return
            elif aiCheckInventory(Mob):
                return

        # We can't seem to be able to do anything, so find other target.
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

        if Player == None:
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
        else:
            if what == 0: # Save
                game.save()
                sys.exit("Game saved.")
                return
            elif what == 1: # Options
                ui.message("This function is unfortunately not yet supported!", libtcod.chartreuse)
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
    if Key.vk == libtcod.KEY_CHAR and Key.c == ord(';'):
        #if askForConfirmation(Player, "Do you want to activate wizard mode, cheater?"):
        # TODO
        Player.givenName = "Cheater"
        ui.message("Wizard mode activated.", libtcod.azure)
        var.WizModeActivated = True
        return

    if var.WizModeActivated and Player != None:
        # Walk through walls
        if Key.vk == libtcod.KEY_F1:
            var.WizModeNoClip = not var.WizModeNoClip

            if var.WizModeNoClip == True:
                ui.message("Walking through walls activated.")
            else:
                ui.message("Walking through walls deactivated.")
            return

        # True sight
        if Key.vk == libtcod.KEY_F2:
            var.WizModeTrueSight = not var.WizModeTrueSight

            if var.WizModeNoClip == True:
                ui.message("True sight activated.")
            else:
                ui.message("True sight deactivated.")
            return

        # Change character
        if Key.vk == libtcod.KEY_F3:
            options = [
            "Raise stats",
            "Lower stats",
            "Detach limb",
            "Create limb",
            "Restore body",
            "Gain all skills",
            "Gain all intrinsics"
            ]

            pass # TODO
            return

        # Create all items
        if Key.vk == libtcod.KEY_F4:
            for i in raw.ItemList:
                NewItem = entity.spawn(Player.x, Player.y, i, 'ITEM')
                var.getEntity().append(NewItem)

        # Summon creature
        if Key.vk == libtcod.KEY_F5:
            pass # TODO
            return

        # Possess
        if Key.vk == libtcod.KEY_F6:
            where = askForDirection(Player)

            if where == None or where == 'self':
                ui.message("Never mind.")
                return

            x = Player.x + where[0]
            y = Player.y + where[1]

            Player.actionPossess(x, y)
            return

        # Polymorph self
        if Key.vk == libtcod.KEY_F7:
            pass # TODO
            return

        # Instakill all
        if Key.vk == libtcod.KEY_F8:
            for i in var.getEntity():
                if i.hasFlag('MOB') and not i.hasFlag('AVATAR'):
                    i.receiveDamage(i.maxHP * 3, DamageType = 'NECROTIC')
            return

        # See stats
        if Key.vk == libtcod.KEY_F9:
            options = []

            for i in Player.intrinsics:
                options.append(i)

            for i in Player.getEquipment():
                for n in i.intrinsics:
                    options.append(n)

            if len(options) == 0:
                ui.message("You have no special features.")
            else:
                ui.option_menu("Your intrinsics:", options)
            return

        if Key.vk == libtcod.KEY_F10:
            return

        # Level teleport
        if Key.vk == libtcod.KEY_F11:
            where = askForDirection(Player)

            if where == None or where == 'self':
                ui.message("Never mind.")
                return
            else:
                dz = where[2]

                if dz == 0:
                    ui.message("Never mind.")
                    return

            if dz > 0:
                if var.DungeonLevel - 1 >= 0:
                    if var.Maps[var.DungeonLevel - 1] == None:
                        dungeon.makeMap(True, var.DungeonLevel - 1)

                    toClimb = [Player.x, Player.y]

                    for y in range(0, var.MapHeight):
                        for x in range(0, var.MapWidth):
                            if var.Maps[var.DungeonLevel - 1][x][y].hasFlag('STAIRS_DOWN'):
                                toClimb = [x, y]

                    Player.x = toClimb[0]
                    Player.y = toClimb[1]

                    var.Entities[var.DungeonLevel - 1].append(Player)
                    var.getEntity().remove(Player)
                    var.DungeonLevel -= 1

                    if Player.hasFlag('AVATAR'):
                        game.save()           # This is to prevent crashes from completely erasing
                        var.calculateFOVMap() # all progress you had.
                        libtcod.console_clear(var.MapConsole)

                    ui.message("You level-teleport.", libtcod.chartreuse)
                    return
                else:
                    ui.message("You cannot teleport furhter up!", libtcod.chartreuse)
                    return
            elif dz < 0:
                if var.DungeonLevel + 1 <= var.FloorMaxNumber:
                    if var.Maps[var.DungeonLevel + 1] == None:
                        dungeon.makeMap(True, var.DungeonLevel + 1)

                    toClimb = [Player.x, Player.y]

                    for y in range(0, var.MapHeight):
                        for x in range(0, var.MapWidth):
                            if var.Maps[var.DungeonLevel + 1][x][y].hasFlag('STAIRS_UP'):
                                toClimb = [x, y]

                    Player.x = toClimb[0]
                    Player.y = toClimb[1]

                    var.Entities[var.DungeonLevel + 1].append(Player)
                    var.getEntity().remove(Player)
                    var.DungeonLevel += 1

                    if Player.hasFlag('AVATAR'):
                        game.save()
                        var.calculateFOVMap()
                        libtcod.console_clear(var.MapConsole)

                    ui.message("You level-teleport.", libtcod.chartreuse)
                    return
                else:
                    ui.message("You cannot teleport furhter down!", libtcod.chartreuse)
                    return

            return # Just to be sure we'll have no fallthrough.

        # Regenerate map
        if Key.vk == libtcod.KEY_F12:
            # Heh heh, if I don't clear the console, it looks quite trippy after
            # redrawing a new map over the old one.
            libtcod.console_clear(var.MapConsole)
            var.WizModeNewMap = True
            return


    # You can do some stuff even when dead:
    # Wait
    if ((not Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord('.')) or
        libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
        if Player != None:
            Player.actionWait()
        return

    # Look
    if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('l'))):
        examined = askForTarget(Player, "Looking around.")
        if examined != None:
            # TODO: Descriptions.
            pass
        return

    # Message history
    if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('m'))):
        ui.text_menu("Message history:", var.MessageHistory)
        return

    # Take a screenshot
    #if Key.vk == libtcod.KEY_CHAR and Key.c == ord(';'):
    #    libtcod.sys_save_screenshot('screenshots/screenshot.png')
    #    ui.message("Screenshot saved.", color = libtcod.chartreuse)
    #    return

    # Following actions can only be performed by living player:
    if Player == None:
        return
    if not Player.hasFlag('DEAD'):
        # GENERAL ACTIONS:
        # Interact
        if Key.vk == libtcod.KEY_SPACE:
            where = askForDirection(Player)
            if where == 'self':
                # TODO
                ui.message("You should not play with yourself right now!")
            elif where != None:
                Player.actionInteract(where)
            else:
                # This should not take a turn.
                ui.message("Never mind.")
            return

        # Apply
        if Key.vk == libtcod.KEY_CHAR and Key.c == ord('a'):
            options = []

            for i in Player.inventory:
                if i.hasFlag('APPLY'):
                    options.append(i)

            if len(options) == 0:
                ui.message("You have nothing to apply.")
                return

            toApply = ui.option_menu("Apply what?", options)

            if toApply == None:
                ui.message("Never mind.")
                return

            where = askForDirection(Player)
            if where == 'self':
                dx = 0
                dy = 0
            elif where != None:
                dx = where[0]
                dy = where[1]
            else:
                ui.message("Never mind.")
                return

            Player.actionApply(options[toApply], dx, dy)
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
            if where == 'self':
                ui.message("You feel very close minded.")
            elif where != None:
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

        # Equipment
        if (Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord('e')):
            while Player.actionEquipment() == True:
                pass # Return to menu.
            ui.message("You change equipment.")
            return

        if (Key.lctrl and Key.vk == libtcod.KEY_CHAR and Key.c == ord('e')):
            Player.actionAutoEquip()
            ui.message("You change equipment.")
            return

        # Inventory
        if (Key.vk == libtcod.KEY_CHAR and Key.c == ord('i')):
            while Player.actionInventory() == True:
                pass
            return

        # Jump
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('j'))):
            where = askForDirection(Player)
            if where == 'self':
                Player.actionJump([0, 0, 0])
            elif where != None:
                Player.actionJump(where)
            else:
                # This should not take a turn.
                ui.message("You decide not to jump.")
            return # We need to return here, or we fall through to vi keys...

        # Open
        if Key.vk == libtcod.KEY_CHAR and Key.c == ord('o'):
            where = askForDirection(Player)
            if where == 'self':
                Player.actionLoot(where)
            elif where != None:
                if Player.actionLoot(where, True):
                    return
                else:
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

        # Quaff
        if not Key.shift and Key.vk == libtcod.KEY_CHAR and Key.c == ord('q'):
            Player.actionQuaff()
            return

        # Save game
        if (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('s'))):
            ui.message("Saving...", libtcod.chartreuse)
            waitForMore(Player)
            game.save()
            sys.exit("Game saved.")
            return

        # Tunnel
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('t'))):
            if Player.hasIntrinsic('CAN_DIG') or Player.hasIntrinsic('CAN_CHOP'):
                where = askForDirection(Player)

                if where == None or where == 'self':
                    # This should not take a turn.
                    ui.message("Never mind.")
                    return
                else:
                    dx = where[0]
                    dy = where[1]

                    if dx != 0 or dy != 0:
                        Player.actionDig(dx, dy)
                        return
                    else:
                        ui.message("Never mind.")
                        return
            else:
                ui.message("You need the right tools to do that.")
            return

        # Swap places
        if (Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('x'))):
            where = askForDirection(Player)
            if where != None and where != 'self':
                x = Player.x + where[0]
                y = Player.y + where[1]

                for i in var.getEntity():
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

        # Tactics
        if Key.vk == libtcod.KEY_TAB:
            Player.tactics = not Player.tactics
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
    ui.message("Select a direction. [dir keys; Esc to exit]", color = libtcod.chartreuse)
    ui.render_all(Player)
    while True:
        Key = libtcod.console_wait_for_keypress(True)

        if Key.vk == libtcod.KEY_ESCAPE:
            return None

        if ((not Key.shift and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('.'))) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP5)):
            return 'self'

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
    ui.message(prompt + " [Y/n]", color = libtcod.chartreuse)
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
    ui.message(prompt + " [dir keys; Enter or . to confirm; Esc to exit]", color = libtcod.chartreuse)
    ui.render_all(Player)

    # This is because we may have None player, if their body got destroyed and they
    # are looking around after death.
    try:
        x = Player.x
        y = Player.y
    except:
        x = var.MapWidth / 2
        y = var.MapHeight / 2

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
            if var.getMap()[x][y].isExplored():
                square = var.getMap()[x][y].name
            else:
                square = None

            mob = None
            stuff = []

            for i in var.getEntity():
                try:
                    if Player.canSense(i):
                        sensed = True
                    else:
                        sensed = False
                except:
                    sensed = True

                if sensed:
                    if i.hasFlag('MOB') and i.x == x and i.y == y:
                        mob = i.getName()
                    elif i.hasFlag('ITEM') and i.x == x and i.y == y:
                        stuff.append(i.getName())

            if len(stuff) < 1:
                names = None
            elif len(stuff) == 1:
                names = stuff[0]
            elif len(stuff) <= 3:
                names = ', '.join(stuff)
            else:
                names = 'many items'

            describeTile = ""
            describeMob = ""
            describeItems = ""

            if (libtcod.map_is_in_fov(var.FOVMap, x, y) and not (Player == None or
                (Player.hasFlag('CANNOT_SEE') or Player.hasIntrinsic('BLIND')))):
                describeTile = "You see here %s. " % square
            elif square != None:
                describeTile = "You remember here %s. " % square

            if mob != None:
                describeMob = "There is %s. " % mob

            if names != None:
                if (libtcod.map_is_in_fov(var.FOVMap, x, y) and not (Player == None or
                    (Player.hasFlag('CANNOT_SEE') or Player.hasIntrinsic('BLIND')))):
                    describeItems = "You see here %s. " % names
                else:
                    describeItems = "You remember here %s. " % names

            # Wizard mode:
            if var.WizModeActivated and Player != None:
                dist = str(Player.distance(x, y))
                blocked = Player.isBlocked(x, y, var.DungeonLevel)

                describeWizard = "Distance: %s. Blocked: %s." % (dist, blocked)
            else:
                describeWizard = ""

            if square != None or mob != None or names != None:
                ui.message(describeTile + describeMob + describeItems + describeWizard)

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
    ui.message("Press Enter, Space or Esc for more.", color = libtcod.chartreuse)
    ui.render_all(Player)

    while True:
        Key = libtcod.console_wait_for_keypress(True)

        if (Key.vk == libtcod.KEY_ESCAPE or Key.vk == libtcod.KEY_ENTER or
            Key.vk == libtcod.KEY_SPACE):
            return

###############################################################################
#  Monster Actions
###############################################################################
def aiDoNothing(Me):
    # This prevents hang-ups when I screw up some AI loop. ;)
    Me.target = None
    Me.goal = None
    Me.actionWait()

def aiCheckFlee(Mob):
    if (Mob.SP <= 0 or Mob.HP <= (Mob.maxHP / 20)):
        if not Mob.hasFlag('AI_FLEE'):
            Mob.flags.append('AI_FLEE') # Start fleeing behaviour.
            Mob.tactics = True          # Switch to defensive.
            ui.message("%s flee&S." % Mob.getName(True), actor = Mob)

    if Mob.hasFlag('AI_FLEE'):
        stop = False

        if Mob.SP >= (Mob.maxSP / 2) and Mob.HP >= (Mob.maxHP / 2):
            stop = True

        if Mob.SP == Mob.maxSP:
            stop = True

        if stop:
            for i in Mob.flags:                 # I had a bug here that would cause
                if i == 'AI_FLEE':              # mobs to never stop fleeing. This
                    Mob.flags.remove('AI_FLEE') # cannot happen anymore.
                    ui.message("%s no longer flee&S." % Mob.getName(True), actor = Mob)

def aiDoFlee(Me, Target):
    if not Me.hasFlag('AI_FLEE'):
        return False
    elif Target == None or not Me.canSense(Target):
        Me.actionWait()
        return True
    else:
        if aiKite(Me, Target) == True:
            return True

        # We failed to move away, so find a friendly target and run for help.
        fails = 0
        Other = None

        while fails < 10:
            Other = random.choice(var.getEntity())

            if Other.hasFlag('MOB'):
                if Me.getRelation(Other) == 1:
                    Me.target = Other
                    break

        if Me.target != None and Me.target != Target:
            if aiMove(Me, Me.target) == True:
                return True

        # We can do nothing. :) But randomly stop fleeing, because sometimes when
        # cornered, you will find the strength to fight some more.
        if Me.hasFlag('HUMANOID'):
            ui.message("%s scream&S like a girl." % Me.getName(True), actor = Me)
        else:
            ui.message("%s shriek&S in terror." % Me.getName(True), actor = Me)

        return False

def aiFindTarget(Mob):
    Target = None

    # Check monster's remembered target:
    if Mob.target != None:
        # Monsters may forget about targets they don't see.
        if (not Mob.canSense(Mob.target) and var.rand_chance(5)):
            Mob.target = None

        # This prevents looking for target that was picked up or something:
        for i in var.getEntity():
            if i == Mob.target:
                Target = Mob.target
                break

        if Target == None:
            Mob.target = None

    # Check for enemies:
    for i in var.getEntity():
        if Mob.canSense(i):
            if i.hasFlag('MOB'):
                if Mob.getRelation(i) < 1 and not i.hasFlag('DEAD'):
                    if Target == None or Mob.range(i) < 4:
                        Target = i
                        Mob.goal = [i.x, i.y]
                        Mob.target = Target
                        break
            elif i.hasFlag('ITEM'):
                if Mob.hasFlag('AI_SCAVENGER') and var.rand_chance(75):
                    if not Mob.isBlocked(i.x, i.y, var.DungeonLevel): # We cannot pick up boulders...
                        Target = i
                        Mob.goal = [i.x, i.y]
                        Mob.target = Target
                        break
                elif var.rand_chance(20):
                    if aiPickEquipment(Mob, i):
                        Target = i
                        Mob.goal = [i.x, i.y]
                        break

    return Target

def aiKite(Me, Target):
    if Me.range(Target) >= Me.getLightRadius():
        return False

    distance = Me.range(Target)
    goal = None

    for y in range(Me.y - 1, Me.y + 2):
        for x in range(Me.x - 1, Me.x + 2):
            if x in range(0, var.MapWidth - 1) and y in range(0, var.MapHeight - 1):
                if (not Me.isBlocked(x, y, var.DungeonLevel) or
                    var.getMap()[x][y].hasFlag('CAN_BE_OPENED')):
                    if Target.distance(x, y) > distance:
                        distance = Target.distance(x, y)
                        goal = [x, y]

    if goal != None:
        Me.goal = goal
        if aiMoveBase(Me, goal[0], goal[1]) == True:
            return True

    return False

def aiMove(Me, Target):
    Me.tactics = True  # We want mobs that try to move past the player to be
                       # defensive rather than aggresive.
    if Me.hasFlag('AI_DIJKSTRA'):
        return aiMoveDijkstra(Me, Target)
    else:
        return aiMoveAStar(Me, Target)

def aiMoveAStar(Me, Target):
    # Create a map that has the dimensions of the map.
    MoveMap = libtcod.map_new(var.MapWidth, var.MapHeight)

    # Set non-walkable spaces:
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            libtcod.map_set_properties(MoveMap, x, y, not var.getMap()[x][y].BlockSight,
                                       (not var.getMap()[x][y].BlockMove or
                                       var.getMap()[x][y].hasFlag('CAN_BE_OPENED')))
    for i in var.getEntity():
        if i.BlockMove == True and i != Me and i != Target:
            libtcod.map_set_properties(MoveMap, i.x, i.y, True, not i.BlockMove)

    path = libtcod.path_new_using_map(MoveMap, 1.41)
    libtcod.path_compute(path, Me.x, Me.y, Target.x, Target.y)

    # Check if the path exists, and in this case, also the path is shorter than 25 tiles.
    # The path size matters for alternative longer paths (for example through other rooms
    # if the player is in a corridor).
    moved = False
    if (not libtcod.path_is_empty(path) and libtcod.path_size(path) < 25 and
        libtcod.path_size(path) >= 1):
        x, y = libtcod.path_walk(path, True)

        if x or y:
            dx = x - Me.x
            dy = y - Me.y

            if dx != 0 or dy != 0:
                if Me.actionBump(dx, dy) == True:
                    moved = True

    if moved == False:
        if aiMoveBase(Me, Target.x, Target.y) == True:
            #print "failed A*, moving base"
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

def aiMoveDijkstra(Me, Target):
    # Create a map that has the dimensions of the map.
    MoveMap = libtcod.map_new(var.MapWidth, var.MapHeight)

    # Set non-walkable spaces:
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            libtcod.map_set_properties(MoveMap, x, y, not var.getMap()[x][y].BlockSight,
                                       (not var.getMap()[x][y].BlockMove or
                                       var.getMap()[x][y].hasFlag('CAN_BE_OPENED')))
    for i in var.getEntity():
        if i.BlockMove == True and i != Me and i != Target:
            libtcod.map_set_properties(MoveMap, i.x, i.y, True, not i.BlockMove)

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

def aiCheckSquare(Me):
    for i in var.getEntity():
        if i.hasFlag('ITEM') and i.x == Me.x and i.y == Me.y:
            if aiPickEquipment(Me, i):
                Me.target = i
                Me.goal = [i.x, i.y]
                return

def aiCheckInventory(Me):
    # Pick best items from inventory to use.
    if len(Me.inventory) == 0:
        return False

    Me.actionAutoEquip()
    return True

def aiPickEquipment(Me, item):
    # Do we want to pick up this item?
    if not item.hasFlag('ITEM'):
        return False
    if Me.getBurdenState() >= 2:
        return False

    if Me.hasFlag('AI_SCAVENGER'):
        return True

    slot = item.getSlot()
    mySlots = 0
    myItems = []

    for part in Me.bodyparts:
        if part.getSlot() == slot:
            mySlots += 1

            if len(part.inventory) == 0:
                if part.hasFlag('GRASP'):
                    myItems.append(part)
            else:
                for equip in part.inventory:
                    myItems.append(equip)

    if mySlots > 0:
        if len(myItems) == 0:
            return True

        while mySlots > 0:
            for equip in myItems:
                if item.getCoolness() >= equip.getCoolness():
                    return True

            mySlots -= 1
    else:
        return False

def aiSidestep(Me, Target):
    # We want to sometimes sidestep player to allow others to join us.
    friends = False

    for i in var.getEntity():
        if i.hasFlag('MOB'):
            if (i != Me and i != Target and i.range(Me) < 2 and
                i.getRelation(Target) < 1):
                friends = True
                break

    if friends == True and var.rand_chance(20):
        dx = 0
        dy = 0

        for y in range(Me.y - 1, Me.y + 2):
            for x in range(Me.x - 1, Me.x + 2):
                if (x in range(0, var.MapWidth - 1) and
                    y in range(0, var.MapHeight - 1)):
                    if Me.isBlocked(x, y, var.DungeonLevel) == False:
                        if Target.distance(x, y) < 2:
                            dx = x - Me.x
                            dy = y - Me.y
                            break

        if dx != 0 or dy != 0:
            if Me.actionBump(dx, dy) == True:
                return True

    return False

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

    while Me.isBlocked(x, y, var.DungeonLevel) == True:
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

    Me.goal = [x, y]
