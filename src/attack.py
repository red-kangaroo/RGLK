# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Attack Type Configuration
###############################################################################

Dummy = {
'verb': 'BUG: dummy attack',
'ToHitBonus': 0,
'DiceNumber': 0,
'DiceValue': 0,
'DamageBonus': 0,
'DamageType': 'BLUNT',
'flags': []
}

Punch = {
'verb': 'punch',
'DiceNumber': 1,
'DiceValue': 3,
'flags': ['UNARMED', 'NATURAL']
}

Claw = {
'verb': 'claw',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH',
'flags': ['NATURAL']
}

NonWeapon = {
'verb': 'bash',
'ToHitBonus': -2,
'DiceNumber': 1,
'DiceValue': 2
}
