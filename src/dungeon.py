# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random
import sys

import entity
import raw
import var

###############################################################################
#  Dungeon Generation
###############################################################################
def makeMap(Populate, DungeonLevel):
    if DungeonLevel < 0 or DungeonLevel > var.FloorMaxNumber:
        sys.exit("Tried building beyond the dungeon.")

    # First create map of dummy terrain:
    map = [[ Terrain('.', libtcod.white, 'BUG: dummy terrain', False, False)
      for y in range(var.MapHeight) ]
        for x in range(var.MapWidth) ]
    # Then fill map with walls:
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            map[x][y].change(raw.RockWall)

    # TODO: Dungeon levels.
    #  0 the Surface
    #  1 \
    #  2 | traditional
    #  3 |  dungeon
    #  4 /
    #  5 Minetown
    #  6 sewers
    #  7 sewers
    #  8 cave
    #  9 cave
    # 10 Big room
    # 11 BSP dungeon
    # 12 BSP dungeon
    # 13 maze
    # 14 maze
    # 15 city
    # 16 deep cave
    # 17 deep cave
    # 18 deep cave
    # 19 ???
    # 20 the Goal?

    which = libtcod.random_get_int(0, 1, 8)
    if which in range(1, 4):
        print "Building traditional dungeon."
        map = buildTraditionalDungeon(map, DungeonLevel)
    elif which == 4:
        print "Building sewers."
        map = buildSewers(map, DungeonLevel)
    elif which == 5:
        print "Building a cave."
        map = buildDrunkenCave(map, DungeonLevel)
    elif which == 6:
        print "Building a maze."
        map = buildMaze(map, DungeonLevel)
    elif which == 7:
        print "Building a city."
        map = buildCity(map, DungeonLevel)
    else:
        print "Building BSP dungeon."
        map = buildBSPDungeon(map, DungeonLevel)

    # Set map to the correct dungeon level.
    var.Maps[DungeonLevel] = map

    # Add entities.
    if Populate:
        populate(DungeonLevel)
    else:
        # We might have trapped someone while re-generating the level:
        for i in var.Entities[DungeonLevel]:
            if i.isBlocked(i.x, i.y, DungeonLevel):
                x = 0
                y = 0

                while i.isBlocked(x, y, DungeonLevel):
                    x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
                    y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

                i.x = x
                i.y = y

def makeLake(liquid, map):
    # This is basically a bit changed drunken cave.
    StepsTaken = 0
    Fails = 0

    x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
    y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

    while (StepsTaken < (var.DrunkenSteps / 4) and Fails < 2000):
        # Create water.
        map[x][y].change(liquid)

        # Other possibilities:
        #  lava
        #  mud
        #  quicksand
        #  deep snow
        #  tall grass

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

    return map

def makeBetterRoom(Rooms, map):
    for room in Rooms:
        if var.rand_chance(4):
            which = libtcod.random_get_int(0, 1, 9)
            # TODO: Add so much more rooms.

            # Wooden room:
            if which == 1:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('WALL'):
                            map[x][y].change(raw.WoodWall)
                        elif not map[x][y].hasFlag('DOOR'):
                            map[x][y].change(raw.WoodFloor)
            # Icy room:
            elif which == 2:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('WALL'):
                            map[x][y].change(raw.IceWall)
                        elif not map[x][y].hasFlag('LIQUID'):
                            if var.rand_chance(5):
                                map[x][y].change(raw.DeepSnow)
                            elif var.rand_chance(15):
                                map[x][y].change(raw.Snow)
                            else:
                                map[x][y].change(raw.IceFloor)
            # Grass room:
            elif which == 3:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('WALL'):
                            map[x][y].change(raw.EarthWall)
                        elif not map[x][y].hasFlag('LIQUID'):
                            if var.rand_chance(5):
                                map[x][y].change(raw.Vines)
                            elif var.rand_chance(60):
                                map[x][y].change(raw.GrassFloor)
                            else:
                                map[x][y].change(raw.TallGrass)
            # Nice room:
            elif which == 4:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('WALL'):
                            map[x][y].change(raw.BrickWall)
                        elif not map[x][y].hasFlag('DOOR'):
                            map[x][y].change(raw.Carpet)
                        elif map[x][y].hasFlag('DOOR'):
                            map[x][y].change(raw.Curtain)
            # Crypt:
            elif which == 5:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('WALL'):
                            map[x][y].change(raw.BrickWall)
                        elif not map[x][y].hasFlag('DOOR'):
                            if var.rand_chance(3):
                                map[x][y].change(raw.BonePile)
                            elif var.rand_chance(20):
                                map[x][y].change(raw.Grave)
                        elif map[x][y].hasFlag('DOOR'):
                            if var.rand_chance(20):
                                map[x][y].change(raw.BrokenDoor)
            # Prison room:
            elif which == 6:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('WALL'):
                            map[x][y].change(raw.IronWall)
                        elif map[x][y].hasFlag('DOOR'):
                            if var.rand_chance(5):
                                map[x][y].change(raw.IronBars)
                            else:
                                map[x][y].change(raw.ClosedPort)
                        else:
                            map[x][y].change(raw.RockFloor)
            # Sandy room:
            elif which == 7:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if not map[x][y].hasFlag('WALL'):
                            if var.rand_chance(5):
                                map[x][y].change(raw.DeepSand)
                            else:
                                map[x][y].change(raw.Sand)
            # Secret room:
            elif which == 8:
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if map[x][y].hasFlag('DOOR'):
                            map[x][y].change(raw.SecretDoor)
            # Pool room:
            elif which == 9:
                which = random.choice([
                raw.ShallowWater,
                raw.DeepWater,
                raw.Lava,
                raw.Mud
                ])
                for x in range(room.x1, room.x2 + 1):
                    for y in range(room.y1, room.y2 + 1):
                        if (not map[x][y].hasFlag('DOOR') and
                            not map[x][y].hasFlag('WALL')):
                            map[x][y].change(which)

    return map

def makePrefabRoom(map, DungeonLevel, Rooms = None, Prefab = None):
    if Prefab == None and Rooms != None:
        for room in Rooms:
            for Prefab in raw.RoomList:

                # Select a file and change terrain based on its map.
                if (room.width + 1 == Prefab['width'] and
                    room.height + 1 == Prefab['height']):
                    try:
                        frequency = Prefab['frequency']
                    except:
                        frequency = raw.DummyRoom['frequency']
                    if not var.rand_chance(frequency):
                        continue # Not break, or some rooms will never get generated,
                                 # because they have same size as others.

                    map = create_prefab(Prefab, room, map, DungeonLevel)

                    # Remove the room from Rooms so that we don't overwrite it later.
                    Rooms.remove(room)
                    break

        # Replace damaged outer walls.
        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                if (x == 0 or x == var.MapWidth - 1 or
                    y == 0 or y == var.MapHeight - 1):
                    if not map[x][y].hasFlag('WALL'):
                        map[x][y].change(raw.RockWall)

        return Rooms, map
    elif Rooms == None:
        if Prefab == None:
            Prefab = random.choice(raw.RoomList)

        fails = 0
        # Be careful, Room.width and Prefab['width'] are different by 1. (Yeah,
        # I will hate myself for this.)
        width = Prefab['width'] - 1
        height = Prefab['height'] - 1

        while fails < 100:
            Fail = False
            x = libtcod.random_get_int(0, 0, var.MapWidth - width - 1)
            y = libtcod.random_get_int(0, 0, var.MapHeight - height - 1)

            for n in range(y, y + height):
                for m in range(x, x + width):
                    if not map[m][n].hasFlag('WALL'):
                        Fail = True

            if Fail == False:
                break
            else:
                fails += 1

        if Fail == False:
            NewRoom = Room(x, y, width, height)
            map = create_prefab(Prefab, NewRoom, map, DungeonLevel)

        # Replace damaged outer walls once again.
        for y in range(var.MapHeight):
            for x in range(var.MapWidth):
                if (x == 0 or x == var.MapWidth - 1 or
                    y == 0 or y == var.MapHeight - 1):
                    if not map[x][y].hasFlag('WALL'):
                        map[x][y].change(raw.RockWall)

        return map
    else:
        print "failed to place prefab rooms."
        return Rooms, map

def create_prefab(Prefab, room, map, DungeonLevel):
    file = open(Prefab['file'], 'r')
    y = room.y1

    #if var.rand_chance(50):
    #    for line in file:
    #        line = reversed(line)

    for line in file:
        x = room.x1

        for i in line:
            try:
                try:
                    (terrain, terrainFlags, item, mob) = Prefab[i]
                except:
                    (terrain, terrainFlags, item, mob) = raw.DummyRoom[i]

                map[x][y].change(terrain)

                if terrainFlags != None:
                    for p in terrainFlags:
                        map[x][y].flags.append(p)

                if item != None:
                    if item == 'RANDOM_ANY':
                        item = var.rand_weighted(getRandomEntity('ITEM', DungeonLevel))
                    elif item == 'RANDOM_ARTIFACT':
                        pass # TODO

                    NewItem = entity.spawn(x, y, item, 'ITEM')
                    var.Entities[DungeonLevel].append(NewItem)

                if mob != None:
                    if mob == 'RANDOM_ANY':
                        mob = var.rand_weighted(getRandomEntity('MOB', DungeonLevel))

                    NewMob = entity.spawn(x, y, mob, 'MOB')
                    var.Entities[DungeonLevel].append(NewMob)

            except:
                pass # This should prevent crashes on newline, if there are any.

            x += 1
        y += 1

    # Now dig tunnels to connect the room.
    y = room.y1
    for x in range(room.x1, room.x2 + 1):
        if map[x][y].isWalkable():
            connected = False
            n = y - 1

            for m in range(x - 1, x + 2):
                if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
                    if map[m][n].isWalkable():
                        connected = True
                else:
                    break

            if connected:
                continue
            else:
                while n > 0 and n < var.MapHeight - 1:
                    connected = False

                    for m in range(x - 1, x + 2):
                        if map[m][n].isWalkable():
                            connected = True

                    if connected:
                        break
                    else:
                        map[x][n].change(raw.RockFloor)

                    n -= 1

    x = room.x2
    for y in range(room.y1, room.y2 + 1):
        if map[x][y].isWalkable():
            connected = False
            m = x + 1

            for n in range(y - 1, y + 2):
                if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
                    if map[m][n].isWalkable():
                        connected = True
                else:
                    break

            if connected:
                continue
            else:
                while m > 0 and m < var.MapWidth - 1:
                    connected = False

                    for n in range(y - 1, y + 2):
                        if map[m][n].isWalkable():
                            connected = True

                    if connected:
                        break
                    else:
                        map[m][y].change(raw.RockFloor)

                    m += 1

    x = room.x1
    for y in range(room.y1, room.y2 + 1):
        if map[x][y].isWalkable():
            connected = False
            m = x - 1

            for n in range(y - 1, y + 2):
                if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
                    if map[m][n].isWalkable():
                        connected = True
                else:
                    break

            if connected:
                continue
            else:
                while m > 0 and m < var.MapWidth - 1:
                    connected = False

                    for n in range(y - 1, y + 2):
                        if map[m][n].isWalkable():
                            connected = True

                    if connected:
                        break
                    else:
                        map[m][y].change(raw.RockFloor)

                    m -= 1

    y = room.y2
    for x in range(room.x1, room.x2 + 1):
        if map[x][y].isWalkable():
            connected = False
            n = y + 1

            for m in range(x - 1, x + 2):
                if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
                    if map[m][n].isWalkable():
                        connected = True
                else:
                    break

            if connected:
                continue
            else:
                while n > 0 and n < var.MapHeight - 1:
                    connected = False

                    for m in range(x - 1, x + 2):
                        if map[m][n].isWalkable():
                            connected = True

                    if connected:
                        break
                    else:
                        map[x][n].change(raw.RockFloor)

                    n += 1
    return map

def makeClosets(map):
    pass

def makeStairs(map, DungeonLevel, Rooms = None):
    # Rooms passed into this function are alredy without prefab rooms (removed in
    # makePrefabRoom), so we only need to check if there are stairs placed in prefabs
    # and don't need to worry about placing the stairs into vaults and such by this.

    upstairs = False
    downstairs = False

    # This prevents creating upstairs on ground floor and downstairs on last floor.
    if DungeonLevel == 0:
        upstairs = True
    elif DungeonLevel == var.FloorMaxNumber:
        downstairs = True

    for y in range(0, var.MapHeight):
        for x in range(0, var.MapWidth):
            if map[x][y].hasFlag('STAIRS_UP'):
                upstairs = True
            elif map[x][y].hasFlag('STAIRS_DOWN'):
                downstairs = True

    if Rooms != None:
        # Place upstairs.
        if upstairs == False:
            room = random.choice(Rooms)
            toPlace = []

            for y in range(room.y1 + 1, room.y2):
                for x in range(room.x1 + 1, room.x2):
                    if (map[x][y].isWalkable() and not map[x][y].hasFlag('DOOR') and
                        not map[x][y].hasFlag('FEATURE')):
                        toPlace.append(map[x][y])

            if len(toPlace) > 0:
                random.choice(toPlace).change(raw.UpStairs)
            else:
                print "Failed to place upstairs."

        # Place downstairs.
        if downstairs == False:
            room = random.choice(Rooms)
            toPlace = []

            for y in range(room.y1 + 1, room.y2):
                for x in range(room.x1 + 1, room.x2):
                    if (map[x][y].isWalkable() and not map[x][y].hasFlag('DOOR') and
                        not map[x][y].hasFlag('FEATURE')):
                        toPlace.append(map[x][y])

            if len(toPlace) > 0:
                random.choice(toPlace).change(raw.DownStairs)
            else:
                print "Failed to place downstairs."
    else:
        if upstairs == False:
            x = 0
            y = 0

            while not (map[x][y].isWalkable() and not map[x][y].hasFlag('DOOR') and
                       not map[x][y].hasFlag('FEATURE')):
                x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
                y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            map[x][y].change(raw.UpStairs)
        if downstairs == False:
            x = 0
            y = 0

            while not (map[x][y].isWalkable() and not map[x][y].hasFlag('DOOR') and
                       not map[x][y].hasFlag('FEATURE')):
                x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
                y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            map[x][y].change(raw.DownStairs)

    # TODO: Check whether we can access both stairs using pathfinding.

    return map

def buildTraditionalDungeon(map, DungeonLevel):
    type = 'DUNGEON'
    if var.rand_chance(5):
        type = 'CATACOMB'

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
        if (RoomNo < 20 and var.rand_chance(20) and type != 'CATACOMB'):
            Fail = False

        if not Fail:
            if var.rand_chance(20):
                map = NewRoom.create_circular_room(map)
            else:
                map = NewRoom.create_square_room(map)

            if RoomNo != 0:
                PrevRoom = Rooms[RoomNo - 1]

                if var.rand_chance(50):
                    map = NewRoom.create_h_tunnel(PrevRoom.CenterX, map)
                    map = PrevRoom.create_v_tunnel(NewRoom.CenterY, map)
                else:
                    map = NewRoom.create_v_tunnel(PrevRoom.CenterY, map)
                    map = PrevRoom.create_h_tunnel(NewRoom.CenterX, map)

            Rooms.append(NewRoom)
            RoomNo += 1

    map = postProcess(map, type)
    Rooms, map = makePrefabRoom(map, DungeonLevel, Rooms)
    map = makeBetterRoom(Rooms, map)
    map = makeStairs(map, DungeonLevel, Rooms)

    return map

def buildBSPDungeon(map, DungeonLevel):
    global BSPmap, BSPRooms

    # Thank you, Aukustus and HexDecimal, for you help in figuring out a way
    # how to do this without the need of global variables as in the tutorial,
    # but I eventually gave up and done it with globals anyway. Maybe one day
    # I'll return to this and change it. :D
    # TODO: Use the standard library's functools.partial to manually add the map
    # to the callback before passing it to bsp_traverse_inverted_level_order.

    # Create a root node, then split it.
    bsp = libtcod.bsp_new_with_size(0, 0, var.MapWidth - 1, var.MapHeight - 1)
    libtcod.bsp_split_recursive(bsp, 0, var.BSPMaxDepth, var.BSPMinSize + 1,
                                var.BSPMinSize + 1, 1.5, 1.5)

    BSPmap = map
    BSPRooms = []

    libtcod.bsp_traverse_inverted_level_order(bsp, makeBSP)

    BSPmap = postProcess(BSPmap, 'BSP')
    BSPRooms, BSPmap = makePrefabRoom(BSPmap, DungeonLevel, BSPRooms)
    BSPmap = makeBetterRoom(BSPRooms, BSPmap)
    BSPmap = makeStairs(BSPmap, DungeonLevel, BSPRooms)

    return BSPmap

def makeBSP(node, data):
    global BSPmap, BSPRooms

    #Create rooms
    if libtcod.bsp_is_leaf(node):
        NewRoom = Room(node.x, node.y, node.w, node.h)

        if var.rand_chance(20):
            BSPmap = NewRoom.create_circular_room(BSPmap)
            BSPmap = NewRoom.create_entrance(BSPmap, True)
        else:
            BSPmap = NewRoom.create_square_room(BSPmap)
            BSPmap = NewRoom.create_entrance(BSPmap)

        BSPRooms.append(NewRoom)

def buildQIXDungeon(map, DungeonLevel):
    pass

def buildDrunkenCave(map, DungeonLevel):
    StepsTaken = 0
    Fails = 0

    x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
    y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

    while (StepsTaken < var.DrunkenSteps and Fails < 2000):
        # Change wall into floor.
        if map[x][y].hasFlag('WALL'):
            map[x][y].change(raw.RockFloor)

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

    map = postProcess(map, 'CAVE')

    while var.rand_chance(50):
        map = makePrefabRoom(map, DungeonLevel)

    map = makeStairs(map, DungeonLevel)

    return map

def buildSewers(map, DungeonLevel):
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
            map = NewRoom.create_square_room(map)
            map = NewRoom.create_d_tunnels(Rooms, map)

            Rooms.append(NewRoom)
            RoomNo += 1

    map = postProcess(map, 'SEWERS')
    map = makeStairs(map, DungeonLevel, Rooms)

    return map

def buildMaze(map, DungeonLevel):
    # Different branch rates can result in quite different mazes:
    MazeBranchRate = 0

    if var.rand_chance(5):
        MazeBranchRate = 10
    elif var.rand_chance(5):
        MazeBranchRate = -5

    # List of coordinates of exposed but undetermined cells.
    frontier = []

    for y in range(1, var.MapHeight - 1):      # I'm using shallow water here because
        for x in range(1, var.MapWidth - 1):   # I tried using flags to mark unmazed
            map[x][y].change(raw.ShallowWater) # tiles and failed horribly in generation.
                                               # Now it works and I'm not touching it again.
    x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
    y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

    map, frontier = carveMaze(x, y, map, frontier)

    while len(frontier) > 0:
        success = False

        pos = random.random()
        pos = pos ** (math.e ** -(MazeBranchRate))
        choice = frontier[int(pos * len(frontier))]
        x, y = choice

        if checkMaze(x, y, map):
            map, frontier = carveMaze(x, y, map, frontier)
            success = True
        else:
            map, success = hardenMaze(x, y, map)

        if success:
            frontier.remove(choice)

    for y in range(0, var.MapHeight):
        for x in range(0, var.MapWidth):
            if map[x][y].hasFlag('LIQUID'):
                map[x][y].change(raw.RockWall)

    RoomMax = libtcod.random_get_int(0, 2, 11)
    Rooms = []
    RoomNo = 0

    # Add rooms.
    while RoomNo < RoomMax:
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

        if not Fail:
            if var.rand_chance(20):
                map = NewRoom.create_circular_room(map)
            else:
                map = NewRoom.create_square_room(map)

            map = NewRoom.create_entrance(map)

            Rooms.append(NewRoom)
            RoomNo += 1

    map = postProcess(map, 'MAZE')
    Rooms, map = makePrefabRoom(map, DungeonLevel, Rooms)
    map = makeBetterRoom(Rooms, map)
    map = makeStairs(map, DungeonLevel)

    return map

def carveMaze(x, y, map, frontier):
    # Make the cell at x, y a space. Update the frontier and map accordingly.
    # This does not remove the current cell from the frontier, it only adds new cells.
    extra = []

    map[x][y].change(raw.RockFloor)

    if x > 0:
        if map[x - 1][y].hasFlag('LIQUID'):
            extra.append((x - 1, y))
    if x < var.MapWidth - 1:
        if map[x + 1][y].hasFlag('LIQUID'):
            extra.append((x + 1, y))
    if y > 0:
        if map[x][y - 1].hasFlag('LIQUID'):
            extra.append((x, y - 1))
    if y < var.MapHeight - 1:
        if map[x][y + 1].hasFlag('LIQUID'):
            extra.append((x, y + 1))

    random.shuffle(extra)
    for i in extra:
        frontier.append(i)

    return map, frontier

def hardenMaze(x, y, map):
    if map[x][y].hasFlag('GROUND'):
        return map, False

    map[x][y].change(raw.RockWall)

    return map, True

def checkMaze(x, y, map):
    # Test if the cell at x, y can become a floor.
    # True indicates it should become a floor, False indicates it should become a wall.
    edgestate = 0

    if x > 0:
        if map[x - 1][y].hasFlag('GROUND'):
            edgestate += 1
    if x < var.MapWidth - 1:
        if map[x + 1][y].hasFlag('GROUND'):
            edgestate += 2
    if y > 0:
        if map[x][y - 1].hasFlag('GROUND'):
            edgestate += 4
    if y < var.MapHeight - 1:
        if map[x][y + 1].hasFlag('GROUND'):
            edgestate += 8

    if edgestate == 1:
        if x < var.MapWidth - 1:
            if y > 0:
                if map[x + 1][y - 1].hasFlag('GROUND'):
                    return False
            if y < var.MapHeight - 1:
                if map[x + 1][y + 1].hasFlag('GROUND'):
                    return False
        return True
    elif edgestate == 2:
        if x > 0:
            if y > 0:
                if map[x - 1][y - 1].hasFlag('GROUND'):
                    return False
            if y < var.MapHeight - 1:
                if map[x - 1][y + 1].hasFlag('GROUND'):
                    return False
        return True
    elif edgestate == 4:
        if y < var.MapHeight - 1:
            if x > 0:
                if map[x - 1][y + 1].hasFlag('GROUND'):
                    return False
            if x < var.MapWidth - 1:
                if map[x + 1][y + 1].hasFlag('GROUND'):
                    return False
        return True
    elif edgestate == 8:
        if y > 0:
            if x > 0:
                if map[x - 1][y - 1].hasFlag('GROUND'):
                    return False
            if x < var.MapWidth - 1:
                if map[x + 1][y - 1].hasFlag('GROUND'):
                    return False
        return True
    return False

def buildPerlinForest(map, DungeonLevel):
    # TODO: Not working!!!

    noise = libtcod.noise_new(2)

    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            tile = libtcod.noise_get_fbm(noise, [x, y], 32.0)

            # TODO

    libtcod.noise_delete(noise)
    return map

def buildCity(map, DungeonLevel):
    # Make open arena.
    for y in range(1, var.MapHeight - 1):
        for x in range(1, var.MapWidth - 1):
            map[x][y].change(raw.RockFloor)

    Rooms = []

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

        if not Fail:
            map = NewRoom.create_square_room(map, True)
            map = NewRoom.create_entrance(map)

            Rooms.append(NewRoom)

    map = postProcess(map, 'CITY')
    Rooms, map = makePrefabRoom(map, DungeonLevel, Rooms)
    map = makeBetterRoom(Rooms, map)
    map = makeStairs(map, DungeonLevel, Rooms)

    return map

def postProcess(map, type = None):
    print "Starting post-processing dungeon."
    # TODO: Make this better.

    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            if type == 'CATACOMB':
                which = random.choice([
                raw.BonePile,
                raw.BonePile,
                raw.BonePile,
                raw.Grave
                ])
            elif type == 'CAVE':
                which = random.choice([
                raw.Vines,
                raw.Vines,
                raw.TallGrass,
                raw.TallGrass,
                raw.RockPile,
                raw.EarthFloor,
                raw.LeafyTree,
                raw.ConifTree,
                raw.ShallowWater,
                raw.ShallowWater,
                ])
            else:
                which = random.choice([
                raw.Vines,
                raw.Vines,
                raw.Vines,
                raw.RockPile,
                raw.ShallowWater,
                raw.ShallowWater,
                ])

            if (map[x][y].hasFlag('GROUND') and var.rand_chance(10)):
                map[x][y].change(which)

            if (map[x][y].hasFlag('WALL') and type == 'MAZE' and var.rand_chance(5)):
                which = random.choice([
                raw.WoodDoor,
                raw.ClosedPort,
                raw.SecretDoor,
                raw.SecretDoor,
                raw.SecretDoor
                ])

                map[x][y].change(which)

            # Replace damaged outer walls.
            if (x == 0 or x == var.MapWidth - 1 or
                y == 0 or y == var.MapHeight - 1):
                if not map[x][y].hasFlag('WALL'):
                    map[x][y].change(raw.RockWall)

    while var.rand_chance(15):
        if type == 'DUNGEON':
            liquid = raw.ShallowWater
        elif type == 'CATACOMB':
            liquid = random.choice([
            raw.Sand,
            raw.Sand,
            raw.DeepSand
            ])
        elif type == 'SEWERS':
            liquid = random.choice([
            raw.Mud,
            raw.ShallowWater,
            raw.ShallowWater,
            raw.ShallowWater,
            raw.DeepWater
            ])
        else:
            liquid = random.choice([
            raw.EarthFloor,
            raw.GrassFloor,
            raw.IceFloor,
            raw.Sand,
            raw.Snow,
            raw.DeepSnow,
            raw.TallGrass,
            raw.ShallowWater,
            raw.ShallowWater,
            raw.ShallowWater,
            raw.DeepWater
            ])

        print "Making a lake."
        map = makeLake(liquid, map)

    # Clean door generation must be after lake handling, or lakes will break our
    # door placement. This unfortunately means we cannot run through the tiles
    # only once with the above code.
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            if map[x][y].hasFlag('DOOR'):
                Path = False
                DoorFrame = False

                if (x - 1 > 0 and x + 1 < var.MapWidth):
                    if (map[x - 1][y].hasFlag('WALL') and
                        map[x + 1][y].hasFlag('WALL')):
                        DoorFrame = True
                    elif (map[x - 1][y].isWalkable() and
                          map[x + 1][y].isWalkable()):
                          Path = True
                if (y - 1 > 0 and y + 1 < var.MapHeight):
                    if (map[x][y - 1].hasFlag('WALL') and
                        map[x][y + 1].hasFlag('WALL')):
                        DoorFrame = True
                    elif (map[x][y - 1].isWalkable() and
                          map[x][y - 1].isWalkable()):
                          Path = True
                if (x - 1 > 0 and x + 1 < var.MapWidth and
                    y - 1 > 0 and y + 1 < var.MapHeight):
                    if (map[x - 1][y - 1].isWalkable() and
                        map[x + 1][y + 1].isWalkable()):
                        Path = True
                    if (map[x + 1][y - 1].isWalkable() and
                        map[x - 1][y + 1].isWalkable()):
                        Path = True

                if not DoorFrame or not Path:
                    map[x][y].change(raw.RockFloor)

    return map

def populate(DungeonLevel):
    MonsterNo = 0
    MonsterMax = var.MonsterMaxNumber + (2 * DungeonLevel)
    NewMob = None

    while MonsterNo < MonsterMax: # TODO: Danger level.
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        which = var.rand_weighted(getRandomEntity('MOB', DungeonLevel))
        NewMob = entity.spawn(x, y, which, 'MOB')

        if NewMob.isBlocked(x, y, DungeonLevel):
            NewMob = None

        if NewMob != None:
            var.Entities[DungeonLevel].append(NewMob)
            MonsterNo += 1

        NewMob = None

    ItemNo = 0
    NewItem = None
    # TODO: Item generation.

    while ItemNo < var.ItemMaxNumber:
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        which = var.rand_weighted(getRandomEntity('ITEM', DungeonLevel))
        NewItem = entity.spawn(x, y, which, 'ITEM')

        if NewItem.isBlocked(x, y, DungeonLevel):
            NewItem = None

        if NewItem != None:
            var.Entities[DungeonLevel].append(NewItem)

            ItemNo += 1

        NewItem = None

    # Special bosses:
    if DungeonLevel == 2: # A guaranteed kobold miner.
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        NewMob = entity.spawn(x, y, raw.KoboldMiner, 'MOB')
        var.Entities[DungeonLevel].append(NewMob)

        if NewMob.isBlocked(x, y, DungeonLevel):
            while NewMob.isBlocked(x, y, DungeonLevel):
                x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
                y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            NewMob.x = x
            NewMob.y = y

    if DungeonLevel in [0, 15]: # The black knight.
        x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
        y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

        NewMob = entity.spawn(x, y, raw.BlackKnight, 'MOB')
        var.Entities[DungeonLevel].append(NewMob)

        if NewMob.isBlocked(x, y, DungeonLevel):
            while NewMob.isBlocked(x, y, DungeonLevel):
                x = libtcod.random_get_int(0, 1, var.MapWidth - 2)
                y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            NewMob.x = x
            NewMob.y = y

def getRandomEntity(type, DungeonLevel = 0):
    # TODO: Base frequency on DL.
    choices = []

    if type == 'MOB':
        stuff = raw.MobList
    elif type == 'ITEM':
        stuff = raw.ItemList
    else:
        return None

    for i in stuff:
        frequency = 0

        try:
            frequency = i['frequency']
        except:
            if type == 'MOB':
                frequency = raw.DummyMonster['frequency']
            elif type == 'ITEM':
                frequency = raw.DummyItem['frequency']

        choices.append((i, frequency))
        #print "%s, %s" % (i['name'], frequency)

    return choices

###############################################################################
#  Objects
###############################################################################
class Terrain(object):
    def __init__(self, char, color, name, BlockMove, BlockSight, flags = []):
        self.char = char
        self.color = color
        self.name = name
        self.material = 'STONE'
        self.BlockMove = BlockMove
        self.BlockSight = BlockSight
        self.explored = None
        self.flags = flags

    def draw(self, x, y, Player):
        if Player != None:
            if ((libtcod.map_is_in_fov(var.FOVMap, x, y) and
                not (Player.hasFlag('CANNOT_SEE') or Player.hasIntrinsic('BLIND'))) or
                var.WizModeTrueSight):
                libtcod.console_set_default_foreground(var.MapConsole, self.color)
                libtcod.console_put_char(var.MapConsole, x, y, self.char, libtcod.BKGND_SCREEN)

                self.makeExplored()

            elif self.isExplored():
                libtcod.console_set_default_foreground(var.MapConsole, libtcod.darkest_grey)
                libtcod.console_put_char(var.MapConsole, x, y, self.explored, libtcod.BKGND_SCREEN)
        else:
            return
            #libtcod.console_set_default_foreground(var.Con, libtcod.black)
            #libtcod.console_put_char(var.MapConsole, x, y, ' ', libtcod.BKGND_SCREEN)

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
            self.material = NewTerrain['material']
        except:
            self.material = raw.DummyTerrain['material']
        try:
            self.BlockMove = NewTerrain['BlockMove']
        except:
            self.BlockMove = raw.DummyTerrain['BlockMove']
        try:
            self.BlockSight = NewTerrain['BlockSight']
        except:
            self.BlockSight = raw.DummyTerrain['BlockSight']
        # Clear all flags. This way works, otherwise strange errors in dungeon
        # generation crop up from time to time.
        try:
            del self.flags
        except:
            print "Failed to clear flags from %s." % self.name
        try:
            self.flags = NewTerrain['flags']
        except:
            self.flags = raw.DummyTerrain['flags']

    def hasFlag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False

    def isWalkable(self):
        if ((self.hasFlag('GROUND') or self.hasFlag('DOOR') or
            self.hasFlag('LIQUID') or self.hasFlag('FEATURE')) and
            not self.hasFlag('SWIM')):
            return True
        else:
            return False

    def isExplored(self):
        if self.explored == None:
            return False
        else:
            return True

    def makeExplored(self):
        self.explored = self.char

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
    def create_square_room(self, map, makeWalls = False):
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                map[x][y].change(raw.RockFloor)

        if makeWalls == True:
            for x in [self.x1, self.x2]:
                for y in range(self.y1, self.y2 + 1):
                    map[x][y].change(raw.RockWall)
            for y in [self.y1, self.y2]:
                for x in range(self.x1, self.x2 + 1):
                    map[x][y].change(raw.RockWall)

        return map

    def create_circular_room(self, map):
        r = min(self.width / 2, self.height / 2)

        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                if math.sqrt((x - self.CenterX) ** 2 +
                             (y - self.CenterY) ** 2) <= r:
                    map[x][y].change(raw.RockFloor)

        return map

    def create_h_tunnel(self, OtherX, map):
        for x in range(min(self.CenterX, OtherX), max(self.CenterX, OtherX) + 1):
            if (x == self.x1 or x == self.x2):
                if var.rand_chance(5):
                    which = random.choice([raw.SecretDoor, raw.ClosedPort])
                    map[x][self.CenterY].change(which)
                else:
                    map[x][self.CenterY].change(raw.WoodDoor)
            else:
                map[x][self.CenterY].change(raw.RockFloor)

        return map

    def create_v_tunnel(self, OtherY, map):
        for y in range(min(self.CenterY, OtherY), max(self.CenterY, OtherY) + 1):
            if (y == self.y1 or y == self.y2):
                if var.rand_chance(5):
                    which = random.choice([raw.SecretDoor, raw.ClosedPort])
                    map[self.CenterX][y].change(which)
                else:
                    map[self.CenterX][y].change(raw.WoodDoor)
            else:
                map[self.CenterX][y].change(raw.RockFloor)

        return map

    def create_d_tunnels(self, OtherRooms, map):
        # This must be possible in some easier way...
        end = False
        x = self.x1
        y = self.y1
        dx = -1
        dy = -1

        while (x + dx >= 0 and x + dx < var.MapWidth and
               y + dy >= 0 and y + dy < var.MapHeight):
            if (x == self.x1 and y == self.y1):
                map[x][y].change(raw.WoodDoor)
            elif len(OtherRooms) == 0:
                which = random.choice([
                raw.RockFloor,
                raw.RockFloor,
                raw.ShallowWater,
                raw.ShallowWater,
                raw.Mud
                ])

                map[x][y].change(which)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        which = random.choice([
                        raw.RockFloor,
                        raw.RockFloor,
                        raw.ShallowWater,
                        raw.ShallowWater,
                        raw.Mud
                        ])

                        map[x][y].change(which)

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
                map[x][y].change(raw.WoodDoor)
            elif len(OtherRooms) == 0:
                which = random.choice([
                raw.RockFloor,
                raw.RockFloor,
                raw.ShallowWater,
                raw.ShallowWater,
                raw.Mud
                ])

                map[x][y].change(which)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        which = random.choice([
                        raw.RockFloor,
                        raw.RockFloor,
                        raw.ShallowWater,
                        raw.ShallowWater,
                        raw.Mud
                        ])

                        map[x][y].change(which)

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
                map[x][y].change(raw.WoodDoor)
            elif len(OtherRooms) == 0:
                which = random.choice([
                raw.RockFloor,
                raw.RockFloor,
                raw.ShallowWater,
                raw.ShallowWater,
                raw.Mud
                ])

                map[x][y].change(which)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        which = random.choice([
                        raw.RockFloor,
                        raw.RockFloor,
                        raw.ShallowWater,
                        raw.ShallowWater,
                        raw.Mud
                        ])

                        map[x][y].change(which)

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
                map[x][y].change(raw.WoodDoor)
            elif len(OtherRooms) == 0:
                which = random.choice([
                raw.RockFloor,
                raw.RockFloor,
                raw.ShallowWater,
                raw.ShallowWater,
                raw.Mud
                ])

                map[x][y].change(which)
            else:
                for room in OtherRooms:
                    if (x <= room.x2 and x >= room.x1 and
                        y <= room.y2 and y >= room.y2 and room != self):
                        end = True
                        break
                    else:
                        which = random.choice([
                        raw.RockFloor,
                        raw.RockFloor,
                        raw.ShallowWater,
                        raw.ShallowWater,
                        raw.Mud
                        ])

                        map[x][y].change(which)

            if end:
                break
            else:
                x = x + dx
                y = y + dy

        return map

    def create_entrance(self, map, circular = False):
        # Not really recommended for circular rooms. EDIT: Works for circular rooms now!

        # Find possible placement of doors:
        possible = []
        for x in [self.x1, self.x2]:
            if circular:
                possible.append((x, self.CenterY))
            else:
                for y in range(self.y1 + 1, self.y2):
                    possible.append((x, y))
        for y in [self.y1, self.y2]:
            if circular:
                possible.append((self.CenterX, y))
            else:
                for x in range(self.x1 + 1, self.x2):
                    possible.append((x, y))

        # We can have between 1 and 5 doors for every room.
        doorMax = libtcod.random_get_int(0, 1, 5)
        doorNo = 0
        # Let's have same door type for one room:
        which = random.choice([
        raw.RockFloor,
        raw.WoodDoor,
        raw.WoodDoor,
        raw.WoodDoor,
        raw.WoodDoor,
        raw.ClosedPort,
        raw.ClosedPort,
        #raw.Curtain,
        raw.SecretDoor
        ])

        while doorNo < doorMax:
            x, y = random.choice(possible)

            map[x][y].change(which)
            doorNo += 1

        return map
