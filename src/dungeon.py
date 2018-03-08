# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import entity
import var

###############################################################################
#  Dungeon Generation
###############################################################################
class Terrain(object):
    def __init__(self, char, color, name, BlockMove, BlockSight, CanBeOpened):
        self.char = char
        self.color = color
        self.name = name
        self.BlockMove = BlockMove
        self.BlockSight = BlockSight
        self.CanBeOpened = CanBeOpened
        self.explored = False

    def draw(self, x, y):
        if (libtcod.map_is_in_fov(var.FOVMap, x, y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.Con, self.color)
            self.explored = True
        elif (self.explored == True):
            libtcod.console_set_default_foreground(var.Con, libtcod.darkest_grey)
        else:
            return
            #libtcod.console_set_default_foreground(var.Con, libtcod.black)
        libtcod.console_put_char(var.Con, x, y, self.char, libtcod.BKGND_NONE)

    def change(self, NewTerrain):
        self.char = NewTerrain.char
        self.color = NewTerrain.color
        self.name = NewTerrain.name
        self.BlockMove = NewTerrain.BlockMove
        self.BlockSight = NewTerrain.BlockSight
        self.CanBeOpened = NewTerrain.CanBeOpened

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
                map[x][y].change(RockFloor)

    def create_circular_room(self):
        r = min(self.width / 2, self.height / 2)

        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                if math.sqrt((x - self.CenterX) ** 2 +
                             (y - self.CenterY) ** 2) <= r:
                    map[x][y].change(RockFloor)

    def create_h_tunnel(self, OtherX):
        for x in range(min(self.CenterX, OtherX), max(self.CenterX, OtherX) + 1):
            if (x == self.x1 or x == self.x2):
                map[x][self.CenterY].change(WoodDoor)
            else:
                map[x][self.CenterY].change(RockFloor)

    def create_v_tunnel(self, OtherY):
        for y in range(min(self.CenterY, OtherY), max(self.CenterY, OtherY) + 1):
            if (y == self.y1 or y == self.y2):
                map[self.CenterX][y].change(WoodDoor)
            else:
                map[self.CenterX][y].change(RockFloor)

    def create_d_tunnels(self, OtherRooms):
        # This must be possible in some easier way...
        end = False
        x = self.x1
        y = self.y1
        dx = -1
        dy = -1

        while (x + dx >= 0 and x + dx < var.MapWight and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x1 and y == self.y1):
                map[x][y].change(WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(RockFloor)
                else:
                    map[x][y].change(ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(RockFloor)
                        else:
                            map[x][y].change(ShallowWater)

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

        while (x + dx >= 0 and x + dx < var.MapWight and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x2 and y == self.y1):
                map[x][y].change(WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(RockFloor)
                else:
                    map[x][y].change(ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(RockFloor)
                        else:
                            map[x][y].change(ShallowWater)

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

        while (x + dx >= 0 and x + dx < var.MapWight and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x1 and y == self.y2):
                map[x][y].change(WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(RockFloor)
                else:
                    map[x][y].change(ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(RockFloor)
                        else:
                            map[x][y].change(ShallowWater)

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

        while (x + dx >= 0 and x + dx < var.MapWight and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x2 and y == self.y2):
                map[x][y].change(WoodDoor)
            elif len(OtherRooms) == 0:
                if var.rand_chance(50):
                    map[x][y].change(RockFloor)
                else:
                    map[x][y].change(ShallowWater)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        if var.rand_chance(50):
                            map[x][y].change(RockFloor)
                        else:
                            map[x][y].change(ShallowWater)

            if end:
                break
            else:
                x = x + dx
                y = y + dy

class Builder(object):
    def makeMap(self, populate):
        global map

        # Fill map with walls.
        map = [[ Terrain('#', libtcod.dark_grey, 'wall', True, True, False)
          for y in range(var.MapHeight) ]
            for x in range(var.MapWight) ]

        # TODO: Dungeon levels.
        which = libtcod.random_get_int(0, 1, 5)
        if which in range(1, 4):
            self.buildTraditionalDungeon()
        elif which == 4:
            self.buildSewers()
        else:
            self.buildDrunkenCave()

        if populate:
            self.populate()
        # On the off-chance we trap someone in dungeon generatoi:
        for i in var.Entities:
            if i.isBlocked(i.x, i.y):
                x = 0
                y = 0

                while i.isBlocked(x, y):
                    x = libtcod.random_get_int(0, 1, var.MapWight - 2)
                    y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

                i.x = x
                i.y = y

        # Make FOV map:
        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                libtcod.map_set_properties(var.FOVMap, x, y, not map[x][y].BlockSight, not map[x][y].BlockMove)

    def makeLake(self, liquid):
        # This is basically a bit changed drunken cave.
        StepsTaken = 0
        Fails = 0

        x = libtcod.random_get_int(0, 1, var.MapWight - 2)
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

            if (x + dx > 0 and x + dx < var.MapWight - 1 and
                y + dy > 0 and y + dy < var.MapHeight - 1):
                x += dx
                y += dy

                StepsTaken += 1
            else:
                Fails += 1

    def buildTraditionalDungeon(self):
        Rooms = []
        RoomNo = 0

        # Add rooms.
        for i in range(var.RoomMaxNumber):
            width = libtcod.random_get_int(0, var.RoomMinSize, var.RoomMaxSize)
            height = libtcod.random_get_int(0, var.RoomMinSize, var.RoomMaxSize)

            x = libtcod.random_get_int(0, 0, var.MapWight - width - 1)
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
            for x in range(var.MapWight):

                if map[x][y].name == 'door':
                    #AdjacentWalls = 0
                    Fail = True

                    if (x - 1 > 0 and x + 1 < var.MapWight):
                        if (map[x - 1][y].name == 'wall' and
                            map[x + 1][y].name == 'wall'):
                            Fail = False
                    if (y - 1 > 0 and y + 1 < var.MapHeight):
                        if (map[x][y - 1].name == 'wall' and
                            map[x][y + 1].name == 'wall'):
                            Fail = False

                    if Fail == True:
                        map[x][y].change(RockFloor)

    def buildBSPDungeon(self):
        pass

    def buildQIXDungeon(self):
        pass

    def buildDrunkenCave(self):
        StepsTaken = 0
        Fails = 0

        x = libtcod.random_get_int(0, 1, var.MapWight - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        while (StepsTaken < var.DrunkenSteps and Fails < 2000):
            # Change wall into floor.
            if map[x][y].name == 'wall':
                map[x][y].change(RockFloor)

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

            if (x + dx > 0 and x + dx < var.MapWight - 1 and
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
            x = libtcod.random_get_int(0, 2, var.MapWight - dim - 3)
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
            for x in range(var.MapWight):

                if map[x][y].name == 'door':
                    #AdjacentWalls = 0
                    Fail = True

                    if (x - 1 > 0 and x + 1 < var.MapWight):
                        if (map[x - 1][y].name == 'wall' and
                            map[x + 1][y].name == 'wall'):
                            Fail = False
                    if (y - 1 > 0 and y + 1 < var.MapHeight):
                        if (map[x][y - 1].name == 'wall' and
                            map[x][y + 1].name == 'wall'):
                            Fail = False

                    if Fail == True:
                        map[x][y].change(RockFloor)

    def buildMaze(self):
        pass

    def buildPerlinForest(self):
        noise = libtcod.noise_new(2)

        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                tile = libtcod.noise_get_fbm(noise, [x, y], 32.0)

                # TODO

        libtcod.noise_delete(noise)

    def postProcess(self):
        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                # TODO: Move all of those into script file.
                if (map[x][y].name == 'floor' and var.rand_chance(3)):
                    map[x][y].change(Vines)

                elif (map[x][y].name == 'floor' and var.rand_chance(2)):
                    map[x][y].change(ShallowWater)

                elif (map[x][y].name == 'floor' and var.rand_chance(2)):
                    map[x][y].change(RockPile)

        while var.rand_chance(15):
            self.makeLake(ShallowWater)

    def populate(self):
        MonsterNo = 0
        NewMob = None

        while MonsterNo < var.MonsterMaxNumber:
            x = libtcod.random_get_int(0, 1, var.MapWight - 2)
            y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            # TODO: Rework.
            if var.rand_chance(80):
                NewMob = entity.Mob(x, y, 'o', libtcod.desaturated_green, 'orc', 0, 0, 0)
            else:
                NewMob = entity.Mob(x, y, 'T', libtcod.dark_green, 'troll', 2, -1, 3)

            if NewMob.isBlocked(x, y):
                NewMob = None

            if NewMob != None:
                var.Entities.append(NewMob)
                MonsterNo += 1

            NewMob = None

###############################################################################
#  Tiles
###############################################################################

# TODO: All of this should go to a script file.
RockWall = Terrain('#', libtcod.dark_grey, 'wall', True, True, False)
RockFloor = Terrain('.', libtcod.light_grey, 'floor', False, False, False)
WoodDoor = Terrain('+', libtcod.darkest_orange, 'door', False, True, True)
OpenDoor = Terrain('\'', libtcod.darkest_orange, 'open door', False, False, False)
Vines = Terrain('|', libtcod.dark_green, 'hanging vines', False, True, False)
ShallowWater = Terrain('~', libtcod.blue, 'water', False, False, False)
Lava = Terrain('~', libtcod.dark_red, 'lava', False, False, False)
RockPile = Terrain('*', libtcod.darker_grey, 'rock pile', False, False, False)