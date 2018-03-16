# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import textwrap

import dungeon
import var

###############################################################################
#  User Interface
###############################################################################

def render_all(Player):
    # Remove SEEN flag from entities.
    for i in var.Entities:
        if i.hasFlag('SEEN'):
            try:
                i.flags.remove('SEEN')
            except:
                print "Failed to remove SEEN flag."

    render_map(Player)
    render_UI(Player)
    render_messages(Player)

    # And draw it all on the screen:
    libtcod.console_flush()

def render_map(Player):
    libtcod.console_set_default_background(var.MapConsole, libtcod.black)

    # Draw map.
    for y in range(var.MapHeight):
        for x in range(var.MapWidth):
            tile = dungeon.map[x][y]
            tile.draw(x, y)
    # Draw first features, then items, then mobs.
    for i in var.Entities:
        if i.hasFlag('FEATURE'):
            i.draw()
    for i in var.Entities:
        if i.hasFlag('ITEM'):
            i.draw()
    for i in var.Entities:
        if i.hasFlag('MOB'):
            i.draw()
    # Draw player last, over everything else.
    if not Player.hasFlag('DEAD'):
        Player.draw()

    # Render map:
    libtcod.console_blit(var.MapConsole, 0, 0, var.MapWidth, var.MapHeight, 0, 0, 0)

def render_messages(Player):
    libtcod.console_set_default_foreground(var.MessagePanel, var.TextColor)
    libtcod.console_set_default_background(var.MessagePanel, libtcod.black)
    libtcod.console_clear(var.MessagePanel)

    messagesToPrint = var.MessageHistory

    while len(messagesToPrint) > var.PanelHeight:
        del messagesToPrint[0]

    y = 0
    for (line, color, turn) in messagesToPrint:
        if turn >= (var.TurnCount - 1): # Turn count increases before redrawing
                                        # screen, so here we chance for T - 1.
            libtcod.console_set_default_foreground(var.MessagePanel, color)
        else:
            libtcod.console_set_default_foreground(var.MessagePanel, libtcod.darker_grey)

        libtcod.console_print_ex(var.MessagePanel, 1, y, libtcod.BKGND_NONE, libtcod.LEFT,
                                 line)
        y += 1

    # Render messages:
    libtcod.console_blit(var.MessagePanel, 0, 0, var.ScreenWidth - var.PanelWidth, var.PanelHeight, 0,
                         0, var.ScreenHeight - var.PanelHeight)

def render_UI(Player):
    libtcod.console_set_default_foreground(var.UIPanel, var.TextColor)
    libtcod.console_set_default_background(var.UIPanel, libtcod.black)
    libtcod.console_clear(var.UIPanel)

    # Player's name:
    libtcod.console_print_ex(var.UIPanel, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT,
                             Player.name)

    # Health bar:
    render_bar(1, 3, 18, 'HP', int(math.floor(Player.HP)), int(math.floor(Player.maxHP)),
               libtcod.dark_red, libtcod.darker_red)
    # Mana bar:
    render_bar(1, 4, 18, 'MP', int(math.floor(Player.MP)), int(math.floor(Player.maxMP)),
               libtcod.blue, libtcod.darker_blue)
    # Stamina bar:
    render_bar(1, 5, 18, 'SP', int(math.floor(Player.SP)), int(math.floor(Player.maxSP)),
               libtcod.dark_green, libtcod.darker_green)

    # Attributes:
    libtcod.console_print_ex(var.UIPanel, 1, 7, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Str: ' + str(Player.Str))
    libtcod.console_print_ex(var.UIPanel, 1, 8, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dex: ' + str(Player.Dex))
    libtcod.console_print_ex(var.UIPanel, 1, 9, libtcod.BKGND_NONE, libtcod.LEFT,
                             'End: ' + str(Player.End))
    libtcod.console_print_ex(var.UIPanel, 10, 7, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Wit: ' + str(Player.Wit))
    libtcod.console_print_ex(var.UIPanel, 10, 8, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Ego: ' + str(Player.Ego))
    libtcod.console_print_ex(var.UIPanel, 10, 9, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Spd: ' + str(int(Player.speed * 100)))

    libtcod.console_print_ex(var.UIPanel, 1, 11, libtcod.BKGND_NONE, libtcod.LEFT,
                             'T: ' + str(var.TurnCount))

    # Effects:
    if Player.hasFlag('DEAD'):
        libtcod.console_set_default_foreground(var.UIPanel, libtcod.dark_red)
        libtcod.console_print_ex(var.UIPanel, 1, 13, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Dead')
    elif Player.HP < 1:
        libtcod.console_set_default_foreground(var.UIPanel, libtcod.red)
        libtcod.console_print_ex(var.UIPanel, 1, 13, libtcod.BKGND_NONE, libtcod.LEFT,
                                 'Dying')
    # TODO

    # Render UI:
    libtcod.console_blit(var.UIPanel, 0, 0, var.PanelWidth, var.ScreenHeight, 0,
                         var.ScreenWidth - var.PanelWidth, 0)

def menu(header, options):
    # TODO: Several screens.
    if len(options) > 26:
        print "Too many menu options."

    libtcod.console_set_default_foreground(var.MenuPanel, var.TextColor)
    libtcod.console_set_default_background(var.MenuPanel, libtcod.black)
    libtcod.console_clear(var.MenuPanel)

    libtcod.console_print_rect_ex(var.MenuPanel, 1, 1, var.MenuWidth, var.MenuHeight,
                                  libtcod.BKGND_SET, libtcod.LEFT, header + " [press letter; Esc to exit]")

    index = ord('a')
    y = 3
    for option in options:
        text = chr(index) + ') ' + option.name
        libtcod.console_print_ex(var.MenuPanel, 2, y, libtcod.BKGND_SET, libtcod.LEFT,
                                 text)
        index += 1
        y += 1

    libtcod.console_blit(var.MenuPanel, 0, 0, var.MenuWidth, var.MenuHeight, 0, 5, 5)

    # Draw it and wait for input:
    libtcod.console_flush()

    while True:
        Key = libtcod.console_wait_for_keypress(True)

        if Key.vk == libtcod.KEY_ESCAPE:
            return None
        # TODO: Next page.
        else:
            what = Key.c - ord('a')

            if what in range(0, len(options) + 1):
                return what

def render_bar(x, y, totalWidth, name, value, maxValue, barColor, backColor):
    # Calculate width of bar:
    barWidth = int(float(value) / maxValue * totalWidth)

    libtcod.console_set_default_background(var.UIPanel, backColor)
    libtcod.console_rect(var.UIPanel, x, y, totalWidth, 1, False, libtcod.BKGND_SCREEN)

    # Render bar:
    libtcod.console_set_default_background(var.UIPanel, barColor)
    if barWidth > 0:
        libtcod.console_rect(var.UIPanel, x, y, barWidth, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_print_ex(var.UIPanel, x, y, libtcod.BKGND_NONE, libtcod.LEFT,
                             name + ': ' + str(value) + '/'+ str(maxValue))

def message(text, color = var.TextColor, actor = None):
    seen = True
    if actor != None:
        try:
            if not actor.hasFlag('SEEN'):
                seen = False
        except:
            pass # No need for special message here.
    if seen == True:
        textWrapped = textwrap.wrap(text, var.ScreenWidth - var.PanelWidth - 2)
        turn = var.TurnCount

        # Save message as a tuple:
        for i in textWrapped:
            var.MessageHistory.append((i, color, turn))
