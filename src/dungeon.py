# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import entity
import monster as mon
import terrain as ter
import var

###############################################################################
#  Dungeon Generation
###############################################################################
class Terrain(object):
    def __init__(self, char, color, name, BlockMove, BlockSight, flags = []):
        self.char = char
        self.color = color
        self.name = name
        self.BlockMove = BlockMove
        self.BlockSight = BlockSight
        self.explored = False
        self.flags = flags

    def draw(self, x, y):
        if (libtcod.map_is_in_fov(var.FOVMap, x, y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.MapConsole, self.color)
            self.explored = True
        elif (self.explored == True):
            libtcod.console_set_default_foreground(var.MapConsole, libtcod.darkest_grey)
        else:
            return
            #libtcod.console_set_default_foreground(var.Con, libtcod.black)
        libtcod.console_put_char(var.MapConsole, x, y, self.char, libtcod.BKGND_SCREEN)

    def change(self, NewTerrain):
        try:
            self.char = NewTerrain['char']
        except:
            print "Failed to change %s" % self.name
        try:
            self.color = NewTerrain['color']
        except:
            print "Failed to change %s" % self.name
        try:
            self.name = NewTerrain['name']
        except:
            print "Failed to change %s" % self.name
        try:
            self.BlockMove = NewTerrain['BlockMove']
        except:
            print "Failed to change %s" % self.name
        try:
            self.BlockSight = NewTerrain['BlockSight']
        except:
            print "Failed to change %s" % self.name
        # Clear all flags. This way works, otherwise strange errors in dungeon
        # generation crop up from time to time.
        try:
            del self.flags
        except:
            print "Failed to clear flags from %s." % self.name
        try:
            self.flags = NewTerrain['flags']
        except:
            self.flags = []

    def hasFlag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False

class Room(object):
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.CenterX = (self.x1 + self.x2) / 2
        self.CenterY = (self.y1 + self.y2) / 2

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    # TODO: Move floor, wall etc. parameters into script files.
    def create_square_room(self):
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                map[x][y].change(ter.RockFloor)

    def create_circular_room(self):
        r = min(self.width / 2, self.height / 2)

        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                if math.sqrt((x - self.CenterX) ** 2 +
                             (y - self.CenterY) ** 2) <= r:
                    map[x][y].change(ter.RockFloor)

    def create_h_tunnel(self, OtherX):
        for x in range(min(self.CenterX, OtherX), max(self.CenterX, OtherX) + 1):
            if (x == self.x1 or x == self.x2):
                map[x][self.CenterY].change(ter.WoodDoor)
            else:
                map[x][self.CenterY].change(ter.RockFloor)

    def create_v_tunnel(self, OtherY):
        for y in range(min(self.CenterY, OtherY), max(self.CenterY, OtherY) + 1):
            if (y == self.y1 or y == self.y2):
                map[self.CenterX][y].change(ter.WoodDoor)
            else:
                map[self.CenterX][y].change(ter.RockFloor)

    def create_d_tunnels(self, OtherRooms):
        # This must be possible in some easier way...
        end = False
        x = self.x1
        y = self.y1
        dx = -1
        dy = -1

        while (x + dx >= 0 and x + dx < var.MapWidth and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x1 and y == self.y1):
                map[x][y].change(ter.WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(ter.RockFloor)
                else:
                    map[x][y].change(ter.ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(ter.RockFloor)
                        else:
                            map[x][y].change(ter.ShallowWater)

            if end:
                break
            else:
                x = x + dx
                y = y + dy

        end = False
        x = self.x2
        y = self.y1
        dx = 1
        dy = -1

        while (x + dx >= 0 and x + dx < var.MapWidth and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x2 and y == self.y1):
                map[x][y].change(ter.WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(ter.RockFloor)
                else:
                    map[x][y].change(ter.ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(ter.RockFloor)
                        else:
                            map[x][y].change(ter.ShallowWater)

            if end:
                break
            else:
                x = x + dx
                y = y + dy

        end = False
        x = self.x1
        y = self.y2
        dx = -1
        dy = 1

        while (x + dx >= 0 and x + dx < var.MapWidth and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x1 and y == self.y2):
                map[x][y].change(ter.WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(ter.RockFloor)
                else:
                    map[x][y].change(ter.ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(ter.RockFloor)
                        else:
                            map[x][y].change(ter.ShallowWater)

            if end:
                break
            else:
                x = x + dx
                y = y + dy

        end = False
        x = self.x2
        y = self.y2
        dx = 1
        dy = 1

        while (x + dx >= 0 and x + dx < var.MapWidth and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x2 and y == self.y2):
                map[x][y].change(ter.WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(ter.RockFloor)
                else:
                    map[x][y].change(ter.ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(ter.RockFloor)
                        else:
                            map[x][y].change(ter.ShallowWater)

            if end:
                break
            else:
                x = x + dx
                y = y + dy

class Builder(object):
    def makeMap(self, populate):
        global map

        # First create map of dummy terrain:
        map = [[ Terrain('.', libtcod.white, 'bug: dummy terrain', False, False)
          for y in range(var.MapHeight) ]
            for x in range(var.MapWidth) ]
        # Then fill map with walls:
        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                map[x][y].change(ter.RockWall)

        # TODO: Dungeon levels.
        which = libtcod.random_get_int(0, 1, 5)
        if which in range(1, 4):
            print "Building traditional dungeon."
            self.buildTraditionalDungeon()
        elif which == 4:
            print "Building sewers."
            self.buildSewers()
        else:
            print "Building a cave."
            self.buildDrunkenCave()

        if populate:
            self.populate()

        for i in var.Entities:
            # On the off-chance we trap someone in dungeon generation:
            if i.isBlocked(i.x, i.y):
                x = 0
                y = 0

                while i.isBlocked(x, y):
                    x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
                    y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

                i.x = x
                i.y = y

        var.calculateFOVMap()

    def makeLake(self, liquid):
        # This is basically a bit changed drunken cave.
        StepsTaken = 0
        Fails = 0

        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        while (StepsTaken < (var.DrunkenSteps / 4) and Fails < 2000):
            # Create water.
            map[x][y].change(liquid)

            step = libtcod.random_get_int(0, 1, 4)
            dx = 0
            dy = 0

            if step == 1:
                dy -=1
            elif step == 2:
                dx -= 1
            elif step == 3:
                dx += 1
            elif step == 4:
                dy += 1

            if (x + dx > 0 and x + dx < var.MapWidth - 1 and
                y + dy > 0 and y + dy < var.MapHeight - 1):
                x += dx
                y += dy

                StepsTaken += 1
            else:
                Fails += 1

    def makeBetterRoom(self, Rooms):
        for room in Rooms:
            if var.rand_chance(2):
                which = libtcod.random_get_int(0, 1, 2)
                # TODO: Add so much more rooms.

                # Wooden room:
                if which == 1:
                    for x in range(room.x1, room.x2 + 1):
                        for y in range(room.y1, room.y2 + 1):
                            if map[x][y].hasFlag('WALL'):
                                map[x][y].change(ter.WoodWall)
                            elif not map[x][y].hasFlag('DOOR'):
                                map[x][y].change(ter.WoodFloor)
                # Icy room:
                elif which == 2:
                    for x in range(room.x1, room.x2 + 1):
                        for y in range(room.y1, room.y2 + 1):
                            if map[x][y].hasFlag('WALL'):
                                map[x][y].change(ter.IceWall)
                            elif not map[x][y].hasFlag('LIQUID'):
                                map[x][y].change(ter.IceFloor)

    def buildTraditionalDungeon(self):
        Rooms = []
        RoomNo = 0

        # Add rooms.
        for i in range(var.RoomMaxNumber):
            width = libtcod.random_get_int(0, var.RoomMinSize, var.RoomMaxSize)
            height = libtcod.random_get_int(0, var.RoomMinSize, var.RoomMaxSize)

            x = libtcod.random_get_int(0, 0, var.MapWidth - width - 1)
            y = libtcod.random_get_int(0, 0, var.MapHeight - height - 1)

            NewRoom = Room(x, y, width, height)
            Fail = False

            for OtherRoom in Rooms:
                if NewRoom.intersect(OtherRoom):
                    Fail = True
                    break

            # We want some rooms to overlap, it looks better.
            if (RoomNo < 20 and var.rand_chance(20)):
                Fail = False

            if not Fail:
                if var.rand_chance(20):
                    NewRoom.create_circular_room()
                else:
                    NewRoom.create_square_room()

                if RoomNo != 0:
                    PrevRoom = Rooms[RoomNo - 1]

                    if var.rand_chance(50):
                        NewRoom.create_h_tunnel(PrevRoom.CenterX)
                        PrevRoom.create_v_tunnel(NewRoom.CenterY)
                    else:
                        NewRoom.create_v_tunnel(PrevRoom.CenterY)
                        PrevRoom.create_h_tunnel(NewRoom.CenterX)

                Rooms.append(NewRoom)
                RoomNo += 1

        # Clean door generation and add some decorations.
        self.postProcess() # Must be before door handling, or lakes will break
                           # our door placement.

        for y in range(var.MapHeight):
            for x in range(var.MapWidth):

                if map[x][y].hasFlag('DOOR'):
                    #AdjacentWalls = 0
                    Fail = True

                    if (x - 1 > 0 and x + 1 < var.MapWidth):
                        if (map[x - 1][y].hasFlag('WALL') and
                            map[x + 1][y].hasFlag('WALL')):
                            Fail = False
                    if (y - 1 > 0 and y + 1 < var.MapHeight):
                        if (map[x][y - 1].hasFlag('WALL') and
                            map[x][y + 1].hasFlag('WALL')):
                            Fail = False

                    if Fail == True:
                        map[x][y].change(ter.RockFloor)

        self.makeBetterRoom(Rooms)

    def buildBSPDungeon(self):
        pass

    def buildQIXDungeon(self):
        pass

    def buildDrunkenCave(self):
        StepsTaken = 0
        Fails = 0

        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        while (StepsTaken < var.DrunkenSteps and Fails < 2000):
            # Change wall into floor.
            if map[x][y].hasFlag('WALL'):
                map[x][y].change(ter.RockFloor)

            step = libtcod.random_get_int(0, 1, 8)
            dx = 0
            dy = 0

            if step == 1:
                dx -= 1
                dy -= 1
            elif step == 2:
                dy -=1
            elif step == 3:
                dx += 1
                dy -= 1
            elif step == 4:
                dx -= 1
            elif step == 5:
                dx += 1
            elif step == 6:
                dx -= 1
                dy +=1
            elif step == 7:
                dy += 1
            elif step == 8:
                dx += 1
                dy += 1

            if (x + dx > 0 and x + dx < var.MapWidth - 1 and
                y + dy > 0 and y + dy < var.MapHeight - 1):
                x += dx
                y += dy

                StepsTaken += 1
            else:
                Fails += 1

        self.postProcess()

    def buildSewers(self):
        Rooms = []
        RoomNo = 0

        # Add rooms.
        for i in range(6):
            dim = libtcod.random_get_int(0, 4, 7)

            # Increase space on sides for better corridor placement.
            x = libtcod.random_get_int(0, 2, var.MapWidth - dim - 3)
            y = libtcod.random_get_int(0, 2, var.MapHeight - dim - 3)

            NewRoom = Room(x, y, dim, dim)
            Fail = False

            for OtherRoom in Rooms:
                if NewRoom.intersect(OtherRoom):
                    Fail = True
                    break

            if not Fail:
                NewRoom.create_square_room()
                NewRoom.create_d_tunnels(Rooms)

                Rooms.append(NewRoom)
                RoomNo += 1

        # Clean door generation and add some decorations.
        self.postProcess() # Must be before door handling, or lakes will break
                           # our door placement.

        for y in range(var.MapHeight):
            for x in range(var.MapWidth):

                if map[x][y].hasFlag('DOOR'):
                    #AdjacentWalls = 0
                    Fail = True

                    if (x - 1 > 0 and x + 1 < var.MapWidth):
                        if (map[x - 1][y].hasFlag('WALL') and
                            map[x + 1][y].hasFlag('WALL')):
                            Fail = False
                    if (y - 1 > 0 and y + 1 < var.MapHeight):
                        if (map[x][y - 1].hasFlag('WALL') and
                            map[x][y + 1].hasFlag('WALL')):
                            Fail = False

                    if Fail == True:
                        map[x][y].change(ter.RockFloor)

    def buildMaze(self):
        pass

    def buildPerlinForest(self):
        noise = libtcod.noise_new(2)

        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                tile = libtcod.noise_get_fbm(noise, [x, y], 32.0)

                # TODO

        libtcod.noise_delete(noise)

    def postProcess(self):
        print "Starting post-processing dungeon."
        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                # TODO: Move all of those into script file.
                if (map[x][y].hasFlag('GROUND') and var.rand_chance(3)):
                    map[x][y].change(ter.Vines)

                elif (map[x][y].hasFlag('GROUND') and var.rand_chance(2)):
                    map[x][y].change(ter.ShallowWater)

                elif (map[x][y].hasFlag('GROUND') and var.rand_chance(2)):
                    map[x][y].change(ter.RockPile)

        while var.rand_chance(15):
            print "Making a lake."
            self.makeLake(ter.ShallowWater)

    def populate(self):
        MonsterNo = 0
        NewMob = None

        while MonsterNo < var.MonsterMaxNumber:
            x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
            y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            # TODO: Rework.
            if var.rand_chance(80):
                NewMob = entity.spawn(x, y, mon.Orc)
            else:
                NewMob = entity.spawn(x, y, mon.Troll)

            if NewMob.isBlocked(x, y):
                NewMob = None

            if NewMob != None:
                var.Entities.append(NewMob)
                MonsterNo += 1

            NewMob = None
