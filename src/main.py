# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import var

###############################################################################
#  Objects
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
        if (libtcod.map_is_in_fov(FOVMap, self.x, self.y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(Con, self.color)
            libtcod.console_put_char(Con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def isBlocked(self, x, y):
        if map[x][y].BlockMove:
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
        libtcod.map_compute_fov(FOVMap, self.x, self.y, self.FOVRadius, True, 0)

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
            if map[x][y].CanBeOpened == True:
                if(self.actionOpen(x, y)):
                    self.AP -= 1
                    return

        self.actionWalk(dx, dy)

    def actionOpen(self, x, y):
        if (x > 0 and x < var.MapWight and y > 0 and y < var.MapHeight):
            if map[x][y].CanBeOpened == True:
                if map[x][y].name == 'door':
                    map[x][y].change(OpenDoor)
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

# Map objects.
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
        if (libtcod.map_is_in_fov(FOVMap, x, y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(Con, self.color)
            self.explored = True
        elif (self.explored == True):
            libtcod.console_set_default_foreground(Con, libtcod.darkest_grey)
        else:
            return
            #libtcod.console_set_default_foreground(Con, libtcod.black)
        libtcod.console_put_char(Con, x, y, self.char, libtcod.BKGND_NONE)

    def change(self, NewTerrain):
        self.char = NewTerrain.char
        self.color = NewTerrain.color
        self.name = NewTerrain.name
        self.BlockMove = NewTerrain.BlockMove
        self.BlockSight = NewTerrain.BlockSight
        self.CanBeOpened = NewTerrain.CanBeOpened

# Dungeon generation:
# TODO: Move into Dungeon.py
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
                if rand_chance(50):
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
                        if rand_chance(50):
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
                if rand_chance(50):
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
                        if rand_chance(50):
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
                if rand_chance(50):
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
                        if rand_chance(50):
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
                if rand_chance(50):
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
                        if rand_chance(50):
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
        if rand_chance(50):
            self.buildTraditionalDungeon()
        else:
            self.buildDrunkenCave()
        #self.buildSewers()

        if populate:
            self.populate()
        else:
            for i in var.Entities:
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
                libtcod.map_set_properties(FOVMap, x, y, not map[x][y].BlockSight, not map[x][y].BlockMove)

        # On the off-chance we trap the player:
        if Player.isBlocked(Player.x, Player.y):
            x = 0
            y = 0

            while Player.isBlocked(x, y):
                x = libtcod.random_get_int(0, 1, var.MapWight - 2)
                y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            Player.x = x
            Player.y = y

        Player.UpdateFOV()

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
            if (RoomNo < 20 and rand_chance(20)):
                Fail = False

            if not Fail:
                if rand_chance(20):
                    NewRoom.create_circular_room()
                else:
                    NewRoom.create_square_room()

                if RoomNo != 0:
                    PrevRoom = Rooms[RoomNo - 1]

                    if rand_chance(50):
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
                if (map[x][y].name == 'floor' and rand_chance(3)):
                    map[x][y].change(Vines)

                elif (map[x][y].name == 'floor' and rand_chance(2)):
                    map[x][y].change(ShallowWater)

                elif (map[x][y].name == 'floor' and rand_chance(2)):
                    map[x][y].change(RockPile)

        while rand_chance(15):
            self.makeLake(ShallowWater)

    def populate(self):
        MonsterNo = 0
        NewMob = None

        while MonsterNo < var.MonsterMaxNumber:
            x = libtcod.random_get_int(0, 1, var.MapWight - 2)
            y = libtcod.random_get_int(0, 1, var.MapHeight - 2)

            # TODO: Rework.
            if rand_chance(80):
                NewMob = Mob(x, y, 'o', libtcod.desaturated_green, 'orc', 0, 0, 0)
            else:
                NewMob = Mob(x, y, 'T', libtcod.dark_green, 'troll', 2, -1, 3)

            if NewMob.isBlocked(x, y):
                NewMob = None

            if NewMob != None:
                var.Entities.append(NewMob)
                MonsterNo += 1

            NewMob = None

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(var.ScreenWidth, var.ScreenHeight, 'RGLK', False)

# Base console:
Con = libtcod.console_new(var.ScreenWidth, var.ScreenHeight)
# Set FOV:
FOVMap = libtcod.map_new(var.MapWight, var.MapHeight)

# Player must be defined here, we work with him shortly.
Player = Mob(1, 1, '@', libtcod.white, 'Player', 0, 0, 0)
var.Entities.append(Player)
# TODO: All of this should go to a script file.
RockWall = Terrain('#', libtcod.dark_grey, 'wall', True, True, False)
RockFloor = Terrain('.', libtcod.light_grey, 'floor', False, False, False)
WoodDoor = Terrain('+', libtcod.darkest_orange, 'door', False, True, True)
OpenDoor = Terrain('\'', libtcod.darkest_orange, 'open door', False, False, False)
Vines = Terrain('|', libtcod.dark_green, 'hanging vines', False, True, False)
ShallowWater = Terrain('~', libtcod.blue, 'water', False, False, False)
Lava = Terrain('~', libtcod.dark_red, 'lava', False, False, False)
RockPile = Terrain('*', libtcod.darker_grey, 'rock pile', False, False, False)

###############################################################################
#  Functions
###############################################################################

# Let's hope I didn't mess up the chances...
def rand_chance(percent):
    if libtcod.random_get_int(0, 1, 100) > percent:
        return False
    else:
        return True

# Player input
def handle_keys():

    Key = libtcod.console_wait_for_keypress(True)

    # Alt+Enter goes fullscreen
    if Key.vk == libtcod.KEY_ENTER and Key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # Exit game with Ctrl + Q
    if (Key.lctrl and (Key.vk == libtcod.KEY_CHAR and Key.c == ord('q'))):
        return 'exit'


    # WIZARD MODE:
    # Walk through walls
    if Key.vk == libtcod.KEY_F1:
        var.WizModeNoClip
        var.WizModeNoClip = not var.WizModeNoClip

    # Magic map
    if Key.vk == libtcod.KEY_F2:
        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                map[x][y].explored = True

    if Key.vk == libtcod.KEY_F3:
        var.WizModeTrueSight
        var.WizModeTrueSight = not var.WizModeTrueSight

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        for y in range(var.MapHeight):
            for x in range(var.MapWight):
                libtcod.console_put_char_ex(Con, x, y, ' ', libtcod.black, libtcod.black)
        # Does not work with monster generation, TODO?

        Dungeon.makeMap(False)


    # MOVEMENT:
    if not var.PlayerIsDead:
        dx = 0
        dy = 0

        if (libtcod.console_is_key_pressed(libtcod.KEY_UP) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP8)):
            dy -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_DOWN) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP2)):
            dy += 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_LEFT) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP4)):
            dx -= 1
        elif (libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) or
            libtcod.console_is_key_pressed(libtcod.KEY_KP6)):
            dx += 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP7):
            dx -= 1
            dy -= 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP9):
            dx += 1
            dy -= 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP1):
            dx -= 1
            dy += 1
        elif libtcod.console_is_key_pressed(libtcod.KEY_KP3):
            dx += 1
            dy += 1

        if (dx != 0 or dy != 0):
            Player.actionBump(dx, dy)

def render_all():
    for y in range(var.MapHeight):
        for x in range(var.MapWight):
            tile = map[x][y]
            tile.draw(x, y)

    for mob in var.Entities:
        if mob != Player:
            mob.draw()
    # Draw player last, over everything else.
    Player.draw()

    libtcod.console_blit(Con, 0, 0, var.ScreenWidth, var.ScreenHeight, 0, 0, 0)

###############################################################################
#  Main Loop
###############################################################################

Dungeon = Builder()
Dungeon.makeMap(True)

while not libtcod.console_is_window_closed():
    for i in var.Entities:
        # How else to check if entity has a speed variable?
        try:
            i.AP += i.speed
        except:
            i.AP += 1

    # Player turn
    while Player.AP >= 1:
        # Redraw screen with each of the player's turns.
        # Draw screen:
        render_all()
        # Print screen:
        libtcod.console_flush()
        # Handle player input
        Exit = handle_keys()
        if Exit == 'exit':
            break
    # This looks ugly...
    if Exit == 'exit':
        break

    # Monster turn
    #for i in var.Entities:
    #    while i.AP >= 1:
    #        handle_monsters(i)
