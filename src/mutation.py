# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

import entity
import raw
import var

###############################################################################
#  Mutations
###############################################################################

MutationList = [
'MUTATION_CLAWS',
'MUTATION_LARGE_CLAWS',
'MUTATION_WINGS'
]

###############################################################################
#  Functions
###############################################################################

def gain(mutation, mutant):
    if not mutation in MutationList:
        print "Unhandled mutation: %s" % mutation
        return False

    if mutation == 'MUTATION_CLAWS':
        for part in mutant.bodyparts:
            if part.hasFlag('HAND'):
                part.attack = raw.Claw

    elif mutation == 'MUTATION_LARGE_CLAWS':
        for part in mutant.bodyparts:
            if part.hasFlag('HAND'):
                part.attack = raw.LargeClaw

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
        StrScaling = BluePrint['StrScaling']
    except:
        StrScaling = raw.DummyPart['StrScaling']
    try:
        DexScaling = BluePrint['DexScaling']
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

    New = entity.BodyPart(name, mutant, cover, place, size, eyes, attack,
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
            continue

        if part.hasFlag('HAND'):
            if handNo == 0:
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('LEFT')
                else:
                    part.flags.append('RIGHT')

                part.flags.append('MAIN')
                handNo += 1
            elif handNo == 1:
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('RIGHT')
                else:
                    part.flags.append('LEFT')

                handNo += 1
            else:
                part.flags.append('OTHER')
                handNo += 1
        elif part.hasFlag('ARM'):
            if armNo == 0:
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('LEFT')
                else:
                    part.flags.append('RIGHT')

                armNo += 1
            elif armNo == 1:
                if mutant.hasIntrinsic('LEFT_HANDED'):
                    part.flags.append('RIGHT')
                else:
                    part.flags.append('LEFT')

                armNo += 1
            else:
                part.flags.append('OTHER')
                armNo += 1
        elif part.hasFlag('LEG'):
            if legNo == 0:
                part.flags.append('RIGHT')
                legNo += 1
            elif legNo == 1:
                part.flags.append('LEFT')
                legNo += 1
            else:
                part.flags.append('OTHER')
                legNo += 1
        elif part.hasFlag('WING'):
            if wingNo == 0:
                part.flags.append('RIGHT')
                wingNo += 1
            elif wingNo == 1:
                part.flags.append('LEFT')
                wingNo += 1
            else:
                part.flags.append('OTHER')
                wingNo += 1

    mutant.baseArms = armNo
    mutant.baseLegs = legNo
    mutant.baseWings = wingNo
    mutant.baseEyes = eyeNo
