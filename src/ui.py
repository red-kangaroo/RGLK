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

    if len(var.MessageHistory) > 10:
        s = len(var.MessageHistory) - 10
    else:
        s = 0
    y = 0

    while y <= var.PanelHeight:
        try:
            (line, color, turn) = var.MessageHistory[s]
            if turn >= (var.TurnCount - 1): # Turn count increases before redrawing
                                            # screen, so here we need T - 1 for color.
                libtcod.console_set_default_foreground(var.MessagePanel, color)
            else:
                libtcod.console_set_default_foreground(var.MessagePanel, libtcod.darker_grey)

            libtcod.console_print_ex(var.MessagePanel, 1, y, libtcod.BKGND_NONE, libtcod.LEFT,
                                     line)
        except:
            break

        y += 1
        s += 1

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
    render_bar(1, 3, 18, 'Health ', int(math.floor(Player.HP)), int(math.floor(Player.maxHP)),
               libtcod.dark_red, libtcod.darker_red)
    # Mana bar:
    render_bar(1, 4, 18, 'Aether ', int(math.floor(Player.MP)), int(math.floor(Player.maxMP)),
               libtcod.blue, libtcod.darker_blue)
    # Stamina bar:
    render_bar(1, 5, 18, 'Stamina', int(math.floor(Player.SP)), int(math.floor(Player.maxSP)),
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

    # Display target stats:
    if Player.target != None:
        libtcod.console_set_default_foreground(var.UIPanel, var.TextColor)
        libtcod.console_print_ex(var.UIPanel, 1, 54, libtcod.BKGND_NONE, libtcod.LEFT,
                                 Player.target.name)

        # This will one day only work in WizMode:
        render_bar(1, 56, 18, 'HP', int(math.floor(Player.target.HP)), int(math.floor(Player.target.maxHP)),
                   libtcod.dark_red, libtcod.darker_red)
        render_bar(1, 57, 18, 'MP', int(math.floor(Player.target.MP)), int(math.floor(Player.target.maxMP)),
                   libtcod.blue, libtcod.darker_blue)
        render_bar(1, 58, 18, 'SP', int(math.floor(Player.target.SP)), int(math.floor(Player.target.maxSP)),
                   libtcod.dark_green, libtcod.darker_green)

    # TODO

    # Render UI:
    libtcod.console_blit(var.UIPanel, 0, 0, var.PanelWidth, var.ScreenHeight, 0,
                         var.ScreenWidth - var.PanelWidth, 0)

def option_menu(header, options):
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

def text_menu(header, text):
    libtcod.console_set_default_foreground(var.MenuPanel, var.TextColor)
    libtcod.console_set_default_background(var.MenuPanel, libtcod.black)

    # Clear and print header:
    libtcod.console_clear(var.MenuPanel)
    libtcod.console_print_rect_ex(var.MenuPanel, 1, 1, var.MenuWidth, var.MenuHeight,
                                  libtcod.BKGND_SET, libtcod.LEFT,
                                  header + " [Space for next page; Esc to exit]")

    # Text should always be a list of lines.
    line = -1
    y = 28

    while abs(line) <= len(text):
        (toPrint, color, turn) = text[line]

        try:
            libtcod.console_set_default_foreground(var.MenuPanel, color)
        except:
            libtcod.console_set_default_foreground(var.MenuPanel, var.TextColor)

        libtcod.console_print_ex(var.MenuPanel, 2, y, libtcod.BKGND_SET, libtcod.LEFT,
                                 toPrint)
        line -= 1
        y -= 1

        if y < 4 or abs(line) > len(text):
            # Draw it and wait for input:
            libtcod.console_blit(var.MenuPanel, 0, 0, var.MenuWidth, var.MenuHeight, 0, 5, 5)
            libtcod.console_flush()

            while True:
                Key = libtcod.console_wait_for_keypress(True)

                if Key.vk == libtcod.KEY_ESCAPE:
                    return None

                if Key.vk == libtcod.KEY_SPACE:
                    libtcod.console_clear(var.MenuPanel)
                    libtcod.console_print_rect_ex(var.MenuPanel, 1, 1, var.MenuWidth, var.MenuHeight,
                                                  libtcod.BKGND_SET, libtcod.LEFT,
                                                  header + " [Space for next page; Esc to exit]")
                    y = 28
                    # Ugly:
                    break

def main_menu(Player = None):
    libtcod.console_set_default_foreground(var.MainMenu, var.TextColor)
    # No background to allow for an image, one day.
    #libtcod.console_set_default_background(var.MainMenu, libtcod.BKGND_NONE)
    libtcod.console_set_alignment(var.MainMenu, libtcod.CENTER)
    libtcod.console_clear(var.MainMenu)

    libtcod.console_print(var.MainMenu, (var.MainWidth / 2), 1, var.GameName)

    index = ord('a')
    options = []

    if Player == None:
        options = [
        "Quick Start",
        "Create Character",
        "Continue Game",
        "Tutorial",
        "Options",
        #"Credits",
        "Quit"
        ]
    else:
        options = [
        "Save and Quit",
        "Options",
        "Quit and Abandon"
        ]

    y = 3
    for option in options:
        text = chr(index) + ') ' + option
        libtcod.console_print(var.MainMenu, (var.MainWidth / 2), y, text)
        index += 1
        y += 1

    libtcod.console_print_ex(var.MainMenu, var.MainWidth - 1, var.MainHeight - 1,
                             libtcod.BKGND_NONE, libtcod.RIGHT, "by red_kangaroo")

    libtcod.console_blit(var.MainMenu, 0, 0, var.MainWidth, var.MainHeight, 0,
    (var.ScreenWidth - var.MainWidth) / 2, (var.ScreenHeight - var.MainHeight) / 2)

    # Draw it and wait for input:
    libtcod.console_flush()

    while True:
        Key = libtcod.console_wait_for_keypress(True)
        what = Key.c - ord('a')

        if what in range(0, len(options) + 1):
            return what
        elif Key.vk == libtcod.KEY_ESCAPE:
            return None

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

#def grammar(text, actor):
#    text = str.replace(&D, getPronoun(actor.sex, 'DEFINITE'))
#    text = str.replace(&D, getPronoun(actor.sex, 'INDEFINITE'))
#    return text
