# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

import raw
import var

###############################################################################
#  Intrinsics
###############################################################################

class Intrinsic(object):
    def __init__(self, type, duration = 0, power = 0):
        for i in raw.IntrinsicList:
            if i['type'] == type:
                break

        self.type = type
        self.duration = duration
        self.power = power

        try:
            self.name = i['name']
        except:
            self.name = raw.DummyIntrinsic['name']
        try:
            self.color = i['color']
        except:
            self.color = raw.DummyIntrinsic['color']
        try:
            self.secret = i['secret']
        except:
            self.secret = raw.DummyIntrinsic['secret']

    def isPermanent(self):
        if self.duration >= 30000:
            return True
        else:
            return False

    def getName(self, capitalize = False):
        name = self.name

        if self.type == 'BLEED' and self.power >= 5:
            name = 'hemorrhage'
        if self.type == 'POISON':
            if self.power <= 1:
                name = 'mildly ' + name
            # Normal == 2
            elif self.power == 3:
                name = 'strongly ' + name
            elif self.power == 4:
                name = 'harshly ' + name
            elif self.power >= 5:
                name = 'deadly ' + name + '!'

        if capitalize == True:
            name = name.capitalize()

        return name

    def getColor(self):
        if self.color == libtcod.white:
            if self.isPermanent():
                return libtcod.azure
            else:
                return libtcod.white
        else:
            return self.color

    def getHandled(self, owner):
        # TODO: Handle intrinsics for 'MOB' and 'ITEM', not others.

        if self.type == None:
            return None
        if not self.isPermanent():
            self.duration -= 1

            if self.duration <= 0:
                return None

        # TODO: The effects.

        # Bleeding:
        if self.type == 'BLEED':
            if owner.hasFlag('MOB'):
                # Large bleeding results in permanent hemorrhage.
                if not self.isPermanent():
                    if self.power >= 5:
                        self.duration == 30000

                power = max(0, var.rand_int_from_float(self.power))
                damage = libtcod.random_get_int(0, 0, power)
                owner.receiveDamage(damage, DamageType = 'BLEED')

        # Poison:
        if self.type == 'POISON':
            if owner.hasFlag('MOB'):
                # Let's make sure we're in poison power 1 - 5 range, for damage
                # from 1d2 to 5d6.
                power = max(1, min(5, self.power))
                damage = var.rand_dice(power, power + 1, 0)

        return True
