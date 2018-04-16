# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

import raw
import ui
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
        try:
            self.begin = i['beginMsg']
        except:
            self.begin = raw.DummyIntrinsic['beginMsg']
        try:
            self.end = i['endMsg']
        except:
            self.end = raw.DummyIntrinsic['endMsg']

    def isPermanent(self):
        if self.duration >= 30000:
            return True
        else:
            return False

    def getName(self, capitalize = False, full = False):
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

        if full:
            name = name + ", duration: " + str(self.duration) + ", power: " + str(self.power)

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

        # Returning None gets rid of the intrinsic.
        if self.type == None:
            return None
        if self.power < 0:
            return None
        if not self.isPermanent():
            self.duration -= 1
        if self.duration <= 0:
            return None

        # TODO: The effects.

        # Aflame:
        if self.type == 'AFLAME':
            if owner.hasFlag('MOB'):
                ui.message("%s burn&S!" % owner.getName(True), libtcod.light_red, owner)

                limb = owner.getLimbToHit()

                # Fire wounds limbs.
                if var.rand_chance(self.power * 10):
                    limb.wounded = True

                damage = libtcod.random_get_int(0, 1, 6) # Take 1d6 fire damage.
                owner.receiveDamage(damage, limb = limb, DamageType = 'FIRE')

            elif owner.hasFlag('ITEM'):
                pass # TODO: item destruction

        # Bleeding:
        if self.type == 'BLEED':
            if owner.hasFlag('MOB'):
                # Large bleeding results in permanent hemorrhage.
                if not self.isPermanent():
                    if self.power >= 5:
                        self.duration == 30000

                power = max(1, var.rand_int_from_float(self.power))
                damage = libtcod.random_get_int(0, 1, power)
                owner.receiveDamage(damage, DamageType = 'BLEED')

        # Poison:
        if self.type == 'POISON':
            if owner.hasFlag('MOB'):
                # Let's make sure we're in poison power 1 - 5 range, for damage
                # from 1d2 to 5d6.
                power = max(1, min(5, self.power))

                if power <= 2:
                    fullStop = "."
                elif power <= 4:
                    fullStop = "!"
                else:
                    fullStop = "!!!"

                ui.message("%s &ISARE poisoned%s" % (owner.getName(True), fullStop), libtcod.light_red, owner)

                if var.rand_chance(power * 5):
                    owner.actionVomit()

                damage = var.rand_dice(power, power + 1, 0)
                owner.receiveDamage(damage, DamageType = 'POISON')

        return True
