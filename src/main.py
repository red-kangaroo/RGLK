# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Global Variables
###############################################################################

# TODO: Most of this should be in a script file.
# TODO: Also split it into multiple files.

ScreenWidth = 100
ScreenHeight = 55
MapWight = 80
MapHeight = 50

RoomMinSize = 5
RoomMaxSize = 10
RoomMaxNumber = 99
DrunkenSteps = 5000

FOVDefault = 0 # Default algorithm
FOVLightsWalls = True
FOVRadius = 6 # TODO: This should depend on stats and equipment.

MonsterMaxNumber = 30

PlayerIsDead = False

WizModeNoClip = False
WizModeTrueSight = False

Entities = []

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
        self.turn = 0.0 # Start with 0 turns to take.
        self.BlockMove = BlockMove

    def move(self, dx, dy):
        if (self.x + dx < 0 or self.x + dx > MapWight - 1 or
            self.y + dy < 0 or self.y + dy > MapHeight - 1):
            return

        self.x += dx
        self.y += dy

    def draw(self):
        # Set color and draw character on screen.
        if (libtcod.map_is_in_fov(FOVMap, self.x, self.y) or WizModeTrueSight):
            libtcod.console_set_default_foreground(Con, self.color)
            libtcod.console_put_char(Con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def isBlocked(self, x, y):
        if map[x][y].BlockMove:
            return True

        for i in Entities:
            if (i.BlockMove and i.x == x and i.y == y):
                return True

        return False

class Mob(Entity):
    def __init__(self, x, y, char, color, name,
                 Str, Dex, End, speed = 1.0):
        self.Str = Str
        self.Dex = Dex
        self.End = End
        self.speed = speed
        BlockMove = True # All mobs block movement, but not all entities,
                         # so pass this to Entity __init__

        super(Mob, self).__init__(x, y, char, color, name, BlockMove)

    def UpdateFOV(self):
        libtcod.map_compute_fov(FOVMap, self.x, self.y, FOVRadius, FOVLightsWalls, FOVDefault)

    # Actions:
    def actionAttack(self, dx, dy, victim):
        print "%s attacks %s." % (self.name, victim.name)
        self.turn -= 1

    def actionBump(self, dx, dy):
        bumpee = None
        x = self.x + dx
        y = self.y + dy

        for i in Entities:
            if i.x == x and i.y == y:
                bumpee = i
                break

        if bumpee != None:
            self.actionAttack(dx, dy, bumpee)
            return

        if (x > 0 and x < MapWight and y > 0 and y < MapHeight):
            if map[x][y].CanBeOpened == True:
                if(self.actionOpen(x, y)):
                    return

        self.actionWalk(dx, dy)

    def actionOpen(self, x, y):
        if (x > 0 and x < MapWight and y > 0 and y < MapHeight):
            if map[x][y].CanBeOpened == True:
                if map[x][y].name == 'door':
                    map[x][y].change(OpenDoor)
                    return True
        return False

    def actionWalk(self, dx, dy):
        moved = False

        if (not self.isBlocked(self.x + dx, self.y + dy) or WizModeNoClip):
            self.move(dx, dy)
            moved = True

        if moved == True:
            self.UpdateFOV()

        self.turn -= 1

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
        if (libtcod.map_is_in_fov(FOVMap, x, y) or WizModeTrueSight):
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
        pass

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

class Builder(object):
    def makeMap(self):
        global map

        # Fill map with walls.
        map = [[ Terrain('#', libtcod.dark_grey, 'wall', True, True, False)
          for y in range(MapHeight) ]
            for x in range(MapWight) ]

        if rand_chance(50):
            self.buildTraditionalDungeon()
        else:
            self.buildDrunkenCave()

        # Make FOV map:
        for y in range(MapHeight):
            for x in range(MapWight):
                libtcod.map_set_properties(FOVMap, x, y, not map[x][y].BlockSight, not map[x][y].BlockMove)

        Player.UpdateFOV()

    def makeLake(self, liquid):
        # This is basically a bit changed drunken cave.
        StepsTaken = 0
        Fails = 0

        x = libtcod.random_get_int(0, 1, MapWight - 2)
        y = libtcod.random_get_int(0, 1, MapHeight - 2)

        while (StepsTaken < (DrunkenSteps / 4) and Fails < 2000):
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

            if (x + dx > 0 and x + dx < MapWight - 1 and
                y + dy > 0 and y + dy < MapHeight - 1):
                x += dx
                y += dy

                StepsTaken += 1
            else:
                Fails += 1

    def buildTraditionalDungeon(self):
        Rooms = []
        RoomNo = 0

        # Add rooms.
        for i in range(RoomMaxNumber):
            width = libtcod.random_get_int(0, RoomMinSize, RoomMaxSize)
            height = libtcod.random_get_int(0, RoomMinSize, RoomMaxSize)

            x = libtcod.random_get_int(0, 0, MapWight - width - 1)
            y = libtcod.random_get_int(0, 0, MapHeight - height - 1)

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
                NewRoom.create_square_room()

                if RoomNo == 0:
                    Player.x = NewRoom.CenterX
                    Player.y = NewRoom.CenterY
                else:
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

        for y in range(MapHeight):
            for x in range(MapWight):

                if map[x][y].name == 'door':
                    #AdjacentWalls = 0
                    Fail = True

                    if (x - 1 > 0 and x + 1 < MapWight):
                        if (map[x - 1][y].name == 'wall' and
                            map[x + 1][y].name == 'wall'):
                            Fail = False
                    if (y - 1 > 0 and y + 1 < MapHeight):
                        if (map[x][y - 1].name == 'wall' and
                            map[x][y + 1].name == 'wall'):
                            Fail = False

                    #for m in range(max(0, x - 1), min(MapWight, x + 2)):
                    #    for n in range(max(0, y - 1), min(MapHeight, y + 2)):
                    #        if map[m][n].name == 'wall':
                    #            AdjacentWalls += 1
                    #
                    #            if (m + 2 < MapWight and n + 2 < MapHeight):
                    #                if (map[m + 2][n].name == 'wall' or
                    #                    map[m][n + 2].name == 'wall'):
                    #                    Fail = False

                    if Fail == True:
                        map[x][y].change(RockFloor)

    def buildBSPDungeon(self):
        pass

    def buildQIXDungeon(self):
        pass

    def buildDrunkenCave(self):
        StepsTaken = 0
        Fails = 0

        x = libtcod.random_get_int(0, 1, MapWight - 2)
        y = libtcod.random_get_int(0, 1, MapHeight - 2)

        Player.x = x
        Player.y = y

        while (StepsTaken < DrunkenSteps and Fails < 2000):
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

            if (x + dx > 0 and x + dx < MapWight - 1 and
                y + dy > 0 and y + dy < MapHeight - 1):
                x += dx
                y += dy

                StepsTaken += 1
            else:
                Fails += 1

        self.postProcess()

    def buildSewers(self):
        pass

    def buildMaze(self):
        pass

    def postProcess(self):
        for y in range(MapHeight):
            for x in range(MapWight):
                # TODO: Move all of those into script file.
                if (map[x][y].name == 'floor' and rand_chance(3)):
                    map[x][y].change(Vines)

                elif (map[x][y].name == 'floor' and rand_chance(2)):
                    map[x][y].change(ShallowWater)

                elif (map[x][y].name == 'floor' and rand_chance(2)):
                    map[x][y].change(RockPile)

        if rand_chance(20):
            self.makeLake(ShallowWater)

        self.populate()

    def populate(self):
        MonsterNo = 0
        NewMob = None

        while MonsterNo < MonsterMaxNumber:
            x = libtcod.random_get_int(0, 1, MapWight - 2)
            y = libtcod.random_get_int(0, 1, MapHeight - 2)

            # TODO: Rework.
            if rand_chance(80):
                NewMob = Mob(x, y, 'o', libtcod.desaturated_green, 'orc', 0, 0, 0)
            else:
                NewMob = Mob(x, y, 'T', libtcod.dark_green, 'troll', 2, -1, 3)

            if NewMob.isBlocked(x, y):
                NewMob = None

            if NewMob != None:
                Entities.append(NewMob)
                MonsterNo += 1

            NewMob = None

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(ScreenWidth, ScreenHeight, 'RGLK', False)

# Base console:
Con = libtcod.console_new(ScreenWidth, ScreenHeight)
# Set FOV:
FOVMap = libtcod.map_new(MapWight, MapHeight)

# Player must be defined here, we work with him shortly.
Player = Mob(1, 1, '@', libtcod.white, 'Player', 0, 0, 0)
Entities.append(Player)

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
        global WizModeNoClip
        WizModeNoClip = not WizModeNoClip

    # Magic map
    if Key.vk == libtcod.KEY_F2:
        for y in range(MapHeight):
            for x in range(MapWight):
                map[x][y].explored = True

    if Key.vk == libtcod.KEY_F3:
        global WizModeTrueSight
        WizModeTrueSight = not WizModeTrueSight

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        # Heh heh, if I don't clear the console, it looks quite trippy after
        # redrawing a new map over the old one.
        for y in range(MapHeight):
            for x in range(MapWight):
                libtcod.console_put_char_ex(Con, x, y, ' ', libtcod.black, libtcod.black)
        # Does not work with monster generation, TODO?
        for i in Entities:
            if i != Player:
                Entities.remove(i)

        Dungeon.makeMap()


    # MOVEMENT:
    if not PlayerIsDead:
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
    for y in range(MapHeight):
        for x in range(MapWight):
            tile = map[x][y]
            tile.draw(x, y)

    for mob in Entities:
        if mob != Player:
            mob.draw()
    # Draw player last, over everything else.
    Player.draw()

    libtcod.console_blit(Con, 0, 0, ScreenWidth, ScreenHeight, 0, 0, 0)

###############################################################################
#  Main Loop
###############################################################################

Dungeon = Builder()
Dungeon.makeMap()

while not libtcod.console_is_window_closed():
    for i in Entities:
        # How else to check if entity has a speed variable?
        try:
            i.turn += i.speed
        except:
            i.turn += 1

    # Player turn
    while Player.turn >= 1:
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
    #for i in Entities:
    #    while i.turn >= 1:
    #        handle_monsters(i)
