# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

import dungeon
import var

###############################################################################
#  Entities
###############################################################################

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

    def draw(self):
        # Set color and draw character on screen.
        if (libtcod.map_is_in_fov(var.FOVMap, self.x, self.y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.Con, self.color)
            libtcod.console_put_char(var.Con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def isBlocked(self, x, y):
        if dungeon.map[x][y].BlockMove:
            return True

        for i in var.Entities:
            if (i.BlockMove and i.x == x and i.y == y):
                return True

        return False

class Mob(Entity):
    def __init__(self, x, y, char, color, name,
                 Str, Dex, End, speed = 1.0, FOVRadius = 6):
        self.Str = Str
        self.Dex = Dex
        self.End = End
        self.speed = speed
        self.FOVRadius = FOVRadius # TODO: This should depend on stats and equipment.
        BlockMove = True # All mobs block movement, but not all entities,
                         # so pass this to Entity __init__

        super(Mob, self).__init__(x, y, char, color, name, BlockMove)

    def UpdateFOV(self):
        libtcod.map_compute_fov(var.FOVMap, self.x, self.y, self.FOVRadius, True, 0)

    # Actions:
    def actionAttack(self, dx, dy, victim):
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
                    self.AP -= 1
                    return

        self.actionWalk(dx, dy)

    def actionOpen(self, x, y):
        if (x > 0 and x < var.MapWight and y > 0 and y < var.MapHeight):
            if dungeon.map[x][y].CanBeOpened == True:
                if dungeon.map[x][y].name == 'door':
                    dungeon.map[x][y].change(OpenDoor)
                    return True
        return False

    def actionWalk(self, dx, dy):
        moved = False

        if (not self.isBlocked(self.x + dx, self.y + dy) or var.WizModeNoClip):
            self.move(dx, dy)
            moved = True

        if moved == True:
            self.UpdateFOV()

        self.AP -= 1
