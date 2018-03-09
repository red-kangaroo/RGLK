# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import ai
import dungeon
import var

###############################################################################
#  Entities
###############################################################################

def spawn(x, y, BluePrint):
    NewMob = Mob(x, y, BluePrint.char, BluePrint.color, BluePrint.name,
                 BluePrint.Str, BluePrint.Dex, BluePrint.End, BluePrint.speed)
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

    def move(self, dx, dy):
        if (self.x + dx < 0 or self.x + dx > var.MapWight - 1 or
            self.y + dy < 0 or self.y + dy > var.MapHeight - 1):
            return

        self.x += dx
        self.y += dy

    def draw(self, Player):
        # Set color and draw character on screen.
        if (libtcod.map_is_in_fov(Player.FOVMap, self.x, self.y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.Con, self.color)
            libtcod.console_put_char(var.Con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def range(self, Other):
        dx = Other.x - self.x
        dy = Other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def isBlocked(self, x, y):
        if dungeon.map[x][y].BlockMove:
            return True

        for i in var.Entities:
            if (i.BlockMove and i.x == x and i.y == y):
                return True

        return False

class Mob(Entity):
    def __init__(self, x, y, char, color, name, #These are base Entity arguments.
                 Str, Dex, End, speed = 1.0, FOVRadius = 6, isAvatar = False):
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
        self.FOVMap = libtcod.map_new(var.MapWight, var.MapHeight)
        self.recalculateFOV()
        # Calculate health:
        self.bonusHP = 0
        self.maxHP = self.recalculateHealth()
        self.HP = self.maxHP
        # General:
        self.isAvatar = isAvatar # Flag the player.
        self.goal = None

    def recalculateFOV(self):
        libtcod.map_compute_fov(self.FOVMap, self.x, self.y, self.FOVRadius, True, 0)

    def recalculateHealth(self):
        return (20 * (1.2 ** self.End)) + self.bonusHP

    # Actions:
    def actionAttack(self, dx, dy, victim):
        # TODO
        print "%s attacks %s." % (self.name, victim.name)
        self.AP -= 1

    def actionBump(self, dx, dy):
        bumpee = None
        x = self.x + dx
        y = self.y + dy

        for i in var.Entities:
            if i.x == x and i.y == y:
                bumpee = i
                break

        if bumpee != None:
            self.actionAttack(dx, dy, bumpee)
            return

        if (x > 0 and x < var.MapWight and y > 0 and y < var.MapHeight):
            if dungeon.map[x][y].CanBeOpened == True:
                if(self.actionOpen(x, y)):
                    return

        self.actionWalk(dx, dy)

    def actionOpen(self, x, y):
        if (x > 0 and x < var.MapWight and y > 0 and y < var.MapHeight):
            if dungeon.map[x][y].CanBeOpened == True:
                if dungeon.map[x][y].name == 'door':
                    dungeon.map[x][y].change(dungeon.OpenDoor)
                    var.changeFOVMap(x, y)
                    self.recalculateFOV()
                    self.AP -= 1
                    return True
        return False

    def actionWait(self):
        print "%s waits." % self.name
        self.AP -= 1

    def actionWalk(self, dx, dy):
        moved = False

        if (not self.isBlocked(self.x + dx, self.y + dy) or var.WizModeNoClip):
            self.move(dx, dy)
            moved = True

        if moved:
            self.recalculateFOV()

        # Take a turn even if we walk into a wall.
        self.AP -= 1
        return moved

###############################################################################
#  Tiles
###############################################################################

Orc = Mob(0, 0, 'o', libtcod.desaturated_green, 'orc', 0, 0, 0)
Troll = Mob(0, 0, 'T', libtcod.dark_green, 'troll', 2, -1, 3)
