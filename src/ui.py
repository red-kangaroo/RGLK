# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math

import dungeon
import var

###############################################################################
#  User Interface
###############################################################################

def render_all(Player):
    render_map(Player)
    render_UI(Player)
    render_messages(Player)

def render_map(Player):
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
    Player.draw()

    # Render map:
    libtcod.console_blit(var.MapConsole, 0, 0, var.MapWidth, var.MapHeight, 0, 0, 0)

def render_messages(Player):
    libtcod.console_set_default_foreground(var.MessagePanel, var.TextColor)
    libtcod.console_set_default_background(var.MessagePanel, libtcod.black)
    libtcod.console_clear(var.MessagePanel)

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

    # Attributes:
    libtcod.console_print_ex(var.UIPanel, 1, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Str: ' + str(Player.Str))
    libtcod.console_print_ex(var.UIPanel, 1, 6, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dex: ' + str(Player.Dex))
    libtcod.console_print_ex(var.UIPanel, 1, 7, libtcod.BKGND_NONE, libtcod.LEFT,
                             'End: ' + str(Player.End))
    libtcod.console_print_ex(var.UIPanel, 9, 5, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Spd: ' + str(int(Player.speed * 100)))

    # Render UI:
    libtcod.console_blit(var.UIPanel, 0, 0, var.PanelWidth, var.ScreenHeight, 0,
                         var.ScreenWidth - var.PanelWidth, 0)

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
