#!/usr/bin/env python

import libtcodpy as libtcod

###############################################################################
#  Global Variables
###############################################################################

# TODO: Most of this should be in a script file.
# TODO: Also split it into multiple files.

ScreenWidth = 80
ScreenHeight = 50
MapWight = 80
MapHeight = 45

RoomMinSize = 4
RoomMaxSize = 10
RoomMaxNumber = 99

WizModeNoClip = False
WizModeTrueSight = False

###############################################################################
#  Objects
###############################################################################

# Player, monsters...
class Entity(object):
    def __init__(self, x, y, char, color, name):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name

    def move(self, dx, dy):
        global WizModeNoClip

        if (self.x + dx < 0 or self.x + dx > MapWight - 1 or
            self.y + dy < 0 or self.y + dy > MapHeight - 1):
            return

        if ((not map[self.x + dx][self.y + dy].BlockMove) or WizModeNoClip):
            self.x += dx
            self.y += dy

    def draw(self):
        # Set color and draw character on screen.
        libtcod.console_set_default_foreground(Con, self.color)
        libtcod.console_put_char(Con, self.x, self.y, self.char, libtcod.BKGND_NONE)

# Map objects.
class Terrain(object):
    def __init__(self, char, color, name, BlockMove, BlockSight = None):
        self.char = char
        self.color = color
        self.name = name
        self.BlockMove = BlockMove

        # By default, BlockMove also BlockSight
        if BlockSight == None:
            BlockSight = BlockMove
        self.BlockSight = BlockSight

    def draw(self, x, y):
        # Set color and draw character on screen.
        libtcod.console_set_default_foreground(Con, self.color)
        libtcod.console_put_char(Con, x, y, self.char, libtcod.BKGND_NONE)

class Rect(object):
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
    def create_room(self):
        global map
        for x in range(self.x1 + 1, self.x2):
            for y in range(self.y1 + 1, self.y2):
                map[x][y].char = '.'
                map[x][y].color = libtcod.grey
                map[x][y].name = 'floor'
                map[x][y].BlockMove = False
                map[x][y].BlockSight = False

    def create_h_tunnel(self, OtherX):
        global map
        for x in range(min(self.CenterX, OtherX), max(self.CenterX, OtherX) + 1):
            if (x == self.x1 or x == self.x2):
                map[x][self.CenterY].char = '+'
                map[x][self.CenterY].color = libtcod.darkest_orange
                map[x][self.CenterY].name = 'door'
                map[x][self.CenterY].BlockMove = False
                map[x][self.CenterY].BlockSight = True
            else:
                map[x][self.CenterY].char = '.'
                map[x][self.CenterY].color = libtcod.grey
                map[x][self.CenterY].name = 'floor'
                map[x][self.CenterY].BlockMove = False
                map[x][self.CenterY].BlockSight = False

    def create_v_tunnel(self, OtherY):
        global map
        for y in range(min(self.CenterY, OtherY), max(self.CenterY, OtherY) + 1):
            if (y == self.y1 or y == self.y2):
                map[self.CenterX][y].char = '+'
                map[self.CenterX][y].color = libtcod.darkest_orange
                map[self.CenterX][y].name = 'door'
                map[self.CenterX][y].BlockMove = False
                map[self.CenterX][y].BlockSight = True
            else:
                map[self.CenterX][y].char = '.'
                map[self.CenterX][y].color = libtcod.grey
                map[self.CenterX][y].name = 'floor'
                map[self.CenterX][y].BlockMove = False
                map[self.CenterX][y].BlockSight = False

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(ScreenWidth, ScreenHeight, 'RGLK', False)
# Base console:
Con = libtcod.console_new(ScreenWidth, ScreenHeight)

# Player must be defined here, we work with him shortly. TODO?
Player = Entity(1, 1, '@', libtcod.white, 'Player')
Entities = [Player]

###############################################################################
#  Functions
###############################################################################

# Let's hope I didn't mess up the chances...
def rand_chance(percent):
    if libtcod.random_get_int(0, 1, 101) > percent:
        return False
    else:
        return True

# Player input
def handle_keys():

    Key = libtcod.console_wait_for_keypress(True)

    # Alt+Enter goes fullscreen
    if Key.vk == libtcod.KEY_ENTER and Key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # Exit game with Esc
    if Key.vk == libtcod.KEY_ESCAPE:
        return True


    # WIZARD MODE:
    # Walk through walls
    if Key.vk == libtcod.KEY_F1:
        global WizModeNoClip
        WizModeNoClip = not WizModeNoClip

    # See whole map
    if Key.vk == libtcod.KEY_F2:
        global WizModeTrueSight
        WizModeTrueSight = not WizModeTrueSight

    # Regenerate map
    if Key.vk == libtcod.KEY_F12:
        make_map()


    # MOVEMENT:
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

    Player.move(dx, dy)

def render_all():
    for y in range(MapHeight):
        for x in range(MapWight):
            tile = map[x][y]
            tile.draw(x, y)

    for mob in Entities:
        if mob != Player:
            mob.draw()
    Player.draw()

    libtcod.console_blit(Con, 0, 0, ScreenWidth, ScreenHeight, 0, 0, 0)

# Dungeon generation:
# TODO: Move into Dungeon.py
def make_map():
    global map

    # Fill map with walls.
    map = [[ Terrain('#', libtcod.darkest_grey, 'wall', True)
      for y in range(MapHeight) ]
        for x in range(MapWight) ]

    Rooms = []
    RoomNo = 0

    # Add rooms.
    for i in range(RoomMaxNumber):
        width = libtcod.random_get_int(0, RoomMinSize, RoomMaxSize)
        height = libtcod.random_get_int(0, RoomMinSize, RoomMaxSize)

        x = libtcod.random_get_int(0, 0, MapWight - width - 1)
        y = libtcod.random_get_int(0, 0, MapHeight - height - 1)

        NewRoom = Rect(x, y, width, height)
        Fail = False

        for OtherRoom in Rooms:
            if NewRoom.intersect(OtherRoom):
                Fail = True
                break

        # We want some rooms to overlap, it looks better.
        if (RoomNo < 20 and rand_chance(20)):
            Fail = False

        if not Fail:
            NewRoom.create_room()

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
    for y in range(MapHeight):
        for x in range(MapWight):

            if map[x][y].name == 'door':
                AdjacentWalls = 0
                Fail = True

                for m in range(max(0, x - 1), min(MapWight, x + 2)):
                    for n in range(max(0, y - 1), min(MapHeight, y + 2)):
                        if map[m][n].name == 'wall':
                            AdjacentWalls += 1

                            if (m + 2 < MapWight and n + 2 < MapHeight):
                                if (map[m + 2][n].name == 'wall' or
                                    map[m][n + 2].name == 'wall'):
                                    Fail = False

                if (AdjacentWalls < 3 or Fail == True):
                    map[x][y].char = '.'
                    map[x][y].color = libtcod.grey
                    map[x][y].name = 'floor'
                    map[x][y].BlockMove = False
                    map[x][y].BlockSight = False

            elif (map[x][y].name == 'floor' and rand_chance(5)):
                map[x][y].char = '|'
                map[x][y].color = libtcod.dark_green
                map[x][y].name = 'vines'
                map[x][y].BlockMove = False
                map[x][y].BlockSight = True

###############################################################################
#  Main Loop
###############################################################################

make_map()

while not libtcod.console_is_window_closed():

    # Draw screen:
    render_all()

    # Print screen:
    libtcod.console_flush()

    ## Clear old entities:
    #for mob in Entities:
    #    mob.clear()

    # Handle player input
    Exit = handle_keys()
    if Exit:
        break
