# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

import ai
import dungeon
import game
import raw
import ui
import var

###############################################################################
#  Functions
###############################################################################

def spawn(x, y, BluePrint, type):
    # Requires at least a colored character with a name.
    try:
        char = BluePrint['char']
        color = BluePrint['color']
        name = BluePrint['name']
    except:
        print "Failed to spawn an entity."
        return False

    if type == 'MOB':
        try:
            material = BluePrint['material']
        except:
            material = raw.DummyMonster['material']
        try:
            size = BluePrint['size']
        except:
            size = raw.DummyMonster['size']
        try:
            Str = BluePrint['Str']
        except:
            Str = raw.DummyMonster['Str']
        try:
            Dex = BluePrint['Dex']
        except:
            Dex = raw.DummyMonster['Dex']
        try:
            End = BluePrint['End']
        except:
            End = raw.DummyMonster['End']
        try:
            Wit = BluePrint['Wit']
        except:
            Wit = raw.DummyMonster['Wit']
        try:
            Ego = BluePrint['Ego']
        except:
            Ego = raw.DummyMonster['Ego']
        try:
            speed = BluePrint['speed']
        except:
            speed = raw.DummyMonster['speed']
        try:
            sight = BluePrint['sight']
        except:
            sight = raw.DummyMonster['sight']
        try:
            sex = BluePrint['sex']
        except:
            sex = raw.DummyMonster['sex']
        try:
            diet = BluePrint['diet']
        except:
            diet = raw.DummyMonster['diet']
        try:
            addFlags = BluePrint['flags']
        except:
            addFlags = []
        try:
            addIntrinsics = BluePrint['intrinsics']
        except:
            addIntrinsics = []

        New = Mob(x, y, char, color, name, material, size,
                     Str, Dex, End, Wit, Ego, sex, speed, sight, addFlags)

        New.diet = diet
    elif type == 'ITEM':
        #try:
        #    attack = BluePrint['something']
        #except:
        #    attack = raw.DummyItem['something']
        try:
            material = BluePrint['material']
        except:
            material = raw.DummyItem['material']
        try:
            size = BluePrint['size']
        except:
            size = raw.DummyItem['size']
        try:
            attack = BluePrint['attack']
        except:
            attack = raw.DummyItem['attack']
        try:
            ranged = BluePrint['ranged']
        except:
            ranged = raw.DummyItem['ranged']
        try:
            DV = BluePrint['DV']
        except:
            DV = raw.DummyItem['DV']
        try:
            PV = BluePrint['PV']
        except:
            PV = raw.DummyItem['PV']
        try:
            BlockMove = BluePrint['BlockMove']
        except:
            BlockMove = raw.DummyItem['BlockMove']
        try:
            addFlags = BluePrint['flags']
        except:
            addFlags = []
        try:
            addIntrinsics = BluePrint['intrinsics']
        except:
            addIntrinsics = []

        New = Item(x, y, char, color, name, material, size, BlockMove,
                   attack, ranged, DV, PV, addFlags)
    else:
        print "Failed to spawn unknown entity type."

    try:
        New.intrinsics.append(addIntrinsics)
    except:
        print "Failed to spawn with intrinsics."

    return New

###############################################################################
#  Entities
###############################################################################

# Player, monsters...
class Entity(object):
    def __init__(self, x, y, char, color, name, material, size, BlockMove = False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.material = material
        self.size = size
        self.BlockMove = BlockMove

        self.AP = 0.0 # Start with 0 turns to take.
        self.attack = raw.Slam
        self.ranged = raw.MisThrown
        self.beautitude = 0 # Negative for cursed/doomed, positive for blessed/holy.
        self.enchantment = 0

        self.flags = []
        self.inventory = [] # For both mobs and containers.
        self.intrinsics = []

        # Mobs for pathfinding and items/features for liking may have either goal
        # (an [x, y] list) or a target (any entity, ie. mob or item).
        self.goal = None
        self.target = None

    def move(self, dx, dy):
        if (self.x + dx < 0 or self.x + dx > var.MapWidth - 1 or
            self.y + dy < 0 or self.y + dy > var.MapHeight - 1):
            return

        self.x += dx
        self.y += dy

    def draw(self):
        # Set color and draw character on screen.
        if (libtcod.map_is_in_fov(var.FOVMap, self.x, self.y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.MapConsole, self.getColor())
            libtcod.console_put_char(var.MapConsole, self.x, self.y, self.char, libtcod.BKGND_SCREEN)
            self.flags.append('SEEN')

    def range(self, Other): # Range between to entities.
        dx = Other.x - self.x
        dy = Other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y): # Distance between self and map square.
        dx = x - self.x
        dy = y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def isBlocked(self, x, y, DL):
        if (x < 0 or x > var.MapWidth - 1 or
            y < 0 or y > var.MapHeight - 1):
            return True

        if var.Maps[DL][x][y].BlockMove:
            return True

        for i in var.Entities[DL]:
            if (i.BlockMove and i.x == x and i.y == y):
                return True

        return False

    def hasFlag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False

    def hasIntrinsic(self, intrinsic):
        pass

    def getName(self, capitalize = False, full = False):
        name = self.name

        if capitalize == True:
            name = name.capitalize()

        return name

    def getColor(self):
        return self.color

    def getDefenseValue(self):
        return 0

    def getProtectionValue(self):
        return 0

    # Heartbeat of all entities.
    def Be(self):
        # How else to check if entity has a speed variable?
        if self.hasFlag('MOB'):
            if self.checkDeath() == False:
                self.regainActions()
                self.regainHealth()
                self.regainMana()
                self.regainStamina()
        else:
            self.AP += 1
        # TODO: Check terrain for special effects.
        # TODO: Intrinsics and status effects.
        # TODO: Call Be() for inventory items from here, because they will not go
        #       through the main loop of var.Entities

class Mob(Entity):
    def __init__(self, x, y, char, color, name, material, size, #These are base Entity arguments.
                 Str, Dex, End, Wit, Ego, sex, speed = 1.0, FOVRadius = 6, addFlags = []):
        BlockMove = True # All mobs block movement, but not all entities,
                         # so pass this to Entity __init__
        super(Mob, self).__init__(x, y, char, color, name, material, size, BlockMove)

        # Attributes:
        self.Str = Str
        self.Dex = Dex
        self.End = End
        self.Wit = Wit
        self.Ego = Ego
        self.speed = speed

        # Sex:
        if sex == 'MOF':
            if var.rand_chance(50):
                self.sex = 'MALE'
            else:
                self.sex = 'FEMALE'
        else:
            self.sex = sex

        # FOV:
        self.FOVRadius = FOVRadius # TODO: This should depend on stats and equipment.
        self.recalculateFOV()

        # Calculate stats:
        self.bonusHP = 0
        self.bonusMP = 0
        self.maxHP = self.recalculateHealth()
        self.HP = self.maxHP
        self.maxMP = self.recalculateMana()
        self.MP = self.maxMP
        self.maxSP = self.recalculateStamina()
        self.SP = self.maxSP
        # TODO: NP, pain, heat
        self.XL = 1
        self.XP = 0

        # General:
        self.carry = self.recalculateCarryingCapacity() # Burdened if len(inventory) == self.carry.
        self.givenName = None
        self.tactics = True # True is defensive, False aggresive.

        self.flags.append('MOB')
        for i in addFlags:
            self.flags.append(i)

        self.baseArms = 0
        self.baseLegs = 0
        self.baseWings = 0
        self.baseEyes = 0

        self.bodyparts = []
        self.gainBody()
        self.gainMutation()

    def gainBody(self):
        body = None
        for i in self.flags:
            if i in raw.BodyTypes.keys():
                body = i
                break

        if body != None:
            BodyParts = raw.BodyTypes[body]
        else:
            return # No body parts. This will kill us next heartbeat.

        for part in BodyParts:
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
                addFlags = part['flags']
            except:
                addFlags = raw.DummyPart['flags']
            try:
                material = part['material']
            except:
                material = None

            New = BodyPart(name, self, cover, place, size, eyes, attack, addFlags,
                           material)

            self.bodyparts.append(New)

        armNo = 0
        legNo = 0
        wingNo = 0
        eyeNo = 0

        for part in self.bodyparts:
            eyeNo += part.eyes

            if part.hasFlag('ARM'):
                if armNo == 0:
                    part.flags.append('RIGHT')
                    part.flags.append('MAIN') # TODO: Left-handedness.
                    armNo += 1
                elif armNo == 1:
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
                if legNo == 0:
                    part.flags.append('RIGHT')
                    wingNo += 1
                elif legNo == 1:
                    part.flags.append('LEFT')
                    wingNo += 1
                else:
                    part.flags.append('OTHER')
                    wingNo += 1

        self.baseArms = armNo
        self.baseLegs = legNo
        self.baseWings = wingNo
        self.baseEyes = eyeNo

    def gainMutation(self):
        # TODO
        for i in self.flags:
            if i in raw.MutationTypes:
                if i == 'MUTATION_CLAWS':
                    for part in self.bodyparts:
                        if part.hasFlag('ARM'):
                            part.attack = raw.Claw
                elif i == 'MUTATION_LARGE_CLAWS':
                    for part in self.bodyparts:
                        if part.hasFlag('ARM'):
                            part.attack = raw.LargeClaw

    def recalculateFOV(self):
        libtcod.map_compute_fov(var.FOVMap, self.x, self.y, self.FOVRadius, True, 0)

    def recalculateCarryingCapacity(self):
        return max(1, 10 + (2 * self.Str))

    def recalculateHealth(self):
        return max(1, ((20 * (1.2 ** self.End)) + self.bonusHP))

    def recalculateMana(self):
        return max(0, ((20 * (1.2 ** self.Ego)) + self.bonusMP))

    def recalculateStamina(self):
        return max(1, (20 * (1.2 ** self.Str)))

    def regainHealth(self):
        if not self.hasFlag('DEAD') and self.HP < self.maxHP:
            self.HP += 0.2

        # TODO:
        #  Regeneration
        #  Full / Stuffed
        #  Unhealing

        if self.HP > self.maxHP:
            self.HP = self.maxHP

    def regainMana(self):
        if not self.hasFlag('DEAD') and self.MP < self.maxMP:
            self.MP += 0.3

        # TODO:
        #  Starpower
        #  Manaburn

        if self.MP > self.maxMP:
            self.MP = self.maxMP

    def regainStamina(self):
        if not self.hasFlag('DEAD') and self.SP < self.maxSP:
            self.SP += 0.5

        # TODO:
        #  Vigor
        #  Fatigue

        if self.SP > self.maxSP:
            self.SP = self.maxSP

    def regainActions(self):
        # This works even when dead, because items can have actions, too.
        self.AP += self.speed

        # Energy randomization:
        if var.rand_chance(5):
            self.AP += 0.1
        elif var.rand_chance(5):
            self.AP -= 0.1

    def getAccuracyBonus(self, weapon = None, base = False):
        toHit = self.Dex # TODO: Scaling

        if self.tactics == False:
            toHit += 1

        if weapon != None:
            try:
                toHit += weapon.getAccuracyValue()
            except:
                pass # Body parts have no accuracy bonus.

        mod = random.random() # Between 0.0 and 1.0, so can be used as a % modifier.

        if base == True:
            return toHit
        else:
            return (toHit * mod)

    def getDamageBonus(self, victim = None, weapon = None):
        bonus = 0
        # TODO: Intrinsics.

        # Size difference:
        if victim != None:
            bonus += self.size - victim.size

        # Enchantment:
        if weapon != None:
            bonus += weapon.enchantment

        mod = random.random() # Between 0.0 and 1.0, so can be used as a % modifier.

        return (bonus * mod)

    def getDodgeBonus(self, attacker = None, weapon = None, base = False):
        # TODO:
        # Bonus after move.
        # Unarmored / Light Armor

        toDodge = self.Dex

        if self.tactics:
            toDodge += 1

        # Get equipment bonus:
        for part in self.bodyparts:
            for item in part.inventory:
                slot = part.getSlot()

                if slot != None:
                    if slot == 'GRASP':
                        if item.hasFlag('WEAPON') or item.hasFlag('SHIELD'): # Wielded armor gives no
                            toDodge += item.getDefenseValue()                # bonuses.
                        elif item.getDefenseValue() < 0:      # This makes wielding huge, heavy misc
                            toDodge += item.getDefenseValue() # items with DV penalties a bad idea.
                    elif item.hasFlag(slot):
                        toDodge += item.getDefenseValue()

        if base == True:
            return toDodge

        # Modify by number of adjacent walls:
        AdjacentWalls = 0
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if x in range(0, var.MapWidth) and y in range(0, var.MapHeight):
                    #if x != self.x and y != self.y:
                    if var.Maps[var.DungeonLevel][x][y].BlockMove == True:
                        AdjacentWalls += 1
                else:
                    AdjacentWalls += 1
                # We get a modifier between +2 and -2, based on how many walls are adjacent.
        wallMod = 2 - int(math.floor(AdjacentWalls / 2))
        toDodge += wallMod

        # Modify by size difference:
        if weapon != None and not weapon.hasFlag('BODY_PART'):
            if weapon.size > self.size:
                toDodge += abs(self.size - weapon.size)
        elif attacker != None:
            if attacker.size > self.size:
                toDodge += abs(self.size - attacker.size)

        mod = random.random() # Between 0.0 and 1.0, so can be used as a % modifier.

        return (toDodge * mod)

    def getLimbToHit(self, attacker):
        # TODO: Maybe armor?
        choices = []

        for part in self.bodyparts:
            chance = part.cover * (1.2 ** -abs(attacker.size - part.size))
            print "part chance: %s" % chance

            if var.rand_chance(chance):
                choices.append(part)

        if len(choices) == 0:
            for part in self.bodyparts:
                if part.hasFlag('TORSO'):
                    choices.append(part)

        return random.choice(choices)

    def tryBlocking(self, attacker, weapon, toHit, damage, forcedHit):
        # Non-physical damage should not get into this method.

        # Find what to block with:
        choices = []
        for part in self.bodyparts:
            if part.hasFlag('GRASP'):
                for item in part.inventory:
                    if item.hasFlag('SHIELD') or self.tactics:
                        choices.append(item)
        # We block with shields first.
        # choices = sorted(choices, lambda x: x.hasFlag('SHIELD'), True)
        print "blockers:"
        print len(choices)

        for defender in choices:
            forcedBlock = False

            rerolls = 0
            if self.HP < self.maxHP / 10:
                rerolls += 1
            # TODO: rerolls from skills

            toBlock = var.rand_gaussian_d20(rerolls)

            if toBlock == 20:
                forcedBlock = True

            if defender.hasFlag('SHIELD'):
                toBlock += self.getAccuracyBonus(defender, True)
            else:
                toBlock += self.getAccuracyBonus(defender)
            print "blocking %s vs %s" % (toBlock, toHit)

            if forcedBlock or toBlock > toHit:
                # We blocked the attack.
                print "successful block"

                # Find how much we blocked:
                try:
                    DiceNumber = defender.attack['DiceNumber']
                except:
                    DiceNumber = raw.DummyAttack['DiceNumber']
                try:
                    DiceValue = defender.attack['DiceValue']
                except:
                    DiceValue = raw.DummyAttack['DiceValue']
                try:
                    DamageBonus = defender.attack['DamageBonus']
                except:
                    DamageBonus = raw.DummyAttack['DamageBonus']

                if defender.hasFlag('SHIELD'):
                    blocked = DiceNumber * DiceValue + DamageBonus
                else:
                    blocked = var.rand_dice(DiceNumber, DiceValue, DamageBonus)

                blocked += self.getDamageBonus(attacker, defender)
                withWhat = "&POSS " + defender.getName()

                if forcedHit:
                    how = "luckily "
                elif forcedBlock:
                    how = "easily "
                else:
                    how = ""

                if blocked >= damage:
                    blocked = damage
                    damage = 0
                    partially = ""
                else:
                    damage -= blocked
                    partially = "partially "

                message = "But %s %smanage&S to %sblock the attack with %s." % (self.getName(),
                               how, partially, withWhat)
                ui.message(message, actor = self)

                # Find size difference:
                staminaMod = 1.0

                if weapon != None:
                    # Mod is 100% for bigger weapon of attacker.
                    if weapon.size == defender.size:
                        staminaMod = 0.75
                    elif weapon.size < defender.size:
                        staminaMod = 0.5
                if defender.hasFlag('SHIELD'):
                    staminaMod /= 2

                self.SP -= max(1, (blocked * staminaMod))
                # TODO: If this bring us below 0, be off-balanced.

                # Debug:
                print "blocked %s damage" % blocked
                cost = blocked * staminaMod
                print "lost %s stamina" % cost

                return damage
            else:
                self.SP -= 1 # Trying to block is tirying anyway.
                print "Failed to block."

        return damage

    def resistDamage(self, damage, DamageType):
        pass

    def severLimb(self, limb):
        pass

    def getRelation(self, Other):
        # TODO: Add factions, pets etc.
        #       Special cases for golden beetle, vampire bat, ...
        if (self.hasFlag('AVATAR') or Other.hasFlag('AVATAR')):
            return 0
        else:
            return 1

    def getColor(self):
        if self.hasFlag('AVATAR'):
            for i in self.bodyparts:
                if i.hasFlag('TORSO') and len(i.inventory) > 0:
                    for n in i.inventory:
                        return n.color
            return self.color
        else:
            return self.color

    def getEquipment(self):
        equipment = []
        for part in self.bodyparts:
            for item in part.inventory:
                equipment.append(item)

        return equipment

    def getActionAPCost(self):
        return 1

    def getAttackAPCost(self):
        return 1

    def getMoveAPCost(self):
        return 1

    def getName(self, capitalize = False, full = False, possessive = False):
        name = self.name

        if self.hasFlag('AVATAR') and full == False:
            name = 'you'

        if possessive == True:
            full = False

            if self.hasFlag('AVATAR'):
                name = 'your'
            else:
                name = name + '\'s'

        # TODO:
        if full == True:
            # Whole name and title:
            if self.givenName != None:
                name = self.givenName + ' the ' + name

            # Corpses:
            if self.hasFlag('ITEM'):
                # Enchantment:
                if self.enchantment < 0:
                    name = str(self.enchantment) + ' ' + name
                else:
                    name = '+' + str(self.enchantment) + ' ' + name
                # Beautitude:
                if self.beautitude > 1:
                    name = "holy " + name
                elif self.beautitude == 1:
                    name = "blessed " + name
                elif self.beautitude == 0:
                    name = "uncursed " + name
                elif self.beautitude == -1:
                    name = "cursed " + name
                elif self.beautitude < -1:
                    name = "doomed " + name

        if capitalize == True:
            name = name.capitalize()

        return name

    def hasHead(self):
        for part in self.bodyparts:
            if part.hasFlag('HEAD'):
                return True

        return False

    def hasEyes(self, boolean = True):
        eyeNo = 0

        for part in self.bodyparts:
            eyeNo += part.eyes

        if boolean:
            if eyeNo >= self.baseEyes and eyeNo > 0:
                return True
            else:
                return False
        else:
            return eyeNo

    def hasArms(self, boolean = True):
        armNo = 0

        for part in self.bodyparts:
            if part.hasFlag('ARM'):
                armNo += 1

        if boolean:
            if armNo >= self.baseArms and armNo > 0:
                return True
            else:
                return False
        else:
            return armNo

    def hasLegs(self, boolean = True):
        legNo = 0

        for part in self.bodyparts:
            if part.hasFlag('LEG'):
                legNo += 1

        if boolean:
            if legNo >= self.baseLegs and legNo > 0:
                return True
            else:
                return False
        else:
            return legNo

    def hasWings(self, boolean = True):
        # Also used for check whether you can fly - you need at least two wings,
        # otherwise you need to go for magical levitation.

        wingNo = 0

        for part in self.bodyparts:
            if part.hasFlag('WING'):
                wingNo += 1

        if boolean:
            if wingNo >= self.baseWings and wingNo >= 2:
                return True
            else:
                return False
        else:
            return wingNo

    def isExtreFragile(self):
        if self.End < 0:
            return True
        else:
            return False

    def handleIntrinsics(self):
        pass

    def receiveHeal(self, amount):
        if self.hasFlag('DEAD'):
            return False
        if amount > 0:
            self.HP += amount
        else:
            return False
        if self.HP > self.maxHP:
            self.HP = self.maxHP
        return True

    def receiveMana(self, amount):
        if self.hasFlag('DEAD'):
            return False
        if amount > 0:
            self.MP += amount
        else:
            return False
        if self.MP > self.maxMP:
            self.MP = self.maxMP
        return True

    def receiveStamina(self, amount):
        if self.hasFlag('DEAD'):
            return False
        if amount > 0:
            self.SP += amount
        else:
            return False
        if self.SP > self.maxSP:
            self.SP = self.maxSP
        return True

    def receiveExperience(self, amount):
        if self.hasFlag('DEAD'):
            return False
        if amount > 0:
            self.XP += amount
        elif amount < self.XP:
            self.XP += amount # This deducts negative experience.
        else:
            self.XP = 0
        if self.XP >= 1000:
            self.XL += 1
            self.XP -= 1000
        return True

    def receiveAttack(self, attacker, weapon, multiplier):
        # TODO: launcher
        self.target = attacker

        forcedHit = False
        forcedMiss = False

        # TODO: rerolls from skills
        toHit = var.rand_gaussian_d20()
        toDodge = var.rand_gaussian_d20()

        # Pseudocode:
        # if (OffBalance || (Fumble && RandChance(25))):
        #    forcedmiss
        # if (tohit = 1):
        #    if (!forcedhit):
        #        forcedmiss
        # if (Fumble):
        #    DropYourWeapon

        if toHit == 20:
            forcedHit = True
        elif (toHit == 1 or toDodge == 20):
            forcedMiss = True

        # Debug:
        print "-" * 10
        print "%s to hit roll: %s; %s to dodge roll: %s" % (attacker.name, toHit,
                                                            self.name, toDodge)

        toHit += attacker.getAccuracyBonus(weapon)
        toDodge += self.getDodgeBonus(attacker, weapon)

        print "modified hit chance: %s vs %s" % (toHit, toDodge)

        try:
            if weapon == None:
                verb = raw.Slam['verb']
                withWhat = ""
            else:
                verb = weapon.attack['verb']
                withWhat = " with &POSS %s" % weapon.getName()
        except:
            verb = 'hit&S'
            withWhat = ""

        limb = self.getLimbToHit(attacker)
        whatLimb = self.getName(possessive = True) + ' ' + limb.getName()

        if forcedMiss == False or forcedHit == True:
            if (forcedHit == True or toHit > toDodge):
                if forcedHit == True:
                    ui.message("%s easily %s %s%s." % (attacker.getName(True), verb,
                              whatLimb, withWhat), actor = attacker)
                else:
                    ui.message("%s %s %s%s." % (attacker.getName(True), verb,
                               whatLimb, withWhat), actor = attacker)

                try:
                    if weapon == None:
                        DiceNumber = raw.Slam['DiceNumber']
                    else:
                        DiceNumber = weapon.attack['DiceNumber']
                except:
                    print "BUG: dummy attack"
                    DiceNumber = raw.DummyAttack['DiceNumber']
                try:
                    if weapon == None:
                        DiceValue = raw.Slam['DiceValue']
                    else:
                        DiceValue = weapon.attack['DiceValue']
                except:
                    DiceValue = raw.DummyAttack['DiceValue']
                try:
                    if weapon == None:
                        DamageBonus = raw.Slam['DamageBonus']
                    else:
                        DamageBonus = weapon.attack['DamageBonus']
                except:
                    DamageBonus = raw.DummyAttack['DamageBonus']
                try:
                    if weapon == None:
                        DamageType = raw.Slam['DamageType']
                    else:
                        DamageType = weapon.attack['DamageType']
                except:
                    DamageType = raw.DummyAttack['DamageType']
                try:
                    if weapon == None:
                        AttackFlags = raw.Slam['AttackFlags']
                    else:
                        AttackFlags = weapon.attack['flags']
                except:
                    AttackFlags = raw.DummyAttack['flags']

                # Try crits:
                if weapon == None:
                    toCrit = 10
                elif weapon.size < 0:
                    toCrit = 4
                elif weapon.size == 0:
                    toCrit = 8
                elif weapon.size > 0:
                    toCrit = 12

                CritNo = (toHit - toDodge) / toCrit
                DiceNumber += int(math.floor(CritNo))
                # TODO: Message.

                # Add strength:
                try:
                    DiceValue += attacker.Str # TODO: Scaling
                except:
                    pass # How do we have no attacker?

                # Add damage bonuses:
                DamageBonus += attacker.getDamageBonus(self, weapon)

                # Roll for damage:
                damage = var.rand_dice(DiceNumber, DiceValue, DamageBonus)
                damage *= multiplier

                print "rolling " + str(DiceNumber) + "d" + str(DiceValue) + "+" + str(DamageBonus)
                print "    + " + str(attacker.Str) + " ="
                print "    " + str(damage) + " damage"

                # Try blocking the attack:
                if self.SP > 0:
                    if DamageType in ['BLUNT', 'SLASH', 'PIERCE']:
                        damage = self.tryBlocking(attacker, weapon, toHit, damage, forcedHit)

                if damage > 0:
                    self.receiveDamage(damage, limb, DamageType, AttackFlags)
            else:
                ui.message("%s miss&ES %s." % (attacker.getName(True), self.getName()), actor = attacker)
        else:
            ui.message("%s completely miss&ES %s." % (attacker.getName(True), self.getName()), actor = attacker)
            # TODO: if toHit + bonus < 0, fumble

        # TODO: Different SP costs, but min 1 SP.
        attacker.SP -= 2

    def receiveDamage(self, damage, limb, type = None, flags = []):
        # TODO: Resistances
        #       Different materials.
        #       Limb wounds, severing etc.

        if damage > 0:
            self.HP -= damage
            self.checkDeath()
        else:
            ui.message("%s &ISARE not hurt." % self.getName(True), actor = self)

    def checkDeath(self, forceDie = False):
        if self.hasFlag('DEAD'):
            return True

        if self.HP <= 0:
            forceDie = True

        vitalBodyParts = 0

        for part in self.bodyparts:
            if part.hasFlag('VITAL'):
                vitalBodyParts += 1

        if vitalBodyParts == 0:
            forceDie = True

        if forceDie:
            ui.message("%s die&S." % self.getName(True), libtcod.red, self)

            # Drop all equipped and carried items.
            for part in self.bodyparts:
                item = part.doDeEquip()
                if item != None:
                    self.inventory.append(item)
            self.actionDrop(True)

            self.flags.remove('MOB')
            self.flags.append('ITEM')
            self.flags.append('DEAD')

            if self.hasFlag('AVATAR'):
                game.save() # No savescumming for you! (Unless you prepare for this, of course.)
                ai.waitForMore(self)
                var.WizModeTrueSight = True
                ui.message("You have failed in your quest! You can (L)ook around, or (Ctrl + q)uit the game.")

            self.char = '%'
            self.color = libtcod.red
            self.name = str(self.name + ' corpse')
            self.BlockMove = False

            for i in var.Entities[var.DungeonLevel]:
                if i.target == self:
                    i.target = None

            return True
        else:
            return False

    # Actions:
    def actionAttack(self, dx, dy, victim):
        # Set our victim as AI target:
        self.target = victim

        # Prevent weird cases:
        if self.AP < 1:
            return False
        if self.SP <= 0:
            if self.hasFlag('AVATAR'):
                ui.message("You are too exhausted to fight.")
            return False
        if not victim.hasFlag('MOB'):
            if self.hasFlag('AVATAR'):
                ui.message("You can only attack creatures.")
            return False

        # Get all useable body parts:
        armNo = 0
        legNo = 0
        for i in self.bodyparts:
            if i.hasFlag('ARM'):
                armNo += 1
            elif i.hasFlag('LEG'):
                legNo += 1

        # TODO: This does not work well!
        attacks = []
        weapons = False
        for i in self.bodyparts:
            if i.hasFlag('GRASP'):
                if len(i.inventory) > 0:
                    for n in i.inventory: # If this produces more than one weapon, we have a bug in equipping.
                        if not n.hasFlag('SHIELD'):
                            attacks.append(n)
                        weapons = True
            if i.hasFlag('ARM') and weapons == False:
                # You attack unarmed only if you are wielding no weapons.
                attacks.append(i)
            elif (i.hasFlag('LEG') and (self.hasFlag('USE_LEGS') or armNo == 0)):
                attacks.append(i)
            elif (i.hasFlag('HEAD') and (self.hasFlag('USE_HEAD') or
                  (armNo == 0 and legNo == 0))):
                attacks.append(i)
            elif ((i.hasFlag('TAIL') or i.hasFlag('WING')) and self.hasFlag('USE_NATURAL')):
                attacks.append(i)

        # If we found no attacks, we will use the first available.
        if len(attacks) == 0:
            for i in reversed(self.bodyparts):
                attacks.append(i)
                break

        # Get multiplier:
        multiplier = 1.0

        if len(attacks) == 0:
            victim.receiveAttack(self, None, multiplier)
        else:
            for i in attacks:
                if victim.hasFlag('DEAD'):
                    break

                victim.receiveAttack(self, i, multiplier)

        self.AP -= self.getAttackAPCost()
        # self.NP -= 5
        return True

    def actionBump(self, dx, dy):
        if self.AP < 1:
            return False

        bumpee = None
        x = self.x + dx
        y = self.y + dy

        for i in var.Entities[var.DungeonLevel]:
            if i.x == x and i.y == y and i.hasFlag('MOB'):
                bumpee = i
                break

        if bumpee != None:
            if self.hasFlag('AI_FLEE'):
                self.actionSwap(bumpee)
                return True
            elif self.getRelation(bumpee) < 1:
                self.actionAttack(dx, dy, bumpee)
                return True
            else:
                if (self.hasFlag('AVATAR') or var.rand_chance(50)):
                    self.actionSwap(bumpee)
                    return True
                else:
                    self.actionWait()
                    return True

        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            if var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_OPENED'):
                if(self.actionOpen(x, y)):
                    return True
            elif var.Maps[var.DungeonLevel][x][y].BlockMove == True:
                for n in range(y - 1, y + 2):
                    for m in range(x - 1, x + 2):
                        if (m > 0 and m < var.MapWidth - 1 and
                            n > 0 and n < var.MapHeight - 1):
                            if var.Maps[var.DungeonLevel][m][n].hasFlag('CAN_BE_CLOSED'):
                                if(self.actionClose(m, n)):
                                    return True

        if self.actionWalk(dx, dy):
            return True
        else:
            return False

    def actionClose(self, x, y):
        if self.AP < 1:
            return False

        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            blocked = False

            for i in var.Entities[var.DungeonLevel]:
                if i.x == x and i.y == y:
                    blocked = True
                    break

            if not blocked == True and var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_CLOSED'):
                if var.Maps[var.DungeonLevel][x][y].hasFlag('DOOR'):
                    if var.Maps[var.DungeonLevel][x][y].hasFlag('PORTCULLIS'):
                        var.Maps[var.DungeonLevel][x][y].change(raw.ClosedPort)
                    else:
                        var.Maps[var.DungeonLevel][x][y].change(raw.WoodDoor)

                    var.changeFOVMap(x, y)
                    ui.message("%s close&S the door." % self.getName(True), actor = self)
                    self.AP -= self.getActionAPCost()
                    return True
                else:
                    print "BUG: Unhandled closeable terrain."
            elif var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_CLOSED') and self.hasFlag('AVATAR'):
                ui.message("There is something in the way.")
            elif self.hasFlag('AVATAR'):
                ui.message("There is nothing to close.")
        return False

    def actionClimb(self, dz):
        if self.AP < 1:
            return False
        if self.SP < 5:
            ui.message("%s &ISARE too tired to climb the stairs." % self.getName(True), actor = self)
            self.AP -= self.getMoveAPCost()
            return False

        if dz > 0 and var.Maps[var.DungeonLevel][self.x][self.y].hasFlag('STAIRS_UP'):
            if var.DungeonLevel - 1 >= 0:
                if var.Maps[var.DungeonLevel - 1] == None:
                    dungeon.makeMap(True, var.DungeonLevel - 1)

                toClimb = [self.x, self.y]

                for y in range(0, var.MapHeight):
                    for x in range(0, var.MapWidth):
                        if var.Maps[var.DungeonLevel - 1][x][y].hasFlag('STAIRS_DOWN'):
                            toClimb = [x, y]

                self.x = toClimb[0]
                self.y = toClimb[1]

                var.Entities[var.DungeonLevel - 1].append(self)
                var.Entities[var.DungeonLevel].remove(self)
                var.DungeonLevel -= 1

                if self.hasFlag('AVATAR'):
                    var.calculateFOVMap()
                    libtcod.console_clear(var.MapConsole)

                ui.message("%s climb&S the stairs." % self.getName(True), actor = self)
                self.SP -= 8 # It's a bit more tiring to go upstairs.
                self.AP -= self.getMoveAPCost()
                return True
            else:
                ui.message("The stairs lead nowhere!", actor = self)
                return False
        elif dz < 0 and var.Maps[var.DungeonLevel][self.x][self.y].hasFlag('STAIRS_DOWN'):
            if var.DungeonLevel + 1 <= var.FloorMaxNumber:
                if var.Maps[var.DungeonLevel + 1] == None:
                    dungeon.makeMap(True, var.DungeonLevel + 1)

                toClimb = [self.x, self.y]

                for y in range(0, var.MapHeight):
                    for x in range(0, var.MapWidth):
                        if var.Maps[var.DungeonLevel + 1][x][y].hasFlag('STAIRS_UP'):
                            toClimb = [x, y]

                self.x = toClimb[0]
                self.y = toClimb[1]

                var.Entities[var.DungeonLevel + 1].append(self)
                var.Entities[var.DungeonLevel].remove(self)
                var.DungeonLevel += 1

                if self.hasFlag('AVATAR'):
                    var.calculateFOVMap()
                    libtcod.console_clear(var.MapConsole)

                ui.message("%s climb&S the stairs." % self.getName(True), actor = self)
                # TODO: Knock back entities that are standing on the stairs.
                #       Enemies and pets follow you. (Requires findNearestFreeSpot().)
                self.SP -= 3
                self.AP -= self.getMoveAPCost()
                return True
            else:
                ui.message("The stairs lead nowhere!", actor = self)
                return False
        else:
            if dz > 0:
                ui.message("%s jump&S up and down." % self.getName(True), actor = self)
            elif dz < 0:
                ui.message("%s crouch&ES a bit." % self.getName(True), actor = self)
            self.AP -= self.getMoveAPCost()
            return True

    def actionDrop(self, dropAll = False):
        #if self.AP < 1:
        #    return False

        if len(self.inventory) == 0:
            if self.hasFlag('AVATAR') and not self.hasFlag('DEAD'):
                ui.message("You carry nothing to drop.")
            return False
        elif dropAll == True:
            for item in self.inventory:
                if item == None: # I somehow managed to end up with some None items
                    continue     # in inventory and then crashed on death...

                self.inventory.remove(item)

                item.x = self.x
                item.y = self.y
                var.Entities[var.DungeonLevel].append(item)
                # Used only on death, so no AP nor drop messages.
        else:
            if not self.hasFlag('AVATAR'):
                toDrop = libtcod.random_get_int(0, 0, len(self.inventory) - 1)
            else:
                toDrop = ui.option_menu("What do you want to drop?", self.inventory)

            if toDrop == None:
                return False
            else:
                item = self.inventory[toDrop]

                self.inventory.remove(item)

                item.x = self.x
                item.y = self.y
                var.Entities[var.DungeonLevel].append(item)
                ui.message("%s drop&S %s." % (self.getName(True), item.getName()),
                           actor = self)
                self.AP -= (self.getActionAPCost() / 3) # It's quick.

        if len(self.inventory) >= 1:
            return True
        else:
            return False

    def actionInteract(self, where):
        if self.AP < 1:
            return False

        dx = where[0]
        dy = where[1]

        x = self.x + dx
        y = self.y + dy

        # No interactions beyond the map.
        if (x < 0 or x > var.MapWidth - 1 or y < 0):
            if self.hasFlag('AVATAR'):
                ui.message("Be careful or you will break the backlight.")
            self.AP -= self.getMoveAPCost()
            return False
        elif (y > var.MapHeight - 1):
            if self.hasFlag('AVATAR'):
                ui.message("You hear someone mashing buttons.")
            self.AP -= self.getMoveAPCost()
            return False

        for i in var.Entities[var.DungeonLevel]:
            if i.x == x and i.y == y:
                if i.hasFlag('ITEM'):
                    self.actionPickUp(x, y)
                    return True
                elif i.hasFlag('MOB'):
                    # TODO
                    #i.selectAction(self)
                    if not self.hasFlag('AVATAR') and not i.hasFlag('AVATAR'):
                        ui.message("%s chat&S with %s." % (self.getName(True), i.getName()),
                                   actor = self)
                    self.AP -= self.getActionAPCost()
                    return True

        if var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_OPENED'):
            self.actionOpen(x, y)
            return True
        elif var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_CLOSED'):
            self.actionClose(x, y)
            return True

        # TODO: More actions.
        #   actionOpen for containers, both ITEM and FEATURE

    def actionInventory(self):
        if len(self.inventory) == 0:
            ui.message("You carry no items.")
            return False
        else:
            ui.option_menu("You carry the following:", self.inventory)
            return True

    def actionEquipment(self):
        if len(self.bodyparts) == 0:
            ui.message("%s should be dead." % self.getName(True), actor = self)
            self.checkDeath()
            return False
        else:
            part = ui.equip_menu(self.bodyparts)

            if part == None:
                return False

            if len(self.bodyparts[part].inventory) != 0:
                item = self.bodyparts[part].doDeEquip()
                self.inventory.append(item)
                self.AP -= self.getActionAPCost()
                return True
            else:
                slot = self.bodyparts[part].getSlot()

                options = []
                if slot == None:
                    ui.message("You cannot equip anything on that body part.", actor = self)
                    ui.render_all(self)
                    return True
                elif slot == 'GRASP':
                    options = self.inventory
                else:
                    for i in self.inventory:
                        if i.hasFlag(slot):
                            options.append(i)

                # TODO:
                # Items of size larger than self are two-handed.

                if len(options) == 0:
                    ui.message("You carry nothing to equip on that body part.", actor = self)
                    ui.render_all(self)
                    return True
                else:
                    item = ui.option_menu("What do you want to equip:", options)

                    if item == None:
                        return True

                    if self.bodyparts[part].doEquip(options[item]) == True:
                        self.inventory.remove(options[item])
                        self.AP -= self.getActionAPCost()
                        return True
                    else:
                        ui.message("You fail to equip %s." % options[item].getName())
                        ui.render_all(self)
                        return True

    def actionJump(self, where):
        if self.AP < 1:
            return False

        dx = where[0]
        dy = where[1]
        dz = where[2]

        if dx == 0 and dy == 0:
            if dz > 0:
                ui.message("You jump up and down.")
                self.AP -= self.getMoveAPCost()
                return True
            elif dz < 0:
                ui.message("Wait, how do you jump downwards?")
                self.AP -= self.getMoveAPCost()
                return True
            else:
                ui.message("You completely fail to jump.")
                return False

        nx = self.x + dx
        ny = self.y + dy
        nnx = nx + dx
        nny = ny + dy
        moved = False

        # TODO: Leap attack, stamina cost, jumping out of pits.
        if self.SP <= 5:
            if self.hasFlag('AVATAR'):
                ui.message("You are too exhausted to jump.")
            self.AP -= (self.getMoveAPCost() / 2)
            return False

        if (not self.isBlocked(nx, ny, var.DungeonLevel) and
            not self.isBlocked(nnx, nny, var.DungeonLevel) and
            libtcod.map_is_in_fov(var.FOVMap, nnx, nny)):
            ui.message("%s leap&S." % self.getName(True), actor = self)
            self.move(dx * 2, dy * 2)
            moved = True
        else:
            ui.message("%s balk&S at the leap." % self.getName(True), actor = self)

        self.AP -= self.getMoveAPCost()
        self.SP -= 5
        # self.NP -= 10
        return moved

    def actionOpen(self, x, y):
        if self.AP < 1:
            return False

        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            if var.Maps[var.DungeonLevel][x][y].hasFlag('CAN_BE_OPENED'):
                if var.Maps[var.DungeonLevel][x][y].hasFlag('DOOR'):
                    # Blocked door will only appear in vault where we want to keep
                    # monsters inside.
                    if (var.Maps[var.DungeonLevel][x][y].hasFlag('BLOCKED') and
                        not self.hasFlag('AVATAR')):
                        return False

                    # TODO: LOCKED flag.
                    if var.Maps[var.DungeonLevel][x][y].hasFlag('SECRET'):
                        ui.message("%s discover&S a secret door!" % self.getName(True),
                                   libtcod.azure, actor = self)

                    if var.Maps[var.DungeonLevel][x][y].hasFlag('PORTCULLIS'):
                        var.Maps[var.DungeonLevel][x][y].change(raw.OpenPort)
                    else:
                        var.Maps[var.DungeonLevel][x][y].change(raw.OpenDoor)

                    var.changeFOVMap(x, y)
                    ui.message("%s open&S the door." % self.getName(True), actor = self)
                    self.AP -= self.getActionAPCost()
                    return True
                else:
                    print "BUG: Unhandled openable terrain."
            elif self.hasFlag('AVATAR'):
                ui.message("There is nothing to open.")
        return False

    def actionPickUp(self, x, y, pickAll = False):
        #if self.AP < 1:
        #    return False

        if len(self.inventory) >= self.carry:
            if self.hasFlag('AVATAR'):
                ui.message("Your inventory is already full.")
            return False
        if not self.hasFlag('AVATAR'):
            pickAll = True

        options = []

        for i in var.Entities[var.DungeonLevel]:
            if i.hasFlag('ITEM') and i.x == x and i.y == y:
                options.append(i)

        if len(options) == 0:
            if self.hasFlag('AVATAR'):
                quips = [
                "You grope foolishly on the floor.",
                "There is nothing to pick up.",
                "You return emtpy-handed."
                ]
                ui.message(random.choice(quips))

            self.AP -= (self.getActionAPCost() / 2)
            return False
        elif pickAll == True:
            # TODO: Not if monsters in sight?
            for i in options:
                if len(self.inventory) >= self.carry:
                    ui.message("%s cannot pick up any more items." % self.getName(True), actor = self)
                    break

                self.inventory.append(i)
                var.Entities[var.DungeonLevel].remove(i)
                ui.message("%s pick&S up %s." % (self.getName(True), i.getName()), actor = self)
                self.AP -= self.getActionAPCost()
        else:
            if not self.hasFlag('AVATAR'):
                return False

            toPick = ui.option_menu("What do you want to pick up?", options)

            if toPick == None:
                return False
            else:
                self.inventory.append(options[toPick])
                var.Entities[var.DungeonLevel].remove(options[toPick])
                ui.message("%s pick&S up %s." % (self.getName(True), options[toPick].getName()),
                           actor = self)
                self.AP -= self.getActionAPCost()

        if len(options) > 1:
            return True
        else:
            return False # Closes window after picking up the only item on ground.

    def actionPush(self, dx, dy):
        pass

    def actionSwap(self, Other):
        if self.AP < 1:
            return False
        if self == Other:
            ui.message("%s attempt&S to swap with &SELF and fail&S." % self.getName(True), actor = self)
            return False

        x1 = self.x
        y1 = self.y
        x2 = Other.x
        y2 = Other.y

        self.x = x2
        self.y = y2
        Other.x = x1
        Other.y = y1

        ui.message("%s swap&S places with %s." % (self.getName(True), Other.getName()), actor = self)

        self.AP -= self.getMoveAPCost()

    def actionVomit(self):
        # self.NP -= 100
        pass

    def actionWait(self):
        #print "%s waits." % self.name
        self.AP -= 1
        self.receiveStamina(2)

    def actionWalk(self, dx, dy):
        if self.AP < 1:
            return False

        # TODO: If running, takes half a turn. With Unarmored and not running,
        #       you recover 1 SP per move.

        moved = False

        if (not self.isBlocked(self.x + dx, self.y + dy, var.DungeonLevel) or
           (self.hasFlag('AVATAR') and var.WizModeNoClip)):
            self.move(dx, dy)
            moved = True
        else:
            if self.hasFlag('AVATAR'):
                ui.message("You cannot go there.")

        if moved and self.hasFlag('AVATAR'):
            stuff = []

            for i in var.Entities[var.DungeonLevel]:
                if i.hasFlag('ITEM') and i.x == self.x and i.y == self.y:
                    stuff.append(i.getName())

            if len(stuff) < 1:
                names = None
            elif len(stuff) == 1:
                names = "There is a " + stuff[0] + "."
            elif len(stuff) <= 3:
                names = "There are " + ', '.join(stuff) + "."
            else:
                names = "There are many items."

            if names != None:
                ui.message(names)

        # Take a turn even if we walk into a wall.
        self.AP -= self.getMoveAPCost()
        return moved

class Item(Entity):
    def __init__(self, x, y, char, color, name, material, size, BlockMove, #These are base Entity arguments.
                 attack, ranged, DV, PV, addFlags):
        super(Item, self).__init__(x, y, char, color, name, material, size, BlockMove)

        self.attack = attack
        self.ranged = ranged
        self.DefenseValue = DV
        self.ProtectionValue = PV

        self.flags.append('ITEM')
        for i in addFlags:
            self.flags.append(i)

    def getName(self, capitalize = False, full = False):
        name = self.name

        # TODO:
        # if full == False, show only base name
        if full == True:
            # Size:
            if self.hasFlag('ARMOR') and self.hasFlag('TORSO') and self.size != 0:
                size = raw.Sizes[self.size]
                name = size + ' ' + name

            # Enchantment:
            if self.enchantment < 0:
                name = str(self.enchantment) + ' ' + name
            else:
                name = '+' + str(self.enchantment) + ' ' + name
            # BUC:
            if self.beautitude > 1:
                name = "holy " + name
            elif self.beautitude == 1:
                name = "blessed " + name
            elif self.beautitude == 0:
                name = "uncursed " + name
            elif self.beautitude == -1:
                name = "cursed " + name
            elif self.beautitude < -1:
                name = "doomed " + name

            # Stats:
            try:
                ToHitBonus = self.attack['ToHitBonus']
            except:
                ToHitBonus = raw.DummyAttack['ToHitBonus']
            try:
                DiceNumber = self.attack['DiceNumber']
            except:
                DiceNumber = raw.DummyAttack['DiceNumber']
            try:
                DiceValue = self.attack['DiceValue']
            except:
                DiceValue = raw.DummyAttack['DiceValue']
            try:
                DamageBonus = self.attack['DamageBonus']
            except:
                DamageBonus = raw.DummyAttack['DamageBonus']

            # TODO:
            if ToHitBonus > 0:
                acc = "+" + str(ToHitBonus) + ", "
            elif ToHitBonus < 0:
                acc = str(ToHitBonus) + ", "
            else:
                acc = ""

            damage = str(DiceNumber) + "d" + str(DiceValue)
            if DamageBonus != 0:
                damage += "+" + str(DamageBonus)

            if self.hasFlag('WEAPON'):
                attack = " (" + acc + damage + ")"
            else:
                attack = ""

            if self.getDefenseValue() != 0 or self.getProtectionValue() != 0:
                if self.getDefenseValue() >= 0:
                    DV = "+" + str(self.getDefenseValue()) + ", "
                else:
                    DV = str(self.getDefenseValue()) + ", "

                if self.getProtectionValue() >= 0:
                    PV = "+" + str(self.getProtectionValue())
                else:
                    PV = str(self.getProtectionValue())

                defense = " [" + DV + PV + "]"
            else:
                defense = ""

            name = name + attack + defense

        if capitalize == True:
            name = name.capitalize()

        return name

    def getAccuracyValue(self):
        try:
            toHit = self.attack['ToHitBonus']
        except:
            toHit = raw.DummyAttack['ToHitBonus']

        toHit += self.enchantment
        return toHit

    def getDefenseValue(self):
        DV = self.DefenseValue

        if self.hasFlag('ARMOR') or self.hasFlag('SHIELD'):
            DV += self.enchantment
        return DV

    def getProtectionValue(self):
        PV = self.ProtectionValue

        if self.hasFlag('ARMOR') or self.hasFlag('SHIELD'):
            PV += self.enchantment
        return PV

    def beEaten(self, Eater):
        # return if too full
        if self.hasFlag('POTION'):
            pass # quaffing
        elif self.material in Eater.diet:
            pass
        else:
            if Eater.hasFlag('AVATAR'):
                ui.message("You cannot eat that.")
            return False

    def beZapped(self, Zapper):
        pass

    def handleIntrinsics(self):
        pass

class BodyPart(Entity):
    def __init__(self, name, #These are base Entity arguments.
                 mob, cover, place, size, eyes, attack, addFlags, material = None):
        x = mob.x
        y = mob.y
        char = '~'
        color = libtcod.red

        if material == None:
            material = mob.material

        # Different body parts are differently smaller then mob, plus cannot
        # equip items smaller than the body part.
        size = min(2, max(-2, mob.size + size))

        super(BodyPart, self).__init__(x, y, char, color, name, material, size)

        self.flags.append('ITEM')
        self.flags.append('BODY_PART')
        for i in addFlags:
            self.flags.append(i)

        self.attack = attack
        self.cover = cover
        self.placement = place
        self.eyes = eyes

        self.wounded = False

    def getName(self, capitalize = False, full = True):
        name = self.name

        # Size:
        #size = raw.Sizes[self.size]
        #name = size + ' ' + name

        # Right/left:
        if (self.hasFlag('ARM') or self.hasFlag('LEG')) and self.hasFlag('RIGHT'):
            name = 'right ' + name
        if (self.hasFlag('ARM') or self.hasFlag('LEG')) and self.hasFlag('LEFT'):
            name = 'left ' + name
        if (self.hasFlag('ARM') or self.hasFlag('LEG')) and self.hasFlag('OTHER'):
            name = 'other ' + name

        #if self.hasFlag('ARM') and self.hasFlag('MAIN'):
        #    name = name + '*'

        if self.wounded == True:
            name = 'wounded ' + name

        #if full == True:
        #    if len(self.inventory) > 0:
        #        name = name + self.inventory[0].getName()

        if capitalize == True:
            name = name.capitalize()

        return name

    def getSlot(self):
        slot = None
        for i in self.flags:
            if i in ['HEAD', 'TORSO', 'GROIN', 'ARM', 'LEG', 'WING', 'TAIL', 'GRASP']:
                slot = i # Grasp must be last!
        return slot

    def doEquip(self, item):
        if len(self.inventory) > 0:
            return False

        slot = self.getSlot()

        if slot != None:
            if not (slot in item.flags or slot == 'GRASP'):
                return False
        else:
            return False

        if not slot == 'GRASP' and item.size < self.size:
            return False

        self.inventory.append(item)
        return True

    def doDeEquip(self):
        if len(self.inventory) == 0:
            return None
        else:
            for item in self.inventory:
                self.inventory.remove(item)
                return item

#class Cloud(Entity):
#    def __init__(self, x, y, color, name, #These are base Entity arguments.
#                 attack, addFlags):
#        char = chr(177)
#        material = 'AIR'
#        size = 2 # Clouds should count as huge.
#
#        super(Cloud, self).__init__(x, y, char, color, name, material, size)
#
#        self.flags.append('CLOUD')
#        for i in addFlags:
#            self.flags.append(i)
#
#        self.attack = attack
