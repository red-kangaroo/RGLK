# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import ai
import dungeon
import monster as mon
import terrain as ter
import ui
import var

###############################################################################
#  Entities
###############################################################################

def spawn(x, y, BluePrint):
    # Careful, will only work for mobs now.
    try:
        char = BluePrint['char']
        color = BluePrint['color']
        name = BluePrint['name']
    except:
        print "Failed to spawn a monster."
        return False

    try:
        Str = BluePrint['Str']
    except:
        Str = mon.Dummy['Str']
    try:
        Dex = BluePrint['Dex']
    except:
        Dex = mon.Dummy['Dex']
    try:
        End = BluePrint['End']
    except:
        End = mon.Dummy['End']
    try:
        speed = BluePrint['speed']
    except:
        speed = mon.Dummy['speed']
    try:
        sight = BluePrint['sight']
    except:
        sight = mon.Dummy['sight']
    try:
        addFlags = BluePrint['flags']
    except:
        addFlags = []
    try:
        addIntrinsics = BluePrint['intrinsics']
    except:
        addIntrinsics = []

    NewMob = Mob(x, y, char, color, name, Str, Dex, End, speed, sight)
    NewMob.flags.append(addFlags)
    try:
        NewMob.intrinsics.append(addIntrinsics)
    except:
        print "Failed to spawn non-mob with intrinsics."

    return NewMob

# Player, monsters...
class Entity(object):
    def __init__(self, x, y, char, color, name, BlockMove = False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.AP = 0.0 # Start with 0 turns to take.
        self.BlockMove = BlockMove

        self.flags = []

    def move(self, dx, dy):
        if (self.x + dx < 0 or self.x + dx > var.MapWidth - 1 or
            self.y + dy < 0 or self.y + dy > var.MapHeight - 1):
            return

        self.x += dx
        self.y += dy

    def draw(self):
        # Set color and draw character on screen.
        if (libtcod.map_is_in_fov(var.FOVMap, self.x, self.y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.MapConsole, self.color)
            libtcod.console_put_char(var.MapConsole, self.x, self.y, self.char, libtcod.BKGND_SCREEN)
            self.flags.append('SEEN')

    def range(self, Other):
        dx = Other.x - self.x
        dy = Other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def isBlocked(self, x, y):
        if (x < 0 or x > var.MapWidth - 1 or
            y < 0 or y > var.MapHeight - 1):
            return True

        if dungeon.map[x][y].BlockMove:
            return True

        for i in var.Entities:
            if (i.BlockMove and i.x == x and i.y == y):
                return True

        return False

    def hasFlag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False

    # Heartbeat of all entities.
    def Be(self):
        # How else to check if entity has a speed variable?
        try:
            self.AP += self.speed
            self.regainHealth()
        except:
            self.AP += 1
        # TODO: Check terrain for special effects.
        # TODO: Intrinsics and status effects.

class Mob(Entity):
    def __init__(self, x, y, char, color, name, #These are base Entity arguments.
                 Str, Dex, End, speed = 1.0, FOVRadius = 6):
        BlockMove = True # All mobs block movement, but not all entities,
                         # so pass this to Entity __init__
        super(Mob, self).__init__(x, y, char, color, name, BlockMove)

        # Attributes:
        self.Str = Str
        self.Dex = Dex
        self.End = End
        self.speed = speed
        # FOV:
        self.FOVRadius = FOVRadius # TODO: This should depend on stats and equipment.
        self.recalculateFOV()
        # Calculate health:
        self.bonusHP = 0
        self.maxHP = self.recalculateHealth()
        self.HP = self.maxHP
        # General:
        self.goal = None
        self.intrinsics = []
        self.flags.append('MOB')

    def recalculateFOV(self):
        libtcod.map_compute_fov(var.FOVMap, self.x, self.y, self.FOVRadius, True, 0)

    def recalculateHealth(self):
        return (20 * (1.2 ** self.End)) + self.bonusHP

    def regainHealth(self):
        if not self.hasFlag('DEAD') and self.HP < self.maxHP:
            self.HP += 0.2

    def getRelation(self, Other):
        # TODO: Add factions, pets etc.
        if (self.hasFlag('AVATAR') or Other.hasFlag('AVATAR')):
            return 0
        else:
            return 1

    def hasIntrinsic(self, intrinsic):
        pass

    def receiveHeal(self, amount):
        if amount > 0:
            self.HP += amount
        if self.HP > self.maxHP:
            self.HP = self.maxHP

    def receiveDamage(self, damage, type = None):
        # TODO
        if damage > 0:
            self.HP -= damage

        self.checkDeath()

    def checkDeath(self):
        if self.HP <= 0:
            ui.message("%s dies." % str.capitalize(self.name), libtcod.red, self)

            self.flags.remove('MOB')
            self.flags.append('ITEM')
            self.flags.append('DEAD')
            self.char = '%'
            self.color = libtcod.red
            self.name = str(self.name + ' corpse')
            self.BlockMove = False
            return True
        else:
            return False

    # Actions:
    def actionAttack(self, dx, dy, victim):
        # TODO
        if not victim.hasFlag('MOB'):
            if self.hasFlag('AVATAR'):
                ui.message("You can only attack creatures.")
            return

        #ui.message("%s attacks %s." % (str.capitalize(self.name), victim.name))

        forcedHit = False
        forcedMiss = False
        toHit = var.rand_gaussian_d20()
        toDodge = var.rand_gaussian_d20()

        if toHit == 20:
            forcedHit = True
        elif (toHit == 1 or toDodge == 20):
            forcedMiss = True

        if not forcedMiss:
            toHit += self.Dex
            toDodge += victim.Dex

            if (forcedHit or toHit > toDodge):
                # For now:
                ui.message("%s hits %s." % (str.capitalize(self.name), victim.name), actor = self)

                damage = libtcod.random_get_int(0, 1, 6) + self.Str
                victim.receiveDamage(damage)
            else:
                ui.message("%s misses %s." % (str.capitalize(self.name), victim.name), actor = self)
        else:
            ui.message("%s completely misses %s." % (str.capitalize(self.name), victim.name), actor = self)

        self.AP -= 1

    def actionBump(self, dx, dy):
        bumpee = None
        x = self.x + dx
        y = self.y + dy

        for i in var.Entities:
            if i.x == x and i.y == y and i.hasFlag('MOB'):
                bumpee = i
                break

        if bumpee != None:
            if self.getRelation(bumpee) < 1:
                self.actionAttack(dx, dy, bumpee)
                return True
            else:
                if (self.hasFlag('AVATAR') or var.rand_chance(50)):
                    self.actionSwap(bumpee)
                    return True

        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            if dungeon.map[x][y].hasFlag('CAN_BE_OPENED'):
                if(self.actionOpen(x, y)):
                    return True

        if self.actionWalk(dx, dy):
            return True
        else:
            return False

    def actionClose(self, x, y):
        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            blocked = False

            for i in var.Entities:
                if i.x == x and i.y == y:
                    blocked = True
                    break

            if not blocked == True and dungeon.map[x][y].hasFlag('CAN_BE_CLOSED'):
                if dungeon.map[x][y].hasFlag('DOOR'):
                    dungeon.map[x][y].change(ter.WoodDoor)
                    var.changeFOVMap(x, y)
                    ui.message("%s closes the door." % str.capitalize(self.name), actor = self)
                    self.AP -= 1
                    return True
                else:
                    print "BUG: Unhandled closeable terrain."
            elif dungeon.map[x][y].hasFlag('CAN_BE_CLOSED') and self.hasFlag('AVATAR'):
                ui.message("There is something in the way.")
        return False

    def actionInteract(self, where):
        dx = where[0]
        dy = where[1]

        x = self.x + dx
        y = self.y + dy

        # No interactions beyond the map.
        if (x < 0 or x > var.MapWidth - 1 or y < 0):
            if self.hasFlag('AVATAR'):
                ui.message("Be careful or you will break the backlight.")
                return False
        elif (y > var.MapHeight - 1):
            if self.hasFlag('AVATAR'):
                ui.message("You hear someone mashing buttons.")
                return False

        if dungeon.map[x][y].hasFlag('CAN_BE_CLOSED'):
            self.actionClose(x, y)

        # TODO: More actions.

    def actionJump(self, where):
        dx = where[0]
        dy = where[1]
        dz = where[2]
        nx = self.x + dx
        ny = self.y + dy
        nnx = nx + dx
        nny = ny + dy
        moved = False

        # TODO: Leap attack, stamina cost, jumping out of pits with dz

        if (not self.isBlocked(nx, ny) and not self.isBlocked(nnx, nny)):
            ui.message("%s leaps." % str.capitalize(self.name), actor = self)
            self.move(dx * 2, dy * 2)
            moved = True
        else:
            ui.message("%s balks at the leap." % str.capitalize(self.name), actor = self)

        self.AP -= 1
        return moved

    def actionOpen(self, x, y):
        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            if dungeon.map[x][y].hasFlag('CAN_BE_OPENED'):
                if dungeon.map[x][y].hasFlag('DOOR'):
                    dungeon.map[x][y].change(ter.OpenDoor)
                    var.changeFOVMap(x, y)
                    ui.message("%s opens the door." % str.capitalize(self.name), actor = self)
                    self.AP -= 1
                    return True
                else:
                    print "BUG: Unhandled openable terrain."
        return False

    def actionSwap(self, Other):
        x1 = self.x
        y1 = self.y
        x2 = Other.x
        y2 = Other.y

        self.x = x2
        self.y = y2
        Other.x = x1
        Other.y = y1

        ui.message("%s swaps places with %s." % (str.capitalize(self.name), Other.name), actor = self)

        self.AP -= 1

    def actionWait(self):
        #print "%s waits." % self.name
        self.AP -= 1

    def actionWalk(self, dx, dy):
        moved = False

        if (not self.isBlocked(self.x + dx, self.y + dy) or
           (self.hasFlag('AVATAR') and var.WizModeNoClip)):
            self.move(dx, dy)
            moved = True
        else:
            if self.hasFlag('AVATAR'):
                ui.message("You cannot go there.")

        # Take a turn even if we walk into a wall.
        self.AP -= 1
        return moved

class Item(Entity):
    def __init__(self, x, y, char, color, name, #These are base Entity arguments.
                 ):
        super(Mob, self).__init__(x, y, char, color, name)

        self.flags.append('ITEM')

class Feature(Entity):
    def __init__(self, x, y, char, color, name, #These are base Entity arguments.
                 ):
        super(Mob, self).__init__(x, y, char, color, name)

        self.flags.append('FEATURE')
