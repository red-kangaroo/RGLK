# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import attack as atk

###############################################################################
#  Monster Configuration
###############################################################################

Dummy = {
'char': '?',
'color': libtcod.white,
'name': 'BUG: dummy monster',
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 5,
'BaseAttack': atk.Punch,
'material': 'FLESH',
'diet': ['FLESH', 'WATER'],
'intrinsics': [],
'flags': []
}

Player = {
'char': '@',
'color': libtcod.white,
'name': 'Player',
'Str': 2,
'Dex': 2,
'End': 4,
'Wit': 0,
'Ego': 0,
'speed': 1.2,
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
'Wit': 0,
'Ego': 0,
'flags': ['AI_SCAVENGER']
}

Troll = {
'char': 'T',
'color': libtcod.dark_green,
'name': 'troll',
'Str': 2,
'Dex': -1,
'End': 3,
'Wit': -1,
'Ego': 0,
'speed': 1.0,
'intrinsics': [],
'flags': []
}
