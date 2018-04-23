# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random
import sys

import entity
import raw
import ui
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

    # TODO: Dungeon levels:
    #  0 the Surface
    #  1 traditional dungeon
    #  2 traditional / cave
    #  3 traditional / cave
    #  4 traditional / cave
    #  5 the Minetown (city?)
    #  6 sewers
    #  7 sewers
    #  8 BSP / maze
    #  9 BSP / maze
    # 10 the Big room
    # 11 traditional / cave / BSP / city
    # 12 traditional / cave / BSP / city
    # 13 traditional / cave / BSP / city
    # 14 traditional / cave / BSP / city
    # 15 the Goal

    which = libtcod.random_get_int(0, 1, 4)

    if DungeonLevel == 0:
        print "Building the world."
        map = buildWorld(map, DungeonLevel)
    elif DungeonLevel == 1:
        print "Building traditional dungeon."
        map = buildTraditionalDungeon(map, DungeonLevel)
    elif DungeonLevel in [10, 15]:
        print "Building a special map."
        map = buildBigRoom(map, DungeonLevel)
    elif DungeonLevel < 5:
        if which < 3:
            print "Building a cave."
            map = buildDrunkenCave(map, DungeonLevel)
        else:
            print "Building traditional dungeon."
            map = buildTraditionalDungeon(map, DungeonLevel)
    elif DungeonLevel == 5:
        print "Building a city."
        map = buildCity(map, DungeonLevel)
    elif DungeonLevel < 8:
        print "Building sewers."
        map = buildSewers(map, DungeonLevel)
    elif DungeonLevel < 10:
        if which < 3:
            print "Building BSP dungeon."
            map = buildBSPDungeon(map, DungeonLevel)
        else:
            print "Building a maze."
            map = buildMaze(map, DungeonLevel)
    else:
        if which == 1:
            print "Building traditional dungeon."
            map = buildTraditionalDungeon(map, DungeonLevel)
        elif which == 2:
            print "Building BSP dungeon."
            map = buildBSPDungeon(map, DungeonLevel)
        elif which == 3:
            print "Building a city."
            map = buildCity(map, DungeonLevel)
        else:
            print "Building a cave."
            map = buildDrunkenCave(map, DungeonLevel)

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
        List = list(raw.RoomList)
        random.shuffle(List)

        for room in Rooms:
            for Prefab in List:

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
        for x in [0, var.MapWidth - 1]:
            for y in range(var.MapHeight):
                if not map[x][y].hasFlag('WALL'):
                    map[x][y].change(raw.RockWall)

        for y in [0, var.MapHeight - 1]:
            for x in range(var.MapWidth):
                if not map[x][y].hasFlag('WALL'):
                    map[x][y].change(raw.RockWall)

        return Rooms, map
    elif Rooms == None:
        if Prefab == None:
            Prefab = random.choice(raw.RoomList)

        fails = 0
        # Be careful, Room.width and Prefab['width'] are different by 1. (Yeah,
        # I will hate myself for this.)
        width = Prefab['width']
        height = Prefab['height']

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
        for x in [0, var.MapWidth - 1]:
            for y in range(var.MapHeight):
                if not map[x][y].hasFlag('WALL'):
                    map[x][y].change(raw.RockWall)

        for y in [0, var.MapHeight - 1]:
            for x in range(var.MapWidth):
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
                    special = False

                    if item in ['RANDOM_ANY', 'RANDOM_SPECIAL']:
                        if item == 'RANDOM_SPECIAL':
                            special = True
                            
                        item = var.rand_weighted(getRandomEntity('ITEM', DungeonLevel))
                    elif item == 'RANDOM_ARTIFACT':
                        pass # TODO

                    NewItem = entity.spawn(x, y, item, 'ITEM')

                    if special:
                        NewItem.gainMagic(True)

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
                        if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
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
                        if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
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
                        if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
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
                        if m in range(0, var.MapWidth) and n in range(0, var.MapHeight):
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

def makeVaults(map, Rooms):
    # TODO: After stairs creation, try adding secret rooms.
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
    map = makeBetterDoor(map)
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
    BSPmap = makeBetterDoor(BSPmap)
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
    type = 'CAVE'
    if var.rand_chance(5):
        type = 'ICE'

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

    map = postProcess(map, type)

    while var.rand_chance(50):
        map = makePrefabRoom(map, DungeonLevel)

    map = makeBetterDoor(map)
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
    map = makeBetterDoor(map)
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
    map = makeBetterDoor(map)
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

def buildWorld(map, DungeonLevel):
    # TODO

    HeightMap = libtcod.heightmap_new(var.MapWidth, var.MapHeight)

    # Main hills:
    if var.rand_chance(90):
        islands = False

        for i in range(25):
            libtcod.heightmap_add_hill(HeightMap,
                                       libtcod.random_get_int(0, var.MapWidth / 10, var.MapWidth - var.MapWidth / 10),
                                       libtcod.random_get_int(0, var.MapHeight / 10, var.MapHeight - var.MapHeight / 10),
                                       libtcod.random_get_int(0, 8, 12),
                                       libtcod.random_get_int(0, 6, 10))
    else:
        islands = True

    # Small hills:
    if islands:
        hills = 100
    else:
        hills = 200

    for i in range(hills):
        libtcod.heightmap_add_hill(HeightMap,
                                   libtcod.random_get_int(0, var.MapWidth / 10, var.MapWidth - var.MapWidth / 10),
                                   libtcod.random_get_int(0, var.MapHeight / 10, var.MapHeight - var.MapHeight / 10),
                                   libtcod.random_get_int(0, 2, 4),
                                   libtcod.random_get_int(0, 6, 10))

    libtcod.heightmap_normalize(HeightMap, 0.0, 1.0)

    # Apply simplex:
    '''
    NoiseMap = libtcod.heightmap_new(var.MapWidth, var.MapHeight)
    noise = libtcod.noise_new(2)
    libtcod.heightmap_add_fbm(NoiseMap, noise, 6, 6, 0, 0, 32, 1, 1)
    libtcod.heightmap_normalize(NoiseMap, 0.0, 1.0)
    libtcod.heightmap_multiply_hm(HeightMap, NoiseMap, HeightMap)
    '''

    # Erosion:
    '''
    erosion = abs(random.random())
    sedimentation = abs(random.random())

    if sedimentation > erosion:
        sedimentation = erosion
    '''

    libtcod.heightmap_rain_erosion(HeightMap, var.MapWidth * var.MapHeight, 0.07, 0, 0)
    libtcod.heightmap_clamp(HeightMap, 0.0, 1.0)

    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            tile = libtcod.heightmap_get_value(HeightMap, x, y)

            if tile < 0.1:
                map[x][y].change(raw.DeepWater)
            elif tile < 0.2:
                map[x][y].change(raw.ShallowWater)
            elif tile < 0.3:
                map[x][y].change(raw.Sand)
            elif tile > 0.8:
                map[x][y].change(raw.Mountain)
            elif tile > 0.6:
                if var.rand_chance(15):
                    map[x][y].change(raw.ConifTree)
                elif var.rand_chance(15):
                    map[x][y].change(raw.LeafyTree)
                else:
                    map[x][y].change(raw.TallGrass)
            else:
                map[x][y].change(raw.GrassFloor)

    libtcod.heightmap_delete(HeightMap)
    #libtcod.heightmap_delete(NoiseMap)
    #libtcod.noise_delete(noise)

    map = postProcess(map, 'FOREST')
    map = makeStairs(map, DungeonLevel)

    return map

def buildBigRoom(map, DungeonLevel):
    #if DungeonLevel == 0:
    #    type = 'SURFACE'
    #    which = random.choice(raw.SurfaceList)
    if DungeonLevel == 10:
        type = 'BIG'
        which = random.choice(raw.BigRoomList)
    elif DungeonLevel == 15:
        type = 'GOAL'
        which = random.choice(raw.GoalList)
    else:
        # Should not happen.
        type = None
        which = random.choice(raw.BigRoomList)


    width = which['width'] - 1
    height = which['height'] - 1

    x = (var.MapWidth - width) / 2
    y = (var.MapHeight - height) / 2

    NewRoom = Room(x, y, width, height)
    map = create_prefab(which, NewRoom, map, DungeonLevel)

    # Surface and goal levels are set, so no postProcess() and similar in here,
    # but otherwise add something nice.
    if type in ['BIG', None]:
        map = postProcess(map, type)
        map = makeBetterDoor(map) # Must be here because of postProcess().

    map = makeStairs(map, DungeonLevel, [NewRoom])

    return map

def buildPrefabLevel(map, DungeonLevel):
    # Let's see how this works out.
    Rooms = []

    for i in range(var.RoomMaxNumber):
        Prefab = random.choice(raw.RoomList)

        width = Prefab['width']
        height = Prefab['height']

        x = libtcod.random_get_int(0, 0, var.MapWidth - width - 1)
        y = libtcod.random_get_int(0, 0, var.MapHeight - height - 1)

        NewRoom = Room(x, y, width, height)
        Fail = False

        for OtherRoom in Rooms:
            if NewRoom.intersect(OtherRoom):
                Fail = True
                break

        if not Fail:
            map = create_prefab(Prefab, NewRoom, map, DungeonLevel)

            Rooms.append(NewRoom)

    map = makeBetterDoor(map)
    # TODO: Check connectivity of stairs.
    map = makeStairs(map, DungeonLevel)

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
    map = makeBetterDoor(map)
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
                raw.Grave,
                raw.Pit
                ])
            elif type == 'FOREST':
                which = random.choice([
                raw.Vines,
                raw.TallGrass,
                raw.TallGrass,
                raw.RockPile,
                raw.EarthFloor,
                raw.LeafyTree,
                raw.ConifTree
                ])
            elif type == 'ICE':
                which = random.choice([
                raw.IceFloor,
                raw.IceFloor,
                raw.DeepSnow,
                raw.SnowTree,
                raw.SnowTree,
                raw.RockPile,
                raw.SnowPile,
                raw.ShallowWater,
                raw.ShallowWater
                ])
            elif type in ['CAVE', 'BIG']:
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
                raw.ShallowWater
                ])
            else:
                which = random.choice([
                raw.Vines,
                raw.Vines,
                raw.Vines,
                raw.RockPile,
                raw.ShallowWater,
                raw.ShallowWater
                ])

            if map[x][y].hasFlag('GROUND') and var.rand_chance(10):
                if var.rand_chance(1) and not type == 'FOREST':
                    which = raw.Pit

                map[x][y].change(which)
            elif map[x][y].hasFlag('GROUND') and type == 'ICE':
                map[x][y].change(raw.Snow)

            if (map[x][y].hasFlag('WALL') and type == 'MAZE' and var.rand_chance(5)):
                which = random.choice([
                raw.WoodDoor,
                raw.ClosedPort,
                raw.SecretDoor,
                raw.SecretDoor,
                raw.SecretDoor,
                raw.Pit
                ])

                map[x][y].change(which)

            # Replace damaged outer walls.
            if type != 'FOREST':
                if (x == 0 or x == var.MapWidth - 1 or
                    y == 0 or y == var.MapHeight - 1):
                    if not map[x][y].hasFlag('WALL'):
                        map[x][y].change(raw.RockWall)

    while var.rand_chance(15) and type != 'FOREST':
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
        elif type == 'ICE':
            liquid = random.choice([
            raw.IceFloor,
            raw.Snow,
            raw.DeepSnow,
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

    return map

def makeBetterDoor(map):
    # Clean door generation must be after handling everything else, or lakes and
    # prefabs may break our door placement. This unfortunately means we cannot run
    # through the tiles only once with postProcess().
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
                          map[x][y + 1].isWalkable()):
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
    # Monster generation:
    if DungeonLevel != 0:
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

    # Item generation.
    if DungeonLevel != 0 and DungeonLevel != 15:
        ItemNo = 0
        NewItem = None

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

        if type == 'MOB':
            try:
                DangerLevel = i['DL']
            except:
                DangerLevel = raw.DummyMonster['DL']

            if DangerLevel > DungeonLevel:
                continue

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
        self.BlockMove = BlockMove
        self.BlockSight = BlockSight
        self.flags = flags

        self.material = 'STONE'
        self.explored = None
        self.inventory = []

    def draw(self, x, y, canSee): # This canSee refers to the Player, whether he's blind or not.
        if (libtcod.map_is_in_fov(var.FOVMap, x, y) and canSee) or var.WizModeTrueSight:
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

        # TODO: Chopped down shelves, buried items in newly dug pits.
        '''
        if len(self.inventory) > 0:
            for item in self.inventory:
                self.inventory.remove(item)
                # TODO: item.x, item.y
                var.getEntity().append(item)
                item.tryStacking()
        '''

    def getName(self, capitalize = False, full = False):
        name = self.name

        if capitalize == True:
            name = name.capitalize()

        return name

    def hasFlag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False

    def isWalkable(self):
        if self.BlockMove and not self.hasFlag('DOOR'):
            return False

        for flag in self.flags:
            if flag in ['BURN', 'DISSOLVE', 'HARM', 'SWIM']:
                return False

        return True

    def isExplored(self):
        if self.explored == None:
            return False
        else:
            return True

    def makeExplored(self):
        self.explored = self.char

    def beDug(self, Digger):
        if Digger.SP <= 0:
            return False

        # Dig and chop!
        if Digger.hasIntrinsic('CAN_CHOP') and self.hasFlag('CAN_BE_CHOPPED'):
            ui.message("%s chop&S down the %s." % (Digger.getName(True), self.name), actor = Digger)

            if self.hasFlag('DOOR') and self.material == 'WOOD':
                self.change(raw.BrokenDoor)
            else:
                self.change(raw.DestroyedTerrainList[self.material])

            modifier = 5 * (0.9 ** Digger.getIntrinsicPower('CAN_CHOP'))
            Digger.AP -= Digger.getActionAPCost(modifier)
            return True
        elif Digger.hasIntrinsic('CAN_DIG') and self.hasFlag('CAN_BE_DUG'):
            ui.message("%s dig&S the %s." % (Digger.getName(True), self.name), actor = Digger)

            if self.hasFlag('WALL'):
                self.change(raw.DestroyedTerrainList[self.material])
            else:
                print "Unhandled diggable tile."
                return False

            modifier = 5 * (0.9 ** Digger.getIntrinsicPower('CAN_DIG'))
            Digger.AP -= Digger.getActionAPCost(modifier)
            return True

        return False

    def beLooted(self, Looter):
        if not self.hasFlag('CONTAINER'):
            if Looter.hasFlag('AVATAR'):
                ui.message("You cannot loot the %s." % self.getName())
            return False

        if self.hasFlag('MAGIC_BOX') and len(var.MagicBox) == 0:
            if Looter.hasFlag('AVATAR'):
                ui.message("%s is empty." % self.getName(True))
            return False
        elif not self.hasFlag('MAGIC_BOX') and len(self.inventory) == 0:
            if Looter.hasFlag('AVATAR'):
                ui.message("%s is empty." % self.getName(True))
            return False

        if Looter.getBurdenState() == 3:
            if Looter.hasFlag('AVATAR'):
                ui.message("Your inventory is already full.")
            return False

        if self.hasFlag('MAGIC_BOX'):
            if Looter.hasFlag('AVATAR'):
                toLoot = ui.option_menu("Take what?", var.MagicBox)
            else:
                toLoot = libtcod.random_get_int(0, 0, len(var.MagicBox))
        else:
            if Looter.hasFlag('AVATAR'):
                toLoot = ui.option_menu("Take what?", self.inventory)
            else:
                toLoot = libtcod.random_get_int(0, 0, len(self.inventory))

        if toLoot == None:
            return False
        elif self.hasFlag('MAGIC_BOX'):
            try:
                item = var.MagicBox[toLoot]

                Looter.inventory.append(item)
                item.tryStacking(Looter)
                var.MagicBox.remove(item)
                Looter.AP -= Looter.getActionAPCost()
            except:
                pass # Out-of-bounds letter was pressed.
        else:
            try:
                item = self.inventory[toLoot]

                Looter.inventory.append(item)
                item.tryStacking(Looter)
                self.inventory.remove(item)
                Looter.AP -= Looter.getActionAPCost()
            except:
                pass # Out-of-bounds letter was pressed.

        if len(self.inventory) >= 1:
            return True
        else:
            return False

    def beStored(self, Looter):
        if not self.hasFlag('CONTAINER'):
            if Looter.hasFlag('AVATAR'):
                ui.message("You cannot loot the %s." % self.getName())
            return False

        if len(self.inventory) >= 30 and not self.hasFlag('HOLDING'):
            if Looter.hasFlag('AVATAR'):
                ui.message("%s is full." % self.getName(True))
            return False

        toLoot = ui.option_menu("Put in what?", Looter.inventory)

        if toLoot == None:
            return False
        elif self.hasFlag('MAGIC_BOX'):
            try:
                item = Looter.inventory[toLoot]

                var.MagicBox.append(item)
                print "appended"
                Looter.inventory.remove(item)
                Looter.AP -= Looter.getActionAPCost()
            except:
                pass # Out-of-bounds letter was pressed.
        else:
            try:
                item = Looter.inventory[toLoot]

                self.inventory.append(item)
                item.tryStacking(self)
                Looter.inventory.remove(item)
                Looter.AP -= Looter.getActionAPCost()
            except:
                pass # Out-of-bounds letter was pressed.

        if len(Looter.inventory) >= 1:
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

def isOnMap(x, y):
    if x in range(0, var.MapWidth) and y in range(0, var.MapHeight):
        return True
    else:
        return False

def isOnMapEdge(x, y):
    if x == 0 or y == 0 or x == var.MapWidth - 1 or y == var.MapHeight - 1:
        return True
    else:
        return False
