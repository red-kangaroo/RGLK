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
'inflict': [('BLEED', 1, 3, 1, 2, 40)],
'flags': ['NATURAL']
}

Bite = {
'verb': 'bite&S',
'DiceNumber': 1,
'DiceValue': 4,
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

MaceAttack = {
'verb': 'smash&ES',
'DiceNumber': 2,
'DiceValue': 4
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

KnifeAttack = {
'verb': 'jab&S',
'DiceNumber': 1,
'DiceValue': 3,
'DamageBonus': 1,
'DamageType': 'SLASH'
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

HugeSword = {
'verb': 'slash&ES',
'DiceNumber': 2,
'DiceValue': 5,
'DamageBonus': 2,
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
'ToHitBonus': 1,
'DiceNumber': 1,
'DiceValue': 3
}

MediumShield = {
'verb': 'bash&ES',
'ToHitBonus': 1,
'DiceNumber': 2,
'DiceValue': 3
}

LargeShield = {
'verb': 'bash&ES',
'ToHitBonus': 1,
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

###############################################################################
#  Intrinsics
###############################################################################

DummyIntrinsic = {
'name': 'BUG: dummy intrinsic',
'type': None,
'secret': False,
'beginMsg': " gain&S a dummy intrinsic. Yes, seeing this is a bug.",
'endMsg': " loose&S a dummy intrinsic. Yes, seeing this is a bug.",
'color': libtcod.white
}

ResistBlunt = {
'name': 'blunt attack resistance',
'type': 'RESIST_BLUNT',
'beginMsg': " look&S tough.",
'endMsg': " look&S squishy.",
'secret': True
}

ResistSlash = {
'name': 'slashing attack resistance',
'type': 'RESIST_SLASH',
'beginMsg': " look&S hardy.",
'endMsg': " look&S feeble.",
'secret': True
}

ResistPierce = {
'name': 'piercing attack resistance',
'type': 'RESIST_PIERCE',
'beginMsg': " look&S thick-skinned.",
'endMsg': " look&S frail.",
'secret': True
}

ResistAcid = {
'name': 'acid resistance',
'type': 'RESIST_ACID',
'beginMsg': " feel&S basic.",
'endMsg': " feel&S acidic.",
'secret': True
}

ResistFire = {
'name': 'fire resistance',
'type': 'RESIST_FIRE',
'beginMsg': " feel&S a pleasant chill.",
'endMsg': " feel&S feverish.",
'secret': True
}

ResistCold = {
'name': 'cold resistance',
'type': 'RESIST_COLD',
'beginMsg': " feel&S quite warm.",
'endMsg': " feel&S an icy chill.",
'secret': True
}

ResistElectricity = {
'name': 'shock resistance',
'type': 'RESIST_SHOCK',
'beginMsg': " feel&S grounded.",
'endMsg': " feel&S electrified.",
'secret': True
}

ResistNecrotic = {
'name': 'necrotic resistance',
'type': 'RESIST_NECRO',
'beginMsg': " feel&S truly alive.",
'endMsg': " feel&S a deadly chill.",
'secret': True
}

ResistPoison = {
'name': 'poison resistance',
'type': 'RESIST_POISON',
'beginMsg': " feel&S especially healthy.",
'endMsg': " feel&S weak of stomach.",
'secret': True
}

ResistLight = {
'name': 'light resistance',
'type': 'RESIST_LIGHT',
'beginMsg': " feel&S enlightened.",
'endMsg': " feel&S a light headache.",
'secret': True
}

ResistDark = {
'name': 'darkness resistance',
'type': 'RESIST_DARK',
'beginMsg': " &ISARE no longer afraid of the dark.",
'endMsg': " hear&S something go bump.", # in the night
'secret': True
}

ResistSound = {
'name': 'sonic resistance',
'type': 'RESIST_SOUND',
'beginMsg': " &ISARE hard of hearing.",
'endMsg': " feel&S an upcoming migraine.",
'secret': True
}

VulnBlunt = {
'name': 'blunt attack vulnerability',
'type': 'VULN_BLUNT',
'beginMsg': " look&S squishy.",
'endMsg': " look&S tough.",
'secret': True
}

VulnSlash = {
'name': 'slashing attack vulnerability',
'type': 'VULN_SLASH',
'beginMsg': " look&S feeble.",
'endMsg': " look&S hardy.",
'secret': True
}

VulnPierce = {
'name': 'piercing attack vulnerability',
'type': 'VULN_PIERCE',
'beginMsg': " look&S frail.",
'endMsg': " look&S thick-skinned.",
'secret': True
}

VulnAcid = {
'name': 'acid vulnerability',
'type': 'VULN_ACID',
'beginMsg': " feel&S very acidic.",
'endMsg': " feel&S much less acidic.",
'secret': True
}

VulnFire = {
'name': 'fire vulnerability',
'type': 'VULN_FIRE',
'beginMsg': " feel&S too hot.",
'endMsg': " cool&S down a bit.",
'secret': True
}

VulnCold = {
'name': 'cold vulnerability',
'type': 'VULN_COLD',
'beginMsg': " shiver&S.",
'endMsg': " warm&S up a bit.",
'secret': True
}

VulnElectricity = {
'name': 'shock vulnerability',
'type': 'VULN_SHOCK',
'beginMsg': " feel&S currently amplified.",
'endMsg': " feel&S insulated.",
'secret': True
}

VulnNecrotic = {
'name': 'necrotic vulnerability',
'type': 'VULN_NECRO',
'beginMsg': " feel&S a deadly chill.",
'endMsg': " feel&S truly alive.",
'secret': True
}

VulnPoison = {
'name': 'poison vulnerability',
'type': 'VULN_POISON',
'beginMsg': " feel&S somewhat sickly.",
'endMsg': " feel&S rather healthy.",
'secret': True
}

VulnLight = {
'name': 'light vulnerability',
'type': 'VULN_LIGHT',
'beginMsg': " feel&S a light headache.",
'endMsg': " want&S to be in the dark no longer.",
'secret': True
}

VulnDark = {
'name': 'darkness vulnerability',
'type': 'VULN_DARK',
'beginMsg': " fear&S the shadows.",
'endMsg': " feel&S goth.",
'secret': True
}

VulnSound = {
'name': 'sonic vulnerability',
'type': 'VULN_SOUND',
'beginMsg': " feel&S an upcoming migraine.",
'endMsg': " &ISARE hard of hearing.",
'secret': True
}

ImmunePhysical = {
'name': 'physical immunity',
'type': 'IMMUNE_PHYSICAL',
'beginMsg': " feel&S rock-hard.",
'endMsg': " feel&S soft.",
'secret': True
}

ImmuneAcid = {
'name': 'acid immunity',
'type': 'IMMUNE_ACID',
'beginMsg': " feel&S very basic.",
'endMsg': " feel&S acidic.",
'secret': True
}

ImmuneFire = {
'name': 'fire immunity',
'type': 'IMMUNE_FIRE',
'beginMsg': " feel&S very cool!",
'endMsg': " feel&S feverish.",
'secret': True
}

ImmuneCold = {
'name': 'cold immunity',
'type': 'IMMUNE_COLD',
'beginMsg': " feel&S smoking hot.",
'endMsg': " feel&S an icy chill.",
'secret': True
}

ImmuneElectricity = {
'name': 'shock immunity',
'type': 'IMMUNE_SHOCK',
'beginMsg': " feel&S insulated.",
'endMsg': " feel&S electrified.",
'secret': True
}

ImmuneNecrotic = {
'name': 'necrotic immunity',
'type': 'IMMUNE_NECRO',
'beginMsg': " feel&S truly alive.",
'endMsg': " feel&S a deadly chill.",
'secret': True
}

ImmunePoison = {
'name': 'poison immunity',
'type': 'IMMUNE_POISON',
'beginMsg': " feel&S especially healthy.",
'endMsg': " feel&S weak of stomach.",
'secret': True
}

ImmuneDark = {
'name': 'darkness immunity',
'type': 'IMMUNE_DARK',
'beginMsg': " feel&S the darkness rising.",
'endMsg': " feel&S the darkness subside.",
'secret': True
}

Aflame = {
'name': 'aflame',
'type': 'AFLAME',
'beginMsg': " catch&ES aflame!",
'endMsg': " no longer burn&S.",
'secret': False,
'color': libtcod.red
}

Bleed = {
'name': 'bleeding',
'type': 'BLEED',
'beginMsg': " bleed&S profusely!",
'endMsg': " no longer bleed&S.",
'secret': False,
'color': libtcod.red
}

Poison = {
'name': 'poisoned',
'type': 'POISON',
'beginMsg': " &ISARE posioned.",
'endMsg': " feel&S better.",
'secret': False,
'color': libtcod.green
}

Regeneration = {
'name': 'regeneration',
'type': 'REGEN_LIFE',
'beginMsg': " can see &POSS bruises fading quickly.",
'endMsg': " feel&S unwell.",
'secret': True
}

Starpower = {
'name': 'starpower',
'type': 'REGEN_MANA',
'beginMsg': " feel&S the stars watching.",
'endMsg': " feel&S down.",
'secret': True
}

Vigor = {
'name': 'vigor',
'type': 'REGEN_STAM',
'beginMsg': " feel&S invigorated.",
'endMsg': " feel&S fatigued.",
'secret': True
}

Unhealing = {
'name': 'unhealing',
'type': 'DRAIN_LIFE',
'beginMsg': " can feel all &POSS old pains.",
'endMsg': " feel&S better.",
'secret': True
}

Manaburn = {
'name': 'manaburn',
'type': 'DRAIN_MANA',
'beginMsg': " can smell the aether burning in &POSS veins.",
'endMsg': " feel&S energized.",
'secret': True
}

Fatigue = {
'name': 'fatigue',
'type': 'DRAIN_STAM',
'beginMsg': " feel&S fatigued.",
'endMsg': " feel&S refreshed.",
'secret': True
}

Haste = {
'name': 'hasted',
'type': 'HASTE',
'beginMsg': " &ISARE moving faster.",
'endMsg': " slow&S down.",
'secret': False
}

Slow = {
'name': 'slowed',
'type': 'SLOW',
'beginMsg': " &ISARE moving slowly.",
'endMsg': " speed&S up.",
'secret': False
}

Blindness = {
'name': 'blind',
'type': 'BLIND',
'beginMsg': " cannot see!",
'endMsg': " can see again.",
'secret': False,
'color': libtcod.grey
}

LeftHanded = {
'name': 'left-handed',
'type': 'LEFT_HANDED',
'beginMsg': " feel&S sinister.",
'endMsg': " feel&S right.",
'secret': True
}

Bloodless = {
'name': 'bloodless',
'type': 'BLOODLESS',
'beginMsg': " feel&S exsanguinated.",
'endMsg': " listen&S to &POSS heart.",
'secret': True
}

Fragile = {
'name': 'fragile',
'type': 'FRAGILE',
'beginMsg': " feel&S very fragile.",
'endMsg': " toughen&S up.",
'secret': True
}

CanDig = {
'name': 'tunnelling',
'type': 'CAN_DIG',
'beginMsg': " feel&S like some mining.",
'endMsg': " feel&S lazy.",
'secret': True
}

CanChop = {
'name': 'woodchopping',
'type': 'CAN_CHOP',
'beginMsg': " feel&S like some woodcutting.",
'endMsg': " feel&S lazy.",
'secret': True
}

NoneIntrinsic = {
'name': 'none intrinsic',
'type': None,
'beginMsg': " feel&S nothing at all.",
'endMsg': " feel&S even less than nothing.",
'secret': False
}

###############################################################################
#  Items
###############################################################################

# Must be defined before monsters to allow for generating inventories.

DummyItem = {
'char': '?',
'color': libtcod.white,
'name': 'BUG: dummy item',
'BlockMove': False,
'material': 'STONE',
'size': 0,
'attack': NonWeapon,
'ranged': MisThrown,
'accuracy': 0,             # This is not normal to hit, but a general bonus.
'light': 0,
'StrScaling': 'F',
'DexScaling': 'F',
'DV': 0,
'PV': 0,
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

LanternHammer = { # In my language, 'lucerna' means lantern, so this is a play on
'char': '\\',     # the good old D&D 'lucerne hammer'. ;)
'color': libtcod.amber,
'name': 'lantern hammer',
'material': 'IRON',
'size': 2,
'light': 2,
'StrScaling': 'A',
'DexScaling': 'D',
'attack': Hammer,
'flags': ['MELEE', 'WEAPON'],
'frequency': 100
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
'frequency': 50
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
'frequency': 150
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
'frequency': 250
}

QuarterStaff = {
'char': '|',
'color': libtcod.darkest_orange,
'name': 'quarterstaff',
'material': 'WOOD',
'size': 1,
'DV': 1,
'StrScaling': 'B',
'DexScaling': 'B',
'attack': WoodStaff,
'flags': ['MELEE', 'WEAPON', 'ENCHANT_DODGE'],
'frequency': 150
}

IronShodStaff = {
'char': '|',
'color': libtcod.silver,
'name': 'iron-shod staff',
'material': 'IRON',
'size': 1,
'StrScaling': 'C', # TODO: ???
'DexScaling': 'C',
'attack': IronStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 150
}

SilverTipStaff = {
'char': '|',
'color': libtcod.white,
'name': 'silver-tipped staff',
'material': 'SILVER',
'size': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': IronStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 100
}

LeadFillStaff = {
'char': '|',
'color': libtcod.dark_grey,
'name': 'lead-filled staff',
'material': 'WOOD',
'size': 1,
'StrScaling': 'C',
'DexScaling': 'C',
'attack': LeadStaff,
'flags': ['MELEE', 'WEAPON'],
'frequency': 100
}

Knife = {
'char': ')',
'color': libtcod.dark_grey,
'name': 'knife',
'material': 'IRON',
'size': -2,
'StrScaling': 'C',
'DexScaling': 'A',
'attack': KnifeAttack,
'ranged': KnifeThrown,
'flags': ['MELEE', 'WEAPON']
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
'frequency': 100
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
'frequency': 100
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
'frequency': 100
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
'frequency': 500
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
'frequency': 250
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
'frequency': 150
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
'frequency': 150
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
'frequency': 300
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
'frequency': 250
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
'frequency': 250
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
'frequency': 400
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
'frequency': 150
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
'frequency': 150
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
'flags': ['SHIELD'],
'frequency': 700
}

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
'frequency': 250
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
'frequency': 100
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
'frequency': 100
}

Skullcap = {
'char': '-',
'color': libtcod.darker_orange,
'name': 'skullcap',
'material': 'LEATHER',
'PV': 1,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 750
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
'frequency': 250
}

Helm = {
'char': '-',
'color': libtcod.silver,
'name': 'helmet',
'material': 'IRON',
'PV': 2,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 400
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
'frequency': 750
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
'frequency': 500
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
'frequency': 100
}

Mask = {
'char': '-',
'color': libtcod.darkest_orange,
'name': 'mask',
'material': 'WOOD',
'PV': 0,
'DV': 0,
'size': -2,
'flags': ['HEAD', 'ARMOR'],
'frequency': 300
}

# horned helmet
# gladiator helmet
# plumed helmet
# fedora
# witch hat
# wizard hat

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
'frequency': 600
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
'frequency': 200
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

CrystalShard = {
'char': ']',
'color': libtcod.cyan,
'name': 'crystal shard mail',
'material': 'GLASS',
'size': 0,
'DV': -4,
'PV': 8,
'flags': ['TORSO', 'ARMOR'],
'frequency': 50
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
'frequency': 50
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
'accuracy': 2,
'flags': ['TORSO', 'ARMOR'],
'frequency': 300
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
'frequency': 200
}

SnakeVest = {
'char': ']',
'color': libtcod.desaturated_green,
'name': 'snakeskin vest',
'material': 'LEATHER',
'size': 0,
'accuracy': 1,
'flags': ['TORSO', 'ARMOR', 'ENCHANT_ACCURACY'],
'frequency': 250
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
'frequency': 200
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
'frequency': 200
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
'frequency': 200
}

BlueDress = {
'char': ']',
'color': libtcod.blue,
'name': 'blue dress',
'material': 'CLOTH',
'size': -1,
'DV': 0,
'PV': 0,
'intrinsics': [('HASTE', 1)],
'flags': ['TORSO', 'ARMOR'],
'frequency': 100
}

# zombie hide armor
# troll hide armor
# mithril chain mail
# dragon scale mail
# gold plate mail
# fur cloak
# cloak of invisibility

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
'frequency': 600
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
'frequency': 700
}

# belt of levitation

# Legwear:
Sandal = {
'char': '(',
'color': libtcod.darker_orange,
'name': 'sandal',
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
'frequency': 100
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
'frequency': 400
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
'frequency': 800
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
'frequency': 200
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
'coolness': 20, # TODO
'frequency': 300
}

MutationPotion = {
'char': '!',
'color': libtcod.green,
'name': 'vial of mutagen',
'material': 'WATER',
'size': -2,
'ranged': MisThrown, # TODO: Splash.
'flags': ['POTION', 'MUTATION'],
'coolness': 0,
'frequency': 50
}

# Tools:
Bandage = {
'char': '{',
'color': libtcod.white,
'name': 'bandage',
'material': 'CLOTH',
'size': -2,
'flags': ['APPLY', 'BANDAGE'],
'coolness': 10,
'frequency': 500
}

# General:
GoldPiece = {
'char': '$',
'color': libtcod.yellow,
'name': 'gold nugget',
'material': 'GOLD',
'size': -2,
'frequency': 50
}

SunStone = {
'char': '*',
'color': libtcod.yellow,
'name': 'sunstone',
'material': 'STONE',
'light': 3,
'size': -2,
'flags': ['ENCHANT_LIGHT', 'CARRY_LIGHT'],
'frequency': 50
}

Berry = {
'char': chr(236),
'color': libtcod.blue,
'name': 'berry',
'material': 'PLANT',
'size': -2,
'flags': ['FOOD'],
'frequency': 300
}

MacGuffin = {
'char': chr(12),
'color': libtcod.yellow,
'name': 'amulet of Yendor',
'material': 'GOLD',
'size': -2,
'flags': ['MAC_GUFFIN', 'ALWAYS_BLESSED', 'ENCHANT_LIGHT'],
'frequency': 0
}

# Furniture, containers and similar:
Boulder = {
'char': '0',
'color': libtcod.dark_grey,
'name': 'boulder',
'BlockMove': True,
'size': 2,
'DV': -10,
'attack': BoulderRoll,
'flags': ['FEATURE'], # TODO: Block sight.
'frequency': 50
}

Chest = {
'char': chr(127),
'color': libtcod.darker_orange,
'name': 'chest',
'material': 'WOOD',
'size': 1,
'DV': -10,
'flags': ['FEATURE', 'CONTAINER', 'CAN_BE_OPENED'],
'frequency': 100
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
'Str': 2,
'Dex': 2,
'End': 2,
'Wit': 0,
'Ego': 0,
'speed': 1.0,
'sight': 0,
'sex': 'MOF',
'intrinsics': [],
'inventory': [ShortSword, RoundShield, LeatherArmor, HealPotion, SunStone],
'flags': ['HUMANOID', 'AVATAR', 'UNDEAD'], # TODO
'frequency': 0
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
'flags': ['HUMANOID', 'AI_SCAVENGER'],
'mutations': ['MUTATION_CLAWS'],
'frequency': 600
}

KoboldHunter = {
'char': 'k',
'color': libtcod.darker_orange,
'name': 'kobold hunter',
'Str': 1,
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
'frequency': 600
}

KoboldFisher = {
'char': 'k',
'color': libtcod.blue,
'name': 'kobold fisher',
'Str': 0,
'Dex': 3,
'End': -2,
'Wit': 1,
'Ego': 0,
'speed': 1,
'sight': 5,
'size': -1,
'sex': 'MOF',
'inventory': [Spear],
'flags': ['HUMANOID'],
'mutations': ['MUTATION_CLAWS'],
'frequency': 600
}

KoboldMiner = {
'char': 'k',
'color': libtcod.dark_grey,
'name': 'kobold miner',
'Str': 1,
'Dex': 2,
'End': -2,
'Wit': 1,
'Ego': 0,
'speed': 1,
'sight': 5,
'size': -1,
'sex': 'MOF',
'inventory': [PickAxe],
'flags': ['HUMANOID'],
'mutations': ['MUTATION_CLAWS'],
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
'inventory': [LongSword, KiteShield, LeatherArmor, LowBoot, LowBoot],
'flags': ['HUMANOID']
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
'frequency': 200
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
'flags': ['ALIEN', 'USE_LEGS', 'AI_DIJKSTRA'],
'frequency': 5
}

BlackKnight = {
'char': 'K',
'color': libtcod.darkest_grey,
'name': 'black knight',
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
'inventory': [FlamingSword, IceShield, FullHelm, Gauntlet, Gauntlet, PlateArmor,
              PlateSkirt, Greave, Greave, MacGuffin],
'mutations': ['RANDOM_ANY'],
'flags': ['HUMANOID', 'USE_LEGS'],
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
'StrScaling': 'C', # No, had is not really that good for attacking.
'DexScaling': 'C',
'attack': Bite,
'flags': ['HEAD', 'VITAL']
}

Torso = {
'name': 'torso',
'flags': ['TORSO', 'VITAL', 'CANNOT_SEVER']
}

SlimeTorso = {
'name': 'blob',
'eyes': 1,
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
'flags': ['DOOR']
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

Vines = {
'char': '|',
'color': libtcod.dark_green,
'name': 'hanging vines',
'material': 'PLANT',
'BlockMove': False,
'BlockSight': True,
'flags': ['GROUND', 'CAN_BE_BURNED', 'PLANT']
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
RockPile = {
'char': '*',
'color': libtcod.darker_grey,
'name': 'rock pile',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_KICKED']
}

BonePile = {
'char': '*',
'color': libtcod.white,
'name': 'bone pile',
'material': 'BONE',
'BlockMove': False,
'BlockSight': False,
'flags': ['GROUND', 'CAN_BE_KICKED']
}

Grave = {
'char': chr(241), # Ie. ±
'color': libtcod.white,
'name': 'gravestone',
'BlockMove': False,
'BlockSight': False,
'flags': ['CAN_BE_KICKED']
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

BookShelf = {
'char': chr(252),
'color': libtcod.darker_orange,
'name': 'bookshelf',
'material': 'WOOD',
'BlockMove': True,
'BlockSight': True,
'flags': ['FEATURE', 'CONTAINER', 'CAN_BE_OPENED', 'CAN_BE_CHOPPED', 'CAN_BE_BURNED']
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
'frequency': 15,
' ': (RockWall, None, None, None),
'#': (RockWall, None, None, None),
'.': (RockFloor, None, None, None),
'+': (WoodDoor, None, None, None),
'S': (SecretDoor, None, None, None),
'x': (WoodDoor, ['BLOCKED'], None, None),
'$': (RockFloor, None, GoldPiece, None)
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
'height': 9
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
Library = {
'file': 'rooms/library',
'width': 7,
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
'width': 7,
'height': 7,
'~': (DeepWater, None, None, None)
}

Pool2b = {
'file': 'rooms/pool2',
'width': 7,
'height': 7,
'~': (Lava, None, None, None)
}

Pool2c = {
'file': 'rooms/pool2',
'width': 7,
'height': 7,
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
'width': 4,
'height': 4
}

Circle2 = {
'file': 'rooms/circle2',
'width': 5,
'height': 5
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
')': (RockFloor, None, 'RANDOM_ANY', None)
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

DamageTypeList = [
'BLUNT',
'SLASH',
'PIERCE',
'ACID',
'FIRE',
'COLD',
'ELECTRIC',
'NECROTIC',
'POISON',
'BLEED',
'LIGHT',
'DARK',
'SOUND'
]

NonWoundingList = [
'NECROTIC',
'POISON',
'BLEED',
'DARK'
]

ResistanceTypeList = {
'BLEED': None,
'BLUNT': 'RESIST_BLUNT',
'SLASH': 'RESIST_SLASH',
'PIERCE': 'RESIST_PIERCE',
'ACID': 'RESIST_ACID',
'FIRE': 'RESIST_FIRE',
'COLD': 'RESIST_COLD',
'ELECTRIC': 'RESIST_SHOCK',
'NECROTIC': 'RESIST_NECRO',
'POISON': 'RESIST_POISON',
'LIGHT': 'RESIST_LIGHT',
'DARK': 'RESIST_DARK',
'SOUND': 'RESIST_SOUND'
}

VulnerabilityTypeList = {
'BLEED': None,
'BLUNT': 'VULN_BLUNT',
'SLASH': 'VULN_SLASH',
'PIERCE': 'VULN_PIERCE',
'ACID': 'VULN_ACID',
'FIRE': 'VULN_FIRE',
'COLD': 'VULN_COLD',
'ELECTRIC': 'VULN_SHOCK',
'NECROTIC': 'VULN_NECRO',
'POISON': 'VULN_POISON',
'LIGHT': 'VULN_LIGHT',
'DARK': 'VULN_DARK',
'SOUND': 'VULN_SOUND'
}

ImmunityTypeList = {
'BLEED': 'BLOODLESS',
'BLUNT': 'IMMUNE_PHYSICAL',
'SLASH': 'IMMUNE_PHYSICAL',
'PIERCE': 'IMMUNE_PHYSICAL',
'ACID': 'IMMUNE_ACID',
'FIRE': 'IMMUNE_FIRE',
'COLD': 'IMMUNE_COLD',
'ELECTRIC': 'IMMUNE_SHOCK',
'NECROTIC': 'IMMUNE_NECRO',
'POISON': 'IMMUNE_POISON',
'LIGHT': 'BLIND',
'DARK': 'IMMUNE_DARK',
'SOUND': 'DEAF'
}

# Items:
# ------
ItemList = [
# Weapons:
Cudgel,
Mace,
WarHammer,
LanternHammer,
GiantSpikedClub,
BroadAxe,
PickAxe,
BattleAxe,
Spear,
Scythe,
QuarterStaff,
IronShodStaff,
SilverTipStaff,
LeadFillStaff,
Knife,
Dagger,
VenomDagger,
SilverSickle,
GoldSickle,
Rapier,
GoldRapier,
ShortSword,
VorpalSword,
LongSword,
FlamingSword,
GreatSword,
Scimitar,
Chain,
Whip,
# Shields:
Buckler,
RoundShield,
LanternShield,
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
ScaleArmor,
PlateArmor,
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
# Belts:
LeatherBelt,
BlackBelt,
Girdle,
PlateSkirt,
Baldric,
# Legwear:
Sandal,
SnakeSandal,
LowBoot,
HighBoot,
Clog,
Greave,
Anklet,
# Potions:
HealPotion,
MutationPotion,
# Tools:
Bandage,
# Other:
GoldPiece,
SunStone,
Berry,
Boulder,
Chest,
#Chair,
#Table,
#Bed
]

# Intrinsics:
# -----------
IntrinsicList = [
# Resistances, vulnerabilities and immunities:
ResistLight,
ResistDark,
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
ImmuneCold,
ImmuneFire,
ImmuneAcid,
ImmunePoison,
ImmuneNecrotic,
ImmuneElectricity,
# DoT:
Aflame,
Bleed,
Poison,
# Buffs:
Regeneration,
Starpower,
Vigor,
Haste,
CanDig,
CanChop,
# Debuffs:
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
KoboldForager,
KoboldFisher,
KoboldHunter,
KoboldMiner,
KoboldWarrior,
KoboldWhelp,
Orc,
Ogre,
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
Head,
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
LetterS,
LetterX,
Library,
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
TJunction,
Whirl,
Why1,
Why2
]
