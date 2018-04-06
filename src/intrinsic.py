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

        if self.type == 'BLEED':
            if owner.hasFlag('MOB'):
                try:
                    owner.receiveDamage(libtcod.random_get_int(0, 0, self.power), DamageType = 'BLEED', flags = ['BLEED'])
                except:
                    pass

        # TODO: The effects.
        return True
