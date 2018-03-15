# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Monster Scripts
###############################################################################

Dummy = {
'char': '?',
'color': libtcod.white,
'name': 'BUG: dummy monster',
'Str': 0,
'Dex': 0,
'End': 0,
'Int': 0,
'speed': 1.0,
'sight': 4,
'intrinsics': [],
'flags': []
}

Player = {
'char': '@',
'color': libtcod.white,
'name': 'player',
'Str': 0,
'Dex': 0,
'End': 0,
'Int': 0,
'speed': 1.0,
'sight': 6,
'intrinsics': [],
'flags': ['AVATAR']
}

Orc = {
'char': 'o',
'color': libtcod.desaturated_green,
'name': 'orc',
'Str': 0,
'Dex': 0,
'End': 0,
'Int': 0,
}

Troll = {
'char': 'T',
'color': libtcod.dark_green,
'name': 'troll',
'Str': 2,
'Dex': -1,
'End': 3,
'Int': 0,
'speed': 1.0,
'sight': 3,
'intrinsics': [],
'flags': []
}
