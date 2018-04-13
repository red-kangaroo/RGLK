# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

import entity
import raw
import ui
import var

###############################################################################
#  Mutations
###############################################################################

MutationList = [
'MUTATION_HEAD_EXTRA',
'MUTATION_ARM_EXTRA',
'MUTATION_ARM_TENTACLE',
'MUTATION_LEG_EXTRA',
'MUTATION_LEG_TALON',
'MUTATION_LEG_TENTACLE',
'MUTATION_CLAWS',
'MUTATION_CLAWS_LARGE',
'MUTATION_EYE_EXTRA',
'MUTATION_WINGS',
'MUTATION_TAIL_WEAPON',
'MUTATION_TAIL_PREHENSIVE'
]

###############################################################################
#  Functions
###############################################################################

def gain(mutation, mutant):
    if mutation == 'RANDOM_ANY':
        mutation = random.choice(MutationList)
    elif not mutation in MutationList:
        print "Unhandled mutation: %s" % mutation
        return False

    if mutation == 'MUTATION_HEAD_EXTRA':
        new = create_part(raw.Head, mutant)
        mutant.bodyparts.insert(0, new)

        ui.message("%s grow&S a new head." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_ARM_EXTRA':
        index = None

        # Hands should be normally placed after arms, so look for the last hand in
        # body parts. Also don't break, because we're looking for the last one, not
        # the first one. In case any hands were cut off, we also look for the last
        # arm. And finally, if no arms exist, look for a torso.

        for part in mutant.bodyparts:
            if part.hasFlag('ARM') or part.hasFlag('HAND'):
                index = mutant.bodyparts.index(part)

        if index == None:
            for part in mutant.bodyparts:
                if part.hasFlag('TORSO'):
                    index = mutant.bodyparts.index(part)
                    break

        if index != None:
            new1 = create_part(raw.Arm, mutant)
            new2 = create_part(raw.Hand, mutant)

            mutant.bodyparts.insert(index + 1, new1)
            mutant.bodyparts.insert(index + 2, new2)

            name_parts(mutant)

            ui.message("%s grow&S a new arm." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_ARM_TENTACLE':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('ARM') or part.hasFlag('HAND'):
                index = mutant.bodyparts.index(part)

        if index == None:
            for part in mutant.bodyparts:
                if part.hasFlag('TORSO'):
                    index = mutant.bodyparts.index(part)
                    break

        if index != None:
            new = create_part(raw.TentacleArm, mutant)
            mutant.bodyparts.insert(index + 1, new)

            name_parts(mutant)

            ui.message("%s grow&S a tentacle." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_LEG_EXTRA':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('LEG'):
                index = mutant.bodyparts.index(part)

        new = create_part(raw.Leg, mutant)

        if index != None:
            mutant.bodyparts.insert(index + 1, new)
        else:
            mutant.bodyparts.append(new)

        name_parts(mutant)

        ui.message("%s grow&S a new leg." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_LEG_TALON':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('LEG'):
                index = mutant.bodyparts.index(part)

        new = create_part(raw.Talon, mutant)

        if index != None:
            mutant.bodyparts.insert(index + 1, new)
        else:
            mutant.bodyparts.append(new)

        if not mutant.hasFlag('USE_LEGS'):
            mutant.flags.append('USE_LEGS')

        name_parts(mutant)

        ui.message("%s grow&S a talon." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_LEG_TENTACLE':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('LEG'):
                index = mutant.bodyparts.index(part)

        new = create_part(raw.TentacleLeg, mutant)

        if index != None:
            mutant.bodyparts.insert(index + 1, new)
        else:
            mutant.bodyparts.append(new)

        name_parts(mutant)

        ui.message("%s grow&S a tentacle." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_CLAWS':
        for part in mutant.bodyparts:
            if part.hasFlag('HAND'):
                part.attack = raw.Claw

        ui.message("%s grow&S claws." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_CLAWS_LARGE':
        for part in mutant.bodyparts:
            if part.hasFlag('HAND'):
                part.attack = raw.LargeClaw

        ui.message("%s grow&S large claws." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_EYE_EXTRA':
        part = random.choice(mutant.bodyparts)
        part.eyes += 1

        ui.message("%s grow&S an eye on &POSS %s." % (mutant.getName(True), part.getName()),
                   libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_WINGS':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('TORSO'):
                index = mutant.bodyparts.index(part)
                break

        if index != None:
            new1 = create_part(raw.Wing, mutant)
            new2 = create_part(raw.Wing, mutant)

            mutant.bodyparts.insert(index + 1, new1)
            mutant.bodyparts.insert(index + 2, new2)

            name_parts(mutant)

            if not mutant.hasFlag('FLY'):
                mutant.flags.append('FLY')

            ui.message("%s grow&S wings." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_TAIL_WEAPON':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('GROIN'):
                index = mutant.bodyparts.index(part)
                break

        new = create_part(raw.Tail, mutant)

        if index != None:
            mutant.bodyparts.insert(index + 1, new)
        else:
            mutant.bodyparts.append(new)

        if not mutant.hasFlag('USE_NATURAL'):  # Thanks to this, we will use the tail
            mutant.flags.append('USE_NATURAL') # to attack.

        ui.message("%s grow&S a bony tail." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    elif mutation == 'MUTATION_TAIL_PREHENSIVE':
        index = None
        for part in mutant.bodyparts:
            if part.hasFlag('GROIN'):
                index = mutant.bodyparts.index(part)
                break

        new = create_part(raw.PrehensiveTail, mutant)

        if index != None:
            mutant.bodyparts.insert(index + 1, new)
        else:
            mutant.bodyparts.append(new)

        ui.message("%s grow&S a prehensive tail." % mutant.getName(True), libtcod.chartreuse, actor = mutant)

    return True

def create_part(part, mutant):
    try:
        name = part['name']
    except:
        name = raw.DummyPart['name']
    try:
        cover = part['cover']
    except:
        cover = raw.DummyPart['cover']
    try:
        place = part['place']
    except:
        place = raw.DummyPart['place']
    try:
        size = part['size']
    except:
        size = raw.DummyPart['size']
    try:
        eyes = part['eyes']
    except:
        eyes = raw.DummyPart['eyes']
    try:
        attack = part['attack']
    except:
        attack = raw.DummyPart['attack']
    try:
        StrScaling = part['StrScaling']
    except:
        StrScaling = raw.DummyPart['StrScaling']
    try:
        DexScaling = part['DexScaling']
    except:
        DexScaling = raw.DummyPart['DexScaling']
    try:
        addFlags = part['flags']
    except:
        addFlags = raw.DummyPart['flags']
    try:
        material = part['material']
    except:
        material = None

    New = entity.BodyPart(name, part, mutant, cover, place, size, eyes, attack,
                          StrScaling, DexScaling, addFlags, material)

    return New

def name_parts(mutant):
    handNo = 0
    armNo = 0
    legNo = 0
    wingNo = 0
    eyeNo = 0

    for part in mutant.bodyparts:
        eyeNo += part.eyes

        if part.getPlacement() != None:
            if part.hasFlag('HAND'):
                handNo += 1
            elif part.hasFlag('ARM'):
                armNo += 1
            elif part.hasFlag('LEG'):
                legNo += 1
            elif part.hasFlag('WING'):
                wingNo += 1

            continue # Don't name again.

        if part.hasFlag('HAND'):
            if handNo == 0:
                part.flags.append('MAIN')

            handNo += 1

            if var.isEven(handNo):
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('RIGHT')
                else:
                    part.flags.append('LEFT')
            else:
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('LEFT')
                else:
                    part.flags.append('RIGHT')
        elif part.hasFlag('ARM'):
            armNo += 1

            if var.isEven(armNo):
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('RIGHT')
                else:
                    part.flags.append('LEFT')
            else:
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('LEFT')
                else:
                    part.flags.append('RIGHT')
        elif part.hasFlag('LEG'):
            legNo += 1

            if var.isEven(legNo):
                part.flags.append('LEFT')
            else:
                part.flags.append('RIGHT')
        elif part.hasFlag('WING'):
            wingNo += 1

            if var.isEven(wingNo):
                part.flags.append('LEFT')
            else:
                part.flags.append('RIGHT')

    mutant.baseArms = armNo
    mutant.baseLegs = legNo
    mutant.baseWings = wingNo
    mutant.baseEyes = eyeNo
