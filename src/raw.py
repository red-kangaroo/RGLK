# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod

###############################################################################
#  Attack Types
###############################################################################

DummyAttack = {
'verb': 'BUG: dummy attack',
'ToHitBonus': 0,
'DiceNumber': 1,
'DiceValue': 1,
'DamageBonus': 0,
'DamageType': 'BLUNT',
'range': 1,
'flags': [],
'inflict': None, # list of tuples: (intrinsic, DiceNumber, DiceValue, Bonus, power, chance)
'explode': None
}

# TODO:
#  special effects
#  ranged
#  explosions / clouds
#
#  peck, lick, touch, slap

# Natural attacks:
Slam = {
'verb': 'slam&S',
'ToHitBonus': -2,
'DiceNumber': 1,
'DiceValue': 3,
'flags': ['NATURAL']
}

Punch = {
'verb': 'punch&ES',
'DiceNumber': 1,
'DiceValue': 2,
'flags': ['UNARMED', 'NATURAL']
}

Claw = {
'verb': 'claw&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH',
'flags': ['NATURAL']
}

LargeClaw = {
'verb': 'claw&S',
'DiceNumber': 2,
'DiceValue': 3,
'DamageType': 'SLASH',
'inflict': [('BLEED', 1, 3, 1, 2, 30)],
'flags': ['NATURAL']
}

Bite = {
'verb': 'bite&S',
'DiceNumber': 1,
'DiceValue': 4,
'DamageType': 'PIERCE',
'flags': ['NATURAL']
}

Beak = {
'verb': 'peck&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 4,
'DamageBonus': 1,
'DamageType': 'PIERCE',
'flags': ['NATURAL']
}

Kick = {
'verb': 'kick&S',
'DiceNumber': 1,
'DiceValue': 5,
'flags': ['NATURAL']
}

Buffet = {
'verb': 'buffet&S',
'ToHitBonus': -1,
'DiceNumber': 2,
'DiceValue': 2,
'flags': ['NATURAL']
}

AcidSlime = {
'verb': 'slime&S',
'DiceNumber': 3,
'DiceValue': 4,
'DamageType': 'ACID',
'flags': ['NATURAL']
}

# Weapon attacks:
NonWeapon = {
'verb': 'bash&S',
'ToHitBonus': -2,
'DiceNumber': 1,
'DiceValue': 2
}

Club = {
'verb': 'club&S',
'DiceNumber': 1,
'DiceValue': 4,
'DamageBonus': 1
}

TorchAttack = {
'verb': 'club&S',
'DiceNumber': 1,
'DiceValue': 4,
'DamageBonus': 1,
'flags': ['FLAME']
}

MaceAttack = {
'verb': 'smash&ES',
'DiceNumber': 2,
'DiceValue': 4
}

IceMaceAttack = {
'verb': 'smash&ES',
'DiceNumber': 2,
'DiceValue': 4,
'inflict': [('SLOW', 2, 4, 0, 2, 30)],
'flags': ['ICE']
}

Hammer = {
'verb': 'crush&ES',
'DiceNumber': 3,
'DiceValue': 4
}

GiantClub = {
'verb': 'club&S',
'ToHitBonus': -2,
'DiceNumber': 4,
'DiceValue': 4,
'DamageType': 'PIERCE'
}

SmallAxe = {
'verb': 'hack&S',
'DiceNumber': 1,
'DiceValue': 6,
'DamageBonus': 1,
'DamageType': 'SLASH'
}

LargeAxe = {
'verb': 'hack&S',
'DiceNumber': 2,
'DiceValue': 6,
'DamageType': 'SLASH'
}

WoodStaff = {
'verb': 'strike&S',
'DiceNumber': 2,
'DiceValue': 2
}

IronStaff = {
'verb': 'strike&S',
'DiceNumber': 2,
'DiceValue': 2,
'DamageBonus': 2
}

LeadStaff = {
'verb': 'strike&S',
'DiceNumber': 2,
'DiceValue': 3
}

VenomStaff = {
'verb': 'bite&S', # Heh, heh.
'DiceNumber': 2,
'DiceValue': 2,
'inflict': [('POISON', 2, 5, 0, 'power = 1 + weapon.enchantment', 30)],
}

KnifeAttack = {
'verb': 'jab&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH'
}

VampKnifeAttack = {
'verb': 'jab&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH',
'flags': ['STEAL_LIFE']
}

ManaKnifeAttack = {
'verb': 'jab&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH',
'flags': ['STEAL_MANA']
}

DaggerAttack = {
'verb': 'stab&S',
'DiceNumber': 1,
'DiceValue': 4,
'DamageType': 'PIERCE'
}

VenomDaggerAttack = {
'verb': 'stab&S',
'DiceNumber': 1,
'DiceValue': 4,
'inflict': [('POISON', 2, 5, 0, 'power = 1 + weapon.enchantment', 30)],
'DamageType': 'PIERCE'
}

SickleAttack = {
'verb': 'slash&ES',
'ToHitBonus': 1,
'DiceNumber': 2,
'DiceValue': 3,
'DamageType': 'SLASH'
}

SmallSword = {
'verb': 'slash&ES',
'DiceNumber': 1,
'DiceValue': 6,
'DamageType': 'SLASH'
}

VorpalSwordAttack = {
'verb': 'shred&S',
'DiceNumber': 1,
'DiceValue': 6,
'DamageType': 'SLASH',
'flags': ['VORPAL']
}

MediumSword = {
'verb': 'slash&ES',
'DiceNumber': 1,
'DiceValue': 8,
'DamageType': 'SLASH'
}

FlamingSwordAttack = {
'verb': 'slash&ES',
'DiceNumber': 1,
'DiceValue': 8,
'DamageType': 'SLASH',
'flags': ['FLAME']
}

LargeSword = {
'verb': 'slash&ES',
'DiceNumber': 2,
'DiceValue': 5,
'DamageType': 'SLASH'
}

FierySwordAttack = {
'verb': 'burn&S',
'DiceNumber': 2,
'DiceValue': 5,
'DamageType': 'FIRE',
'inflict': [('AFLAME', 2, 3, 0, 2, 20)]
}

HugeSword = {
'verb': 'slash&ES',
'DiceNumber': 2,
'DiceValue': 5,
'DamageBonus': 2,
'DamageType': 'SLASH'
}

TripleSwordAttack = {
'verb': 'slash&ES',
'DiceNumber': 3,
'DiceValue': 5,
'DamageType': 'SLASH'
}

KlaiveAttack = {
'verb': 'slash&ES',
'DiceNumber': 2,
'DiceValue': 7,
'DamageType': 'SLASH'
}

RapierAttack = {
'verb': 'pierce&S',
'ToHitBonus': 2,
'DiceNumber': 1,
'DiceValue': 7,
'DamageType': 'PIERCE'
}

SmallShield = {
'verb': 'bash&ES',
'DiceNumber': 1,
'DiceValue': 3
}

TurtleShieldAttack = {
'verb': 'bash&ES',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 3
}

MediumShield = {
'verb': 'bash&ES',
'DiceNumber': 2,
'DiceValue': 3
}

LargeShield = {
'verb': 'bash&ES',
'DiceNumber': 3,
'DiceValue': 3
}

HugeShield = {
'verb': 'bash&ES',
'DiceNumber': 4,
'DiceValue': 3
}

WhipAttack = {
'verb': 'whip&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 5,
'DamageType': 'SLASH'
}

ChainAttack = {
'verb': 'whip&S',
'DiceNumber': 1,
'DiceValue': 5,
'DamageBonus': 1
}

SpearAttack = {
'verb': 'stab&S',
'DiceNumber': 1,
'DiceValue': 12,
'DamageType': 'PIERCE'
}

WyrdSpearAttack = {
'verb': 'stab&S',
'DiceNumber': 1,
'DiceValue': 12,
'DamageType': 'PIERCE',
'flags': ['DAMAGE_MANA']
}

ScytheAttack = {
'verb': 'reap&S',
'DiceNumber': 3,
'DiceValue': 3,
'DamageType': 'SLASH'
}

BoulderRoll = {
'verb': 'crush&ES',
'ToHitBonus': -4,
'DiceNumber': 2,
'DiceValue': 10
}

# Ranged attacks:
MisThrown = {
'verb': 'hit&S',
'ToHitBonus': -4,
'DiceNumber': 1,
'DiceValue': 2,
'range': 2,
'flags': ['RANGED']
}

ClubThrown = {
'verb': 'strike&S',
'DiceNumber': 1,
'DiceValue': 4,
'range': 4,
'flags': ['RANGED']
}

TorchThrown = {
'verb': 'strike&S',
'DiceNumber': 1,
'DiceValue': 4,
'range': 4,
'inflict': [('AFLAME', 1, 4, 0, 1, 40)],
'flags': ['RANGED']
}

RockThrown = {
'verb': 'strike&S',
'DiceNumber': 2,
'DiceValue': 2,
'range': 6,
'flags': ['RANGED']
}

KnifeThrown = {
'verb': 'stab&S',
'ToHitBonus': 2,
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 2,
'range': 6,
'DamageType': 'PIERCE',
'flags': ['RANGED']
}

DaggerThrown = {
'verb': 'stab&S',
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 4,
'range': 5,
'DamageType': 'PIERCE',
'flags': ['RANGED']
}

AxeThrown = {
'verb': 'hack&S',
'DiceNumber': 1,
'DiceValue': 6,
'range': 5,
'DamageType': 'SLASH',
'flags': ['RANGED']
}

SpearThrown = {
'verb': 'pierce&S',
'DiceNumber': 1,
'DiceValue': 8,
'DamageBonus': 1,
'range': 5,
'DamageType': 'PIERCE',
'flags': ['RANGED']
}

WyrdSpearThrown = {
'verb': 'pierce&S',
'DiceNumber': 1,
'DiceValue': 8,
'DamageBonus': 1,
'range': 5,
'DamageType': 'PIERCE',
'flags': ['RANGED', 'DAMAGE_MANA']
}

###############################################################################
#  Intrinsics
###############################################################################

DummyIntrinsic = {
'name': 'BUG: dummy intrinsic',
'type': None,
'flags': [],
'beginMsg': " gain&S a dummy intrinsic. Yes, seeing this is a bug.",
'endMsg': " loose&S a dummy intrinsic. Yes, seeing this is a bug.",
'color': libtcod.white
}

ResistBlunt = {
'name': 'blunt attack resistance',
'type': 'RESIST_BLUNT',
'beginMsg': " look&S tough.",
'endMsg': " look&S squishy.",
'flags': ['SECRET']
}

ResistSlash = {
'name': 'slashing attack resistance',
'type': 'RESIST_SLASH',
'beginMsg': " look&S hardy.",
'endMsg': " look&S feeble.",
'flags': ['SECRET']
}

ResistPierce = {
'name': 'piercing attack resistance',
'type': 'RESIST_PIERCE',
'beginMsg': " look&S thick-skinned.",
'endMsg': " look&S frail.",
'flags': ['SECRET']
}

ResistAcid = {
'name': 'acid resistance',
'type': 'RESIST_ACID',
'beginMsg': " feel&S basic.",
'endMsg': " feel&S acidic.",
'flags': ['SECRET']
}

ResistFire = {
'name': 'fire resistance',
'type': 'RESIST_FIRE',
'beginMsg': " feel&S a pleasant chill.",
'endMsg': " feel&S feverish.",
'flags': ['SECRET']
}

ResistCold = {
'name': 'cold resistance',
'type': 'RESIST_COLD',
'beginMsg': " feel&S quite warm.",
'endMsg': " feel&S an icy chill.",
'flags': ['SECRET']
}

ResistElectricity = {
'name': 'shock resistance',
'type': 'RESIST_SHOCK',
'beginMsg': " feel&S grounded.",
'endMsg': " feel&S electrified.",
'flags': ['SECRET']
}

ResistNecrotic = {
'name': 'necrotic resistance',
'type': 'RESIST_NECRO',
'beginMsg': " feel&S truly alive.",
'endMsg': " feel&S a deadly chill.",
'flags': ['SECRET']
}

ResistPoison = {
'name': 'poison resistance',
'type': 'RESIST_POISON',
'beginMsg': " feel&S especially healthy.",
'endMsg': " feel&S weak of stomach.",
'flags': ['SECRET']
}

ResistLight = {
'name': 'light resistance',
'type': 'RESIST_LIGHT',
'beginMsg': " feel&S enlightened.",
'endMsg': " feel&S a light headache.",
'flags': ['SECRET']
}

ResistDark = {
'name': 'darkness resistance',
'type': 'RESIST_DARK',
'beginMsg': " &ISARE no longer afraid of the dark.",
'endMsg': " hear&S something go bump.", # in the night
'flags': ['SECRET']
}

ResistSound = {
'name': 'sonic resistance',
'type': 'RESIST_SOUND',
'beginMsg': " &ISARE hard of hearing.",
'endMsg': " feel&S an upcoming migraine.",
'flags': ['SECRET']
}

ResistChoke = {
'name': 'unbreathing',
'type': 'RESIST_CHOKE',
'beginMsg': " &ISARE breathing lightly.",
'endMsg': " take&S a deep breath.",
'flags': ['SECRET']
}

ResistMind = {
'name': 'mind resistance',
'type': 'RESIST_MIND',
'beginMsg': " feel&S iron-willed.",
'endMsg': " feel&S feeble-minded.",
'flags': ['SECRET']
}

VulnBlunt = {
'name': 'blunt attack vulnerability',
'type': 'VULN_BLUNT',
'beginMsg': " look&S squishy.",
'endMsg': " look&S tough.",
'flags': ['SECRET']
}

VulnSlash = {
'name': 'slashing attack vulnerability',
'type': 'VULN_SLASH',
'beginMsg': " look&S feeble.",
'endMsg': " look&S hardy.",
'flags': ['SECRET']
}

VulnPierce = {
'name': 'piercing attack vulnerability',
'type': 'VULN_PIERCE',
'beginMsg': " look&S frail.",
'endMsg': " look&S thick-skinned.",
'flags': ['SECRET']
}

VulnAcid = {
'name': 'acid vulnerability',
'type': 'VULN_ACID',
'beginMsg': " feel&S very acidic.",
'endMsg': " feel&S much less acidic.",
'flags': ['SECRET']
}

VulnFire = {
'name': 'fire vulnerability',
'type': 'VULN_FIRE',
'beginMsg': " feel&S too hot.",
'endMsg': " cool&S down a bit.",
'flags': ['SECRET']
}

VulnCold = {
'name': 'cold vulnerability',
'type': 'VULN_COLD',
'beginMsg': " shiver&S.",
'endMsg': " warm&S up a bit.",
'flags': ['SECRET']
}

VulnElectricity = {
'name': 'shock vulnerability',
'type': 'VULN_SHOCK',
'beginMsg': " feel&S currently amplified.",
'endMsg': " feel&S insulated.",
'flags': ['SECRET']
}

VulnNecrotic = {
'name': 'necrotic vulnerability',
'type': 'VULN_NECRO',
'beginMsg': " feel&S a deadly chill.",
'endMsg': " feel&S truly alive.",
'flags': ['SECRET']
}

VulnPoison = {
'name': 'poison vulnerability',
'type': 'VULN_POISON',
'beginMsg': " feel&S somewhat sickly.",
'endMsg': " feel&S rather healthy.",
'flags': ['SECRET']
}

VulnLight = {
'name': 'light vulnerability',
'type': 'VULN_LIGHT',
'beginMsg': " feel&S a light headache.",
'endMsg': " want&S to be in the dark no longer.",
'flags': ['SECRET']
}

VulnDark = {
'name': 'darkness vulnerability',
'type': 'VULN_DARK',
'beginMsg': " fear&S the shadows.",
'endMsg': " feel&S goth.",
'flags': ['SECRET']
}

VulnSound = {
'name': 'sonic vulnerability',
'type': 'VULN_SOUND',
'beginMsg': " feel&S an upcoming migraine.",
'endMsg': " &ISARE hard of hearing.",
'flags': ['SECRET']
}

VulnMind = {
'name': 'mind vulnerability',
'type': 'VULN_MIND',
'beginMsg': " feel&S feeble-minded.",
'endMsg': " feel&S iron-willed.",
'flags': ['SECRET']
}

ImmunePhysical = {
'name': 'physical immunity',
'type': 'IMMUNE_PHYSICAL',
'beginMsg': " feel&S rock-hard.",
'endMsg': " feel&S soft.",
'flags': ['SECRET']
}

ImmuneAcid = {
'name': 'acid immunity',
'type': 'IMMUNE_ACID',
'beginMsg': " feel&S very basic.",
'endMsg': " feel&S acidic.",
'flags': ['SECRET']
}

ImmuneFire = {
'name': 'fire immunity',
'type': 'IMMUNE_FIRE',
'beginMsg': " feel&S very cool!",
'endMsg': " feel&S feverish.",
'flags': ['SECRET']
}

ImmuneCold = {
'name': 'cold immunity',
'type': 'IMMUNE_COLD',
'beginMsg': " feel&S smoking hot.",
'endMsg': " feel&S an icy chill.",
'flags': ['SECRET']
}

ImmuneElectricity = {
'name': 'shock immunity',
'type': 'IMMUNE_SHOCK',
'beginMsg': " feel&S insulated.",
'endMsg': " feel&S electrified.",
'flags': ['SECRET']
}

ImmuneNecrotic = {
'name': 'necrotic immunity',
'type': 'IMMUNE_NECRO',
'beginMsg': " feel&S truly alive.",
'endMsg': " feel&S a deadly chill.",
'flags': ['SECRET']
}

ImmunePoison = {
'name': 'poison immunity',
'type': 'IMMUNE_POISON',
'beginMsg': " feel&S especially healthy.",
'endMsg': " feel&S weak of stomach.",
'flags': ['SECRET']
}

ImmuneDark = {
'name': 'darkness immunity',
'type': 'IMMUNE_DARK',
'beginMsg': " feel&S the darkness rising.",
'endMsg': " feel&S the darkness subside.",
'flags': ['SECRET']
}

ImmuneMind = {
'name': 'mind immunity',
'type': 'IMMUNE_MIND',
'beginMsg': " feel&S unbreakable determination.",
'endMsg': " feel&S hesitant.",
'flags': ['SECRET']
}

AllergyIron = {
'name': 'iron allergy',
'type': 'VULN_IRON',
'beginMsg': " feel&S disgusted by unclean metals.",
'endMsg': " feel&S like some smithing.",
'flags': ['SECRET']
}

AllergySilver = {
'name': 'silver allergy',
'type': 'VULN_SILVER',
'beginMsg': " feel&S disgusted by the moon metal.",
'endMsg': " feel&S at peace with the Moon.",
'flags': ['SECRET']
}

AllergyGold = {
'name': 'gold allergy',
'type': 'VULN_GOLD',
'beginMsg': " feel&S disgusted by opulent jewelry.",
'endMsg': " feel&S a bit greedy.",
'flags': ['SECRET']
}

AllergyGlass = {
'name': 'glass allergy',
'type': 'VULN_GLASS',
'beginMsg': " feel&S disgusted by translucency.",
'endMsg': " feel&S at peace with windows.", # Linux is better, though.
'flags': ['SECRET']
}

AllergyHoly = {
'name': 'unholy',
'type': 'VULN_HOLY',
'beginMsg': " feel&S unholy.",
'endMsg': " feel&S blessed.",
'flags': ['SECRET']
}

AllergyUnholy = {
'name': 'holy',
'type': 'VULN_UNHOLY',
'beginMsg': " feel&S holy.",
'endMsg': " feel&S cursed.",
'flags': ['SECRET']
}

ResistMetal = {
'name': 'metal protection',
'type': 'RESIST_METAL',
'beginMsg': " yearn&S for metal crashing on metal.",
'endMsg': " shudder&S at the thought of smithing.",
'flags': ['SECRET']
}

ResistMeat = {
'name': 'bodily protection',
'type': 'RESIST_MEAT',
'beginMsg': " yearn&S for some bodily action.",
'endMsg': " yearn&S for some privacy.",
'flags': ['SECRET']
}

ResistEarth = {
'name': 'earth protection',
'type': 'RESIST_EARTH',
'beginMsg': " feel&S in tune with nature.",
'endMsg': " shudder&S at the thought of nature.",
'flags': ['SECRET']
}

ResistWood = {
'name': 'forest protection',
'type': 'RESIST_WOOD',
'beginMsg': " hear&S the trees singing.",
'endMsg': " hate&S the trees.",
'flags': ['SECRET']
}

ResistMundane = {
'name': 'mundanity protection',
'type': 'RESIST_MUNDANE',
'beginMsg': " feel&S special.",
'endMsg': " feel&S mundane.",
'flags': ['SECRET']
}

Aflame = {
'name': 'aflame',
'type': 'AFLAME',
'beginMsg': " catch&ES aflame!",
'endMsg': " no longer burn&S.",
'flags': [],
'color': libtcod.red
}

Bleed = {
'name': 'bleeding',
'type': 'BLEED',
'beginMsg': " bleed&S profusely!",
'endMsg': " no longer bleed&S.",
'flags': [],
'color': libtcod.red
}

Poison = {
'name': 'poisoned',
'type': 'POISON',
'beginMsg': " &ISARE posioned.",
'endMsg': " feel&S better.",
'flags': [],
'color': libtcod.green
}

Regeneration = {
'name': 'regeneration',
'type': 'REGEN_LIFE',
'beginMsg': " can see &POSS bruises fading quickly.",
'endMsg': " feel&S unwell.",
'flags': ['SECRET']
}

Starpower = {
'name': 'starpower',
'type': 'REGEN_MANA',
'beginMsg': " feel&S the stars watching.",
'endMsg': " feel&S down.",
'flags': ['SECRET']
}

Vigor = {
'name': 'vigor',
'type': 'REGEN_STAM',
'beginMsg': " feel&S invigorated.",
'endMsg': " feel&S fatigued.",
'flags': ['SECRET']
}

Unhealing = {
'name': 'unhealing',
'type': 'DRAIN_LIFE',
'beginMsg': " can feel all &POSS old pains.",
'endMsg': " feel&S better.",
'flags': ['SECRET']
}

Manaburn = {
'name': 'manaburn',
'type': 'DRAIN_MANA',
'beginMsg': " can smell the aether burning in &POSS veins.",
'endMsg': " feel&S energized.",
'flags': ['SECRET']
}

Fatigue = {
'name': 'fatigue',
'type': 'DRAIN_STAM',
'beginMsg': " feel&S fatigued.",
'endMsg': " feel&S refreshed.",
'flags': ['SECRET']
}

Haste = {
'name': 'hasted',
'type': 'HASTE',
'beginMsg': " &ISARE moving faster.",
'endMsg': " slow&S down.",
'flags': []
}

Slow = {
'name': 'slowed',
'type': 'SLOW',
'beginMsg': " &ISARE moving slowly.",
'endMsg': " speed&S up.",
'flags': []
}

Levitation = {
'name': 'levitation',
'type': 'LEVITATION',
'beginMsg': " rise&S above the ground.",
'endMsg': " descend&S gently upon the ground.",
'flags': []
}

WaterWalking = {
'name': 'water walking',
'type': 'WATER_WALK',
'beginMsg': " feel&S very holy.",
'endMsg': " feel&S sea-sick.",
'flags': ['SECRET']
}

Swimming = {
'name': 'swimming',
'type': 'SWIM',
'beginMsg': " fondly remember&S the ocean waves.",
'endMsg': " feel&S hydrophobic.",
'flags': ['SECRET']
}

Blindness = {
'name': 'blind',
'type': 'BLIND',
'beginMsg': " cannot see!",
'endMsg': " can see again.",
'flags': [],
'color': libtcod.grey
}

LeftHanded = {
'name': 'left-handed',
'type': 'LEFT_HANDED',
'beginMsg': " feel&S sinister.",
'endMsg': " feel&S right.",
'flags': ['SECRET']
}

Bloodless = {
'name': 'bloodless',
'type': 'BLOODLESS',
'beginMsg': " feel&S exsanguinated.",
'endMsg': " listen&S to &POSS heart.",
'flags': ['SECRET']
}

Fragile = {
'name': 'fragile',
'type': 'FRAGILE',
'beginMsg': " feel&S very fragile.",
'endMsg': " toughen&S up.",
'flags': ['SECRET']
}

CanDig = {
'name': 'tunnelling', # It feels so weird with two n's.
'type': 'CAN_DIG',
'beginMsg': " feel&S like some mining.",
'endMsg': " feel&S lazy.",
'flags': ['SECRET']
}

CanChop = {
'name': 'wood chopping',
'type': 'CAN_CHOP',
'beginMsg': " feel&S like some woodcutting.",
'endMsg': " feel&S lazy.",
'flags': ['SECRET']
}

BuffStrength = {
'name': 'brawny',
'type': 'BUFF_STRENGTH',
'beginMsg': " feel&S strong.",
'endMsg': " feel&S weak.",
'flags': ['SECRET']
}

BuffDexterity = {
'name': 'agile',
'type': 'BUFF_DEXTERITY',
'beginMsg': " feel&S agile.",
'endMsg': " feel&S clumsy.",
'flags': ['SECRET']
}

BuffEndurance = {
'name': 'hardy',
'type': 'BUFF_ENDURANCE',
'beginMsg': " feel&S very tough.",
'endMsg': " feel&S sickly.",
'flags': ['SECRET']
}

BuffWits = {
'name': 'clever',
'type': 'BUFF_WITS',
'beginMsg': " feel&S clever.",
'endMsg': " feel&S dumb.",
'flags': ['SECRET']
}

BuffEgo = {
'name': 'charming',
'type': 'BUFF_EGO',
'beginMsg': " feel&S charming.",
'endMsg': " feel&S obnoxious.",
'flags': ['SECRET']
}

BuffDamage = {
'name': 'dangerous',
'type': 'BUFF_DAMAGE',
'beginMsg': " feel&S dangerous.",
'endMsg': " feel&S harmless.",
'flags': ['SECRET']
}

BuffLight = {
'name': 'shining',
'type': 'BUFF_LIGHT',
'beginMsg': " start&S to glow.",
'endMsg': " no longer glow&S.",
'flags': ['SECRET']
}

DebuffStrength = {
'name': 'weakened',
'type': 'DEBUFF_STRENGTH',
'beginMsg': " feel&S weak.",
'endMsg': " feel&S strong.",
'flags': ['SECRET']
}

DebuffDexterity = {
'name': 'clumsy',
'type': 'DEBUFF_DEXTERITY',
'beginMsg': " feel&S clumsy.",
'endMsg': " feel&S agile.",
'flags': ['SECRET']
}

DebuffEndurance = {
'name': 'sickly',
'type': 'DEBUFF_ENDURANCE',
'beginMsg': " feel&S sickly.",
'endMsg': " feel&S very tough.",
'flags': ['SECRET']
}

DebuffWits = {
'name': 'stupid',
'type': 'DEBUFF_WITS',
'beginMsg': " feel&S dumb.",
'endMsg': " feel&S clever.",
'flags': ['SECRET']
}

DebuffEgo = {
'name': 'aggravating',
'type': 'DEBUFF_EGO',
'beginMsg': " feel&S obnoxious.",
'endMsg': " feel&S charming.",
'flags': ['SECRET']
}

DebuffDamage = {
'name': 'harmless',
'type': 'DEBUFF_DAMAGE',
'beginMsg': " feel&S harmless.",
'endMsg': " feel&S dangerous.",
'flags': ['SECRET']
}

DebuffLight = {
'name': 'dazzled',
'type': 'DEBUFF_LIGHT',
'beginMsg': " cannot see clearly.",
'endMsg': " can see clearly now.",
'flags': ['SECRET']
}

NoneIntrinsic = {
'name': 'none intrinsic',
'type': None,
'beginMsg': " feel&S nothing at all.",
'endMsg': " feel&S even less than nothing.",
'flags': []
}

###############################################################################
#  Magical Egos
###############################################################################

DummyEgo = {
'prefix': None, # All should have one of either prefix or suffix, never none,
'suffix': None, # never both, or something might break.
'material': None,
'color': None,
'size': None,
'accuracy': None,
'light': None,
'Str': None,
'Dex': None,
'End': None,
'Wit': None,
'Ego': None,
'DV': None,
'PV': None,
'StrScaling': None,
'DexScaling': None,
'flags': [],
'intrinsics': []
}

# Stat boosts:
Warrior = {
'prefix': "warrior's",
'Str': 1
}

Thief = {
'prefix': "thief's",
'Dex': 1
}

Healer = {
'prefix': "healer's",
'End': 1
}

Sage = {
'prefix': "sage's",
'Wit': 1
}

Wizard = {
'prefix': "wizard's",
'Ego': 1
}

Berserker = {
'prefix': "berserker's",
'Str': 2,
'Dex': -1
}

Dancer = {
'prefix': "dancer's",
'Dex': 2,
'Str': -1
}

Leper = {
'prefix': "leper's",
'End': 2,
'Str': -1,
'Dex': -1
}

Courtesan = {
'prefix': "courtesan's",
'Dex': 2,
'Ego': 1,
'End': -1
}

Apprentice = {
'prefix': "apprentice's",
'Wit': 2,
'Ego': -1
}

Fool = {
'prefix': "fool's",
'Ego': 2,
'Wit': -1
}

Princess = {
'suffix': "the princess",
'Ego': 2,
'Str': -1
}

EgoStrength = {
'suffix': "giant strength",
'intrinsics': [('BUFF_STRENGTH', 1)]
}

EgoDexterity = {
'suffix': "agility",
'intrinsics': [('BUFF_DEXTERITY', 1)]
}

EgoEndurance = {
'suffix': "the bear",
'intrinsics': [('BUFF_ENDURANCE', 1)]
}

EgoWits = {
'suffix': "quick wits",
'intrinsics': [('BUFF_WITS', 1)]
}

EgoEgo = { # Yep, the name is cool.
'suffix': "adornment",
'intrinsics': [('BUFF_EGO', 1)]
}

# General bonuses and flags:
Balanced = {
'prefix': "balanced",
'accuracy': 2
}

Seeking = {
'suffix': "seeking",
'accuracy': 1,
'flags': ['ENCHANT_ACCURACY']
}

Strapped = {
'prefix': "strapped",
'flags': ['TWO_HAND_OK']
}

Glowing = {
'prefix': "glowing",
'color': libtcod.amber,
'light': 1
}

Luminescence = {
'prefix': "floating",
'suffix': "luminescence",
'color': libtcod.amber,
'flags': ['CARRY_LIGHT'],
'light': 1
}

Sun = {
'suffix': "the Sun",
'color': libtcod.amber,
'flags': ['ENCHANT_LIGHT'],
'light': 1
}

Moon = {
'suffix': "the Moon",
'color': libtcod.white,
'intrinsics': [('BUFF_LIGHT', 1)]
}

Defense = {
'suffix': "defense",
'flags': ['ENCHANT_DODGE']
}

Coward = {
'prefix': "coward's",
'DV': 1
}

Willowy = {
'prefix': "willowy",
'DV': 2,
'PV': -1
}

Protection = {
'suffix': "protection",
'flags': ['ENCHANT_PROTECTION']
}

Sturdy = {
'prefix': "sturdy",
'PV': 1
}

Unyielding = {
'prefix': "impervious",
'DV': -1,
'PV': 2
}

MasterworkArmor = {
'prefix': "masterwork",
'DV': 1,
'PV': 1
}

Massive = {
'prefix': "massive",
'StrScaling': 'A',
'size': 1
}

MasterworkWeapon = {
'prefix': "masterwork",
'DexScaling': 'A'
}

Eldritch = {
'prefix': "eldritch",
'color': libtcod.yellow,
'material': 'GOLD',
'flags': ['ENCHANT_DOUBLE']
}

EgoSilver = {
'prefix': "silvered",
'material': 'SILVER'
}

EgoGold = {
'prefix': "gilded",
'material': 'GOLD'
}

# Intrinsics:
EgoLevitation = {
'suffix': "levitation",
'color': libtcod.azure,
'intrinsics': [('LEVITATION', 1)]
}

EgoRegeneration = {
'suffix': "regeneration",
'color': libtcod.dark_red,
'intrinsics': [('REGEN_LIFE', 1)]
}

EgoStarpower = {
'suffix': "the stars",
'color': libtcod.dark_blue,
'intrinsics': [('REGEN_MANA', 1)]
}

EgoVigor = {
'suffix': "vigor",
'color': libtcod.dark_green,
'intrinsics': [('REGEN_STAM', 1)]
}

Speed = {
'suffix': "speed",
'intrinsics': [('HASTE', 1)]
}

Sailor = {
'prefix': "sailor's",
'intrinsics': [('SWIM', 1)]
}

EgoResistLight = {
'prefix': "shrouded",
'intrinsics': [('RESIST_LIGHT', 1)]
}

EgoResistDark = {
'prefix': "pilgrim's",
'intrinsics': [('RESIST_DARK', 1)]
}

EgoResistMind = {
'suffix': "the village idiot",
'intrinsics': [('RESIST_MIND', 1)]
}

EgoResistChoke = {
'suffix': "the last breath",
'intrinsics': [('RESIST_CHOKE', 1)]
}

EgoResistFire = {
'prefix': "charred",
'intrinsics': [('RESIST_FIRE', 1)]
}

EgoResistCold = {
'prefix': "fur-lined",
'intrinsics': [('RESIST_COLD', 1)]
}

EgoResistPoison = {
'prefix': "poisoner's",
'intrinsics': [('RESIST_POISON', 1)]
}

Thunder = {
'suffix': "the thunderstorm",
'intrinsics': [('RESIST_SHOCK', 1), ('RESIST_SOUND', 1), ('VULN_COLD', 1)]
}

Alchemical = {
'prefix': "alchemical",
'intrinsics': [('RESIST_POISON', 1), ('RESIST_ACID', 1), ('VULN_FIRE', 1)]
}

Violence = {
'suffix': "violence",
'intrinsics': [('BUFF_DAMAGE', 1), ('FRAGILE', 1)]
}

Peace = {
'suffix': "peace",
'intrinsics': [('DEBUFF_DAMAGE', 1), ('RESIST_MUNDANE', 1)]
}

Padded = {
'prefix': "padded",
'intrinsics': [('RESIST_BLUNT', 1), ('VULN_SLASH', 1)]
}

Reinforced = {
'prefix': "reinforced",
'intrinsics': [('RESIST_PIERCE', 1), ('VULN_BLUNT', 1)]
}

Banded = {
'prefix': "banded",
'intrinsics': [('RESIST_SLASH', 1), ('VULN_PIERCE', 1)]
}

EgoForest = {
'suffix': "the forest",
'intrinsics': [('RESIST_WOOD', 1), ('VULN_FIRE', 1)]
}

Fey = {
'prefix': "fey",
'color': libtcod.white,
'material': 'SILVER',
'intrinsics': [('RESIST_MEAT', 1), ('VULN_IRON', 1)]
}

EgoDead = {
'suffix': "the dead",
'color': libtcod.dark_grey,
'intrinsics': [('BLOODLESS', 1), ('SLOW', 1)]
}

EgoGrave = {
'prefix': "graveknight's",
'color': libtcod.light_grey,
'material': 'BONE',
'intrinsics': [('IMMUNE_NECRO', 1), ('VULN_HOLY', 1)]
}

Summer = {
'suffix': "the Summer Court",
'color': libtcod.yellow,
'material': 'GOLD',
'intrinsics': [('IMMUNE_FIRE', 1), ('VULN_COLD', 1)]
}

Winter = {
'suffix': "the Winter Court",
'color': libtcod.white,
'material': 'SILVER',
'intrinsics': [('IMMUNE_COLD', 1), ('VULN_FIRE', 1)]
}

###############################################################################
#  Items
###############################################################################

# Must be defined before monsters to allow for generating inventories.

DummyItem = {
'char': '?',
'color': libtcod.white,
'name': 'BUG: dummy item',
'plural': None,
'givenName': None,
'prefix': "",
'suffix': "",
'BlockMove': False,
'material': 'STONE',
'size': 0,
'attack': NonWeapon,
'ranged': MisThrown,
'accuracy': 0,             # This is not normal to hit, but a general bonus.
'light': 0,
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 0,
'Ego': 0,
'DV': 0,
'PV': 0,
'StrScaling': 'F',
'DexScaling': 'F',
'intrinsics': [],
'flags': [],
'coolness': 0,
'frequency': 1000
}

# Weapons:
Cudgel = {
'char': '\\',
'color': libtcod.darkest_orange,
'name': 'cudgel',
'material': 'WOOD',
'size': -1,
'StrScaling': 'B',
'DexScaling': 'C',
'attack': Club,
'ranged': ClubThrown,
'flags': ['MELEE', 'WEAPON']
}

Torch = {
'char': '\\',
'color': libtcod.red,
'name': 'torch',
'material': 'WOOD',
'size': -1,
'light': 2,
'StrScaling': 'B',
'DexScaling': 'C',
'attack': TorchAttack,
'ranged': TorchThrown,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

Mace = {
'char': '\\',
'color': libtcod.silver,
'name': 'mace',
'material': 'IRON',
'size': 0,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': MaceAttack,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF']
}

SilverMace = {
'char': '\\',
'color': libtcod.white,
'name': 'silver mace',
'material': 'SILVER',
'size': 0,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': MaceAttack,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF'],
'frequency': 50
}

IceMace = {
'char': '\\',
'color': libtcod.cyan,
'name': 'ice mace',
'material': 'IRON',
'size': 0,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': IceMaceAttack,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF'],
'frequency': 10
}

WarHammer = {
'char': '\\',
'color': libtcod.dark_grey,
'name': 'war hammer',
'material': 'IRON',
'size': 2,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': Hammer,
'flags': ['MELEE', 'WEAPON']
}

GoldHammer = {
'char': '\\',
'color': libtcod.yellow,
'name': 'golden maul',
'material': 'GOLD',
'size': 2,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': Hammer,
'flags': ['MELEE', 'WEAPON'],
'frequency': 10
}

LanternHammer = { # In my language, 'lucerna' means lantern, so this is a play on
'char': '\\',     # the good old D&D 'lucerne hammer'. ;)
'color': libtcod.amber,
'name': 'lantern hammer',
'material': 'IRON',
'size': 2,
'light': 3,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': Hammer,
'flags': ['MELEE', 'WEAPON'],
'frequency': 2
}

GiantSpikedClub = {
'char': '\\',
'color': libtcod.darkest_orange,
'name': 'giant spiked club',
'material': 'WOOD',
'size': 2,
'StrScaling': 'A',
'DexScaling': 'E',
'attack': GiantClub,
'flags': ['MELEE', 'WEAPON'],
'frequency': 1
}

BroadAxe = {
'char': '\\',
'color': libtcod.silver,
'name': 'broad axe',
'material': 'IRON',
'size': 0,
'StrScaling': 'D',
'DexScaling': 'C',
'attack': SmallAxe,
'ranged': AxeThrown,
'intrinsics': [('CAN_CHOP', 1)],
'flags': ['MELEE', 'WEAPON']
}

PickAxe = {
'char': '\\',
'color': libtcod.silver,
'name': 'pick axe',
'material': 'IRON',
'size': 1,
'StrScaling': 'D',
'DexScaling': 'C',
'attack': SmallAxe,
'intrinsics': [('CAN_DIG', 1)],
'flags': ['MELEE', 'WEAPON'],
'frequency': 5
}

BattleAxe = {
'char': '\\',
'color': libtcod.dark_grey,
'name': 'battle axe',
'material': 'IRON',
'size': 2,
'StrScaling': 'C',
'DexScaling': 'D',
'attack': LargeAxe,
'flags': ['MELEE', 'WEAPON']
}

Spear = {
'char': '|',
'color': libtcod.darkest_orange,
'name': 'spear',
'material': 'WOOD',
'size': 1,
'StrScaling': 'D',
'DexScaling': 'B',
'attack': SpearAttack,
'ranged': SpearThrown,
'flags': ['MELEE', 'WEAPON']
}

WyrdSpear = {
'char': '|',
'color': libtcod.cyan,
'name': 'wyrd spear',
'material': 'GLASS',
'size': 1,
'StrScaling': 'D',
'DexScaling': 'B',
'attack': WyrdSpearAttack,
'ranged': WyrdSpearThrown,
'flags': ['MELEE', 'WEAPON'],
'frequency': 5
}

Scythe = {
'char': '|',
'color': libtcod.darker_grey,
'name': 'scythe',
'material': 'IRON',
'size': 2,
'StrScaling': 'B',
'DexScaling': 'C',
'attack': ScytheAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 150
}

QuarterStaff = {
'char': '|',
'color': libtcod.darkest_orange,
'name': 'quarterstaff',
'plural': 'quarterstaves',
'material': 'WOOD',
'size': 1,
'DV': 1,
'StrScaling': 'B',
'DexScaling': 'B',
'attack': WoodStaff,
'flags': ['MELEE', 'WEAPON', 'ENCHANT_DODGE'],
'frequency': 50
}

IronShodStaff = {
'char': '|',
'color': libtcod.silver,
'name': 'iron-shod staff',
'plural': 'iron-shod staves',
'material': 'IRON',
'size': 1,
'StrScaling': 'C', # TODO: ???
'DexScaling': 'C',
'attack': IronStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

SilverTipStaff = {
'char': '|',
'color': libtcod.white,
'name': 'silver-tipped staff',
'plural': 'silver-tipped staves',
'material': 'SILVER',
'size': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': IronStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

LeadFillStaff = {
'char': '|',
'color': libtcod.dark_grey,
'name': 'lead-filled staff',
'plural': 'lead-filled staves',
'material': 'WOOD',
'size': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': LeadStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

DragonStaff = {
'char': '|',
'color': libtcod.light_grey,
'name': 'dragonbone staff',
'plural': 'dragonbone staves',
'material': 'BONE',
'size': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': LeadStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

SerpentStaff = {
'char': '|',
'color': libtcod.desaturated_green,
'name': 'serpent staff',
'plural': 'serpent staves',
'material': 'WOOD',
'size': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': VenomStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

Knife = {
'char': ')',
'color': libtcod.dark_grey,
'name': 'knife',
'plural': 'knives',
'material': 'IRON',
'size': -2,
'StrScaling': 'C',
'DexScaling': 'A',
'attack': KnifeAttack,
'ranged': KnifeThrown,
'flags': ['MELEE', 'WEAPON']
}

VampireKnife = {
'char': ')',
'color': libtcod.dark_red,
'name': 'vampire knife',
'plural': 'vampire knives',
'material': 'BONE',
'size': -2,
'StrScaling': 'C',
'DexScaling': 'A',
'attack': VampKnifeAttack,
'ranged': KnifeThrown, # TODO? Probably not at range.
'flags': ['MELEE', 'WEAPON'],
'frequency': 10
}

RitualKnife = {
'char': ')',
'color': libtcod.dark_blue,
'name': 'ritual knife',
'plural': 'ritual knives',
'material': 'STONE', # Obsidian.
'size': -2,
'StrScaling': 'C',
'DexScaling': 'A',
'attack': ManaKnifeAttack,
'ranged': KnifeThrown,
'flags': ['MELEE', 'WEAPON'],
'frequency': 10
}

Dagger = {
'char': ')',
'color': libtcod.dark_grey,
'name': 'dagger',
'material': 'IRON',
'size': -2,
'StrScaling': 'D',
'DexScaling': 'S',
'attack': DaggerAttack,
'ranged': DaggerThrown,
'flags': ['MELEE', 'WEAPON']
}

SilverDagger = {
'char': ')',
'color': libtcod.light_grey,
'name': 'silver dagger',
'material': 'SILVER',
'size': -2,
'StrScaling': 'D',
'DexScaling': 'S',
'attack': DaggerAttack,
'ranged': DaggerThrown,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

ParryDagger = {
'char': ')',
'color': libtcod.dark_grey,
'name': 'parrying dagger',
'material': 'IRON',
'size': -2,
'DV': 1,
'StrScaling': 'D',
'DexScaling': 'S',
'attack': DaggerAttack,
#'ranged': DaggerThrown, # Not really well-weighted for throwing.
'flags': ['MELEE', 'WEAPON'],
'frequency': 10
}

VenomDagger = {
'char': ')',
'color': libtcod.desaturated_green,
'name': 'venom dagger',
'material': 'IRON',
'size': -2,
'StrScaling': 'D',
'DexScaling': 'S',
'attack': VenomDaggerAttack,
'ranged': DaggerThrown,
'flags': ['MELEE', 'WEAPON'],
'frequency': 10
}

SilverSickle = {
'char': ')',
'color': libtcod.white,
'name': 'silver sickle',
'material': 'SILVER',
'size': -1,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': SickleAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

GoldSickle = {
'char': ')',
'color': libtcod.yellow,
'name': 'golden sickle',
'material': 'GOLD',
'size': -1,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': SickleAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

Rapier = {
'char': ')',
'color': libtcod.silver,
'name': 'rapier',
'material': 'IRON',
'size': 0,
'StrScaling': 'C',
'DexScaling': 'B',
'attack': RapierAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 100
}

GoldRapier = {
'char': ')',
'color': libtcod.yellow,
'name': 'gilded rapier',
'material': 'GOLD',
'size': 0,
'StrScaling': 'C',
'DexScaling': 'B',
'attack': RapierAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 10
}

ShortSword = {
'char': ')',
'color': libtcod.silver,
'name': 'short sword',
'material': 'IRON',
'size': -1,
'DV': 1,
'StrScaling': 'D',
'DexScaling': 'A',
'attack': SmallSword,
'flags': ['MELEE', 'WEAPON']
}

VorpalSword = {
'char': ')',
'color': libtcod.azure,
'name': 'vorpal sword',
'material': 'IRON',
'size': -1,
'DV': 1,
'StrScaling': 'D',
'DexScaling': 'A',
'attack': VorpalSwordAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 5
}

QuickSword = {
'char': ')',
'color': libtcod.fuchsia,
'name': 'quick blade',
'material': 'IRON',
'size': -1,
'DV': 1,
'StrScaling': 'D',
'DexScaling': 'A',
'attack': SmallSword,
'intrinsics': [('HASTE', 1)],
'flags': ['MELEE', 'WEAPON'],
'frequency': 5
}

LongSword = {
'char': ')',
'color': libtcod.silver,
'name': 'long sword',
'material': 'IRON',
'size': 0,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': MediumSword,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF']
}

Katana = {
'char': ')',
'color': libtcod.silver,
'name': 'katana',
'material': 'IRON',
'size': 0,
'StrScaling': 'B',
'DexScaling': 'B',
'attack': MediumSword,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF'],
'frequency': 5
}

FlamingSword = {
'char': ')',
'color': libtcod.red,
'name': 'flaming sword',
'material': 'IRON',
'size': 0,
'light': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': FlamingSwordAttack,
'flags': ['MELEE', 'WEAPON', 'TWO_AND_HALF'],
'frequency': 5
}

GreatSword = {
'char': ')',
'color': libtcod.silver,
'name': 'great sword',
'material': 'IRON',
'size': 1,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': LargeSword,
'flags': ['MELEE', 'WEAPON']
}

FierySword = {
'char': ')',
'color': libtcod.red,
'name': 'fiery great sword',
'material': 'AETHER', # This sword is actually just an enchanted flame.
'size': 1,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': FierySwordAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 5
}

Scimitar = {
'char': ')',
'color': libtcod.silver,
'name': 'two-handed scimitar',
'material': 'IRON',
'size': 2,
'StrScaling': 'S',
'DexScaling': 'E',
'attack': HugeSword,
'flags': ['MELEE', 'WEAPON'],
'frequency': 30
}

TripleSword = {
'char': ')',
'color': libtcod.silver,
'name': 'triple sword',
'material': 'IRON',
'size': 2,
'StrScaling': 'B',
'DexScaling': 'D',
'attack': TripleSwordAttack,
'flags': ['MELEE', 'WEAPON', 'NO_PREFIX', 'NO_SUFFIX'],
'frequency': 1
}

DaiKlaive = {
'char': ')',
'color': libtcod.yellow,
'name': 'orichalcum daiklaive',
'material': 'GOLD',
'size': 2,
'StrScaling': 'S',
'DexScaling': 'E',
'attack': KlaiveAttack,
'flags': ['MELEE', 'WEAPON', 'ENCHANT_DOUBLE', 'ALWAYS_BLESSED', 'NO_PREFIX',
          'NO_SUFFIX', 'UNIQUE'],
'frequency': 1
}

Chain = {
'char': 'S',
'color': libtcod.dark_grey,
'name': 'chain',
'material': 'IRON',
'size': 1,
'StrScaling': 'B',
'DexScaling': 'C',
'attack': ChainAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 50
}

Whip = {
'char': 'S',
'color': libtcod.darker_orange,
'name': 'whip',
'material': 'LEATHER',
'size': 0,
'StrScaling': 'E',
'DexScaling': 'S',
'attack': WhipAttack,
'flags': ['MELEE', 'WEAPON'],
'frequency': 100
}

# Shields:
Buckler = {
'char': '[',
'color': libtcod.silver,
'name': 'buckler',
'material': 'IRON',
'size': -1,
'attack': SmallShield,
'StrScaling': 'C',
'DexScaling': 'A',
'flags': ['SHIELD', 'TWO_HAND_OK'],
'frequency': 100
}

TurtleShield = {
'char': '[',
'color': libtcod.desaturated_green,
'name': 'turtle shield',
'material': 'BONE',
'PV': 1,
'size': -1,
'attack': TurtleShieldAttack,
'StrScaling': 'C',
'DexScaling': 'A',
'flags': ['SHIELD'],
'frequency': 5
}

RoundShield = {
'char': '[',
'color': libtcod.darkest_orange,
'name': 'round shield',
'material': 'WOOD',
'size': -1,
'attack': MediumShield,
'StrScaling': 'B',
'DexScaling': 'B',
'flags': ['SHIELD']
}

LanternShield = {
'char': '[',
'color': libtcod.amber,
'name': 'lantern shield',
'material': 'IRON',
'size': -1,
'light': 3,
'attack': MediumShield,
'StrScaling': 'B',
'DexScaling': 'B',
'flags': ['SHIELD'],
'frequency': 5
}

SpikedShield = {
'char': '[',
'color': libtcod.dark_grey,
'name': 'spiked shield',
'material': 'IRON',
'size': -1,
'attack': MediumShield,
'StrScaling': 'B',
'DexScaling': 'B',
'flags': ['SHIELD', 'WEAPON'],
'frequency': 5
}

KiteShield = {
'char': '[',
'color': libtcod.silver,
'name': 'kite shield',
'material': 'IRON',
'size': 0,
'attack': LargeShield,
'StrScaling': 'A',
'DexScaling': 'C',
'flags': ['SHIELD']
}

IceShield = {
'char': '[',
'color': libtcod.cyan,
'name': 'ice shield',
'material': 'WATER', # It's made of ice, d'oh.
'size': 0,
'attack': LargeShield,
'StrScaling': 'A',
'DexScaling': 'C',
'intrinsics': [('RESIST_FIRE', 1)],
'flags': ['SHIELD'],
'frequency': 5
}

TowerShield = {
'char': '[',
'color': libtcod.darkest_orange,
'name': 'tower shield',
'material': 'WOOD',
'size': 2,
'attack': HugeShield,
'StrScaling': 'S',
'DexScaling': 'D',
'flags': ['SHIELD', 'ENCHANT_PROTECTION'],
'frequency': 100
}

# mirror shield

# Headgear:
Bandana = {
'char': '-',
'color': libtcod.dark_green,
'name': 'bandana',
'material': 'CLOTH',
'DV': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

Hood = {
'char': '-',
'color': libtcod.dark_green,
'name': 'hood',
'material': 'CLOTH',
'DV': 2,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 10
}

Headband = {
'char': '-',
'color': libtcod.red,
'name': 'headband',
'material': 'CLOTH',
'accuracy': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

Crown = {
'char': '-',
'color': libtcod.yellow,
'name': 'golden crown',
'material': 'GOLD',
'PV': 0,
'DV': 0,
'size': -2,
'flags': ['HEAD', 'ARMOR', 'ENCHANT_DOUBLE'],
'frequency': 10
}

Circlet = {
'char': '-',
'color': libtcod.white,
'name': 'silver circlet',
'material': 'SILVER',
'PV': 0,
'DV': 0,
'size': -2,
'flags': ['HEAD', 'ARMOR', 'ENCHANT_DODGE'],
'frequency': 10
}

Skullcap = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'skullcap',
'material': 'LEATHER',
'PV': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR']
}

Coif = {
'char': '-',
'color': libtcod.silver,
'name': 'chain coif',
'material': 'IRON',
'PV': 1,
'DV': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 10
}

Helm = {
'char': '-',
'color': libtcod.silver,
'name': 'helmet',
'material': 'IRON',
'PV': 2,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 100
}

FullHelm = {
'char': '-',
'color': libtcod.silver,
'name': 'full helmet',
'material': 'IRON',
'DV': -1,
'PV': 3,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 150
}

GreatHelm = {
'char': '-',
'color': libtcod.silver,
'name': 'great helmet',
'material': 'IRON',
'DV': -2,
'PV': 5,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 200
}

Halo = {
'char': '-',
'color': libtcod.yellow,
'name': 'halo',
'material': 'AETHER',
'PV': 0,
'DV': 0,
'light': 2,
'size': -2,
'flags': ['HEAD', 'ARMOR', 'ENCHANT_LIGHT'],
'frequency': 1
}

Mask = {
'char': '-',
'color': libtcod.darkest_orange,
'name': 'mask',
'material': 'WOOD',
'PV': 0,
'DV': 0,
'size': -2,
'flags': ['HEAD', 'ARMOR', 'ALWAYS_SPECIAL'],
'frequency': 10
}

Blindfold = {
'char': '-',
'color': libtcod.darker_grey,
'name': 'blindfold',
'material': 'CLOTH',
'PV': 0,
'DV': 0,
'size': -2,
'intrinsics': [('BLIND', 1)],
'flags': ['HEAD', 'ARMOR'],
'coolness': -5,
'frequency': 1
}

# horned helmet
# gladiator helmet
# plumed helmet
# fedora
# witch hat
# wizard hat
# gas mask

# Handwear:
LeatherGlove = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'leather glove',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 1,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 800
}

BlackGlove = {
'char': '(',
'color': libtcod.darker_grey,
'name': 'black glove',
'material': 'CLOTH',
'size': -1,
'accuracy': 1,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 400
}

Gauntlet = {
'char': '(',
'color': libtcod.silver,
'name': 'iron gauntlet',
'material': 'IRON',
'size': -1,
'DV': -1,
'PV': 3,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 700
}

Bracer = {
'char': '(',
'color': libtcod.silver,
'name': 'iron bracer',
'material': 'IRON',
'size': -1,
'DV': -2,
'PV': 5,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 500
}

Bracelet = {
'char': '(',
'color': libtcod.yellow,
'name': 'golden bracelet',
'material': 'GOLD',
'size': -1,
'DV': 0,
'PV': 0,
'flags': ['ARM', 'ARMOR', 'ENCHANT_DOUBLE'],
'frequency': 10
}

ArmGuard = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'leather arm-guard',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['ARM', 'ARMOR', 'PAIRED'],
'frequency': 500
}

# Armor:
LeatherArmor = {
'char': ']',
'color': libtcod.darker_orange,
'name': 'boiled leather cuirass',
'plural': 'boiled leather cuirasses',
'material': 'LEATHER',
'size': 0,
'DV': -1,
'PV': 2,
'flags': ['TORSO', 'ARMOR']
}

StuddedArmor = {
'char': ']',
'color': libtcod.darker_orange,
'name': 'studded leather cuirass',
'plural': 'studded leather cuirasses',
'material': 'IRON',
'size': 0,
'DV': -2,
'PV': 3,
'flags': ['TORSO', 'ARMOR']
}

ChainArmor = {
'char': ']',
'color': libtcod.silver,
'name': 'chain mail',
'material': 'IRON',
'size': 0,
'DV': -3,
'PV': 5,
'flags': ['TORSO', 'ARMOR']
}

SilverChainArmor = {
'char': ']',
'color': libtcod.white,
'name': 'mithril chain mail',
'material': 'SILVER',
'size': 0,
'DV': -2,
'PV': 5,
'flags': ['TORSO', 'ARMOR', 'ENCHANT_DODGE'],
'frequency': 50
}

ScaleArmor = {
'char': ']',
'color': libtcod.silver,
'name': 'scale mail',
'material': 'IRON',
'size': 0,
'DV': -4,
'PV': 7,
'flags': ['TORSO', 'ARMOR']
}

PlateArmor = {
'char': ']',
'color': libtcod.silver,
'name': 'plate mail',
'material': 'IRON',
'size': 0,
'DV': -5,
'PV': 9,
'flags': ['TORSO', 'ARMOR']
}

GoldPlateArmor = {
'char': ']',
'color': libtcod.yellow,
'name': 'golden plate mail',
'material': 'GOLD',
'size': 0,
'DV': -5,
'PV': 8,
'flags': ['TORSO', 'ARMOR', 'ENCHANT_DOUBLE'],
'frequency': 1
}

BarkArmor = {
'char': ']',
'color': libtcod.darkest_orange,
'name': 'bark breastplate',
'material': 'WOOD',
'size': 0,
'DV': 1,
'PV': 1,
'flags': ['TORSO', 'ARMOR'],
'frequency': 10
}

CrystalShard = {
'char': ']',
'color': libtcod.cyan,
'name': 'crystal shard mail',
'material': 'GLASS',
'size': 0,
'DV': -4,
'PV': 8,
'flags': ['TORSO', 'ARMOR'],
'frequency': 5
}

CrystalPlate = {
'char': ']',
'color': libtcod.cyan,
'name': 'crystal plate mail',
'material': 'GLASS',
'size': 0,
'DV': -5,
'PV': 10,
'flags': ['TORSO', 'ARMOR'],
'frequency': 5
}

LeatherTunic = {
'char': ']',
'color': libtcod.darker_orange,
'name': 'leather tunic',
'material': 'LEATHER',
'size': 0,
'DV': 0,
'PV': 1,
'flags': ['TORSO', 'ARMOR']
}

GreenTunic = {
'char': ']',
'color': libtcod.dark_green,
'name': 'green tunic',
'material': 'CLOTH',
'size': 0,
'DV': 1,
'PV': 0,
'flags': ['TORSO', 'ARMOR']
}

RedTunic = {
'char': ']',
'color': libtcod.dark_red,
'name': 'red tunic',
'material': 'CLOTH',
'size': 0,
'accuracy': 1,
'flags': ['TORSO', 'ARMOR', 'ENCHANT_ACCURACY'],
'frequency': 10
}

PiedTunic = {
'char': ']',
'color': libtcod.gold,
'name': 'pied tunic',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'intrinsics': [('REGEN_STAM', 1)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 5
}

SnakeVest = {
'char': ']',
'color': libtcod.desaturated_green,
'name': 'snakeskin vest',
'material': 'LEATHER',
'size': 0,
'intrinsics': [('RESIST_POISON', 3)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 10
}

BlackRobe = {
'char': ']',
'color': libtcod.darker_grey,
'name': 'black robe',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'flags': ['TORSO', 'ARMOR'],
'frequency': 20
}

BrownRobe = {
'char': ']',
'color': libtcod.darker_orange,
'name': 'brown robe',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'intrinsics': [('REGEN_LIFE', 1)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 20
}

WhiteRobe = {
'char': ']',
'color': libtcod.white,
'name': 'white robe',
'material': 'CLOTH',
'size': 0,
'DV': 0,
'PV': 0,
'intrinsics': [('REGEN_MANA', 1)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 20
}

BlueDress = {
'char': ']',
'color': libtcod.blue,
'name': 'blue dress',
'plural': 'blue dresses',
'material': 'CLOTH',
'size': -1,
'DV': 0,
'PV': 0,
'intrinsics': [('HASTE', 1), ('WATER_WALK', 1)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 1
}

GreenDress = {
'char': ']',
'color': libtcod.dark_green,
'name': 'green dress',
'plural': 'green dresses',
'material': 'CLOTH',
'size': -1,
'DV': 0,
'PV': 0,
'intrinsics': [('RESIST_WOOD', 1)], # TODO: forestry
'flags': ['TORSO', 'ARMOR'],
'frequency': 1
}

GrayDress = {
'char': ']',
'color': libtcod.grey,
'name': 'gray dress',
'plural': 'gray dresses',
'material': 'CLOTH',
'size': -1,
'DV': 0,
'PV': 0,
'intrinsics': [('RESIST_EARTH', 1), ('CAN_DIG', 1)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 1
}

RedDress = {
'char': ']',
'color': libtcod.dark_red,
'name': 'red dress',
'plural': 'red dresses',
'material': 'CLOTH',
'size': -1,
'DV': 0,
'PV': 0,
'intrinsics': [('BLOODLESS', 1)], # TODO: blood sense?
'flags': ['TORSO', 'ARMOR'],
'frequency': 1
}

# spiked leather cuirass
# zombie hide armor
# troll hide armor
# dragon scale mail
# bone breastplate
# wyrd wrappings
# fur cloak
# cloak of invisibility
# cloak of protection
# cloak of defense

# Belts:
LeatherBelt = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'leather belt',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 1,
'flags': ['GROIN', 'ARMOR'],
'frequency': 800
}

BlackBelt = {
'char': '-',
'color': libtcod.darker_grey,
'name': 'black belt',
'material': 'CLOTH',
'size': -1,
'accuracy': 1,
'flags': ['GROIN', 'ARMOR', 'ENCHANT_ACCURACY'],
'frequency': 60
}

Girdle = {
'char': '-',
'color': libtcod.silver,
'name': 'iron girdle',
'material': 'IRON',
'size': -1,
'DV': -1,
'PV': 3,
'flags': ['GROIN', 'ARMOR'],
'frequency': 700
}

PlateSkirt = {
'char': '-',
'color': libtcod.silver,
'name': 'plate skirt',
'material': 'IRON',
'size': -1,
'DV': -2,
'PV': 5,
'flags': ['GROIN', 'ARMOR'],
'frequency': 600
}

Baldric = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'baldric',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['GROIN', 'ARMOR'],
'frequency': 100
}

# Legwear:
Sandal = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'leather sandal',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['LEG', 'ARMOR', 'PAIRED']
}

SnakeSandal = {
'char': '(',
'color': libtcod.desaturated_green,
'name': 'snakeskin sandal',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'flags': ['LEG', 'ARMOR', 'PAIRED', 'ENCHANT_DODGE'],
'frequency': 10
}

SaintSandal = {
'char': '(',
'color': libtcod.yellow,
'name': 'river-wife sandal',
'material': 'LEATHER',
'size': -1,
'DV': 1,
'PV': 0,
'intrinsics': [('WATER_WALK', 1)],
'flags': ['LEG', 'ARMOR', 'PAIRED'],
'frequency': 5
}

LowBoot = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'low boot',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 1,
'flags': ['LEG', 'ARMOR', 'PAIRED']
}

HighBoot = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'high boot',
'material': 'LEATHER',
'size': -1,
'DV': 0,
'PV': 2,
'flags': ['LEG', 'ARMOR', 'PAIRED'],
'frequency': 100
}

Clog = {
'char': '(',
'color': libtcod.darkest_orange,
'name': 'clog',
'material': 'WOOD',
'size': -1,
'DV': -1,
'PV': 3,
'flags': ['LEG', 'ARMOR', 'PAIRED']
}

Greave = {
'char': '(',
'color': libtcod.silver,
'name': 'iron greave',
'material': 'IRON',
'size': -1,
'DV': -2,
'PV': 5,
'flags': ['LEG', 'ARMOR', 'PAIRED'],
'frequency': 200
}

Anklet = {
'char': '(',
'color': libtcod.white,
'name': 'silver anklet',
'material': 'SILVER',
'size': -1,
'DV': 0,
'PV': 0,
'flags': ['LEG', 'ARMOR', 'ENCHANT_PROTECTION'],
'frequency': 10
}

# Potions:
HealPotion = {
'char': '!',
'color': libtcod.red, # TODO: Randomization.
'name': 'healing potion',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'HEAL'],
'coolness': 20 # TODO
}

MutationPotion = {
'char': '!',
'color': libtcod.green,
'name': 'vial',
'suffix': 'of mutagen',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'MUTATION'],
'coolness': 0,
'frequency': 5
}

StrengthPotion = {
'char': '!',
'color': libtcod.magenta,
'name': 'potion',
'suffix': 'of strength',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'STRENGTH'],
'coolness': 20,
'frequency': 5
}

DexterityPotion = {
'char': '!',
'color': libtcod.magenta,
'name': 'potion',
'suffix': 'of dexterity',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'DEXTERITY'],
'coolness': 20,
'frequency': 5
}

EndurancePotion = {
'char': '!',
'color': libtcod.magenta,
'name': 'potion',
'suffix': 'of endurance',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'ENDURANCE'],
'coolness': 20,
'frequency': 5
}

WitsPotion = {
'char': '!',
'color': libtcod.magenta,
'name': 'potion',
'suffix': 'of intellect',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'WITS'],
'coolness': 20,
'frequency': 5
}

EgoPotion = {
'char': '!',
'color': libtcod.magenta,
'name': 'potion',
'suffix': 'of beauty',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'EGO'],
'coolness': 20,
'frequency': 5
}

# Tools:
Bandage = {
'char': '{',
'color': libtcod.white,
'name': 'bandage',
'material': 'CLOTH',
'size': -2,
'flags': ['TOOL', 'BANDAGE', 'SMALL_PILE'],
'coolness': 10,
'frequency': 500
}

# Valuables:
GoldPiece = {
'char': '$',
'color': libtcod.yellow,
'name': 'gold nugget',
'material': 'GOLD',
'size': -2,
'flags': ['VALUABLE', 'BIG_PILE', 'ALWAYS_MUNDANE', 'NO_PREFIX', 'NO_SUFFIX'],
'frequency': 50
}

SunStone = {
'char': '*',
'color': libtcod.amber,
'name': 'sunstone',
'material': 'STONE',
'light': 10,
'size': -2,
'ranged': RockThrown,
'flags': ['VALUABLE'],
'frequency': 10
}

WyrdLight = {
'char': '*',
'color': libtcod.cyan,
'prefix': 'floating',
'name': 'wyrd-light',
'material': 'GLASS',
'light': 3,
'size': -2,
'flags': ['VALUABLE', 'ENCHANT_LIGHT', 'CARRY_LIGHT', 'NO_PREFIX', 'NO_SUFFIX'],
'frequency': 1
}

MacGuffin = {
'char': chr(12),
'color': libtcod.yellow,
'name': 'amulet',
'suffix': 'of Yendor',
'material': 'GOLD',
'light': 1,
'size': -2,
'intrinsics': [('REGEN_LIFE', 1), ('REGEN_MANA', 1), ('REGEN_STAM', 1)],
'flags': ['VALUABLE', 'MAC_GUFFIN', 'ALWAYS_BLESSED', 'ENCHANT_LIGHT', 'NO_PREFIX',
          'NO_SUFFIX', 'UNIQUE'],
'frequency': 0
}

# Food:
Berry = {
'char': chr(236),
'color': libtcod.blue,
'name': 'berry',
'plural': 'berries',
'material': 'PLANT',
'size': -2,
'flags': ['FOOD'],
'frequency': 300
}

# Containers:
Pouch = {
'char': chr(11),
'color': libtcod.blue,
'name': 'pouch',
'material': 'CLOTH',
'size': -2,
'flags': ['CONTAINER'],
'frequency': 20
}

Sack = {
'char': chr(11),
'color': libtcod.darker_orange,
'name': 'satchel',
'material': 'LEATHER',
'size': 0,
'flags': ['CONTAINER'],
'frequency': 20
}

HoldingBag = {
'char': chr(11),
'color': libtcod.fuchsia,
'name': 'bag',
'suffix': 'of holding',
'material': 'LEATHER',
'size': 0,
'flags': ['CONTAINER', 'HOLDING'],
'frequency': 1
}

Chest = {
'char': chr(127),
'color': libtcod.darker_orange,
'name': 'chest',
'material': 'WOOD',
'size': 2,
'DV': -10,
'flags': ['FEATURE', 'CONTAINER'],
'frequency': 50
}

# Furniture and similar:
Boulder = {
'char': '0',
'color': libtcod.dark_grey,
'name': 'boulder',
'BlockMove': True,
'size': 2,
'DV': -10,
'attack': BoulderRoll,
'flags': ['FEATURE', 'PLUG'], # TODO: Block sight.
'frequency': 50
}

Statue = {
'char': '&',
'color': libtcod.dark_grey,
'name': 'statue',
'BlockMove': True,
'size': 2,
'DV': -10,
'attack': BoulderRoll,
'flags': ['FEATURE'],
'frequency': 5
}

Chair = {
'char': chr(249),
'color': libtcod.darker_orange,
'name': 'chair',
'material': 'WOOD',
'size': 1,
'DV': -10,
'flags': ['FEATURE'],
'frequency': 0
}

Table = {
'char': chr(250),
'color': libtcod.darker_orange,
'name': 'table',
'BlockMove': True,
'material': 'WOOD',
'size': 2,
'DV': -10,
'flags': ['FEATURE'],
'frequency': 0
}

Bed = {
'char': chr(251),
'color': libtcod.darker_orange,
'name': 'bed',
'material': 'WOOD',
'size': 2,
'DV': -10,
'flags': ['FEATURE'],
'frequency': 0
}

###############################################################################
#  Monsters
###############################################################################

DummyMonster = {
'char': 'Q', # The question is, what is this strange monster?
'color': libtcod.white,
'name': 'BUG: dummy monster',
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 3,
'material': 'FLESH',
'sex': 'NEUTER',
'size': 0,
'diet': ['FLESH', 'PLANT', 'WATER'],
'intrinsics': [],
'inventory': [],
'mutations': [],
'flags': ['HUMANOID'],
'frequency': 1000,
'DL': 0
}

Player = {
'char': '@',
'color': libtcod.white,
'name': 'Player',
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 0,
'sex': 'MOF',
#'intrinsics': [],
'inventory': [Knife, Torch, HealPotion],
'flags': ['HUMANOID', 'AVATAR', 'UNIQUE'],
'frequency': 0
}

Ooze = {
'char': 'j',
'color': libtcod.light_green,
'name': 'cave ooze',
'Str': 0,
'Dex': -2,
'End': 0,
'Wit': -20,
'Ego': -20,
'speed': 0.8,
'size': -1,
'sight': 2,
'sex': 'UNDEFINED',
'diet': ['BONE', 'CLOTH', 'FLESH', 'IRON', 'LEATHER', 'PAPER', 'PLANT', 'WATER', 'WOOD'],
'intrinsics': [('IMMUNE_ACID', 1), ('IMMUNE_MIND', 1), ('RESIST_BLUNT', 5),
               ('RESIST_CHOKE', 15), ('BLOODLESS', 1), ('VULN_GLASS', 2)],
'flags': ['SLIME', 'AI_DIJKSTRA'],
'frequency': 200
}

KoboldForager = {
'char': 'k',
'color': libtcod.red,
'name': 'kobold forager',
'Str': 0,
'Dex': 2,
'End': -3,
'Wit': 1,
'Ego': 0,
'speed': 1,
'sight': 5,
'size': -1,
'sex': 'MOF',
'flags': ['HUMANOID', 'AI_KITE', 'AI_SCAVENGER'],
'mutations': ['MUTATION_CLAWS'],
'frequency': 600
}

KoboldHunter = {
'char': 'k',
'color': libtcod.darker_orange,
'name': 'kobold hunter',
'Str': 0,
'Dex': 3,
'End': -3,
'Wit': 1,
'Ego': 0,
'speed': 1.1,
'sight': 8,
'size': -1,
'sex': 'MOF',
'inventory': [Dagger],
'flags': ['HUMANOID'],
'mutations': ['MUTATION_CLAWS'],
'DL': 2,
'frequency': 600
}

KoboldFisher = {
'char': 'k',
'color': libtcod.blue,
'name': 'kobold fisher',
'Str': 0,
'Dex': 3,
'End': -3,
'Wit': 1,
'Ego': 0,
'speed': 1,
'sight': 5,
'size': -1,
'sex': 'MOF',
'inventory': [Spear],
'flags': ['HUMANOID'],
'mutations': ['MUTATION_CLAWS'],
'DL': 2,
'frequency': 600
}

KoboldMiner = {
'char': 'k',
'color': libtcod.dark_grey,
'name': 'kobold miner',
'Str': 1,
'Dex': 1,
'End': -1,
'Wit': 1,
'Ego': 0,
'speed': 1,
'sight': 5,
'size': -1,
'sex': 'MOF',
'inventory': [PickAxe],
'flags': ['HUMANOID'],
'mutations': ['MUTATION_CLAWS'],
'DL': 6,
'frequency': 5
}

KoboldWarrior = {
'char': 'k',
'color': libtcod.pink,
'name': 'kobold warrior',
'Str': 1,
'Dex': 2,
'End': -1,
'Wit': 1,
'Ego': 0,
'speed': 1,
'sight': 5,
'size': -1,
'sex': 'MOF',
'inventory': [Cudgel, RoundShield],
'flags': ['HUMANOID'],
'mutations': ['MUTATION_CLAWS'],
'DL': 2,
'frequency': 300
}

KoboldWhelp = {
'char': 'k',
'color': libtcod.light_red,
'name': 'kobold whelp',
'Str': 0,
'Dex': 2,
'End': -5,
'Wit': 1,
'Ego': 0,
'speed': 1.2,
'sight': 5,
'size': -2,
'sex': 'MOF',
'flags': ['HUMANOID', 'AI_KITE', 'AI_SCAVENGER'],
'frequency': 300
}

Kea = {
'char': 'K',
'color': libtcod.red,
'name': 'kea',
'Str': 0,
'Dex': 0,
'End': -8,
'Wit': -8,
'Ego': -8,
'size': -2,
'flags': ['BIRD', 'USE_HEAD', 'USE_NATURAL', 'FLY'],
'frequency': 800
}

Kestrel = {
'char': 'K',
'color': libtcod.blue,
'name': 'kestrel',
'Str': 0,
'Dex': 0,
'End': -8,
'Wit': -8,
'Ego': -8,
'speed': 1.2,
'size': -2,
'flags': ['BIRD', 'USE_HEAD', 'FLY'],
'frequency': 600
}

Kiwi = {
'char': 'K',
'color': libtcod.darker_orange,
'name': 'kiwi',
'Str': 0,
'Dex': 0,
'End': -8,
'Wit': -8,
'Ego': -8,
'size': -2,
'flags': ['BIRD', 'USE_HEAD']
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
'sex': 'MOF',
'inventory': [LongSword, KiteShield, ChainArmor, LowBoot],
'flags': ['HUMANOID'],
'DL': 2
}

Ogre = {
'char': 'O',
'color': libtcod.desaturated_green,
'name': 'ogre',
'Str': 3,
'Dex': 1,
'End': 0,
'Wit': -2,
'Ego': 0,
'size': 1,
'sex': 'MOF',
'inventory': [GiantSpikedClub],
'intrinsics': [('REGEN_STAM', 3)],
'flags': ['HUMANOID'],
'DL': 5,
'frequency': 200
}

Rat = {
'char': 'r',
'color': libtcod.darker_orange,
'name': 'rat',
'Str': -1,
'Dex': 1,
'End': -13,
'Wit': -10,
'Ego': -10,
'size': -2,
'sex': 'MOF',
'flags': ['ANIMAL', 'USE_HEAD']
}

Troll = {
'char': 'T',
'color': libtcod.dark_green,
'name': 'troll',
'Str': 2,
'Dex': 0,
'End': 2,
'Wit': -1,
'Ego': 0,
'size': 1,
'sex': 'MOF',
'intrinsics': [('REGEN_LIFE', 3)], # TODO: Revival.
'flags': ['HUMANOID', 'USE_HEAD'],
'mutations': ['MUTATION_CLAWS_LARGE'],
'DL': 5,
'frequency': 200
}

Alien = {
'char': 'y',
'color': libtcod.cyan,
'name': 'yill',
'Str': 0,
'Dex': 0,
'End': 0,
'Wit': 3,
'Ego': 3,
'sight': 5,
'sex': 'UNDEFINED',
'intrinsics': [('VULN_GOLD', 3)],
'flags': ['ALIEN', 'USE_LEGS', 'AI_DIJKSTRA'],
'DL': 7,
'frequency': 5
}

BlackKnight = {
'char': 'K',
'color': libtcod.darkest_grey,
'name': 'owl knight',
'Str': 4,
'Dex': 4,
'End': 4,
'Wit': 4,
'Ego': 4,
'speed': 1.5,
'sight': 10,
'size': 2,
'sex': 'MOF',
'intrinsics': [('REGEN_LIFE', 1), ('REGEN_MANA', 1), ('REGEN_STAM', 1),
               ('BLOODLESS', 1), ('CAN_DIG', 2), ('IMMUNE_POISON', 1)],
'inventory': [FlamingSword, TowerShield, FullHelm, Gauntlet, Greave, PlateArmor,
              PlateSkirt, MacGuffin],
'mutations': ['RANDOM_ANY'],
'flags': ['HUMANOID', 'USE_LEGS', 'UNIQUE'],
'frequency': 0
}

###############################################################################
#  Body Parts
###############################################################################

DummyPart = {
'name': 'BUG: dummy body part',
'cover': 100, # Chance of being hit there is based on cover.
'place': 0,   # How high (positive) or low (negative) on the body the part is.
'size': 0,    # How different the size of this part is to main body.
'eyes': 0,
#'breasts': 0,
#'testicles': 0,
'StrScaling': 'B',
'DexScaling': 'B',
'attack': Slam,
'material': 'FLESH',
'flags': []
}

Head = {
'name': 'head',
'cover': 40,
'place': 2,
'size': -2,
'eyes': 2,
'StrScaling': 'C', # No, head is not really that good for attacking.
'DexScaling': 'C',
'attack': Bite,
'flags': ['HEAD', 'VITAL']
}

BirdHead = {
'name': 'head',
'cover': 40,
'place': 2,
'size': -2,
'eyes': 2,
'attack': Beak,
'flags': ['HEAD', 'VITAL']
}

Torso = {
'name': 'torso',
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

SlimeTorso = {
'name': 'blob',
'eyes': 1,
'attack': AcidSlime,
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER', 'GRASP']
}

AlienTorso = {
'name': 'torso',
'eyes': 3,
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

AnimalTorso = {
'name': 'upper body',
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

Groin = {
'name': 'groin',
'cover': 40,
'place': -1,
'size': -1,
'flags': ['GROIN', 'VITAL', 'CANNOT_SEVER']
}

AnimalGroin = {
'name': 'lower body',
'cover': 50,
'size': -1,
'flags': ['GROIN', 'VITAL', 'CANNOT_SEVER']
}

Tail = {
'name': 'tail',
'cover': 50,
'place': -1,
'size': -1,
'StrScaling': 'A',
'DexScaling': 'C',
'attack': Club,
'flags': ['TAIL']
}

PrehensiveTail = {
'name': 'tail',
'cover': 40,
'place': -1,
'size': -1,
'StrScaling': 'C',
'DexScaling': 'A',
'flags': ['TAIL', 'GRASP']
}

Arm = {
'name': 'arm',
'cover': 70,
'place': 1,
'size': -1,
'flags': ['ARM']
}

TentacleArm = {
'name': 'tentacle',
'cover': 80,
'place': 1,
'attack': WhipAttack,
'flags': ['ARM', 'GRASP']
}

Hand = {
'name': 'hand',
'cover': 40,
'size': -2,
'attack': Punch,
'flags': ['HAND', 'GRASP']
}

HookHand = {
'name': 'hook hand',
'cover': 40,
'size': -2,
'attack': DaggerAttack,
'material': 'IRON',
'flags': ['HAND']
}

Leg = {
'name': 'leg',
'cover': 80,
'place': -2,
'size': -1,
'StrScaling': 'A',
'DexScaling': 'C',
'attack': Kick,
'flags': ['LEG']
}

PegLeg = {
'name': 'peg leg',
'cover': 80,
'place': -2,
'size': -1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': Club,
'material': 'WOOD',
'flags': ['LEG']
}

TentacleLeg = {
'name': 'tentacle',
'cover': 90,
'place': -2,
'attack': Club,
'flags': ['LEG']
}

Paw = {
'name': 'paw',
'cover': 80,
'place': -2,
'size': -1,
'attack': Claw,
'flags': ['LEG']
}

Talon = {
'name': 'talon',
'cover': 70,
'place': -2,
'size': -1,
'StrScaling': 'A',
'DexScaling': 'C',
'attack': Claw,
'flags': ['LEG', 'GRASP']
}

Wing = {
'name': 'wing',
'cover': 90,
'size': -1,
'attack': Buffet,
'flags': ['WING']
}

###############################################################################
#  Clouds
###############################################################################

# TODO:
#  flames
#  frost vapours
#  thick smoke
#  acid smoke
#  toxic smoke

###############################################################################
#  Terrains
###############################################################################

DummyTerrain = {
'char': '.',
'color': libtcod.white,
'name': 'BUG: dummy terrain',
'material': 'STONE',
'BlockMove': False,
'BlockSight': False,
'flags': []
}

# Walls:
RockWall = {
'char': '#',
'color': libtcod.dark_grey,
'name': 'rock wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG']
}

BrickWall = {
'char': '#',
'color': libtcod.light_grey,
'name': 'brick wall',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG']
}

WoodWall = {
'char': '#',
'color': libtcod.darkest_orange,
'name': 'wooden wall',
'material': 'WOOD',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_CHOPPED', 'CAN_BE_BURNED']
}

IceWall = {
'char': '#',
'color': libtcod.dark_cyan,
'name': 'ice wall',
'material': 'WATER',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG', 'CAN_BE_MELTED']
}

EarthWall = {
'char': '#',
'color': libtcod.dark_orange,
'name': 'earthen wall',
'material': 'CLAY',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_DUG']
}

GoldWall = {
'char': '#',
'color': libtcod.gold,
'name': 'gold-plated wall',
'material': 'GOLD',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL']
}

IronWall = {
'char': '#',
'color': libtcod.silver,
'name': 'iron wall',
'material': 'IRON',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_CORRODED']
}

IronBars = {
'char': chr(240), # Ie. ≡
'color': libtcod.silver,
'name': 'iron bars',
'material': 'IRON',
'BlockMove': True,
'BlockSight': False,
'flags': ['WALL', 'CAN_BE_CORRODED']
}

Mountain = {
'char': '^',
'color': libtcod.dark_grey,
'name': 'mountain',
'BlockMove': True,
'BlockSight': True,
'flags': ['WALL', 'CAN_BE_CLIMBED']
}

# Floors:
RockFloor = {
'char': '.',
'color': libtcod.light_grey,
'name': 'rock floor',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

WoodFloor = {
'char': '.',
'color': libtcod.darker_orange,
'name': 'parquet',
'material': 'WOOD',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_BURNED']
}

EarthFloor = {
'char': '.',
'color': libtcod.dark_orange,
'name': 'dirt floor',
'material': 'CLAY',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

IronFloor = {
'char': '.',
'color': libtcod.silver,
'name': 'iron floor',
'material': 'IRON',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

GoldFloor = {
'char': '.',
'color': libtcod.yellow,
'name': 'gold-plated floor',
'material': 'GOLD',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

Carpet = {
'char': '.',
'color': libtcod.fuchsia,
'name': 'carpet',
'material': 'CLOTH',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_BURNED']
}

IceFloor = {
'char': '.',
'color': libtcod.cyan,
'name': 'ice floor',
'material': 'WATER',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'SLIDE', 'CAN_BE_MELTED']
}

GrassFloor = {
'char': '.',
'color': libtcod.green,
'name': 'grass',
'material': 'PLANT',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_BURNED']
}

Snow = {
'char': '.',
'color': libtcod.white,
'name': 'snow',
'material': 'WATER',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_MELTED']
}

DeepSnow = {
'char': ',',
'color': libtcod.white,
'name': 'deep snow',
'material': 'WATER',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_MELTED', 'WADE']
}

Sand = {
'char': '.',
'color': libtcod.light_yellow,
'name': 'sand',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND']
}

DeepSand = {
'char': ',',
'color': libtcod.light_yellow,
'name': 'quicksand',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'SWIM']
}

# Doors:
WoodDoor = {
'char': '+',
'color': libtcod.darkest_orange,
'name': 'wooden door',
'material': 'WOOD',
'BlockMove': True,
'BlockSight': True,
'flags': ['DOOR', 'CAN_BE_OPENED', 'CAN_BE_BURNED', 'CAN_BE_CHOPPED', 'CAN_BE_KICKED']
}

SecretDoor = {              # Opened will be revealed and transformed into normal
'char': '#',                # open doors. You need to zap them with invisibility
'color': libtcod.dark_grey, # to make them secret again.
'name': 'rock wall',
'material': 'WOOD',
'BlockMove': True,
'BlockSight': True,
'flags': ['DOOR', 'CAN_BE_OPENED', 'CAN_BE_BURNED', 'CAN_BE_CHOPPED', 'CAN_BE_KICKED', 'SECRET']
}

OpenDoor = {
'char': '\'',
'color': libtcod.darkest_orange,
'name': 'open door',
'material': 'WOOD',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'CAN_BE_CLOSED', 'CAN_BE_BURNED', 'CAN_BE_CHOPPED']
}

BrokenDoor = {
'char': '_',
'color': libtcod.darkest_orange,
'name': 'broken door',
'material': 'WOOD',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'ROUGH']
}

ClosedPort = {
'char': '+',
'color': libtcod.white,
'name': 'lowered portcullis',
'material': 'IRON',
'BlockMove': True,
'BlockSight': False,
'flags': ['DOOR', 'PORTCULLIS', 'CAN_BE_OPENED']
}

OpenPort = {
'char': '\'',
'color': libtcod.white,
'name': 'raised portcullis',
'material': 'IRON',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'PORTCULLIS', 'CAN_BE_CLOSED']
}

ClosedGoldDoor = {
'char': '+',
'color': libtcod.gold,
'name': 'gold-plated door',
'material': 'GOLD',
'BlockMove': True,
'BlockSight': True,
'flags': ['DOOR', 'CAN_BE_OPENED', 'BLOCKED']
}

OpenGoldDoor = {
'char': '\'',
'color': libtcod.gold,
'name': 'open gold-plated door',
'material': 'GOLD',
'BlockMove': False,
'BlockSight': False,
'flags': ['DOOR', 'CAN_BE_CLOSED', 'BLOCKED']
}

Curtain = {
'char': '+',
'color': libtcod.dark_fuchsia,
'name': 'curtain',
'material': 'CLOTH',
'BlockMove': False,
'BlockSight': True,
'flags': ['DOOR']
}

# Plants:
LeafyTree = {
'char': chr(5), # Ie. ♣
'color': libtcod.dark_green,
'name': 'tree',
'material': 'PLANT',
'BlockMove': True,
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'CAN_BE_CHOPPED', 'CAN_BE_CLIMBED', 'PLANT']
}

ConifTree = {   # Coniferous tree
'char': chr(6), # Ie. ♠
'color': libtcod.darker_green,
'name': 'tree',
'material': 'PLANT',
'BlockMove': True,
'BlockSight': True,
'flags': ['CAN_BE_BURNED', 'CAN_BE_CHOPPED', 'CAN_BE_CLIMBED', 'PLANT']
}

SnowTree = {   # Snow-covered tree
'char': chr(6),
'color': libtcod.white,
'name': 'tree',
'material': 'PLANT',
'BlockMove': True,
'BlockSight': True,
'flags': ['CAN_BE_CHOPPED', 'CAN_BE_CLIMBED', 'PLANT']
}

Vines = {
'char': '|',
'color': libtcod.dark_green,
'name': 'hanging vines',
'material': 'PLANT',
'BlockMove': False,
'BlockSight': True,
'flags': ['GROUND', 'ROUGH', 'CAN_BE_BURNED', 'PLANT']
}

TallGrass = {
'char': '\"',
'color': libtcod.dark_green,
'name': 'tall grass',
'material': 'PLANT',
'BlockMove': False,
'BlockSight': True,
'flags': ['GROUND', 'CAN_BE_BURNED', 'PLANT']
}

# Decorations:
AshPile = {
'char': '*',
'color': libtcod.light_grey,
'name': 'pile of ash',
'material': 'WOOD',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'ROUGH', 'CAN_BE_KICKED']
}

BonePile = {
'char': '*',
'color': libtcod.white,
'name': 'bone pile',
'material': 'BONE',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'ROUGH', 'CAN_BE_KICKED']
}

GoldPile = {
'char': '*',
'color': libtcod.yellow,
'name': 'pile of gold',
'material': 'GOLD',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'ROUGH', 'CAN_BE_KICKED']
}

SnowPile = {
'char': '*',
'color': libtcod.white,
'name': 'snow pile',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'ROUGH', 'CAN_BE_KICKED', 'CAN_BE_MELTED']
}

RockPile = {
'char': '*',
'color': libtcod.darker_grey,
'name': 'rock pile',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'ROUGH', 'CAN_BE_KICKED']
}

# Liquids:
ShallowWater = {
'char': '~',
'color': libtcod.blue,
'name': 'shallow water',
'material': 'WATER',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'WADE']
}

DeepWater = {
'char': chr(247),
'color': libtcod.darker_blue,
'name': 'deep water',
'material': 'WATER',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'SWIM']
}

Lava = {
'char': chr(247),
'color': libtcod.dark_red,
'name': 'lava',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'STICKY', 'BURN'] # You cannot swim in lava, it's more like sticky, hot mud.
}

AcidPool = {
'char': '~',
'color': libtcod.yellow,
'name': 'acid',
'material': 'WATER', # Well, yeah. Why not?
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'SWIM', 'DISSOLVE']
}

Mud = {
'char': '~',
'color': libtcod.darker_orange,
'name': 'mud',
'material': 'CLAY',
'BlockMove': False,
'BlockSight': False,
'flags': ['LIQUID', 'STICKY', 'WADE']
}

# Features:
UpStairs = {
'char': '<',
'color': libtcod.white,
'name': 'upward staircase',
'BlockMove': False,
'BlockSight': False,
'flags': ['FEATURE', 'STAIRS_UP']
}

DownStairs = {
'char': '>',
'color': libtcod.white,
'name': 'downward staircase',
'BlockMove': False,
'BlockSight': False,
'flags': ['FEATURE', 'STAIRS_DOWN']
}

Throne = {
'char': chr(20),
'color': libtcod.yellow,
'name': 'golden throne',
'material': 'GOLD',
'BlockMove': False,
'BlockSight': True,
'flags': ['FEATURE', 'CAN_BE_KICKED']
}

Grave = {
'char': chr(241), # Ie. ±
'color': libtcod.white,
'name': 'gravestone',
'BlockMove': False,
'BlockSight': False,
'flags': ['FEATURE', 'CAN_BE_KICKED']
}

Pit = {
'char': chr(224),
'color': libtcod.dark_grey,
'name': 'pit',
'BlockMove': False,
'BlockSight': False,
'flags': ['FEATURE', 'PIT']
}

# TODO: chasm

BookShelf = {
'char': chr(252),
'color': libtcod.darker_orange,
'name': 'bookshelf',
'material': 'WOOD',
'BlockMove': True,
'BlockSight': True,
'flags': ['FEATURE', 'CONTAINER', 'CAN_BE_OPENED', 'CAN_BE_CHOPPED', 'CAN_BE_BURNED']
}

MagicBox = {
'char': chr(252),
'color': libtcod.fuchsia,
'name': 'magic box',
'material': 'SILVER',
'BlockMove': True,
'BlockSight': True,
'flags': ['FEATURE', 'CONTAINER', 'CAN_BE_OPENED', 'MAGIC_BOX', 'HOLDING']
}

'''
# Changing terrain:
ChangedTerrain = {        # Certain actions can change terrain into this, eg. actionOpen on doors.
DummyTerrain: RockFloor,
OpenPort: ClosedPort,
ClosedPort: OpenPort,
WoodDoor: OpenDoor,
SecretDoor: OpenDoor,
OpenDoor: WoodDoor
}

DestroyedTerrain = {      # Damage can change terrain into this.
DummyTerrain: RockFloor,
WoodDoor: BrokenDoor,
OpenDoor: BrokenDoor,
SecretDoor: BrokenDoor,
IceFloor: ShallowWater,
IceWall: IceFloor,
RockWall: RockPile
}
'''
###############################################################################
#  Rooms
##############################################################################

DummyRoom = {
'frequency': 10,
#' ': (RockWall, None, None, None), # Space should be skipped, leaving original terrain.
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None),
'+': (WoodDoor, None, None, None),
'S': (SecretDoor, None, None, None),
'x': (WoodDoor, ['BLOCKED'], None, None),
'$': (RockFloor, None, GoldPiece, None),
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (DeepWater, None, None, None),
'=': (IronBars, None, None, None),
'_': (Carpet, None, None, None),
'@': (MagicBox, None, None, None)
}

# Several small cages.
Cage1 = {
'file': 'rooms/cage1',
'width': 9,
'height': 7
}

Cage2 = {
'file': 'rooms/cage2',
'width': 7,
'height': 7,
'1': (RockFloor, None, 'RANDOM_ANY', 'RANDOM_ANY'),
'x': (ClosedPort, ['LOCKED', 'BLOCKED'], None, None),
'X': (IronBars, None, None, None)
}

# Prison cells.
Prison = {
'file': 'rooms/prison',
'width': 10,
'height': 6,
'#': (BrickWall, None, None, None),
'+': (WoodDoor, ['LOCKED'], None, None)
}

# The letters.
LetterX = {
'file': 'rooms/xxx',
'width': 5,
'height': 5
}

LetterS = {
'file': 'rooms/ss',
'width': 6,
'height': 7
}

# Strange shapes.
Curved = {
'file': 'rooms/curved',
'width': 10,
'height': 8
}

CrissCross = {
'file': 'rooms/crisscross',
'width': 6,
'height': 6
}

Whirl = {
'file': 'rooms/whirl',
'width': 7,
'height': 7
}

Leaves = {
'file': 'rooms/leaves',
'width': 9,
'height': 9
}

# Four-way junctions.
Foursome1 = {
'file': 'rooms/foursome1',
'width': 10,
'height': 8
}

Foursome2 = {
'file': 'rooms/foursome2',
'width': 10,
'height': 8
}

# T-junction.
TJunction = {
'file': 'rooms/tjunction',
'width': 5,
'height': 4,
'0': (RockFloor, None, Boulder, None)
}

# A very secretly hidden rooms.
Secret1 = {
'file': 'rooms/secret1',
'frequency': 5,
'width': 11,
'height': 11,
'#': (WoodWall, None, None, None),
'X': (RockWall, None, None, None),
'.': (WoodFloor, None, None, None),
',': (RockFloor, None, None, None)
}

Secret2 = {
'file': 'rooms/secret2',
'frequency': 10,
'width': 10,
'height': 8
}

Secret3 = {
'file': 'rooms/secret3',
'frequency': 10,
'width': 10,
'height': 8
}

Secret4 = {
'file': 'rooms/secret4',
'frequency': 10,
'width': 10,
'height': 9,
'X': (BookShelf, None, None, None),
'@': (MagicBox, None, None, None),
'T': (RockFloor, None, Table, None),
'c': (RockFloor, None, Chair, None)
}

# Storage rooms (with monsters).
Storage1 = {
'file': 'rooms/storage1',
'width': 10,
'height': 8,
'r': (RockFloor, None, 'RANDOM_ANY', None),
's': (RockFloor, None, 'RANDOM_SPECIAL', None),
'T': (RockFloor, None, None, Ogre)
}

# Barracks.
Barracks1 = {
'file': 'rooms/barracks1',
'width': 9,
'height': 5,
'X': (RockFloor, None, Bed, None)
}

Barracks2 = {
'file': 'rooms/barracks2',
'width': 7,
'height': 7,
'X': (RockFloor, None, Bed, None)
}

# Guard stations.
Guard1 = {
'file': 'rooms/guard1',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard2 = {
'file': 'rooms/guard2',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard3 = {
'file': 'rooms/guard3',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard4 = {
'file': 'rooms/guard4',
'width': 10,
'height': 8,
'!': (IronBars, None, None, None)
}

Guard5 = {
'file': 'rooms/guard5',
'width': 8,
'height': 7,
'!': (IronBars, None, None, None)
}

# Several rooms in one.
SmallRooms1 = {
'file': 'rooms/smallrooms1',
'width': 10,
'height': 8,
}

SmallRooms2 = {
'file': 'rooms/smallrooms2',
'width': 18, # This may be too much.
'height': 11,
'x': (ClosedPort, None, None, None),
'!': (IronBars, None, None, None)
}

SmallRooms3 = {
'file': 'rooms/smallrooms3',
'width': 9,
'height': 9
}

# Why not?
Why1 = {
'file': 'rooms/why1',
'width': 5,
'height': 6,
}

Why2 = {
'file': 'rooms/why2',
'width': 5,
'height': 6,
}

# Checkers room!
Checkers = {
'file': 'rooms/checkers',
'width': 9,
'height': 7
}

# Large castle-like corridor.
Castle = {
'file': 'rooms/castle',
'width': 15,
'height': 15
}

# A small library.
Library1 = {
'file': 'rooms/library1',
'width': 7,
'height': 7,
'X': (BookShelf, None, None, None)
}

Library2 = {
'file': 'rooms/library2',
'width': 9,
'height': 7,
'X': (BookShelf, None, None, None)
}

# Pillars in a room.
Pillars1 = {
'file': 'rooms/pillars1',
'width': 11,
'height': 11,
'>': (DownStairs, None, None, None)
}

Pillars2 = {
'file': 'rooms/pillars2',
'width': 9,
'height': 11
}

Pillars3 = {
'file': 'rooms/pillars3',
'width': 9,
'height': 9
}

Pillars4 = {
'file': 'rooms/pillars4',
'width': 11,
'height': 11
}

Pillars5 = {
'file': 'rooms/pillars5',
'width': 7,
'height': 7
}

Pillars6 = {
'file': 'rooms/pillars6',
'width': 9,
'height': 5
}

Pillars7 = {
'file': 'rooms/pillars7',
'width': 11,
'height': 11
}

Pillars8 = {
'file': 'rooms/pillars8',
'width': 11,
'height': 11
}

Pillars9a = {
'file': 'rooms/pillars9',
'width': 11,
'height': 11,
'~': (DeepWater, None, None, None)
}

Pillars9b = {
'file': 'rooms/pillars9',
'width': 11,
'height': 11,
'~': (Lava, None, None, None)
}

Pillars9c = {
'file': 'rooms/pillars9',
'width': 11,
'height': 11,
'~': (AcidPool, None, None, None)
}

Pillars10 = {
'file': 'rooms/pillars10',
'width': 11,
'height': 9
}

Pillars11 = {
'file': 'rooms/pillars11',
'width': 16,
'height': 9
}

# Pool rooms.
Pool1a = {
'file': 'rooms/pool1',
'width': 9,
'height': 10,
'~': (DeepWater, None, None, None)
}

Pool1b = {
'file': 'rooms/pool1',
'width': 9,
'height': 10,
'~': (Lava, None, None, None)
}

Pool1c = {
'file': 'rooms/pool1',
'width': 9,
'height': 10,
'~': (AcidPool, None, None, None)
}

Pool2a = {
'file': 'rooms/pool2',
'width': 9,
'height': 9,
'~': (DeepWater, None, None, None)
}

Pool2b = {
'file': 'rooms/pool2',
'width': 9,
'height': 9,
'~': (Lava, None, None, None)
}

Pool2c = {
'file': 'rooms/pool2',
'width': 9,
'height': 9,
'~': (AcidPool, None, None, None)
}

Pool3 = {
'file': 'rooms/pool3',
'width': 9,
'height': 9,
'~': (Lava, None, None, None)
}

# Circular corridors.
Circle1 = {
'file': 'rooms/circle1',
'width': 6,
'height': 6
}

Circle2 = {
'file': 'rooms/circle2',
'width': 7,
'height': 7
}

Circle3 = {
'file': 'rooms/circle3',
'width': 7,
'height': 7
}

# Lucy in the skies...
Diamond1 = {
'file': 'rooms/diamond1',
'width': 7,
'height': 7
}

Diamond2 = {
'file': 'rooms/diamond2',
'width': 7,
'height': 7,
')': (RockFloor, None, 'RANDOM_SPECIAL', None)
}

Diamond3 = {
'file': 'rooms/diamond3',
'width': 7,
'height': 7
}

Diamond4 = {
'file': 'rooms/diamond4',
'width': 7,
'height': 7
}

Diamond5 = {
'file': 'rooms/diamond5',
'width': 7,
'height': 7
}

Diamond6 = {
'file': 'rooms/diamond6',
'width': 7,
'height': 7
}

Diamond7 = {
'file': 'rooms/diamond7',
'width': 7,
'height': 7
}

Diamond8 = {
'file': 'rooms/diamond8',
'width': 7,
'height': 7
}

# Magic box rooms:
Magic1 = {
'file': 'rooms/magic1',
'width': 11,
'height': 11
}

Magic2 = {
'file': 'rooms/magic2',
'width': 9,
'height': 9,
',': (Carpet, None, None, None)
}

# Vaults:
Vault1 = {
'file': 'rooms/vault1',
'frequency': 1,
'width': 5,
'height': 5,
'#': (GoldWall, None, None, None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
'M': (GoldFloor, None, 'RANDOM_SPECIAL', 'RANDOM_ANY')
}

Vault2 = {
'file': 'rooms/vault2',
'frequency': 1,
'width': 5,
'height': 5,
'#': (GoldWall, None, None, None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
'M': (GoldFloor, None, 'RANDOM_ANY', 'RANDOM_ANY')
}

Vault3 = {
'file': 'rooms/vault3',
'frequency': 1,
'width': 5,
'height': 5,
'#': (GoldWall, None, None, None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
'M': (GoldFloor, None, 'RANDOM_ANY', 'RANDOM_ANY')
}

Vault4 = {
'file': 'rooms/vault4',
'frequency': 1,
'width': 5,
'height': 5,
'#': (GoldWall, None, None, None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
'M': (GoldFloor, None, 'RANDOM_ANY', 'RANDOM_ANY')
}

Vault5 = {
'file': 'rooms/vault5',
'frequency': 1,
'width': 8,
'height': 10,
'#': (GoldWall, None, None, None),
'X': (RockWall, None, None, None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
'M': (GoldFloor, None, 'RANDOM_ANY', 'RANDOM_ANY')
}

# Gardens.
Alley = {
'file': 'rooms/alley',
'width': 13,
'height': 7,
'T': (LeafyTree, None, None, None)
}

# the Surface:

Entrance1 = {
'file': 'rooms/entrance1',
'width': 35,
'height': 23,
'X': (BrickWall, None, None, None)
}

Entrance2 = {
'file': 'rooms/entrance2',
'width': 33,
'height': 17,
'#': (BrickWall, None, None, None),
',': (GrassFloor, None, None, None)
}

# the Big room:
BigRoom1a = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None)
}

BigRoom1b = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (BrickWall, None, None, None),
'.': (Carpet, None, None, None)
}

BigRoom1c = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (IronWall, None, None, None),
'.': (IronFloor, None, None, None)
}

BigRoom1d = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (GoldWall, None, None, None),
'.': (GoldFloor, None, None, None)
}

BigRoom1e = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (IceWall, None, None, None),
'.': (IceFloor, None, None, None)
}

BigRoom1f = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (EarthWall, None, None, None),
'.': (GrassFloor, None, None, None)
}

BigRoom1g = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (WoodWall, None, None, None),
'.': (WoodFloor, None, None, None)
}

BigRoom1h = {
'file': 'rooms/bigroom1',
'width': 75,
'height': 18,
'#': (RockWall, None, None, None),
'.': (Sand, None, None, None)
}

BigRoom2a = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None)
}

BigRoom2b = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (BrickWall, None, None, None),
'.': (Carpet, None, None, None)
}

BigRoom2c = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (IronWall, None, None, None),
'.': (IronFloor, None, None, None)
}

BigRoom2d = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (GoldWall, None, None, None),
'.': (GoldFloor, None, None, None)
}

BigRoom2e = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (IceWall, None, None, None),
'.': (IceFloor, None, None, None)
}

BigRoom2f = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (EarthWall, None, None, None),
'.': (GrassFloor, None, None, None)
}

BigRoom2g = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (WoodWall, None, None, None),
'.': (WoodFloor, None, None, None)
}

BigRoom2h = {
'file': 'rooms/bigroom2',
'width': 75,
'height': 18,
'#': (RockWall, None, None, None),
'.': (Sand, None, None, None)
}

BigRoom3a = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None)
}

BigRoom3b = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (BrickWall, None, None, None),
'.': (Carpet, None, None, None)
}

BigRoom3c = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (IronWall, None, None, None),
'.': (IronFloor, None, None, None)
}

BigRoom3d = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (GoldWall, None, None, None),
'.': (GoldFloor, None, None, None)
}

BigRoom3e = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (IceWall, None, None, None),
'.': (IceFloor, None, None, None)
}

BigRoom3f = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (EarthWall, None, None, None),
'.': (GrassFloor, None, None, None)
}

BigRoom3g = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (WoodWall, None, None, None),
'.': (WoodFloor, None, None, None)
}

BigRoom3h = {
'file': 'rooms/bigroom3',
'width': 74,
'height': 19,
'#': (RockWall, None, None, None),
'.': (Sand, None, None, None)
}

BigRoom4 = {
'file': 'rooms/bigroom4',
'width': 73,
'height': 19,
'>': (DownStairs, None, None, None),
'<': (UpStairs, None, None, None),
'T': (ConifTree, None, None, None)
}

BigRoom5 = {
'file': 'rooms/bigroom5',
'width': 75,
'height': 19,
'G': (Grave, None, None, None)
}

BigRoom6a = {
'file': 'rooms/bigroom6',
'width': 75,
'height': 18,
'-': (DeepWater, None, None, None)
}

BigRoom6b = {
'file': 'rooms/bigroom6',
'width': 75,
'height': 18,
'-': (Lava, None, None, None)
}

BigRoom6c = {
'file': 'rooms/bigroom6',
'width': 75,
'height': 18,
'-': (AcidPool, None, None, None)
}

BigRoom6d = {
'file': 'rooms/bigroom6',
'width': 75,
'height': 18,
'-': (TallGrass, None, None, None)
}

BigRoom6e = {
'file': 'rooms/bigroom6',
'width': 75,
'height': 18,
'-': (IronBars, None, None, None)
}

BigRoom6f = {
'file': 'rooms/bigroom6',
'width': 75,
'height': 18,
'-': (IceWall, None, None, None)
}

BigRoom7a = {
'file': 'rooms/bigroom7',
'width': 76,
'height': 21,
'-': (DeepWater, None, None, None),
'X': (RockWall, None, None, None)
}

BigRoom7b = {
'file': 'rooms/bigroom7',
'width': 76,
'height': 21,
'-': (RockWall, None, None, None),
'X': (Lava, None, None, None)
}

BigRoom7c = {
'file': 'rooms/bigroom7',
'width': 76,
'height': 21,
'-': (TallGrass, None, None, None),
'.': (GrassFloor, None, None, None),
'X': (LeafyTree, None, None, None)
}

BigRoom7d = {
'file': 'rooms/bigroom7',
'width': 76,
'height': 21,
'-': (IceWall, None, None, None),
'.': (IceFloor, None, None, None),
'X': (ShallowWater, None, None, None)
}

BigRoom7e = {
'file': 'rooms/bigroom7',
'width': 76,
'height': 21,
'-': (RockWall, None, None, None),
'.': (Sand, None, None, None),
'X': (RockWall, None, None, None)
}

BigRoom8 = {
'file': 'rooms/bigroom8',
'width': 73,
'height': 21,
'-': (GrassFloor, None, None, None),
'.': (TallGrass, None, None, None),
'X': (LeafyTree, None, None, None)
}

BigRoom9 = {
'file': 'rooms/bigroom9',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None)
}

BigRoom10a = {
'file': 'rooms/bigroom10',
'width': 19,
'height': 19,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (IceFloor, None, None, None),
'~': (DeepWater, None, None, None)
}

BigRoom10b = {
'file': 'rooms/bigroom10',
'width': 19,
'height': 19,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (Sand, None, None, None),
'~': (Lava, None, None, None)
}

BigRoom10c = {
'file': 'rooms/bigroom10',
'width': 19,
'height': 19,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (IronFloor, None, None, None),
'~': (AcidPool, None, None, None)
}

BigRoom10d = {
'file': 'rooms/bigroom10',
'width': 19,
'height': 19,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (GrassFloor, None, None, None),
'~': (TallGrass, None, None, None)
}

BigRoom11a = {
'file': 'rooms/bigroom11',
'width': 17,
'height': 21,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (IceFloor, None, None, None),
'~': (DeepWater, None, None, None)
}

BigRoom11b = {
'file': 'rooms/bigroom11',
'width': 17,
'height': 21,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (Sand, None, None, None),
'~': (Lava, None, None, None)
}

BigRoom11c = {
'file': 'rooms/bigroom11',
'width': 17,
'height': 21,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (IronFloor, None, None, None),
'~': (AcidPool, None, None, None)
}

BigRoom11d = {
'file': 'rooms/bigroom11',
'width': 17,
'height': 21,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'.': (GrassFloor, None, None, None),
'~': (TallGrass, None, None, None)
}

BigRoom12a = {
'file': 'rooms/bigroom12',
'width': 17,
'height': 17,
'X': (RockWall, None, None, None)
}

BigRoom12b = {
'file': 'rooms/bigroom12',
'width': 17,
'height': 17,
'X': (ConifTree, None, None, None)
}

BigRoom12c = {
'file': 'rooms/bigroom12',
'width': 17,
'height': 17,
'#': (EarthWall, None, None, None),
'X': (LeafyTree, None, None, None),
'.': (GrassFloor, None, None, None)
}

BigRoom13a = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (ShallowWater, None, None, None),
'~': (DeepWater, None, None, None)
}

BigRoom13b = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (LeafyTree, None, None, None),
'~': (TallGrass, None, None, None)
}

BigRoom13c = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (GrassFloor, None, None, None),
'~': (ConifTree, None, None, None)
}

BigRoom13d = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (RockFloor, None, None, None),
'~': (Lava, None, None, None)
}

BigRoom13e = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (RockFloor, None, None, None),
'~': (AcidPool, None, None, None)
}

BigRoom13f = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (ClosedPort, None, None, None),
'~': (IronBars, None, None, None)
}

BigRoom13g = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (Mud, None, None, None),
'~': (EarthWall, None, None, None)
}

BigRoom13h = {
'file': 'rooms/bigroom13',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'x': (GoldFloor, None, None, None),
'~': (GoldWall, None, None, None)
}

BigRoom14a = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (DeepWater, None, None, None)
}

BigRoom14b = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (Lava, None, None, None)
}

BigRoom14c = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (AcidPool, None, None, None)
}

BigRoom14d = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (LeafyTree, None, None, None)
}

BigRoom14e = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (ConifTree, None, None, None)
}

BigRoom14f = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (IceWall, None, None, None)
}

BigRoom14g = {
'file': 'rooms/bigroom14',
'width': 17,
'height': 17,
'<': (UpStairs, None, None, None),
'>': (DownStairs, None, None, None),
'~': (IronBars, None, None, None)
}

BigRoom15 = {
'file': 'rooms/bigroom15',
'width': 17,
'height': 17
}

BigRoom16 = {
'file': 'rooms/bigroom16',
'width': 17,
'height': 17
}

# the Goal:
Goal1 = {
'file': 'rooms/goal1',
'width': 70,
'height': 29,
'<': (UpStairs, None, None, None),
'#': (GoldWall, None, None, None),
'.': (GoldFloor, None, None, None),
',': (GoldFloor, None, 'RANDOM_SPECIAL', None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
'_': (Carpet, None, None, None),
'B': (BookShelf, None, None, None),
'X': (Throne, None, None, BlackKnight)
}

Goal2 = {
'file': 'rooms/goal2',
'width': 21,
'height': 32,
'<': (UpStairs, None, None, None),
'#': (GoldWall, None, None, None),
'.': (GoldFloor, None, None, None),
'+': (WoodDoor, ['BLOCKED'], None, None),
'd': (ClosedGoldDoor, ['BLOCKED'], None, None),
'X': (RockWall, None, None, None),
',': (RockFloor, None, None, None),
'x': (IronWall, None, None, None),
':': (IronFloor, None, None, None),
'-': (ClosedPort, None, None, None),
'=': (IronBars, None, None, None),
'_': (Carpet, None, None, None),
'I': (GoldFloor, None, 'RANDOM_SPECIAL', None),
'M': (GoldFloor, None, 'RANDOM_ANY', 'RANDOM_ANY'),
'T': (Throne, None, None, BlackKnight)
}

Goal3 = {
'file': 'rooms/goal3',
'width': 25,
'height': 43,
'<': (UpStairs, None, None, None),
'X': (GoldWall, None, None, None),
'.': (GoldFloor, None, None, None),
'+': (ClosedGoldDoor, ['BLOCKED'], None, None),
',': (RockFloor, None, None, None),
'-': (DeepWater, None, None, None),
'=': (IronBars, None, None, None),
'*': (Carpet, None, None, None),
'M': (GoldFloor, None, 'RANDOM_SPECIAL', 'RANDOM_ANY'),
'_': (Throne, None, None, BlackKnight)
}

Tutorial = {
'file': 'rooms/tutorial',
'width': 80,
'height': 50
}

###############################################################################
#  Lists
###############################################################################

# Lists must be last to have all stuff already defined.

# General:
# --------
Sizes = {
2: 'huge',
1: 'large',
0: 'medium',
-1: 'small',
-2: 'tiny'
}

Scaling = {
'S': 2.0,
'A': 1.5,
'B': 1.0,
'C': 0.75,
'D': 0.5,
'E': 0.25,
'F': 0.0
}

MaterialsList = [
'AETHER',
'BONE',
'CLAY',
'CLOTH',
'FLESH',
'GLASS',
'GOLD',
'IRON',
'LEATHER',
'PAPER',
'PLANT',
'SILVER',
'STONE',
'WATER',
'WOOD'
]

MaterialNameList = {
'AETHER': ['ethereal '],
'BONE': ['bone '],
'CLAY': ['clay ', 'ceramic '],
'CLOTH': ['cloth '],
'FLESH': ['flesh '],
'GLASS': ['glass ', 'crystal '],
'GOLD': ['gold ', 'golden ', 'gilded ', 'orichalcum '],
'IRON': ['iron ', 'iron-shod ', 'steel '],
'LEATHER': ['leather '],
'PAPER': ['paper ', 'parchment '],
'PLANT': ['plant '],
'SILVER': ['silver ', 'silvered ', 'silver-tipped ', 'mithril '],
'STONE': ['stone ', 'obsidian ', 'jade '],
'WATER': ['water '], # 'ice'
'WOOD': ['wood ', 'wooden ', 'bark ']
}

DamageTypeList = [
'ASPHYX',
'ALLERGY',
'BLUNT',
'SLASH',
'PIERCE',
'ACID',
'FIRE',
'FORCE',
'COLD',
'ELECTRIC',
'NECROTIC',
'POISON',
'BLEED',
'LIGHT',
'DARK',
'SOUND',
'MIND'
]

NonWoundingList = [
'ASPHYX',
'ALLERGY',
'NECROTIC',
'POISON',
'BLEED',
'DARK',
'MIND'
]

MaterialDamageList = {
'ASPHYX': [],
'ALLERGY': [],
'BLUNT': ['BONE', 'CLAY', 'GLASS', 'WATER', 'WOOD'],
'SLASH': ['BONE', 'CLOTH', 'FLESH', 'LEATHER', 'PAPER', 'PLANT', 'WATER', 'WOOD'],
'PIERCE': ['CLOTH', 'FLESH', 'LEATHER', 'PAPER', 'PLANT'],
'ACID': ['BONE', 'CLOTH', 'FLESH', 'IRON', 'LEATHER', 'PAPER', 'PLANT', 'SILVER', 'WOOD'],
'FIRE': ['BONE', 'CLOTH', 'FLESH', 'LEATHER', 'PAPER', 'PLANT', 'WOOD'],
'FORCE': ['AETHER'],
'COLD': ['WATER'],
'ELECTRIC': ['GOLD', 'IRON', 'SILVER'],
'NECROTIC': ['FLESH', 'PLANT', 'WOOD'],
'POISON': ['FLESH'],
'BLEED': [],
'LIGHT': [],
'DARK': [],
'SOUND': ['GLASS'],
'MIND': []
}

ResistanceTypeList = {
'ASPHYX': 'RESIST_CHOKE',
'ALLERGY': None,
'BLEED': None,
'BLUNT': 'RESIST_BLUNT',
'SLASH': 'RESIST_SLASH',
'PIERCE': 'RESIST_PIERCE',
'ACID': 'RESIST_ACID',
'FIRE': 'RESIST_FIRE',
'FORCE': None,
'COLD': 'RESIST_COLD',
'ELECTRIC': 'RESIST_SHOCK',
'NECROTIC': 'RESIST_NECRO',
'POISON': 'RESIST_POISON',
'LIGHT': 'RESIST_LIGHT',
'DARK': 'RESIST_DARK',
'SOUND': 'RESIST_SOUND',
'MIND': 'RESIST_MIND'
}

VulnerabilityTypeList = {
'ASPHYX': None,
'ALLERGY': None,
'BLEED': None,
'BLUNT': 'VULN_BLUNT',
'SLASH': 'VULN_SLASH',
'PIERCE': 'VULN_PIERCE',
'ACID': 'VULN_ACID',
'FIRE': 'VULN_FIRE',
'FORCE': None,
'COLD': 'VULN_COLD',
'ELECTRIC': 'VULN_SHOCK',
'NECROTIC': 'VULN_NECRO',
'POISON': 'VULN_POISON',
'LIGHT': 'VULN_LIGHT',
'DARK': 'VULN_DARK',
'SOUND': 'VULN_SOUND',
'MIND': 'VULN_MIND'
}

ImmunityTypeList = {
'ASPHYX': None,
'ALLERGY': None,
'BLEED': 'BLOODLESS',
'BLUNT': 'IMMUNE_PHYSICAL',
'SLASH': 'IMMUNE_PHYSICAL',
'PIERCE': 'IMMUNE_PHYSICAL',
'ACID': 'IMMUNE_ACID',
'FIRE': 'IMMUNE_FIRE',
'FORCE': None,
'COLD': 'IMMUNE_COLD',
'ELECTRIC': 'IMMUNE_SHOCK',
'NECROTIC': 'IMMUNE_NECRO',
'POISON': 'IMMUNE_POISON',
'LIGHT': 'BLIND',
'DARK': 'IMMUNE_DARK',
'SOUND': 'DEAF',
'MIND': 'IMMUNE_MIND'
}

# Items:
# ------
ItemList = [
# Weapons:
Cudgel,
Torch,
Mace,
SilverMace,
IceMace,
WarHammer,
GoldHammer,
LanternHammer,
GiantSpikedClub,
BroadAxe,
PickAxe,
BattleAxe,
Spear,
WyrdSpear,
Scythe,
QuarterStaff,
IronShodStaff,
SilverTipStaff,
LeadFillStaff,
DragonStaff,
SerpentStaff,
Knife,
VampireKnife,
RitualKnife,
Dagger,
SilverDagger,
ParryDagger,
VenomDagger,
SilverSickle,
GoldSickle,
Rapier,
GoldRapier,
ShortSword,
VorpalSword,
QuickSword,
LongSword,
Katana,
FlamingSword,
GreatSword,
FierySword,
Scimitar,
DaiKlaive,
TripleSword,
Chain,
Whip,
# Shields:
Buckler,
TurtleShield,
RoundShield,
LanternShield,
SpikedShield,
KiteShield,
IceShield,
TowerShield,
# Headgear:
Bandana,
Headband,
Hood,
Skullcap,
Coif,
Helm,
FullHelm,
GreatHelm,
Crown,
Circlet,
Halo,
Mask,
Blindfold,
# Handwear:
LeatherGlove,
BlackGlove,
Gauntlet,
Bracer,
Bracelet,
ArmGuard,
# Body armor:
LeatherArmor,
StuddedArmor,
ChainArmor,
SilverChainArmor,
ScaleArmor,
PlateArmor,
GoldPlateArmor,
BarkArmor,
CrystalShard,
CrystalPlate,
GreenTunic,
RedTunic,
LeatherTunic,
PiedTunic,
SnakeVest,
BlackRobe,
BrownRobe,
WhiteRobe,
BlueDress,
GreenDress,
GrayDress,
RedDress,
# Belts:
LeatherBelt,
BlackBelt,
Girdle,
PlateSkirt,
Baldric,
# Legwear:
Sandal,
SnakeSandal,
SaintSandal,
LowBoot,
HighBoot,
Clog,
Greave,
Anklet,
# Food:
Berry,
# Potions:
HealPotion,
MutationPotion,
StrengthPotion,
DexterityPotion,
EndurancePotion,
WitsPotion,
EgoPotion,
# Tools:
Bandage,
# Gems:
SunStone,
WyrdLight,
GoldPiece,
# Containers:
Pouch,
Sack,
HoldingBag,
Chest,
# Furniture:
Boulder,
Statue,
#Chair,
#Table,
#Bed
]

MagicEgoList = {
'WEAPON': [
           Warrior,
           Thief,
           Berserker,
           Balanced,
           Seeking,
           Glowing,
           Sun,
           Moon,
           Defense,
           Protection,
           Coward,
           Massive,
           MasterworkWeapon,
           Eldritch,
           Violence,
           EgoRegeneration,
           EgoStarpower,
           EgoVigor,
           EgoSilver,
           EgoGold
          ],
'SHIELD': [
           Warrior,
           Thief,
           Healer,
           Balanced,
           Seeking,
           Strapped,
           Glowing,
           Sun,
           Moon,
           Protection,
           Coward,
           Sturdy,
           Eldritch,
           EgoRegeneration,
           EgoStarpower,
           EgoVigor,
           Speed,
           EgoResistLight,
           EgoResistDark,
           EgoResistMind,
           EgoResistFire,
           EgoResistCold,
           EgoResistPoison,
           Peace,
           Massive,
           MasterworkWeapon,
           MasterworkArmor,
           EgoSilver,
           EgoGold
          ],
'ARMOR': [
          Warrior,
          Thief,
          Healer,
          Sage,
          Wizard,
          Berserker,
          Dancer,
          Leper,
          Courtesan,
          Apprentice,
          Fool,
          Princess,
          EgoStrength,
          EgoDexterity,
          EgoEndurance,
          EgoWits,
          EgoEgo,
          Glowing,
          Sun,
          Moon,
          Defense,
          Coward,
          Sturdy,
          Willowy,
          Unyielding,
          MasterworkArmor,
          Eldritch,
          EgoLevitation,
          EgoRegeneration,
          EgoStarpower,
          EgoVigor,
          Speed,
          Sailor,
          EgoResistLight,
          EgoResistDark,
          EgoResistMind,
          EgoResistChoke,
          EgoResistFire,
          EgoResistCold,
          EgoResistPoison,
          Thunder,
          Alchemical,
          Peace,
          Padded,
          Reinforced,
          Banded,
          EgoForest,
          Fey,
          EgoDead,
          EgoGrave,
          Summer,
          Winter,
          EgoSilver,
          EgoGold
         ],
'POTION': [],
'TOOL': [],
'VALUABLE': [
             Luminescence,
             EgoSilver,
             EgoGold
            ],
'FOOD': [],
'CONTAINER': [],
'FEATURE': []
}

# Intrinsics:
# -----------
IntrinsicList = [
# Resistances, vulnerabilities and immunities:
ResistLight,
ResistDark,
ResistMind,
ResistChoke,
ResistSound,
ResistCold,
ResistFire,
ResistAcid,
ResistSlash,
ResistBlunt,
ResistPierce,
ResistPoison,
ResistNecrotic,
ResistElectricity,
VulnLight,
VulnDark,
VulnMind,
VulnSound,
VulnCold,
VulnFire,
VulnAcid,
VulnSlash,
VulnBlunt,
VulnPierce,
VulnPoison,
VulnNecrotic,
VulnElectricity,
ImmunePhysical,
ImmuneDark,
ImmuneMind,
ImmuneCold,
ImmuneFire,
ImmuneAcid,
ImmunePoison,
ImmuneNecrotic,
ImmuneElectricity,
AllergyGold,
AllergyIron,
AllergyGlass,
AllergySilver,
AllergyHoly,
AllergyUnholy,
ResistMeat,
ResistWood,
ResistMetal,
ResistEarth,
ResistMundane,
# DoT:
Aflame,
Bleed,
Poison,
# Buffs:
BuffStrength,
BuffDexterity,
BuffEndurance,
BuffWits,
BuffEgo,
BuffDamage,
BuffLight,
Regeneration,
Starpower,
Vigor,
Haste,
Levitation,
WaterWalking,
Swimming,
CanDig,
CanChop,
# Debuffs:
DebuffStrength,
DebuffDexterity,
DebuffEndurance,
DebuffWits,
DebuffEgo,
DebuffDamage,
DebuffLight,
Slow,
Fragile,
Blindness,
Unhealing,
Manaburn,
Fatigue,
# Other:
Bloodless,
LeftHanded,
NoneIntrinsic
]

SkillList = [

]

SpellList = [

]

# Monsters:
# ---------
MobList = [
Ooze,
KoboldForager,
KoboldFisher,
KoboldHunter,
KoboldMiner,
KoboldWarrior,
KoboldWhelp,
Kea,
Kestrel,
Kiwi,
Orc,
Ogre,
Rat,
Troll,
Alien
]

# Body types:
# -----------
HumanoidList = [
Head,
Torso,
Arm,
Hand,
Arm,
Hand,
Groin,
Leg,
Leg
]

AlienList = [
TentacleArm,
TentacleArm,
TentacleArm,
AlienTorso,
TentacleLeg,
TentacleLeg,
TentacleLeg
]

AnimalList = [
Head,
AnimalTorso,
AnimalGroin,
Paw,
Paw,
Paw,
Paw
]

BirdList = [
BirdHead,
AnimalTorso,
Wing,
Wing,
AnimalGroin,
Talon,
Talon
]

SlimeList = [
SlimeTorso
]

BodyTypes = {
'HUMANOID': HumanoidList,
'ALIEN': AlienList,
'ANIMAL': AnimalList,
'BIRD': BirdList,
'SLIME': SlimeList
}

# Dungeon features:
# -----------------

DestroyedTerrainList = {
'BONE': RockFloor, # TODO: Bone floor.
'CLAY': EarthFloor,
'CLOTH': RockFloor,
'FLESH': RockFloor,
'GLASS': RockFloor,
'GOLD': GoldFloor,
'IRON': IronFloor,
'LEATHER': RockFloor,
'PAPER': RockFloor,
'PLANT': GrassFloor,
'SILVER': RockFloor,
'STONE': RockFloor,
'WATER': IceFloor,
'WOOD': WoodFloor
}

# Prefab rooms:
# -------------
RoomList = [
Alley,
Barracks1,
Barracks2,
Cage1,
Cage2,
Castle,
Checkers,
Circle1,
Circle2,
Circle3,
CrissCross,
Curved,
Diamond1,
Diamond2,
Diamond3,
Diamond4,
Diamond5,
Diamond6,
Diamond7,
Diamond8,
Foursome1,
Foursome2,
Guard1,
Guard2,
Guard3,
Guard4,
Guard5,
Leaves,
LetterS,
LetterX,
Library1,
Library2,
Magic1,
Magic2,
Pillars1,
Pillars2,
Pillars3,
Pillars4,
Pillars5,
Pillars6,
Pillars7,
Pillars8,
Pillars9a,
Pillars9b,
Pillars9c,
Pillars10,
Pillars11,
Pool1a,
Pool1b,
Pool1c,
Pool2a,
Pool2b,
Pool2c,
Pool3,
Prison,
Secret1,
Secret2,
Secret3,
Secret4,
SmallRooms1,
SmallRooms2,
SmallRooms3,
Storage1,
TJunction,
Vault1,
Vault2,
Vault3,
Vault4,
Vault5,
Whirl,
Why1,
Why2
]

SurfaceList = [
Entrance1,
Entrance2
]

GoalList = [
Goal1,
Goal2,
Goal3
]

BigRoomList = [
BigRoom1a,
BigRoom1b,
BigRoom1c,
BigRoom1d,
BigRoom1e,
BigRoom1f,
BigRoom1g,
BigRoom1h,
BigRoom2a,
BigRoom2b,
BigRoom2c,
BigRoom2d,
BigRoom2e,
BigRoom2f,
BigRoom2g,
BigRoom2h,
BigRoom3a,
BigRoom3b,
BigRoom3c,
BigRoom3d,
BigRoom3e,
BigRoom3f,
BigRoom3g,
BigRoom3h,
BigRoom4,
BigRoom5,
BigRoom6a,
BigRoom6b,
BigRoom6c,
BigRoom6d,
BigRoom6e,
BigRoom6f,
BigRoom7a,
BigRoom7b,
BigRoom7c,
BigRoom7d,
BigRoom7e,
BigRoom8,
BigRoom9,
BigRoom10a,
BigRoom10b,
BigRoom10c,
BigRoom10d,
BigRoom11a,
BigRoom11b,
BigRoom11c,
BigRoom11d,
BigRoom12a,
BigRoom12b,
BigRoom12c,
BigRoom13a,
BigRoom13b,
BigRoom13c,
BigRoom13d,
BigRoom13e,
BigRoom13f,
BigRoom13g,
BigRoom13h,
BigRoom14a,
BigRoom14b,
BigRoom14c,
BigRoom14d,
BigRoom14e,
BigRoom14f,
BigRoom14g,
BigRoom15,
BigRoom16
]
