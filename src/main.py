import libtcodpy as libtcod

###############################################################################
#  Global Variables
###############################################################################

# TODO: Most of this should be in a script file.

ScreenWidth = 80
ScreenHeight = 50
MapWight = 80
MapHeight = 45

RoomMinSize = 4
RoomMaxSize = 10
RoomMaxNumber = 99

WizModeNoClip = False

###############################################################################
#  Objects
###############################################################################

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

    #def clear(self):
    #    # Erase self
    #    libtcod.console_put_char_ex(Con, self.x, self.y, '.', ColorDarkFloor, libtcod.black)

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

    def center(self):
        CenterX = (self.x1 + self.x2) / 2
        CenterY = (self.y1 + self.y2) / 2
        return (CenterX, CenterY)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

###############################################################################
#  Initialization
###############################################################################

libtcod.console_set_custom_font('graphics/terminal.png',
  libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INCOL)
libtcod.console_init_root(ScreenWidth, ScreenHeight, 'RGLK', False)

Con = libtcod.console_new(ScreenWidth, ScreenHeight)

Player = Entity(1, 1, '@', libtcod.white, 'Player')
# NPC = Entity(ScreenWidth/2 - 5, ScreenHeight/2 - 5, '@', libtcod.yellow)
Entities = [Player]

###############################################################################
#  Functions
###############################################################################

def rand_chance(percent):
    if libtcod.random_get_int(0, 1, 101) > percent:
        return False
    else:
        return True

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

# Dungeon:
def create_room(room):
    global map

    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].char = '.'
            map[x][y].color = libtcod.grey
            map[x][y].name = 'floor'
            map[x][y].BlockMove = False
            map[x][y].BlockSight = False

def create_h_tunnel(x1, x2, y):
    global map

    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].char = '.'
        map[x][y].color = libtcod.grey
        map[x][y].name = 'floor'
        map[x][y].BlockMove = False
        map[x][y].BlockSight = False


def create_v_tunnel(y1, y2, x):
    global map

    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].char = '.'
        map[x][y].color = libtcod.grey
        map[x][y].name = 'floor'
        map[x][y].BlockMove = False
        map[x][y].BlockSight = False

def make_map():
    global map

    map = [[ Terrain('#', libtcod.darkest_grey, 'wall', True)
      for y in range(MapHeight) ]
        for x in range(MapWight) ]

    Rooms = []
    RoomNo = 0

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

        if (RoomNo < 20 and rand_chance(20)):
            Fail = False

        if not Fail:
            create_room(NewRoom)

            (NewX, NewY) = NewRoom.center()

            if RoomNo == 0:
                Player.x = NewX
                Player.y = NewY
            else:
                (PrevX, PrevY) = Rooms[RoomNo - 1].center()

                if rand_chance(50):
                    create_h_tunnel(PrevX, NewX, PrevY)
                    create_v_tunnel(PrevY, NewY, NewX)
                else:
                    create_v_tunnel(PrevY, NewY, PrevX)
                    create_h_tunnel(PrevX, NewX, NewY)

            Rooms.append(NewRoom)
            RoomNo += 1

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
