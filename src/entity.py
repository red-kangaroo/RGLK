# !/usr/bin/env python
# -*- coding: utf-8 -*-

import libtcodpy as libtcod
import math
import random

import ai
import dungeon
import game
import intrinsic
import mutation
import raw
import ui
import var

###############################################################################
#  Functions
###############################################################################

def spawn(x, y, BluePrint, type, allowSpecial = True):
    # Requires at least a colored character with a name.
    try:
        char = BluePrint['char']
        color = BluePrint['color']
        name = BluePrint['name']
    except:
        print "Failed to spawn an entity."
        return False

    myType = BluePrint

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
        try:
            inventory = BluePrint['inventory']
        except:
            inventory = []
        try:
            mutations = BluePrint['mutations']
        except:
            mutations = []

        if 'HUMANOID' in addFlags:
            if var.rand_chance(25):
                addIntrinsics.append(('LEFT_HANDED', 0))

        New = Mob(x, y, char, color, name, myType, material, size,
                     Str, Dex, End, Wit, Ego, sex, speed, sight, addFlags, addIntrinsics)

        New.diet = diet

        if len(mutations) != 0:
            for m in mutations:
                mutation.gain(m, New)

        if allowSpecial:
            if New.hasFlag('AVATAR'):
                New.makePlayer()

            if len(inventory) != 0: # TODO
                for i in inventory:
                    NewItem = spawn(x, y, i, 'ITEM')
                    New.inventory.append(NewItem)

                New.actionAutoEquip(True)

    elif type == 'ITEM':
        try:
            prefix = BluePrint['prefix']
        except:
            prefix = raw.DummyItem['prefix']
        try:
            suffix = BluePrint['suffix']
        except:
            suffix = raw.DummyItem['suffix']
        try:
            givenName = BluePrint['givenName']
        except:
            givenName = raw.DummyItem['givenName']
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
            accuracy = BluePrint['accuracy']
        except:
            accuracy = raw.DummyItem['accuracy']
        try:
            light = BluePrint['light']
        except:
            light = raw.DummyItem['light']
        try:
            Str = BluePrint['Str']
        except:
            Str = raw.DummyItem['Str']
        try:
            Dex = BluePrint['Dex']
        except:
            Dex = raw.DummyItem['Dex']
        try:
            End = BluePrint['End']
        except:
            End = raw.DummyItem['End']
        try:
            Wit = BluePrint['Wit']
        except:
            Wit = raw.DummyItem['Wit']
        try:
            Ego = BluePrint['Ego']
        except:
            Ego = raw.DummyItem['Ego']
        try:
            DV = BluePrint['DV']
        except:
            DV = raw.DummyItem['DV']
        try:
            PV = BluePrint['PV']
        except:
            PV = raw.DummyItem['PV']
        try:
            StrScaling = BluePrint['StrScaling']
        except:
            StrScaling = raw.DummyItem['StrScaling']
        try:
            DexScaling = BluePrint['DexScaling']
        except:
            DexScaling = raw.DummyItem['DexScaling']
        try:
            cool = BluePrint['coolness']
        except:
            cool = raw.DummyItem['coolness']
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

        if not material in raw.MaterialsList:
            print "Warning: %s is unhandled material." % material

        New = Item(x, y, char, color, name, myType, material, size, BlockMove,
                   attack, ranged, DV, PV, StrScaling, DexScaling, cool, addFlags, addIntrinsics)

        New.givenName = givenName
        New.prefix = prefix
        New.suffix = suffix

        # Add special stats:
        New.acc = accuracy
        New.light = light
        New.Str = Str
        New.Dex = Dex
        New.End = End
        New.Wit = Wit
        New.Ego = Ego

        if allowSpecial:
            New.gainMagic()

    else:
        print "Failed to spawn unknown entity type."

    return New

###############################################################################
#  Entities
###############################################################################

# Player, monsters...
class Entity(object):
    def __init__(self, x, y, char, color, name, type, material, size, BlockMove = False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.type = type
        self.material = material
        self.size = size
        self.BlockMove = BlockMove

        self.AP = 0.0 # Start with 0 turns to take.
        self.attack = raw.Slam
        self.ranged = raw.MisThrown
        self.beautitude = 0 # Negative for cursed/doomed, positive for blessed/holy.
        self.enchantment = 0

        # Naming:
        self.name = name
        self.givenName = None
        self.prefix = ""
        self.suffix = ""

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

    def draw(self, canSee):
        # Set color and draw character on screen.
        if (libtcod.map_is_in_fov(var.FOVMap, self.x, self.y) or var.WizModeTrueSight):
            libtcod.console_set_default_foreground(var.MapConsole, self.getColor())
                       # This canSee refers to the Player, whether he's blind or not.
            if canSee: # We'll draw "seen" monster anyway, but as a question mark.
                libtcod.console_put_char(var.MapConsole, self.x, self.y, self.char, libtcod.BKGND_SCREEN)
            elif self.hasFlag('MOB'):
                libtcod.console_put_char(var.MapConsole, self.x, self.y, '?', libtcod.BKGND_SCREEN)

            # Add a SEEN flag. This is necessary for messages, as FOV can be recalculated for other
            # creatures, but player will still only see the monsters with SEEN flag. We append it
            # even when canSee == False, because we still want to be able to recognize adjacent stuff.
            self.flags.append('SEEN')

    def range(self, Other): # Range between two entities.
        dx = Other.x - self.x
        dy = Other.y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y): # Distance between self and map square.
        dx = x - self.x
        dy = y - self.y

        return math.sqrt(dx ** 2 + dy ** 2)

    def isBlocked(self, x, y, DL, safewalk = True):
        if (x < 0 or x > var.MapWidth - 1 or
            y < 0 or y > var.MapHeight - 1):
            return True

        if var.Maps[DL][x][y].BlockMove:
            return True

        if safewalk:
            if var.Maps[DL][x][y].hasFlag('BURN') and not (self.hasIntrinsic('RESIST_FIRE') or self.hasIntrinsic('IMMUNE_FIRE')):
                return True

            if var.Maps[DL][x][y].hasFlag('DISSOLVE') and not (self.hasIntrinsic('RESIST_ACID') or self.hasIntrinsic('IMMUNE_ACID')):
                return True

            if var.Maps[DL][x][y].hasFlag('SWIM') and not (self.hasIntrinsic('SWIM') or self.hasIntrinsic('WATER_WALK')):
                return True

        if self.BlockMove:
            for i in var.Entities[DL]:
                if i != self and i.BlockMove and i.x == x and i.y == y:
                    return True

        return False

    def isPassable(self, x, y):
        if not dungeon.isOnMap(x, y):
            return False

        if var.getMap()[x][y].BlockMove:
            return False

        if var.getMap()[x][y].hasFlag('CAN_BE_OPENED') and self.hasFlag('CANNOT_OPEN'):
            return False

        if var.getMap()[self.x][self.y].isWalkable() == False:
            return True # Monsters already in dangerous terrain can get out now.

        if (var.getMap()[x][y].hasFlag('BURN') and
            not (self.hasIntrinsic('RESIST_FIRE') or self.hasIntrinsic('IMMUNE_FIRE') or self.isFlying())):
            return False

        if (var.getMap()[x][y].hasFlag('DISSOLVE') and
            not (self.hasIntrinsic('RESIST_ACID') or self.hasIntrinsic('IMMUNE_ACID') or self.isFlying())):
            return False

        if (var.getMap()[x][y].hasFlag('SWIM') and
            not (self.hasIntrinsic('SWIM') or self.hasIntrinsic('WATER_WALK') or self.isFlying())):
            return False

        return True

    def hasFlag(self, flag):
        if flag in self.flags:
            return True
        else:
            return False

    def hasIntrinsic(self, intrinsic):
        for i in self.intrinsics:
            if i.type == intrinsic:
                return True

        return False

    def getIntrinsic(self, intrinsic):
        for i in self.intrinsics:
            if i.type == intrinsic:
                return i

        return None

    def getIntrinsicPower(self, intrinsic):
        if intrinsic == None:
            return 0

        power = 0

        for i in self.intrinsics:
            if i.type == intrinsic:
                power += i.power

        if power > 0:
            power += self.enchantment

        return power

    def addIntrinsic(self, type, duration, power = 0):
        if self.hasIntrinsic(type):
            i = self.getIntrinsic(type)
            i.duration += duration / 2

            if i.power < power:
                i.power = power
            elif i.power == power:
                i.power += 1
        else:
            NewInt = intrinsic.Intrinsic(type, duration, power)
            self.intrinsics.append(NewInt)

    def removeIntrinsic(self, intrinsic, power = None):
        if not self.hasIntrinsic(intrinsic):
            return False
        else:
            if power == None:
                self.intrinsics.remove(self.getIntrinsic(intrinsic))
            else:
                self.getIntrinsic(intrinsic).power -= power
            return True

    def handleIntrinsics(self):
        for i in self.intrinsics:
            if i.getHandled(self) == None:
                self.intrinsics.remove(i)

    def handleTerrain(self):
        if var.getMap()[self.x][self.y].hasFlag('BURN'):
            if self.hasFlag('MOB'):
                if self.isFlying():
                    if self.hasFlag('AVATAR') and var.rand_chance(30):
                        quips = [
                        "very",
                        "extremely",
                        "sweating",
                        "searing"
                        ]
                        ui.message("It is %s hot here!" % random.choice(quips), libtcod.light_red)
                    if var.rand_chance(20):
                        self.addIntrinsic('AFLAME', libtcod.random_get_int(0, 1, 6), 2)
                else:
                    damage = var.rand_dice(3, 4, 6)

                    limb = None
                    for part in self.bodyparts:
                        if part.hasFlag('LEG'):
                            limb = part

                            if var.rand_chance(50):
                                break

                    self.receiveDamage(damage, limb, 'FIRE')
                    self.addIntrinsic('AFLAME', damage / 2, 2)
            elif self.hasFlag('ITEM'):
                if self.material in raw.MaterialDamageList['FIRE']:
                    ui.message("%s burns up!" % self.getName(True), actor = self)
                    self.getDestroyed()

        if var.getMap()[self.x][self.y].hasFlag('DISSOLVE'):
            if self.hasFlag('MOB'):
                if self.isFlying():
                    pass # Acid does no damage when we can fly over it.
                else:
                    ui.message("%s &ISARE dissolved." % self.getName(True), libtcod.light_red, actor = self)

                    damage = var.rand_dice(3, 9)

                    self.receiveDamage(damage, DamageType = 'ACID')
            elif self.hasFlag('ITEM'):
                if self.material in raw.MaterialDamageList['ACID']:
                    ui.message("%s is dissolved." % self.getName(True), libtcod.light_red, actor = self)
                    self.getDestroyed()

        if var.getMap()[self.x][self.y].hasFlag('HARM'):
            if self.hasFlag('MOB'):
                if not self.isFlying():
                    if self.hasFlag('AVATAR'):
                        ui.message("Ouch! You step on something sharp.", libtcod.light_red)
                    else:
                        ui.message("%s look&S pained." % self.getName(True), actor = self)

                    damage = var.rand_dice(1, 4)

                    limb = None
                    for part in self.bodyparts:
                        if part.hasFlag('LEG'):
                            limb = part

                            if var.rand_chance(50):
                                break

                    self.receiveDamage(damage, limb, 'PIERCE')

        if var.getMap()[self.x][self.y].hasFlag('SWIM'):
            if self.hasFlag('MOB'):
                if not self.isFlying() and not self.hasIntrinsic('WATER_WALK') and self.SP <= 0:
                    ui.message("%s drown&S." % self.getName(True), libtcod.light_red, actor = self)
                    damage = var.rand_dice(1, 10)
                    self.receiveDamage(damage, DamageType = 'ASPHYX')
                elif not self.isFlying() and not self.hasIntrinsic('WATER_WALK') and not self.hasIntrinsic('SWIM'):
                    self.SP -= 4

        if var.getMap()[self.x][self.y].hasFlag('LIQUID'):
            # TODO: wetting
            if self.hasFlag('ITEM'):
                if self.hasFlag('PLUG'):
                    ui.message("%s fill&S the %s." % (self.getName(True), var.getMap()[self.x][self.y].getName()),
                               actor = self)
                    self.getDestroyed()
                    var.getMap()[self.x][self.y].change(raw.RockFloor)
                elif self.willSink() and var.rand_chance(10):
                    try:
                        ui.message("%s sink&S into the %s." % (self.getName(True), var.getMap()[self.x][self.y].getName()),
                                   actor = self)
                        var.getMap()[self.x][self.y].inventory.append(self)
                        var.getEntity().remove(self)
                    except:
                        print "Failed to sink an item."

        if var.getMap()[self.x][self.y].hasFlag('PIT'):
            if self.hasFlag('ITEM') and self.hasFlag('PLUG'):
                ui.message("%s fill&S the %s." % (self.getName(True), var.getMap()[self.x][self.y].getName()),
                           actor = self)
                self.getDestroyed()
                var.getMap()[self.x][self.y].change(raw.RockFloor)

    def getName(self, capitalize = False, full = False):
        name = self.name

        if capitalize == True:
            name = name.capitalize()

        return name

    def getDestroyed(self):
        for i in var.getEntity():
            if i == self: # We should make sure we are actually lying on the floor.
                var.getEntity().remove(self)
                del self
                return True

        return False

    def getColor(self):
        return self.color

    def getDefenseValue(self):
        return 0

    def getProtectionValue(self):
        return 0

    def getSPCost(self):
        return 2

    def getCoolness(self):
        return 0

    def getSlot(self):
        return None

    def getAttack(self):
        return None

    def tryStacking(self, Owner = None):
        return False

    def removeFromStack(self, number = None):
        return None

    def willSink(self):
        if self.material in ['AETHER', 'PAPER', 'WOOD']:
            return False
        else:
            return True

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
        self.handleTerrain()

        # Intrinsics and status effects.
        self.handleIntrinsics()

        # TODO: Call Be() for inventory items from here, because they will not go
        #       through the main loop of var.Entities.

class Mob(Entity):
    def __init__(self, x, y, char, color, name, type, material, size, #These are base Entity arguments.
                 Str, Dex, End, Wit, Ego, sex, speed, FOVBase, addFlags = [], addIntrinsics = []):
        BlockMove = True # All mobs block movement, but not all entities,
                         # so pass this to Entity __init__
        super(Mob, self).__init__(x, y, char, color, name, type, material, size, BlockMove)

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
        self.FOVBase = FOVBase # TODO: This should depend on stats and equipment.
        #self.recalculateFOV()

        self.flags.append('MOB')
        for i in addFlags:
            self.flags.append(i)

        for (type, power) in addIntrinsics:
            NewInt = intrinsic.Intrinsic(type, 30000, power)
            self.intrinsics.append(NewInt)

        self.baseArms = 0
        self.baseLegs = 0
        self.baseWings = 0
        self.baseEyes = 0

        self.diet = [] # Filled in spawn() function.
        self.bodyparts = []
        self.gainBody()

        # Calculate stats:
        self.bonusHP = 0
        self.bonusMP = 0
        self.maxHP = 0
        self.recalculateHealth()
        self.HP = self.maxHP
        self.maxMP = 0
        self.recalculateMana()
        self.MP = self.maxMP
        self.maxSP = 0
        self.recalculateStamina()
        self.SP = self.maxSP
        # TODO: NP, pain, heat
        self.XL = 1
        self.XP = 0 # TODO

        # General:
        self.carry = 1
        self.recalculateCarryingCapacity()
        self.tactics = True # True is defensive, False aggresive.

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
            New = mutation.create_part(part, self)
            self.bodyparts.append(New)

        mutation.name_parts(self)

    def makePlayer(self):
        self.givenName = 'Adventurer'

        # Minor randomization of starting attributes:
        iteration = 0

        while iteration < 3:
            mod = random.choice([1, 1, -1])
            stat = libtcod.random_get_int(0, 1, 5)

            if stat == 1:
                self.Str += mod
            elif stat == 2:
                self.Dex += mod
            elif stat == 3:
                self.End += mod
            elif stat == 4:
                self.Wit += mod
            elif stat == 5:
                self.Ego += mod

            iteration += 1

        # TODO: Random starting inventory.

        self.recalculateAll()
        self.HP = self.maxHP
        self.MP = self.maxMP
        self.SP = self.maxSP

    def recalculateAll(self):
        #self.recalculateFOV()
        self.recalculateHealth()
        self.recalculateMana()
        self.recalculateStamina()
        self.recalculateCarryingCapacity()

    def recalculateFOV(self):
        libtcod.map_compute_fov(var.FOVMap, self.x, self.y, self.getLightRadius(), True, 0)

    def recalculateHealth(self):
        self.maxHP = max(1, ((20 * (1.2 ** self.getEnd())) + self.bonusHP))

    def recalculateMana(self):
        self.maxMP = max(0, ((20 * (1.2 ** self.getEgo())) + self.bonusMP))

    def recalculateStamina(self):
        self.maxSP = max(1, (20 * (1.2 ** self.getStr())))

    def recalculateCarryingCapacity(self):
        self.carry = max(1, 10 + (2 * self.getStr()))

    def regainHealth(self):
        if not self.hasFlag('DEAD') and self.HP < self.maxHP:
            toHeal = 0.2

            # Regeneration
            if self.hasIntrinsic('REGEN_LIFE'):
                toHeal += 0.3 * self.getIntrinsicPower('REGEN_LIFE')

            # Unhealing
            if self.hasIntrinsic('DRAIN_LIFE'):
                toHeal -= 0.3 * self.getIntrinsicPower('DRAIN_LIFE')

            # TODO:
            #  Full / Stuffed
            #  Starving

            if toHeal < 0:
                toHeal = 0
            else:
                for part in self.bodyparts:
                    if part.wounded:
                        chance = var.rand_int_from_float(toHeal + self.getEnd())
                        if var.rand_chance(chance, 1000):
                            if self.hasFlag('AVATAR'):
                                ui.message("Your %s heals." % part.getName(), libtcod.azure)

                            part.wounded = False

            if self.HP + toHeal > self.maxHP:
                self.HP = self.maxHP
            else:
                self.HP += toHeal

        # If we are somehow overhealed, loose 1 HP per round.
        if self.HP - 1 >= self.maxHP:
            self.HP -= 1

    def regainMana(self):
        if not self.hasFlag('DEAD') and self.MP < self.maxMP:
            toMana = 0.3

            # Starpower
            if self.hasIntrinsic('REGEN_MANA'):
                toMana += 0.5 * self.getIntrinsicPower('REGEN_MANA')

            # Manaburn
            if self.hasIntrinsic('DRAIN_MANA'):
                toMana -= 0.5 * self.getIntrinsicPower('DRAIN_MANA')

            if self.MP + toMana > self.maxMP:
                self.MP = self.maxMP
            elif self.MP < 0 and (self.MP + toMana) < self.MP:
                pass
            else:
                self.MP += toMana

        if self.MP - 1 >= self.maxMP:
            self.MP -= 1

    def regainStamina(self):
        if not self.hasFlag('DEAD') and self.SP < self.maxSP:
            toStamina = 1.0
            #toStamina = 0.5

            # Encumberance
            toStamina /= (self.getBurdenState() + 1)

            # Vigor
            if self.hasIntrinsic('REGEN_STAM'):
                toStamina += 0.5 * self.getIntrinsicPower('REGEN_STAM')

            # Fatigue
            if self.hasIntrinsic('DRAIN_STAM'):
                toStamina -= 0.5 * self.getIntrinsicPower('DRAIN_STAM')

            if self.SP + toStamina > self.maxSP:
                self.SP = self.maxSP
            elif self.SP < 0 and (self.SP + toStamina) < self.SP:
                pass # Do nothing, or we could increase negative stamina up to 0.
            else:
                self.SP += toStamina

        if self.SP - 1 >= self.maxSP:
            self.SP -= 1

    def regainActions(self):
        # This works even when dead, because items can have actions, too.
        speed = self.speed

        if self.hasIntrinsic('HASTE'):
            speed += self.getIntrinsicPower('HASTE') / 10
        if self.hasIntrinsic('SLOW'):
            speed += self.getIntrinsicPower('SLOW') / 10

        speed = max(0.1, speed)

        self.AP += speed

        # Energy randomization:
        if var.rand_chance(5):
            self.AP += 0.1
        elif var.rand_chance(5):
            self.AP -= 0.1

    def getStr(self):
        Str = self.Str

        # Equipment and body bonuses:
        for i in self.getEquipment():
            if not i.hasFlag('DEAD') and not i.hasFlag('BODY_PART'):
                if i.Str != 0:
                    Str += i.Str

        for i in self.bodyparts:
            if i.Str != 0:
                Str += i.Str

        # Intrinsics:
        if self.hasIntrinsic('BUFF_STRENGTH'):
            Str += self.getIntrinsicPower('BUFF_STRENGTH')
        if self.hasIntrinsic('DEBUFF_STRENGTH'):
            Str -= self.getIntrinsicPower('DEBUFF_STRENGTH')

        return Str

    def getDex(self):
        Dex = self.Dex

        # Equipment and body bonuses:
        for i in self.getEquipment():
            if not i.hasFlag('DEAD') and not i.hasFlag('BODY_PART'):
                if i.Dex != 0:
                    Dex += i.Dex

        for i in self.bodyparts:
            if i.Dex != 0:
                Dex += i.Dex

        # Intrinsics:
        if self.hasIntrinsic('BUFF_DEXTERITY'):
            Dex += self.getIntrinsicPower('BUFF_DEXTERITY')
        if self.hasIntrinsic('DEBUFF_DEXTERITY'):
            Dex -= self.getIntrinsicPower('DEBUFF_DEXTERITY')

        return Dex

    def getEnd(self):
        End = self.End

        # Equipment and body bonuses:
        for i in self.getEquipment():
            if not i.hasFlag('DEAD') and not i.hasFlag('BODY_PART'):
                if i.End != 0:
                    End += i.End

        for i in self.bodyparts:
            if i.End != 0:
                End += i.End

        # Intrinsics:
        if self.hasIntrinsic('BUFF_ENDURANCE'):
            End += self.getIntrinsicPower('BUFF_ENDURANCE')
        if self.hasIntrinsic('DEBUFF_ENDURANCE'):
            End -= self.getIntrinsicPower('DEBUFF_ENDURANCE')

        return End

    def getWit(self):
        Wit = self.Wit

        # Equipment and body bonuses:
        for i in self.getEquipment():
            if not i.hasFlag('DEAD') and not i.hasFlag('BODY_PART'):
                if i.Wit != 0:
                    Wit += i.Wit

        for i in self.bodyparts:
            if i.Wit != 0:
                Wit += i.Wit

        # Intrinsics:
        if self.hasIntrinsic('BUFF_WITS'):
            Wit += self.getIntrinsicPower('BUFF_WITS')
        if self.hasIntrinsic('DEBUFF_WITS'):
            Wit -= self.getIntrinsicPower('DEBUFF_WITS')

        return Wit

    def getEgo(self):
        Ego = self.Ego

        # Equipment and body bonuses:
        for i in self.getEquipment():
            if not i.hasFlag('DEAD') and not i.hasFlag('BODY_PART'):
                if i.Ego != 0:
                    Ego += i.Ego

        for i in self.bodyparts:
            if i.Ego != 0:
                Ego += i.Ego

        # Intrinsics:
        if self.hasIntrinsic('BUFF_EGO'):
            Ego += self.getIntrinsicPower('BUFF_EGO')
        if self.hasIntrinsic('DEBUFF_EGO'):
            Ego -= self.getIntrinsicPower('DEBUFF_EGO')

        return Ego

    def getAppearance(self): # Used for living mobs.
        pass

    def getDescription(self): # Used for corpses.
        lines = []
        underscore = "-" * 26

        lines.append("General")
        lines.append(underscore)
        lines.append("Material: %s" % self.material.lower())
        lines.append("Size    : %s" % raw.Sizes[self.size])
        lines.append("Sex     : %s" % self.sex.lower())
        lines.append("")

        lines.append("Statistics")
        lines.append(underscore)
        lines.append("Strength : %s" % str(self.getStr()))
        lines.append("Dexterity: %s" % str(self.getDex()))
        lines.append("Endurance: %s" % str(self.getEnd()))
        lines.append("Wits     : %s" % str(self.getWit()))
        lines.append("Ego      : %s" % str(self.getEgo()))
        lines.append("Speed    : %s" % str(int(self.speed * 100))) # Gah, % does not work!

        return lines

    def getAccuracyBonus(self, weapon = None, base = False):
        toHit = 0.0

        # Scaled Dex:
        DexBonus = self.getDex() * raw.Scaling[weapon.DexScaling]
        toHit += DexBonus

        if weapon != None:
            try:
                toHit += weapon.getAccuracyValue()
            except:
                pass # Body parts have no accuracy bonus.

            try:
                toHit += weapon.eyes
            except:
                pass # And items have no eyes.

        # Get equipment bonuses:
        for i in self.getEquipment():
            if not i.hasFlag('DEAD') and not i.hasFlag('BODY_PART'):
                try:
                    if i.acc != 0:
                        toHit += i.acc
                    if i.hasFlag('ENCHANT_ACCURACY'):
                        toHit += i.enchantment
                except:
                    print "Failed to add accuracy!"

        # Get terrain penalties:
        if var.getMap()[self.x][self.y].hasFlag('PIT') and not self.isFlying():
            toHit -= 3

        toHit = var.rand_int_from_float(toHit)

        if base == True:
            return toHit

        # We return at least +1 if we get positive toHit, otherwise randomly between
        # toHit and zero.
        elif toHit > 0:
            return libtcod.random_get_int(0, 1, toHit)
        else:
            return libtcod.random_get_int(0, toHit, 0)

    def getMagicBonus(self):
        # Spell to hit.
        pass

    def getDamageBonus(self, victim = None, weapon = None):
        bonus = 0.0

        # Intrinsics:
        if self.hasIntrinsic('BUFF_DAMAGE'):
            bonus += self.getIntrinsicPower('BUFF_DAMAGE')
        if self.hasIntrinsic('DEBUFF_DAMAGE'):
            bonus -= self.getIntrinsicPower('DEBUFF_DAMAGE')

        # Size difference:
        if victim != None:
            bonus += self.size - victim.size

        # Enchantment:
        if weapon != None:
            bonus += weapon.enchantment

            if weapon.hasFlag('ENCHANT_DOUBLE'):
                bonus += weapon.enchantment

        bonus = var.rand_int_from_float(bonus)

        if bonus > 0:
            return libtcod.random_get_int(0, 1, bonus)
        else:
            return libtcod.random_get_int(0, bonus, 0)

    def getDodgeBonus(self, attacker = None, weapon = None, base = False):
        toDodge = 0

        # TODO:
        # Bonus after move.
        # Unarmored / Light Armor
        # Conf, blind, cannot see attacker etc.

        toDodge += self.getDex()

        if self.tactics:
            toDodge += 1

        if self.isFlying():
            toDodge += 2

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

        # Get intrinsics:
        if self.hasIntrinsic('LEVITATION'):
            toDodge += self.getIntrinsicPower('LEVITATION')
        elif self.isFlying(): # Used when flying not through levitation.
            toDodge += 3

        # Get terrain penalties:
        if var.getMap()[self.x][self.y].hasFlag('PIT') and not self.isFlying():
            toDodge -= 3

        if base == True:
            return toDodge

        # Modify by number of adjacent walls:
        AdjacentWalls = 0
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if x in range(0, var.MapWidth) and y in range(0, var.MapHeight):
                    #if x != self.x and y != self.y:
                    if var.getMap()[x][y].BlockMove == True:
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

        if toDodge > 0:
            return libtcod.random_get_int(0, 1, toDodge)
        else:
            return libtcod.random_get_int(0, toDodge, 0)

    def getLimbToHit(self, attacker = None):
        # TODO: Maybe armor?
        choices = []

        for part in self.bodyparts:
            if attacker != None:
                chance = part.cover * (1.2 ** -abs(attacker.size - part.size))
            else:
                chance = part.cover

            if var.rand_chance(chance):
                choices.append(part)

        if len(choices) == 0:
            for part in self.bodyparts:
                if part.hasFlag('TORSO'):
                    choices.append(part)

        return random.choice(choices)

    def getLimbProtection(self, limb):
        PV = 0

        # Find what we are wearing on that limb.
        for item in limb.inventory:
            PV += item.getProtectionValue()

        # Some ther limbs may help with our PV.
        if not limb.hasFlag('TORSO'):
            if limb.hasFlag('HAND'):
                # Hands get full PV of worn gloves.
                index = self.bodyparts.index(limb)
                part = self.bodyparts[index - 1]

                if part.hasFlag('ARM'):
                    for item in part.inventory:
                        PV += item.getProtectionValue()
            else:
                # Body armor gives half its PV to all other body parts,
                # shields give thier full PV, if any.
                for part in self.bodyparts:
                    if part != limb:
                        if part.hasFlag('HAND'):
                            for item in part.inventory:
                                if item.hasFlag('SHIELD'):
                                    PV += item.getProtectionValue()
                        elif part.hasFlag('TORSO'):
                            for item in part.inventory:
                                PV += (item.getProtectionValue() / 2)

        # TODO: Magic items, natural PV.

        if self.getEnd() > 10:
            PV += (self.getEnd() - 10)

        return max(0, PV)

    def getTotalProtection(self):
        PV = 0.0

        for part in self.bodyparts:
            for item in part.inventory:
                PV += (item.getProtectionValue() * part.cover) / 100

        # TODO: Magic items.

        if self.getEnd() > 10:
            PV += (self.getEnd() - 10)

        PV = int(math.ceil(PV))

        return max(0, PV)

    def getTwoWeaponChance(self, weapon, prievous):
        try:
            AttackFlags = weapon.attack['flags']
        except:
            AttackFlags = raw.DummyAttack['flags']

        # You know what? Beer is not a good drink for coding. Really, really not.

        if 'NATURAL' in AttackFlags:
            return True

        if weapon.size > prievous.size:
            return False

        # TODO: Skills affect this.
        if var.rand_chance(30):
            print "Two-weapon chance OK:"
            return True
        else:
            return False

    def checkTwoHander(self, weapon):
        if weapon.hasFlag('TWO_HAND_OK'):
            return True

        handNo = 0

        for part in self.bodyparts:
            if part.hasFlag('GRASP'):
                if len(part.inventory) == 0:
                    handNo += 1
                else:
                    # Bucklers still count as free hand, while one-handed weapons
                    # do not count towards free hands and two-handers decrease the
                    # number of our free hands.
                    for item in part.inventory:
                        if item.hasFlag('TWO_HAND_OK'):
                            handNo += 1
                        elif item.size > self.size:
                            handNo -= 1

        if weapon.size <= self.size and handNo >= 1:
            return True
        elif weapon.size > self.size and handNo >= 2:
            return True
        else:
            return False

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
            if self.HP < (self.maxHP / 10):
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
                (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
                 AttackRange, AttackFlags, inflict, explode) = defender.getAttack()

                # TODO: Shields with inflict or explode.

                # Add strength, scaled:
                StrBonus = self.getStr() * raw.Scaling[defender.StrScaling]
                DiceValue += var.rand_int_from_float(StrBonus)

                # Calculate how much damage we can block:
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

                # Calculate stamina cost:
                staminaCost = blocked * (1.3 ** (weapon.size - defender.size))

                if defender.hasFlag('SHIELD'):
                    staminaCost /= 2

                self.SP -= max(1, staminaCost)
                # TODO: If this bring us below 0, be off-balanced.
                # TODO: Critical blocks cause off-balanced in attacker.

                # Debug:
                print "blocked %s damage, lost %s stamina" % (blocked, staminaCost)

                return damage
            else:
                self.SP -= 1 # Trying to block is exhausting anyway.
                print "Failed to block."

        return damage

    def resistDamage(self, damage, DamageType, PV = None):
        if damage <= 0:
            return 0

        resistance = 0

        # Check resistances and vulnerabilities:
        if self.hasIntrinsic(raw.ResistanceTypeList[DamageType]):
            resistance += self.getIntrinsicPower(raw.ResistanceTypeList[DamageType])
        if self.hasIntrinsic(raw.VulnerabilityTypeList[DamageType]):
            resistance -= self.getIntrinsicPower(raw.VulnerabilityTypeList[DamageType])
        if self.hasIntrinsic('FRAGILE'):
            resistance -= self.getIntrinsicPower('FRAGILE')

        print "done %s damage" % damage

        # Protection Value adds to basic resistances against physical:
        if DamageType in ['BLUNT', 'SLASH', 'PIERCE'] and PV != None:
            resistance += var.rand_int_from_float(PV / 10)

            # TODO: Rerolls for armor skills.
            blocked = libtcod.random_get_int(0, 0, PV)
            damage -= blocked

            if damage < 0:
                damage = 0

            print "   after %s PV (max %s): %s damage" % (blocked, PV, damage)

        # You take 100 % damage at 0 resistance, -20 % per point of resistance.
        resisted = damage * (0.8 ** resistance)

        # Check for immunity.
        if self.hasIntrinsic(raw.ImmunityTypeList[DamageType]):
            resisted = 0

        resisted = var.rand_int_from_float(max(0, resisted))

        print "   after resistances: %s damage" % resisted

        return resisted

    def severLimb(self, limb = None, attacker = None, DamageType = None, silent = False):
        if limb == None:
            limb = self.getLimbToHit()

        if not self.hasFlag('AVATAR') and not self.hasFlag('AI_FLEE'):
            # TODO: Panic?
            self.flags.append('AI_FLEE')

        if limb.hasFlag('CANNOT_SEVER'):
            return False

        if DamageType in raw.NonWoundingList:
            return False

        # De-equip items from the limb to be severed, then drop it on ground.
        item = limb.doDeEquip()
        if item != None:
            item.x = self.x
            item.y = self.y
            var.getEntity().append(item)

        # We need to sever the hand as well when we are severing the arm.
        # TODO: Make this work better with mutliple arms.
        if limb.hasFlag('ARM'):
            index = self.bodyparts.index(limb)
            part = self.bodyparts[index + 1]

            if part.hasFlag('HAND'):
                self.severLimb(part, attacker, silent = True)

        # TODO:
        #  Some damage types destroy limbs.
        #  Eyes on head etc.

        limb.flags.append('ITEM')

        # Name the limb after our victim:
        limb.prefix = self.getName(possessive = True)

        # Drop the limb on ground:
        self.bodyparts.remove(limb)

        limb.x = self.x
        limb.y = self.y
        var.getEntity().append(limb)

        # See what equipment bonuses changed.
        self.recalculateAll()

        if not silent:
            ui.message("%s %s is severed!" % (self.getName(True, possessive = True), limb.getName()),
                       libtcod.red, self)

        if limb.hasFlag('VITAL'):
            self.checkDeath(True, attacker)

        # And we are bleeding... but only if this is not a hand as a part of severing an arm.
        if not silent:
            self.addIntrinsic('BLEED', libtcod.random_get_int(0, 3, 8), 1)

        return True

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

    def getActionAPCost(self, modifier = 1.0):
        cost = 1

        # You will do actions slower when you loose a limb. With more base limbs, you can
        # become more slow then creature with less base limbs, because you are not
        # accustomed to having such a small number of limbs. Imagine a spider - it is not
        # faster because it only lost two legs, even if it still has six remaining.
        if self.baseArms > 0:
            cost *= 1.3 ** (self.baseArms - self.hasHands(False))
        else:
            cost *= 1.5

        cost *= 1.3 ** (self.getBurdenState())
        cost *= modifier

        return max(0.1, cost)

    def getAttackAPCost(self):
        cost = 1

        # Attack speed is not based on lost limbs, because you can attack with any limb,
        # including only body-slamming.

        cost *= 1.3 ** (self.getBurdenState())

        return max(0.1, cost)

    def getMoveAPCost(self):
        cost = 1

        # You will move slower when you loose a limb. With more base limbs, you can
        # become more slow then creature with less base limbs, because you are not
        # accustomed to having such a small number of limbs. Imagine a spider - it is not
        # faster because it only lost two legs, even if it still has six remaining.
        if self.baseLegs > 0:
            cost *= 1.3 ** (self.baseLegs - self.hasLegs(False))
        else:
            # With no legs at all (eg. slug), you move slowly.
            cost *= 1.5

        cost *= 1.3 ** (self.getBurdenState())

        if var.getMap()[self.x][self.y].hasFlag('ROUGH') and not self.isFlying():
            cost += 0.2
        if (var.getMap()[self.x][self.y].hasFlag('SWIM') and self.hasIntrinsic('SWIM') and
            not (self.isFlying() or self.hasIntrinsic('WATER_WALK'))):
            cost *= 0.8 ** self.getIntrinsicPower('SWIM')

        return max(0.1, cost)

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
            if self.prefix != "":
                name = self.prefix + " " + name
            if self.suffix != "":
                name = name + " " + self.suffix
            if self.givenName != None:
                name = self.givenName + ' the ' + name

            # Corpses:
            if self.hasFlag('ITEM') and not self.hasFlag('AVATAR'): # Check for AVATAR here,
                # Enchantment:                                      # or death screen will be
                if self.enchantment < 0:                            # screwed.
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

    def getGivenName(self):
        if self.givenName != None and self.givenName != "":
            return self.givenName.capitalize()
        else:
            return self.name.capitalize()

    def getBurdenState(self):
        if len(self.inventory) <= self.carry:
            return 0 # Unencumbered
        elif len(self.inventory) <= (self.carry * 1.5):
            return 1 # Burdened
        elif len(self.inventory) <= (self.carry * 2):
            return 2 # Strained
        else:
            return 3 # Overweight

    def getLightRadius(self):
        light = self.FOVBase

        # Intrinsics:
        if self.hasIntrinsic('BUFF_LIGHT'):
            light += self.getIntrinsicPower('BUFF_LIGHT')
        if self.hasIntrinsic('DEBUFF_LIGHT'):
            light -= self.getIntrinsicPower('DEBUFF_LIGHT')

        # Get equipment bonuses:
        for i in self.getEquipment():
            try:
                light += i.getLightValue()
            except:
                pass #print "Failed to add light radius!"

        # And special light sources that can only be carried in inventory.
        for i in self.inventory:
            if i.hasFlag('CARRY_LIGHT'):
                try:
                    lit = i.getLightValue() * i.stack
                    light += lit
                except:
                    pass

        # Modifiers:
        if self.hasIntrinsic('AFLAME'):
            light += 2

        if var.DungeonLevel == 0:
            light += 6

        if var.getMap()[self.x][self.y].hasFlag('CAN_BE_CLIMBED'):
            light += 4

        if self.hasIntrinsic('BLIND'):
            light = 1

        if var.getMap()[self.x][self.y].hasFlag('PIT') and not self.isFlying():
            light = 1

        if light <= 0: # Sadly, libtcod requires at least radius 1, because 0 or less
            light = 1  # means unlimited sight radius.

        #    if not self.hasFlag('CANNOT_SEE'):
        #        self.flags.append('CANNOT_SEE')
        #
        #elif light > 0 and self.hasFlag('CANNOT_SEE'):
        #    self.flags.remove('CANNOT_SEE')

        return light

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

    def hasHands(self, boolean = True):
        handNo = 0

        for part in self.bodyparts:
            if part.hasFlag('HAND'):
                handNo += 1

        if boolean:
            if handNo >= self.baseArms and handNo > 0:
                return True
            else:
                return False
        else:
            return handNo

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

    def hasIntrinsic(self, intrinsic):
        for i in self.intrinsics:
            if i.type == intrinsic:
                return True

        for item in self.getEquipment():
            if not item.hasFlag('DEAD') and not item.hasFlag('BODY_PART'):
                if item.hasIntrinsic(intrinsic):
                    return True

        return False

    def hasSkill(self, skill):
        if self.hasIntrinsic('AMNESIA'):
            return False

        for i in self.intrinsics:
            if i.type == skill:
                return True

        for item in self.getEquipment():
            if not item.hasFlag('DEAD') and not item.hasFlag('BODY_PART'):
                if item.hasIntrinsic(skill):
                    return True

        return False

    def getIntrinsic(self, intrinsic):
        toUse = None

        for i in self.intrinsics:
            if i.type == intrinsic:
                toUse = i

        for item in self.getEquipment():
            if not item.hasFlag('DEAD') and not item.hasFlag('BODY_PART'):
                for i in item.intrinsics:
                    if i.type == intrinsic:
                        if toUse != None:
                            if i.power > toUse.power:
                                toUse = i
                        else:
                            toUse = i

        return toUse

    def getIntrinsicPower(self, intrinsic):
        if intrinsic == None:
            return 0

        power = 0

        for i in self.intrinsics:
            if i.type == intrinsic:
                power += i.power

        if power > 0:
            power += self.enchantment

        # TODO: Maybe limit this to equipment in right slot?
        for item in self.getEquipment():
            if not item.hasFlag('DEAD') and not item.hasFlag('BODY_PART'):
                if item.hasIntrinsic(intrinsic):
                    power += item.getIntrinsicPower(intrinsic)

        return power

    def getIntrinsicsToDisplay(self, all = False):
        intrinsics = []

        for i in self.intrinsics:
            already = False
            for n in intrinsics:
                if n.type == i.type:
                    already = True

            if already:
                continue

            if not i.hasFlag('SECRET') or all == True:
                intrinsics.append(i)

        for item in self.getEquipment():
            if not item.hasFlag('DEAD') and not item.hasFlag('BODY_PART'):
                for i in item.intrinsics:
                    already = False
                    for n in intrinsics:
                        if n.type == i.type:
                            already = True

                    if already:
                        continue

                    if not i.hasFlag('SECRET') or all == True:
                        intrinsics.append(i)

        return intrinsics

    def addIntrinsic(self, type, duration, power = 0):
        # Must be special-cased because of equipment - we don't want to add intrinsics
        # from eaten corpses to our equipment, do we?
        toUse = None

        for i in self.intrinsics:
            if i.type == type:
                toUse = i

        if toUse != None:
            toUse.duration += duration / 2

            if toUse.power < power:
                toUse.power = power
            elif toUse.power == power:
                toUse.power += 1

            self.recalculateAll()
        else:
            NewInt = intrinsic.Intrinsic(type, duration, power)
            self.intrinsics.append(NewInt)

            if NewInt.color == libtcod.white:
                color = libtcod.azure
            else:
                color = NewInt.color

            # TODO: Maybe not for DEAD?
            ui.message(self.getName(True) + NewInt.begin, color, actor = self)

            self.recalculateAll()

    def removeIntrinsic(self, intrinsic, power = None):
        for i in self.intrinsics:
            if i.type == intrinsic:
                if power == None:
                    self.intrinsics.remove(i)

                    if i.type != None and not self.hasFlag('DEAD'):
                        ui.message(self.getName(True) + i.end, actor = self)
                else:
                    i.power -= power # If this results in negative power, it will
                                     # be removed by the next handling routine.
                self.recalculateAll()
                return True

        return False

    def handleIntrinsics(self):
        for i in self.intrinsics:
            if i.getHandled(self) == None:
                self.intrinsics.remove(i)

                if i.type != None and not self.hasFlag('DEAD'):
                    ui.message(self.getName(True) + i.end, actor = self)

                self.recalculateAll()

        for item in self.getEquipment():
            if not item.hasFlag('DEAD') and not item.hasFlag('BODY_PART'):
                for i in item.intrinsics:
                    if i.getHandled(self) == None:
                        item.intrinsics.remove(i)

    def isExtraFragile(self):
        if self.getEnd() < 0:
            return True
        else:
            return False

    def isInediate(self):
        if len(self.diet) == 0:
            return True
        else:
            return False

    def isFlying(self):
        if self.hasFlag('FLY') and self.hasWings(True) and self.SP > 0:
            return True

        if self.hasIntrinsic('LEVITATION'):
            return True

        return False

    def isWinner(self):
        if not self.hasFlag('AVATAR'):
            return False

        for i in self.inventory:
            if i.hasFlag('MAC_GUFFIN'):
                return True

        for i in self.getEquipment():
            if i.hasFlag('MAC_GUFFIN'):
                return True

        return False

    def willSink(self):
        # TODO
        return False

    def canBreakCurse(self, power = 0):
        # Through undeath of some skills, you may automatically break curses binding you.
        if self.hasFlag('DEAD'):
            return True
        if self.hasFlag('AVATAR') and var.WizModeActivated:
            return True
        if self.hasFlag('UNDEAD'):
            return True
        # TODO: Barbarians can tear cursed items off, taking damage based on power.
        else:
            return False

    def canSense(self, Target):
        # TODO: Blindness, invisibility, other senses, ...
        can = False

        if libtcod.map_is_in_fov(var.FOVMap, Target.x, Target.y) and not self.hasIntrinsic('BLIND'):
            can = True

        # You can always just touch it.
        if Target.x == self.x and Target.y == self.y:
            can = True

        return can

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

    def receiveAttack(self, attacker, weapon, launcher = None, multiplier = 1.0):
        # TODO: launcher
        self.target = attacker

        forcedHit = False
        forcedMiss = False
        didHit = False

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

        # Penalties.
        if not attacker.canSense(self):
            #print "Unseen defender."
            toHit -= 3 # This is rather hefty penalty, because it is applied after
                       # normally randomized bonus/penalty to accuracy.

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
                didHit = True
                color = var.TextColor
                fullStop = "."

                if forcedHit == True:
                    howWell = "easily "
                else:
                    howWell = ""

                if weapon != None:
                    (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
                     AttackRange, AttackFlags, inflict, explode) = weapon.getAttack()
                else:
                    DiceNumber = raw.Slam['DiceNumber']
                    DiceValue = raw.Slam['DiceValue']
                    DamageBonus = raw.Slam['DamageBonus']
                    DamageType = raw.Slam['DamageType']
                    AttackRange = raw.Slam['range']
                    AttackFlags = raw.Slam['AttackFlags']

                # Try crits:
                # TODO: Not sure where magical attacks will fall with this?
                if weapon == None:
                    toCrit = 15
                elif weapon.hasFlag('BODY_PART'):
                    # TODO: Martial arts should decrease this.
                    toCrit = 10
                else:
                    toCrit = 8 + (2 * weapon.size)

                # Attacker crits less often with defensive tactics:
                if attacker.tactics:
                    toCrit += 1

                CritNo = int(math.floor((toHit - toDodge) / toCrit))

                if CritNo > 0:
                    print "to crit: %s, crits: +%s" % (toCrit, CritNo)
                    DiceNumber += CritNo
                    howWell = "critically "
                    color = libtcod.yellow
                    fullStop = "!" * CritNo

                # Add strength, scaled:
                try:
                    StrBonus = attacker.getStr() * raw.Scaling[weapon.StrScaling]
                    DiceValue += var.rand_int_from_float(StrBonus)
                except:
                    print "Failed to add Str to damage."
                    pass # How do we have no attacker?

                # Add damage bonuses:
                DamageBonus += attacker.getDamageBonus(self, weapon)

                # Roll for damage:
                damage = var.rand_dice(DiceNumber, DiceValue, DamageBonus)
                damage *= multiplier

                if damage <= 0:
                    damage = 0.5

                print "rolling " + str(DiceNumber) + "d" + str(DiceValue) + "+" + str(DamageBonus)
                print "    " + str(damage) + " damage to " + limb.getName()

                # Message:
                ui.message("%s %s%s %s%s%s" % (attacker.getName(True), howWell, verb,
                           whatLimb, withWhat, fullStop), color, actor = attacker)

                # Try blocking the attack:
                if self.SP > 0:
                    if DamageType in ['BLUNT', 'SLASH', 'PIERCE']:
                        damage = self.tryBlocking(attacker, weapon, toHit, damage, forcedHit)

                if damage > 0:
                    self.receiveDamage(damage, limb, DamageType, attacker, weapon, AttackFlags)
            else:
                ui.message("%s miss&ES %s." % (attacker.getName(True), self.getName()),
                           libtcod.light_grey, actor = attacker)
        else:
            ui.message("%s completely miss&ES %s." % (attacker.getName(True), self.getName()),
                       libtcod.light_grey, actor = attacker)
            # TODO: if toHit + bonus < 0, fumble

        # Different SP cost for different weapons, but min 1 SP. We also only take
        # half SP cost for missed attacks.
        try:
            SPcost = weapon.getSPCost()
        except:
            SPcost = 2

        if didHit:
            attacker.SP -= max(1, SPcost)
            print "SP cost: %s" % SPcost
        else:
            attacker.SP -= max(1, (SPcost / 2))
            print "SP cost: %s" % max(1, (SPcost / 2))

        print "-" * 10

    def receiveDamage(self, damage, limb = None, DamageType = None, attacker = None,
                      weapon = None, AttackFlags = []):
        if limb == None:
            limb = self.getLimbToHit()

        # TODO:
        #       Pain.
        #       Armor-piercing crits.
        #       DamageType effects.

        if not DamageType in raw.DamageTypeList:
            print "Unknown damage type: %s" % DamageType
            return

        # Material intrinsics:
        modifier = 1.0

        if weapon != None:
        # Body parts are used as weapons for natural attacks, so attacker made of
        # material will also trigger this.

            # Allergies:
            if weapon.material == 'IRON' and self.hasIntrinsic('VULN_IRON'):
                modifier *= 1.3 ** self.getIntrinsicPower('VULN_IRON')
                ui.message("%s sear&S %s!" % (weapon.getName(True), self.getName()),
                           libtcod.light_red, actor = self)
            if weapon.material == 'SILVER' and self.hasIntrinsic('VULN_SILVER'):
                modifier *= 1.3 ** self.getIntrinsicPower('VULN_SILVER')
                ui.message("%s sear&S %s!" % (weapon.getName(True), self.getName()),
                           libtcod.light_red, actor = self)
            if weapon.material == 'GOLD' and self.hasIntrinsic('VULN_GOLD'):
                modifier *= 1.3 ** self.getIntrinsicPower('VULN_GOLD')
                ui.message("%s sear&S %s!" % (weapon.getName(True), self.getName()),
                           libtcod.light_red, actor = self)
            if weapon.material == 'GLASS' and self.hasIntrinsic('VULN_GLASS'):
                modifier *= 1.3 ** self.getIntrinsicPower('VULN_GLASS')
                ui.message("%s sear&S %s!" % (weapon.getName(True), self.getName()),
                           libtcod.light_red, actor = self)
            if weapon.beautitude > 0 and self.hasIntrinsic('VULN_HOLY'):
                modifier *= 1.3 ** self.getIntrinsicPower('VULN_HOLY')
                ui.message("%s sear&S %s!" % (weapon.getName(True), self.getName()),
                           libtcod.light_red, actor = self)
            if weapon.beautitude < 0 and self.hasIntrinsic('VULN_UNHOLY'):
                modifier *= 1.3 ** self.getIntrinsicPower('VULN_UNHOLY')
                ui.message("%s sear&S %s!" % (weapon.getName(True), self.getName()),
                           libtcod.light_red, actor = self)

            # Resistances:
            if weapon.material in ['BONE', 'FLESH', 'LEATHER'] and self.hasIntrinsic('RESIST_MEAT'):
                modifier *= 0.7 ** self.getIntrinsicPower('RESIST_MEAT')
            if weapon.material in ['GOLD', 'IRON', 'SILVER'] and self.hasIntrinsic('RESIST_METAL'):
                modifier *= 0.7 ** self.getIntrinsicPower('RESIST_METAL')
            if weapon.material in ['CLAY', 'STONE'] and self.hasIntrinsic('RESIST_EARTH'):
                modifier *= 0.7 ** self.getIntrinsicPower('RESIST_EARTH')
            if weapon.material in ['PAPER', 'PLANT', 'WOOD'] and self.hasIntrinsic('RESIST_WOOD'):
                modifier *= 0.7 ** self.getIntrinsicPower('RESIST_WOOD')
            if weapon.beautitude == 0 and self.hasIntrinsic('RESIST_MUNDANE'):
                modifier *= 0.7 ** self.getIntrinsicPower('RESIST_MUNDANE')

        damage *= modifier

        # Resistances:
        if DamageType in ['BLUNT', 'SLASH', 'PIERCE']:
            damage = self.resistDamage(damage, DamageType, self.getLimbProtection(limb))
        else:
            damage = self.resistDamage(damage, DamageType)

        if damage > 0:
            # Inflict effects of the attack:
            if weapon != None:
                try:
                     inflict = weapon.attack['inflict']
                except:
                    inflict = None

                if inflict != None:
                    for (intrinsic, DiceNumber, DiceValue, Bonus, power, chance) in inflict:
                        if var.rand_chance(chance) == True:
                            print "inflict %s" % intrinsic

                            duration = var.rand_dice(DiceNumber, DiceValue, Bonus)

                            try:
                                exec(power)
                            except:
                                pass

                            self.addIntrinsic(intrinsic, duration, power)

            # Wound the limb:
            if not DamageType in raw.NonWoundingList:
                if var.rand_chance(damage) or (weapon != None and 'VORPAL' in AttackFlags):
                    if limb.wounded or self.isExtraFragile():
                        # We sever the limb, but this also means we can no longer use it
                        # for further methods, as it's not attached.
                        if not self.severLimb(limb, attacker, DamageType):
                            self.addIntrinsic('BLEED', max(5, damage), libtcod.random_get_int(0, 1, damage))
                        else:
                            limb = None
                    else:
                        limb.wounded = True
                        ui.message("%s %s is wounded." % (self.getName(True, possessive = True), limb.getName()),
                                   libtcod.light_red, self)

            # TODO: Explode, next attack (through AttackFlags).

        # We might have alredy died here.
        if self.hasFlag('DEAD'):
            return

        # Additional attacks through flags.
        if 'FLAME' in AttackFlags: # Flaming adds 1d3 fire damage.
            print "Adding flaming damage."

            damage += self.resistDamage(libtcod.random_get_int(0, 1, 3), 'FIRE')
            color = var.TextColor
            fullStop = "."

            if weapon != None:
                if var.rand_chance(weapon.enchantment):
                    self.addIntrinsic('AFLAME', var.rand_dice(1, 4, 1), 1)
                    color = libtcod.light_red
                    fullStop = "!"

            if attacker != None:
                ui.message("%s burn&S %s%s" % (attacker.getName(True), self.getName(), fullStop), color, attacker)
            else:
                ui.message("%s &ISARE burned%s" % (self.getName(True), fullStop), color, self)

        if 'ICE' in AttackFlags: # Ice adds 1d3 cold damage.
            print "Adding cold damage."

            damage += self.resistDamage(libtcod.random_get_int(0, 1, 3), 'COLD')
            color = var.TextColor
            fullStop = "."

            # TODO: Freeze them solid.
            #if weapon != None:
            #    if var.rand_chance(weapon.enchantment):
            #        self.addIntrinsic('AFLAME', var.rand_dice(1, 4, 1), 1)
            #        color = libtcod.light_red
            #        fullStop = "!"

            if attacker != None:
                ui.message("%s freeze&S %s%s" % (attacker.getName(True), self.getName(), fullStop), color, attacker)
            else:
                ui.message("%s &ISARE chilled%s" % (self.getName(True), fullStop), color, self)

        if 'STEAL_LIFE' in AttackFlags: # Vampiric weapon.
            print "Vampiric."

            if damage > 0 and attacker != None and not self.hasIntrinsic('BLOODLESS') and not self.hasFlag('UNDEAD'):
                drain = libtcod.random_get_int(0, 0, damage)

                if drain > 0:
                    attacker.receiveHeal(drain)
                    ui.message("%s drain&S %s lifeblood." % (attacker.getName(True), self.getName(possessive = True)),
                               libtcod.light_red, attacker)

        if 'STEAL_MANA' in AttackFlags: # Blood magic weapon.
            print "Blood magic."

            if damage > 0 and attacker != None and not self.hasIntrinsic('BLOODLESS') and not self.hasFlag('UNDEAD'):
                drain = libtcod.random_get_int(0, 0, damage)

                if drain > 0:
                    attacker.receiveMana(drain)
                    ui.message("%s drain&S %s lifeforce." % (attacker.getName(True), self.getName(possessive = True)),
                               libtcod.light_red, attacker)

        if 'DAMAGE_MANA' in AttackFlags: # Wyrdish anti-magic weapon.
            if damage > 0:
                self.MP -= libtcod.random_get_int(0, 1, damage)
                ui.message("%s can smell the aether burning in &POSS veins." % self.getName(True),
                           libtcod.light_red, self)

        if damage > 0:
            # We get instakilled by enough damage.
            # TODO: Maybe the AVATAR is extempt?
            if damage >= (self.maxHP * 2):
                self.HP == 0
                self.checkDeath(True, attacker)
                return

            # Some damage types cannot sever limbs:
            if not DamageType in raw.NonWoundingList:
                if self.HP < damage:
                    # We can loose a limb instead of dying. We still take some damage
                    # if enough is dealt.
                    if self.severLimb(limb, attacker, DamageType):
                        if damage > self.maxHP:
                            damage /= 2
                        else:
                            return # Take no damage here.

            # Special messages:
            if DamageType == 'BLEED':
                ui.message("%s bleed&S." % self.getName(True), libtcod.light_red, self)

            # TODO: Second chance.

            self.HP -= damage
            self.checkDeath(killer = attacker)
        elif not DamageType in ['BLEED', 'POISON']:
            ui.message("%s &ISARE not hurt." % self.getName(True), actor = self)

    def checkDeath(self, forceDie = False, killer = None):
        # TODO: Life saving.

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
            # TODO: Special messages for different creatures and limbs lost.
            ui.message("%s die&S." % self.getName(True), libtcod.red, self)

            self.flags.append('DEAD')

            # Drop all equipped and carried items.
            for part in self.bodyparts:
                item = part.doDeEquip()

                if item != None:
                    self.inventory.append(item)
                    item.tryStacking(self)

            self.actionDrop(True)

            self.flags.remove('MOB')
            self.flags.append('ITEM')

            if self.hasFlag('AVATAR'):
                # TODO: WizMode can prevent death.
                game.save() # No savescumming for you! (Unless you prepare for this, of course.)
                ai.waitForMore(self)
                var.WizModeTrueSight = True
                ui.message("You have failed in your quest! You can (L)ook around, or (Ctrl + q)uit the game.")

            self.char = '%'
            self.color = libtcod.red
            self.name = str(self.name + ' corpse')
            self.BlockMove = False

            for i in var.getEntity():
                if i.target == self:
                    i.target = None

            # TODO: Give XP.
            return True
        else:
            return False

    # Actions:
    def actionApply(self, item, dx, dy):
        # Prevent weird cases:
        if self.AP < 1:
            return False
        if self.hasHands(False) == 0:
            if self.hasFlag('AVATAR'):
                ui.message("You cannot use items with no hands.")
            return False

        if dx == 0 and dy == 0:
            toApply = item.removeFromStack()

            if toApply == None:
                toApply = item

            if toApply.beApplied(self):
                self.AP -= self.getActionAPCost()
                return True
            else:
                if toApply != item:
                    toApply.tryStacking(self)
                return False
        else:
            Target = None
            x = self.x + dx
            y = self.y + dy

            for mob in var.getEntity():
                if mob.x == x and mob.y == y and mob.hasFlag('MOB'):
                    Target = mob
                    break

        if Target == None:
            if self.hasFlag('AVATAR'):
                ui.message("No one is there.")
            return False
        else:
            if item.beApplied(self, Target):
                self.AP -= self.getActionAPCost()
                return True

        return False

    def actionAttack(self, dx, dy, victim):
        # Set our victim as AI target:
        self.target = victim

        # Prevent weird cases:
        if self.AP < 1:
            return False
        if self.SP <= 0:
            if self.hasFlag('AVATAR'):
                ui.message("You are too exhausted to fight.", color = libtcod.light_red)
            return False
        if self.getBurdenState() == 3:
            if self.hasFlag('AVATAR'):
                ui.message("You carry too much to fight.", color = libtcod.light_red)
            return False
        if not victim.hasFlag('MOB'):
            if self.hasFlag('AVATAR'):
                ui.message("You can only attack creatures.")
            return False

        # TODO: This does not work well!
        primaryAttacks = []
        secondaryAttacks = []
        tertiaryAttacks = []

        weapons = False

        for i in self.bodyparts:
            if i.hasFlag('GRASP'):
                if len(i.inventory) > 0:
                    for n in i.inventory: # If this produces more than one weapon, we have a bug in equipping.
                        if n.canAttack():
                            primaryAttacks.append(n)

                    weapons = True

            if i.hasFlag('HAND'):
                if weapons == False:
                    # You attack unarmed only if you are wielding no weapons.
                    primaryAttacks.append(i)
                else:
                    tertiaryAttacks.append(i)

            elif i.hasFlag('LEG'):
                if (self.hasFlag('USE_LEGS') or
                    (self.hasHands(False) == 0 and not (self.hasFlag('USE_HEAD') or self.hasFlag('USE_NATURAL')))):
                    primaryAttacks.append(i)
                else:
                    secondaryAttacks.append(i)

                # TODO: Kicking with boots.

            elif i.hasFlag('HEAD'):
                if self.hasFlag('USE_HEAD') or (self.hasHands(False) == 0 and self.hasLegs() == False):
                    primaryAttacks.append(i)
                else:
                    tertiaryAttacks.append(i)

            elif i.hasFlag('TAIL') or i.hasFlag('WING'):
                if self.hasFlag('USE_NATURAL'):
                    primaryAttacks.append(i)
                else:
                    tertiaryAttacks.append(i)

            else:
                tertiaryAttacks.append(i)

        # We will use the first available attack category.
        attacks = None

        if not len(primaryAttacks) == 0:
            attacks = primaryAttacks
        elif not len(secondaryAttacks) == 0:
            attacks = secondaryAttacks
        elif not len(tertiaryAttacks) == 0:
            attacks = tertiaryAttacks
        else:
            ui.message("%s flail&S ineffectually at %s." % (self.getName(True), victim.getName()), actor = self)
            self.AP -= self.getAttackAPCost()
            return True

        # Get multiplier:
        multiplier = 1.0
        # TODO: charging etc.

        attackNo = 0

        for i in attacks:
            if self.SP < 0:
                break
            if victim.hasFlag('DEAD'):
                break

            prievous = attacks[attackNo - 1]
            if attackNo > 0 and not self.getTwoWeaponChance(i, prievous):
                continue

            victim.receiveAttack(self, i, multiplier = multiplier)
            attackNo += 1

        self.AP -= self.getAttackAPCost()
        # self.NP -= 5
        return True

    def actionBump(self, dx, dy):
        if self.AP < 1:
            return False

        bumpee = None
        x = self.x + dx
        y = self.y + dy

        for i in var.getEntity():
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
                    # TODO: Chatting etc.
                    self.actionWait()
                    return True

        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            # First try opening doors.
            if var.getMap()[x][y].hasFlag('CAN_BE_OPENED'):
                if(self.actionOpen(x, y)):
                    return True

            # Here we want fallthrough with if instead of elif,
            # because we want to chop stuck doors when actionOpen fails.
            # EDIT: We cannot do that, or we'll be automatically chopping down
            # bookshelves any time we try to loot them. :/
            elif self.isBlocked(x, y, var.DungeonLevel, False):
                if var.getMap()[x][y].beDug(self):
                    self.SP -= 10
                    var.changeFOVMap(x, y)
                    return True

                # Try closing adjacent doors.
                for n in range(y - 1, y + 2):
                    for m in range(x - 1, x + 2):
                        if (m > 0 and m < var.MapWidth - 1 and
                            n > 0 and n < var.MapHeight - 1):
                            if var.getMap()[m][n].hasFlag('CAN_BE_CLOSED'):
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

            for i in var.getEntity():
                if i.x == x and i.y == y:
                    blocked = True
                    break

            if not blocked == True and var.getMap()[x][y].hasFlag('CAN_BE_CLOSED'):
                if var.getMap()[x][y].hasFlag('DOOR'):
                    # Fail to close door sometimes.
                    if var.rand_chance(20 - self.getStr()) or self.SP < 0:
                        ui.message("%s fail&S to close the %s." % (self.getName(True), var.getMap()[x][y].getName()),
                                   libtcod.light_red, actor = self)
                        self.AP -= self.getActionAPCost()
                        return True

                    ui.message("%s close&S the %s." % (self.getName(True), var.getMap()[x][y].getName()), actor = self)

                    if var.getMap()[x][y].material == 'IRON':
                        var.getMap()[x][y].change(raw.ClosedPort)
                        self.SP -= 2
                    elif var.getMap()[x][y].material == 'GOLD':
                        var.getMap()[x][y].change(raw.ClosedGoldDoor)
                        self.SP -= 4
                    else:
                        var.getMap()[x][y].change(raw.WoodDoor)
                        self.SP -= 1

                    var.changeFOVMap(x, y)
                    self.AP -= self.getActionAPCost()
                    return True
                else:
                    print "BUG: Unhandled closeable terrain."
            elif var.getMap()[x][y].hasFlag('CAN_BE_CLOSED') and self.hasFlag('AVATAR'):
                ui.message("There is something in the way.")
            elif self.hasFlag('AVATAR'):
                ui.message("There is nothing to close.")
        return False

    def actionClimb(self, dz):
        if self.AP < 1:
            return False
        if self.getBurdenState() == 3:
            if self.hasFlag('AVATAR'):
                ui.message("You cannot climb with so much load.", color = libtcod.light_red)
            return False
        if (self.hasHands(False) == 0 or self.hasLegs(False) == 0) and dz > 0:
            # This prevents us from climbing upwards with no limbs left. We can still
            # "fall" down, though.
            if self.hasFlag('AVATAR'):
                ui.message("You cannot climb with no limbs.", color = libtcod.light_red)
            return False
        if self.SP < 5:
            ui.message("%s &ISARE too tired to climb the stairs." % self.getName(True), actor = self)
            self.AP -= self.getMoveAPCost()
            return False

        if dz > 0 and var.getMap()[self.x][self.y].hasFlag('STAIRS_UP'):
            # Block upstairs on first level.
            if var.DungeonLevel == 1:
                if not self.isWinner():
                    ui.message("You cannot escape with the Seal of Unwept Tears still in place!", color = libtcod.azure)
                    return False
                else:
                    ui.message("Congratulations! You won!", color = libtcod.azure)

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
                var.getEntity().remove(self)
                var.DungeonLevel -= 1

                if self.hasFlag('AVATAR'):
                    game.save()           # This is to prevent crashes from completely erasing
                    var.calculateFOVMap() # all progress you had.
                    libtcod.console_clear(var.MapConsole)

                ui.message("%s climb&S the stairs." % self.getName(True), actor = self)
                self.SP -= 8 # It's a bit more tiring to go upstairs.
                self.AP -= self.getMoveAPCost()
                return True
            else:
                ui.message("The stairs lead nowhere!", actor = self)
                return False
        elif dz < 0 and var.getMap()[self.x][self.y].hasFlag('STAIRS_DOWN'):
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
                var.getEntity().remove(self)
                var.DungeonLevel += 1

                if self.hasFlag('AVATAR'):
                    game.save()
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
            # TODO: Trees, pits.
            for n in range(self.y - 1, self.y + 2):
                for m in range(self.x - 1, self.x + 2):
                    if (m > 0 and m < var.MapWidth - 1 and
                        n > 0 and n < var.MapHeight - 1):
                        if var.getMap()[m][n].hasFlag('CAN_BE_CLIMBED'):
                            if dz > 0 and var.getMap()[m][n].BlockMove:
                                # This is mostly for climbing adjacent trees.
                                climb = False
                                tree = var.getMap()[m][n].name

                                if self.hasFlag('AVATAR'):
                                    climb = ai.askForConfirmation(self, "Do you want to climb the %s?" % tree)
                                else:
                                    climb = True

                                if climb:
                                    self.move(m - self.x, n - self.y)
                                    self.SP -= 5
                                    self.AP -= self.getMoveAPCost()
                                    ui.message("%s climb&S the %s." % (self.getName(True), tree), actor = self)
                                    return True
                            elif dz < 0:
                                # TODO: Safely climb down pits.
                                pass

            if dz > 0:
                ui.message("%s jump&S up and down." % self.getName(True), actor = self)
            elif dz < 0:
                ui.message("%s crouch&ES a bit." % self.getName(True), actor = self)
            self.AP -= self.getMoveAPCost()
            return True

    def actionDig(self, dx, dy):
        if self.SP <= 0:
            if self.hasFlag('AVATAR'):
                ui.message("You are too exhausted to do that.")
            return False

        if var.getMap()[self.x + dx][self.y + dy].beDug(self):
            self.SP -= 10
            var.changeFOVMap(self.x + dx, self.y + dy)
            return True
        else:
            ui.message("%s fail&S in &POSS labour." % self.getName(True), actor = self)

        return False

    def actionDrop(self, dropAll = False, what = None):
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
                var.getEntity().append(item)
                item.tryStacking()
                # Used only on death, so no AP nor drop messages.
        else:
            if what != None:
                toDrop = self.inventory.index(what)
            elif not self.hasFlag('AVATAR'):
                toDrop = libtcod.random_get_int(0, 0, len(self.inventory) - 1)
            else:
                toDrop = ui.item_menu("Drop what?", self.inventory)

            if toDrop == None:
                return False
            else:
                item = self.inventory[toDrop]

                self.inventory.remove(item)

                item.x = self.x
                item.y = self.y
                var.getEntity().append(item)
                item.tryStacking()

                ui.message("%s drop&S %s." % (self.getName(True), item.getName()),
                           actor = self)

                self.AP -= self.getActionAPCost(0.3) # It's quick.

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

        for i in var.getEntity():
            if i.x == x and i.y == y:
                if i.hasFlag('ITEM'):
                    if self.actionLoot(where):
                        return True
                    elif self.actionPickUp(x, y):
                        return True
                    else:
                        return False
                elif i.hasFlag('MOB') and i != self:
                    # TODO:
                    #if self.hasFlag('AVATAR'):
                    #    i.selectAction(self)
                    if not self.hasFlag('AVATAR') and not i.hasFlag('AVATAR'):
                        ui.message("%s chat&S with %s." % (self.getName(True), i.getName()),
                                   actor = self)
                    self.AP -= self.getActionAPCost()
                    return True

        if var.getMap()[x][y].hasFlag('CONTAINER'):
            if self.actionLoot(where):
                return True
            return False
        elif var.getMap()[x][y].hasFlag('CAN_BE_OPENED'):
            if self.actionOpen(x, y):
                return True
            return False
        elif var.getMap()[x][y].hasFlag('CAN_BE_CLOSED'):
            if self.actionClose(x, y):
                return True
            return False
        elif var.getMap()[x][y].hasFlag('CAN_BE_CLIMBED'):
            tree = var.getMap()[x][y].name

            if self.SP < 5:
                ui.message("%s &ISARE too tired to climb the %s." % (self.getName(True), tree), actor = self)
                return False
            else:
                ui.message("%s climb&S the %s." % (self.getName(True), tree), actor = self)

            self.move(x - self.x, y - self.y)
            self.SP -= 5
            self.AP -= self.getMoveAPCost()
            return True

        # TODO: More actions.
        return False

    def actionInventory(self):
        if len(self.inventory) == 0:
            ui.message("You carry no items.")
            return False
        else:
            describe = ui.inventory_menu(self)

            if describe == None:
                return False
            else:
                try:
                    ui.item_description(self.inventory[describe])
                except:
                    pass # Out-of-bounds.
            return True

    def actionAutoEquip(self, forced = False):
        for part in self.bodyparts:
            slot = part.getSlot()

            for item in self.inventory:
                if item.getSlot() == slot:
                    if len(part.inventory) != 0:
                        for equip in part.inventory:
                            cool = equip.getCoolness()

                            if equip.material == 'IRON' and self.hasIntrinsic('VULN_IRON'):
                                cool = -5
                            elif equip.material == 'GOLD' and self.hasIntrinsic('VULN_GOLD'):
                                cool = -5
                            elif equip.material == 'SILVER' and self.hasIntrinsic('VULN_SILVER'):
                                cool = -5
                            elif equip.material == 'GLASS' and self.hasIntrinsic('VULN_GLASS'):
                                cool = -5
                            elif equip.beautitude > 0 and self.hasIntrinsic('VULN_HOLY'):
                                cool = -5
                            elif equip.beautitude < 0 and self.hasIntrinsic('VULN_UNHOLY'):
                                cool = -5
                    elif part.hasFlag('GRASP'):
                        cool = part.getCoolness()
                    else:
                        cool = -1

                    itemCool = item.getCoolness()

                    if item.size != part.size and slot != 'GRASP':
                        if forced:
                            item.size = part.size
                        else:
                            itemCool = -2

                    if item.material == 'IRON' and self.hasIntrinsic('VULN_IRON'):
                        itemCool = -5
                    elif item.material == 'GOLD' and self.hasIntrinsic('VULN_GOLD'):
                        itemCool = -5
                    elif item.material == 'SILVER' and self.hasIntrinsic('VULN_SILVER'):
                        itemCool = -5
                    elif item.material == 'GLASS' and self.hasIntrinsic('VULN_GLASS'):
                        itemCool = -5
                    elif item.beautitude > 0 and self.hasIntrinsic('VULN_HOLY'):
                        itemCool = -5
                    elif item.beautitude < 0 and self.hasIntrinsic('VULN_UNHOLY'):
                        itemCool = -5

                    if itemCool > cool:
                        if slot == 'GRASP':
                            if not self.checkTwoHander(item):
                                continue

                        equip = part.doDeEquip(self)
                        if equip != None:
                            self.inventory.append(equip)
                            equip.tryStacking(self)

                            if not forced:
                                self.AP -= self.getActionAPCost()

                        if len(part.inventory) != 0:
                            continue

                        toEquip = item.removeFromStack()

                        if toEquip == None:
                            toEquip = item

                        if part.doEquip(toEquip) == True:
                            ui.message("%s equip&S %s." % (self.getName(True), item.getName()), actor = self)

                            try:
                                self.inventory.remove(toEquip)
                            except:
                                pass # This happens when toEquip was split from our inventory and not appended in it.

                            if not forced:
                                self.AP -= self.getActionAPCost()
                        else:
                            ui.message("%s fail&S to equip %s." % (self.getName(True), item.getName()), actor = self)

                            if toEquip != item:
                                toEquip.tryStacking(self)

                            if not forced:
                                self.AP -= self.getActionAPCost()
                            if not self.hasFlag('AVATAR'):
                                self.actionDrop(what = item)
                    elif cool < 0:
                        # De-equip and not cool items.

                        equip = part.doDeEquip(self)
                        if equip != None:
                            self.inventory.append(equip)
                            equip.tryStacking(self)

                            if not forced:
                                self.AP -= self.getActionAPCost()

        self.recalculateAll()
        return True # Just for the good sleep of mine.

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
                item = self.bodyparts[part].doDeEquip(self)

                if item != None:
                    self.inventory.append(item)
                    item.tryStacking(self)

                    self.AP -= self.getActionAPCost()
                else:
                    ui.render_all(self)

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

                if len(options) == 0:
                    ui.message("You carry nothing to equip on that body part.", actor = self)
                    ui.render_all(self)
                    return True
                else:
                    item = ui.item_menu("Equip what?", options)

                    if item == None:
                        return True

                    # Items of size larger than self are two-handed and can block
                    # other items from being wielded.
                    if slot == 'GRASP':
                        if not self.checkTwoHander(options[item]):
                            ui.message("Your hands are already full.")
                            ui.render_all(self)
                            return True

                    toEquip = options[item].removeFromStack()

                    if toEquip == None:
                        toEquip = options[item]

                    if self.bodyparts[part].doEquip(toEquip, self) == True:
                        try:
                            self.inventory.remove(toEquip)
                        except:
                            pass

                        self.AP -= self.getActionAPCost()
                        return True
                    else:
                        if toEquip != options[item]:
                            toEquip.tryStacking(self)

                        ui.message("You fail to equip %s." % options[item].getName())
                        ui.render_all(self)
                        return True

    def actionJump(self, where):
        if self.AP < 1:
            return False
        if self.getBurdenState() >= 2:
            if self.hasFlag('AVATAR'):
                ui.message("You cannot jump with so much load.", color = libtcod.light_red)
            return False
        if self.SP <= 5:
            if self.hasFlag('AVATAR'):
                ui.message("You are too exhausted to jump.")
            return False
        if (var.getMap()[self.x][self.y].hasFlag('STICKY') or ((var.getMap()[self.x][self.y].hasFlag('SWIM') or
            var.getMap()[self.x][self.y].hasFlag('WADE')) and not self.hasIntrinsic('WATER_WALK')) or
            (var.getMap()[self.x][self.y].hasFlag('PIT') and self.isFlying())):
            if self.hasFlag('AVATAR'):
                ui.message("You cannot jump in %s." % var.getMap()[self.x][self.y].getName(), color = libtcod.light_red)
            return False # Not even with flying, because you need some solid ground.

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
        if (var.getMap()[self.x][self.y].hasFlag('PIT') and
            not self.isBlocked(nx, ny, var.DungeonLevel) and
            libtcod.map_is_in_fov(var.FOVMap, nx, ny)):
            ui.message("%s jump&S out of the pit." % self.getName(True), actor = self)
            self.move(dx, dy)
            moved = True
        elif (not self.isBlocked(nx, ny, var.DungeonLevel) and
              not self.isBlocked(nnx, nny, var.DungeonLevel) and
              libtcod.map_is_in_fov(var.FOVMap, nnx, nny)):
            ui.message("%s leap&S." % self.getName(True), actor = self)
            self.move(dx * 2, dy * 2)
            moved = True
        elif (self.isFlying() and not var.Maps[var.DungeonLevel][nx][ny].BlockMove and
              not self.isBlocked(nnx, nny, var.DungeonLevel) and
              libtcod.map_is_in_fov(var.FOVMap, nnx, nny)):

              whom = None
              for i in var.Entities[var.DungeonLevel]:
                  if i != self and i.BlockMove and i.x == nx and i.y == ny:
                      whom = i
                      break

              if whom != None:
                  ui.message("%s leap&S over %s." % (self.getName(True), whom.getName()), actor = self)
                  self.move(dx * 2, dy * 2)
                  moved = True
              else: # How did this happen?
                  ui.message("%s leap&S." % self.getName(True), actor = self)
                  self.move(dx * 2, dy * 2)
                  moved = True
        else:
            ui.message("%s balk&S at the leap." % self.getName(True), actor = self)

        self.AP -= self.getMoveAPCost()
        self.SP -= 5
        # self.NP -= 10
        return moved

    def actionLoot(self, where, silent = False):
        #if self.getBurdenState() == 3:
        #    if self.hasFlag('AVATAR') and not silent:
        #        ui.message("Your inventory is already full.")
        #    return False
        #if not self.hasFlag('AVATAR'):
        #    pickAll = True

        options = []

        if where == 'self':
            for i in self.inventory:
                if i.hasFlag('CONTAINER'):
                    options.append(i)
        else:
            dx = where[0]
            dy = where[1]
            dz = where[2]

            if dx != 0 or dy != 0:
                x = self.x + dx
                y = self.y + dy

                for i in var.getEntity():
                    if i.hasFlag('CONTAINER') and i.x == x and i.y == y:
                        options.append(i)

                if var.getMap()[x][y].hasFlag('CONTAINER'):
                    options.append(var.getMap()[x][y])
            elif dz < 0:
                x = self.x
                y = self.y

                for i in var.getEntity():
                    if i.hasFlag('CONTAINER') and i.x == x and i.y == y:
                        options.append(i)

                if var.getMap()[x][y].hasFlag('CONTAINER'):
                    options.append(var.getMap()[x][y])
            else:
                if self.hasFlag('AVATAR') and not silent:
                    ui.message("There is nothing to loot there.")
                return False

        if len(options) == 0:
            if self.hasFlag('AVATAR') and not silent:
                ui.message("You find nothing to loot.")
            return False
        else:
            if self.hasFlag('AVATAR'):
                toLoot = ui.item_menu("Loot what?", options)
            else:
                toLoot = libtcod.random_get_int(0, 0, len(options))

            if toLoot == None:
                return False
            else:
                try:
                    container = options[toLoot]
                except: # Out-of-bounds option.
                    ui.message("%s fail&S in looting." % self.getName(True), actor = self)
                    return False

                if container != None:
                    if self.hasFlag('AVATAR') and len(self.inventory) > 0:
                        if ai.askForConfirmation(self, "Do you want to put something in the %s?" % container.getName()):
                            while container.beStored(self):
                                pass

                            return True

                    while container.beLooted(self):
                        pass # Continue looting.

                    if not self.hasFlag('AVATAR'):
                        ui.message("%s loot&S the %s." % (self.getName(True), options[toLoot].getName()), actor = self)
                    return True

    def actionOpen(self, x, y):
        if self.AP < 1:
            return False

        if (x > 0 and x < var.MapWidth - 1 and y > 0 and y < var.MapHeight - 1):
            if var.getMap()[x][y].hasFlag('CAN_BE_OPENED'):
                if var.getMap()[x][y].hasFlag('DOOR'):
                    # Fail to open door sometimes.
                    if var.rand_chance(20 - self.getStr()) or self.SP < 0:
                        ui.message("%s fail&S to open the %s." % (self.getName(True), var.getMap()[x][y].getName()),
                                   libtcod.light_red, actor = self)
                        self.AP -= self.getActionAPCost()
                        return True

                    # Blocked door will only appear in vault where we want to keep
                    # monsters inside.
                    if var.getMap()[x][y].hasFlag('BLOCKED') and not self.hasFlag('AVATAR'):
                        return False
                    elif var.getMap()[x][y].hasFlag('BLOCKED'):
                        var.getMap()[x][y].flags.remove('BLOCKED')

                    # TODO: LOCKED flag.
                    if var.getMap()[x][y].hasFlag('SECRET'):
                        ui.message("%s discover&S a secret door!" % self.getName(True), # % (self.getName(True), var.getMap()[x][y].getName()),
                                   libtcod.azure, actor = self)

                    ui.message("%s open&S the %s." % (self.getName(True), var.getMap()[x][y].getName()), actor = self)

                    if var.getMap()[x][y].material == 'IRON':
                        var.getMap()[x][y].change(raw.OpenPort)
                        self.SP -= 2
                    elif var.getMap()[x][y].material == 'GOLD':
                        var.getMap()[x][y].change(raw.OpenGoldDoor)
                        self.SP -= 4
                    else:
                        var.getMap()[x][y].change(raw.OpenDoor)
                        self.SP -= 1

                    var.changeFOVMap(x, y)
                    self.AP -= self.getActionAPCost()
                    return True
                elif var.getMap()[x][y].hasFlag('CONTAINER'):
                    if self.actionLoot([x - self.x, y - self.y, 0]):
                        return True
                    return False
                else:
                    print "BUG: Unhandled openable terrain."
            elif self.hasFlag('AVATAR'):
                ui.message("There is nothing to open.")
        return False

    def actionPickUp(self, x, y, pickAll = False):
        #if self.AP < 1:
        #    return False
        if not dungeon.isOnMap(x, y):
            return False
        if self.getBurdenState() == 3:
            if self.hasFlag('AVATAR'):
                ui.message("Your inventory is already full.")
            return False
        if not self.hasFlag('AVATAR'):
            pickAll = True

        options = []

        for i in var.getEntity():
            if i.hasFlag('ITEM') and i.x == x and i.y == y:
                options.append(i)

        if len(options) == 0 and var.getMap()[x][y].hasFlag('LIQUID') and len(var.getMap()[x][y].inventory) != 0:
            options = var.getMap()[x][y].inventory
            pickAll = False
            liquid = True
        else:
            liquid = False

        if len(options) == 0:
            if self.hasFlag('AVATAR'):
                quips = [
                "You grope foolishly on the floor.",
                "There is nothing to pick up.",
                "You return emtpy-handed."
                ]
                ui.message(random.choice(quips))

            self.AP -= self.getActionAPCost(0.5)
            return False
        elif pickAll == True:
            # TODO: Not if monsters in sight?
            carry = self.getBurdenState()

            for i in options:
                if self.getBurdenState() != carry:
                    #ui.message("%s cannot pick up any more items." % self.getName(True), actor = self)
                    break

                self.inventory.append(i)
                i.tryStacking(self)
                var.getEntity().remove(i)
                ui.message("%s pick&S up %s." % (self.getName(True), i.getName()), actor = self)
                self.AP -= self.getActionAPCost()

            return True
        else:
            if not self.hasFlag('AVATAR'):
                return False

            if liquid:
                pickUpLine = "What do you want to fish out of %s?" % var.getMap()[x][y].getName()
            else:
                pickUpLine = "Pick up what?"

            toPick = ui.item_menu(pickUpLine, options)

            if toPick == None:
                return False
            else:
                if liquid:
                    ui.message("%s fish&ES out %s." % (self.getName(True), options[toPick].getName()),
                               actor = self)

                    self.inventory.append(options[toPick])
                    options[toPick].tryStacking(self)
                    var.getMap()[x][y].inventory.remove(options[toPick])
                    self.AP -= self.getActionAPCost(2)
                else:
                    ui.message("%s pick&S up %s." % (self.getName(True), options[toPick].getName()),
                               actor = self)

                    self.inventory.append(options[toPick])
                    options[toPick].tryStacking(self)
                    var.getEntity().remove(options[toPick])
                    self.AP -= self.getActionAPCost()

        if len(options) > 1:
            return True
        else:
            return False # Closes window after picking up the only item on ground.

    def actionPossess(self, x, y):
        if self.hasFlag('AVATAR'):
            for i in var.getEntity():
                if i.x == x and i.y == y and i.hasFlag('MOB'):
                    self.flags.remove('AVATAR')
                    i.flags.append('AVATAR')
                    ui.message("You possess %s." % i.getName(), libtcod.chartreuse)
            return True
        else:
            # TODO
            return False


    def actionPush(self, dx, dy):
        pass

    def actionQuaff(self):
        if self.isInediate():
            if self.hasFlag('AVATAR'):
                ui.message("You cannot drink.")
            return False

        options = []

        for i in self.inventory:
            if i.hasFlag('POTION'):
                options.append(i)

        if len(options) == 0:
            if self.hasFlag('AVATAR'):
                ui.message("You have nothing to drink.")
            return False

        toDrink = ui.item_menu("Quaff what?", options)

        if toDrink == None:
            return False
        else:
            toQuaff = options[toDrink].removeFromStack()

            if toQuaff == None:
                toQuaff = options[toDrink]

            if toQuaff.beEaten(self):
                self.AP -= self.getActionAPCost()
            else:
                if toQuaff != options[toDrink]:
                    toQuaff.tryStacking(self)

        if len(options) > 1:
            return True
        else:
            return False

    def actionSwap(self, Other):
        if self.AP < 1:
            return False
        if self.getBurdenState() == 3:
            if self.hasFlag('AVATAR'):
                ui.message("You can barely move with so much load.", color = libtcod.light_red)
            self.AP -= self.getMoveAPCost()
            return False
        if self == Other:
            ui.message("%s attempt&S to swap with &SELF and fail&S." % self.getName(True), actor = self)
            return False
        if var.getMap()[self.x][self.y].hasFlag('STICKY') and not self.isFlying() and var.rand_chance(20 - self.getStr()):
            ui.message("%s fail&S to move in the sticky %s." % (self.getName(True), var.getMap()[self.x][self.y].getName()),
                       color = libtcod.light_red, actor = self)
            self.AP -= self.getMoveAPCost()
            return False
        if var.getMap()[self.x][self.y].hasFlag('SWIM') and not self.isFlying() and not self.hasIntrinsic('WATER_WALK'):
            if self.hasFlag('AVATAR'):
                ui.message("You cannot swap while swimming.", color = libtcod.light_red)
            return False
        if var.getMap()[self.x][self.y].hasFlag('PIT') and not self.isFlying():
            if self.hasFlag('AVATAR'):
                ui.message("You cannot swap from a pit.", color = libtcod.light_red)
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
        return True # Funny thing - I forgot to put 'return True' here and now I have
                    # no idea how much needed it is. I am checking successful swapping
                    # somewhere, am I not?

    def actionVomit(self):
        if self.isInediate(): # Many undead can eat, so while they will not die from hunger,
            return False      # they will still loose the AP. Also poison will have some
                              # small effect on these undead - no damage, but vomiting.

        ui.message("%s vomit&S." % self.getName(True), actor = self)
        # self.NP -= 100
        # attack random square with acid, plus make tile green
        self.AP -= self.getActionAPCost()
        return True

    def actionWait(self):
        self.AP -= 1
        self.receiveStamina(2)
        return True

    def actionWalk(self, dx, dy):
        if self.AP < 1:
            return False
        if self.getBurdenState() == 3:
            if self.hasFlag('AVATAR'):
                ui.message("You can barely move with so much load.", color = libtcod.light_red)
            self.AP -= self.getMoveAPCost()
            return False
        if var.getMap()[self.x][self.y].hasFlag('STICKY') and not self.isFlying() and var.rand_chance(20 - self.getStr()):
            ui.message("%s fail&S to move in the sticky %s." % (self.getName(True), var.getMap()[self.x][self.y].getName()),
                       color = libtcod.light_red, actor = self)
            self.AP -= self.getMoveAPCost()
            return False
        if var.getMap()[self.x][self.y].hasFlag('PIT') and not self.isFlying() and var.rand_chance(50 - self.getDex()):
            ui.message("%s fail&S to climb out of the %s." % (self.getName(True), var.getMap()[self.x][self.y].getName()),
                       color = libtcod.light_red, actor = self)
            self.AP -= self.getMoveAPCost()
            return False
        if var.getMap()[self.x][self.y].hasFlag('WADE') and not self.isFlying() and not self.hasIntrinsic('WATER_WALK'):
            if self.hasFlag('AVATAR') and var.rand_chance(10):
                ui.message("You wade through the %s." % var.getMap()[self.x][self.y].getName())
            if self.SP > 0:
                self.SP -= 2

        # TODO: If running, takes half a turn. With Unarmored and not running,
        #       you recover 1 SP per move.

        moved = False
        canMove = False

        if self.hasFlag('AVATAR'):
            if not self.isBlocked(self.x + dx, self.y + dy, var.DungeonLevel, False):
                if self.isPassable(self.x + dx, self.y + dy) or not self.isPassable(self.x, self.y):
                    canMove = True
                else:
                    try:
                        if ai.askForConfirmation(self, "Really walk into the %s" % var.getMap()[self.x + dx][self.y + dy].getName()):
                            canMove = True
                    except:
                        pass # Out-of-bounds tile.
            elif var.WizModeNoClip:
                canMove = True
        else:
            if not self.isBlocked(self.x + dx, self.y + dy, var.DungeonLevel):
                canMove = True

        if canMove:
            self.move(dx, dy)
            moved = True

            if self.hasFlag('AVATAR'):
                var.getMap()[self.x][self.y].makeExplored()
        else:
            if self.hasFlag('AVATAR'):
                var.getMap()[self.x + dx][self.y + dy].makeExplored()
                ui.message("You cannot go there.")

        if moved and self.hasFlag('AVATAR'):
            # Describe what we're standing at.
            stuff = []

            for i in var.getEntity():
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

            if var.getMap()[self.x][self.y].hasFlag('FEATURE'):
                if names == None:
                    names = "There is %s." % var.getMap()[self.x][self.y].getName()
                else:
                    names = "There is " + var.getMap()[self.x][self.y].getName() + ". " + names

            if names != None:
                ui.message(names)

        # Take a turn even if we walk into a wall.
        self.AP -= self.getMoveAPCost()
        return moved

class Item(Entity):
    def __init__(self, x, y, char, color, name, type, material, size, BlockMove, #These are base Entity arguments.
                 attack, ranged, DV, PV, StrScaling, DexScaling, cool, addFlags = [], addIntrinsics = []):
        super(Item, self).__init__(x, y, char, color, name, type, material, size, BlockMove)

        self.attack = attack
        self.ranged = ranged
        self.DefenseValue = DV
        self.ProtectionValue = PV
        self.StrScaling = StrScaling
        self.DexScaling = DexScaling
        self.coolness = cool

        self.flags.append('ITEM')
        for i in addFlags:
            self.flags.append(i)

        for (type, power) in addIntrinsics:
            NewInt = intrinsic.Intrinsic(type, 30000, power)
            self.intrinsics.append(NewInt)

        # Generate some blessed and cursed items:
        if self.hasFlag('ALWAYS_MUNDANE'):
            self.beautitude = 0
        elif self.hasFlag('ALWAYS_BLESSED'):
            self.beautitude += 1
        elif self.hasFlag('ALWAYS_CURSED'):
            self.beautitude -= 1
        else:
            if var.rand_chance(10):
                self.beautitude += 1
            elif var.rand_chance(10):
                self.beautitude -= 1

        # And some items are enchanted:
        if not self.hasFlag('ALWAYS_MUNDANE'):
            mod = random.choice([-1, 1, 1])

            while var.rand_chance(10 + var.DungeonLevel): # We can find more and more highly
                self.enchantment += mod                   # enchanted gear deeper into the dungeon.

            if var.rand_chance(var.DungeonLevel):         # Deep enough in the dungeon, gear has much
                self.enchantment = abs(self.enchantment)  # higher chance of positive enchantment.

        # Some armors are of different size:
        if self.hasFlag('ARMOR'):
            mod = random.choice([-1, 1])

            while var.rand_chance(1, 1000):
                self.size += mod

            self.size = min(2, max(-2, self.size)) # We need our size in range -2 to 2.

        # Items in containers.
        if self.hasFlag('CONTAINER'):
            ItemNo = 0

            while ItemNo < self.getCarryingCapacity():
                if var.rand_chance(50): # TODO
                    break

                which = var.rand_weighted(dungeon.getRandomEntity('ITEM', var.DungeonLevel))
                NewItem = spawn(self.x, self.y, which, 'ITEM')

                if NewItem.size > self.size:
                    del NewItem
                    NewItem = None

                if NewItem != None:
                    self.inventory.append(NewItem)

                ItemNo += 1

        # Special bonuses:
        self.acc = 0   # This is not same as ToHitBonus from self.attack, this is used
        self.light = 0 # for general accuracy bonus for all attacks, eg. from armor.
        self.Str = 0
        self.Dex = 0
        self.End = 0
        self.Wit = 0
        self.Ego = 0

        # Item stacks:
        if self.hasFlag('PAIRED'):
            self.stack = 2
        elif self.hasFlag('SMALL_PILE'):
            self.stack = libtcod.random_get_int(0, 1, 4)
        elif self.hasFlag('BIG_PILE'):
            self.stack = libtcod.random_get_int(0, 1, 20)
        else:
            self.stack = 1

    def gainMagic(self, forced = False):
        type = self.getType()

        if type == None:
            return

        if var.rand_chance(var.DungeonLevel, 1000) or self.hasFlag('ALWAYS_SPECIAL') or forced:
            try:
                BluePrint = random.choice(raw.MagicEgoList[type])
            except:
                #print "Failed to create prefixed item, %s." % type
                return

            try:
                prefix = BluePrint['prefix']
            except:
                prefix = None

            if prefix != None:
                if self.hasFlag('NO_PREFIX'):
                    return

                if self.prefix == "":
                    self.prefix = prefix
                else:
                    self.prefix = prefix + " " + self.prefix

            try:
                suffix = BluePrint['suffix']
            except:
                suffix = None

            if suffix != None:
                if self.hasFlag('NO_SUFFIX'):
                    return

                if self.suffix == "":
                    self.suffix = "of " + suffix
                else:
                    self.suffix = self.suffix + " and " + suffix

            if prefix == None and suffix == None:
                print "No prefix and suffix!"
                return

            try:
                material = BluePrint['material']
            except:
                material = None

            if material != None and self.material != material:
                # Change material and get rid of mentions of the item's material
                # in it's name.
                for stuff in raw.MaterialNameList[self.material]:
                    self.name = self.name.replace(stuff, '')

                self.material = material

            try:
                color = BluePrint['color']
            except:
                color = None

            if color != None:
                self.color = color

            try:
                size = BluePrint['size']
            except:
                size = None

            if size != None:
                self.size = size = min(2, max(-2, self.size + size))

            try:
                accuracy = BluePrint['accuracy']
            except:
                accuracy = None

            if accuracy != None:
                self.acc += accuracy

            try:
                light = BluePrint['light']
            except:
                light = None

            if light != None:
                self.light += light

            try:
                Str = BluePrint['Str']
            except:
                Str = None

            if Str != None:
                self.Str += Str

            try:
                Dex = BluePrint['Dex']
            except:
                Dex = None

            if Dex != None:
                self.Dex += Dex

            try:
                End = BluePrint['End']
            except:
                End = None

            if End != None:
                self.End += End

            try:
                Wit = BluePrint['Wit']
            except:
                Wit = None

            if Wit != None:
                self.Wit += Wit

            try:
                Ego = BluePrint['Ego']
            except:
                Ego = None

            if Ego != None:
                self.Ego += Ego

            try:
                DV = BluePrint['DV']
            except:
                DV = None

            if DV != None:
                self.DefenseValue += DV

            try:
                PV = BluePrint['PV']
            except:
                PV = None

            if PV != None:
                self.ProtectionValue += PV

            try:
                StrScaling = BluePrint['StrScaling']
            except:
                StrScaling = None

            if StrScaling != None:
                self.StrScaling = StrScaling

            try:
                DexScaling = BluePrint['DexScaling']
            except:
                DexScaling = None

            if DexScaling != None:
                self.DexScaling = DexScaling

            try:
                addFlags = BluePrint['flags']
            except:
                addFlags = []

            for flag in addFlags:
                if not self.hasFlag(flag):
                    self.flags.append(flag)

            try:
                addIntrinsics = BluePrint['intrinsics']
            except:
                addIntrinsics = []

            for (type, power) in addIntrinsics:
                if not self.hasIntrinsic(type):
                    NewInt = intrinsic.Intrinsic(type, 30000, power)
                    self.intrinsics.append(NewInt)

    def getName(self, capitalize = False, full = False):
        name = self.name

        if self.stack > 1:
            try:
                name = self.type['plural']
            except:
                name = name + "s"

        if self.prefix != "":
            name = self.prefix + " " + name
        if self.suffix != "":
            name = name + " " + self.suffix
        if self.givenName != None:
            name = name + " named " + self.givenName

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
            (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
             AttackRange, AttackFlags, inflict, explode) = self.getAttack()

            ToHitBonus += self.acc
            ToHitBonus += self.enchantment
            DamageBonus += self.enchantment

            if ToHitBonus > 0:
                acc = "+" + str(ToHitBonus) + ", "
            elif ToHitBonus < 0:
                acc = str(ToHitBonus) + ", "
            else:
                acc = ""

            damage = str(DiceNumber) + "d" + str(DiceValue)
            if DamageBonus > 0:
                damage += "+" + str(DamageBonus)
            elif DamageBonus < 0:
                damage += str(DamageBonus)

            if self.hasFlag('WEAPON') or self.hasFlag('SHIELD'):
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

            if self.hasFlag('WEAPON') or self.hasFlag('SHIELD'):
                scaling = " {%s, %s}" % (self.StrScaling, self.DexScaling)
            else:
                scaling = ""

            name = name + attack + defense + scaling

        if self.stack > 1:
            if self.stack == 2 and self.hasFlag('PAIRED'):
                name = "pair of " + name
            else:
                name = "heap of " + str(self.stack) + " " + name
        elif self.stack <= 0:
            name = "BUG: 0 stack item: " + name

        if capitalize == True:
            name = name.capitalize()

        return name

    def getDescription(self):
        lines = []
        underscore = "-" * 26

        lines.append("General")
        lines.append(underscore)
        lines.append("Material: %s" % self.material.lower())
        lines.append("Size    : %s" % raw.Sizes[self.size])
        lines.append("")

        lines.append("Combat")
        lines.append(underscore)

        (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
         AttackRange, AttackFlags, inflict, explode) = self.getAttack()

        ToHitBonus += self.acc
        ToHitBonus += self.enchantment
        DamageBonus += self.enchantment

        if ToHitBonus >= 0:
            acc = "+" + str(ToHitBonus)
        else:
            acc = str(ToHitBonus)

        damage = str(DiceNumber) + "d" + str(DiceValue)
        if DamageBonus > 0:
            damage += "+" + str(DamageBonus)
        elif DamageBonus < 0:
            damage += str(DamageBonus)

        lines.append("Melee:")
        lines.append("  to hit: " + acc)
        lines.append("  damage: " + damage + " " + DamageType.lower())
        lines.append("")

        (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
         AttackRange, AttackFlags, inflict, explode) = self.getRanged()

        ToHitBonus += self.acc
        ToHitBonus += self.enchantment
        DamageBonus += self.enchantment

        if ToHitBonus >= 0:
            acc = "+" + str(ToHitBonus)
        else:
            acc = str(ToHitBonus)

        damage = str(DiceNumber) + "d" + str(DiceValue)
        if DamageBonus > 0:
            damage += "+" + str(DamageBonus)
        elif DamageBonus < 0:
            damage += str(DamageBonus)

        lines.append("Ranged:")
        lines.append("  to hit: " + acc)
        lines.append("  damage: " + damage + " " + DamageType.lower())
        lines.append("  range : " + str(AttackRange) + " squares")
        lines.append("")

        if self.hasFlag('WEAPON') or self.hasFlag('SHIELD'):
            lines.append("Scaling:")
            lines.append("  strength : %s" % self.StrScaling)
            lines.append("  dexterity: %s" % self.DexScaling)
            lines.append("")

        if self.getDefenseValue() != 0 or self.getProtectionValue() != 0:
            if self.getDefenseValue() >= 0:
                DV = "+" + str(self.getDefenseValue())
            else:
                DV = str(self.getDefenseValue())

            if self.getProtectionValue() >= 0:
                PV = "+" + str(self.getProtectionValue())
            else:
                PV = str(self.getProtectionValue())

            lines.append("Defense   : %s" % DV)
            lines.append("Protection: %s" % PV)

        if len(self.intrinsics) > 0 or self.hasSpecialBonuses():
            lines.append("")
            lines.append("Intrinsics")
            lines.append(underscore)

            if self.light != 0:
                if self.light >= 0:
                    lit = "+" + str(self.getLightValue())
                else:
                    lit = str(self.getLightValue())

                lit = "light   : " + lit

                lines.append(lit)

                if self.hasFlag('CARRY_LIGHT'):
                    lines.append("floating nearby")

            if self.acc != 0 and not self.hasFlag('WEAPON'):
                toHit = self.acc

                if self.hasFlag('ENCHANT_ACCURACY'):
                    toHit += self.enchantment

                if toHit >= 0:
                    toHit = "+" + str(toHit)
                else:
                    toHit = str(toHit)

                toHit = "accuracy: " + toHit

                lines.append(toHit)

            if self.Str != 0:
                bonus = self.Str

                if bonus >= 0:
                    bonus = "+" + str(bonus)
                else:
                    bonus = str(bonus)

                bonus = "strength: " + bonus

                lines.append(bonus)

            if self.Dex != 0:
                bonus = self.Dex

                if bonus >= 0:
                    bonus = "+" + str(bonus)
                else:
                    bonus = str(bonus)

                bonus = "dexterity: " + bonus

                lines.append(bonus)

            if self.End != 0:
                bonus = self.End

                if bonus >= 0:
                    bonus = "+" + str(bonus)
                else:
                    bonus = str(bonus)

                bonus = "endurance: " + bonus

                lines.append(bonus)

            if self.Wit != 0:
                bonus = self.Wit

                if bonus >= 0:
                    bonus = "+" + str(bonus)
                else:
                    bonus = str(bonus)

                bonus = "wits    : " + bonus

                lines.append(bonus)

            if self.Ego != 0:
                bonus = self.Ego

                if bonus >= 0:
                    bonus = "+" + str(bonus)
                else:
                    bonus = str(bonus)

                bonus = "ego     : " + bonus

                lines.append(bonus)

            for i in self.intrinsics:
                lines.append(i.getName())

        # TODO
        #lines.append("")
        #lines.append(underscore)
        # text

        return lines

    def getCarryingCapacity(self):
        if self.hasFlag('CONTAINER'):
            if self.hasFlag('HOLDING'):
                return 999

            carry = abs(-3 - self.size)

            if self.size < 0:
                carry *= 5
            else:
                carry *= 10

            carry += self.enchantment

            return max(1, carry)
        else:
            return 0

    def getDestroyed(self, Owner = None):
        if Owner == None:
            for i in var.getEntity():
                if i == self: # We should make sure we are actually lying on the floor.
                    var.getEntity().remove(self)
                    del self
                    return True
        else:
            try:
                Owner.inventory.remove(self)
            except:
                pass # Tmp item that was not appended to Owner.inventory.

            del self
            return True

    def tryStacking(self, Owner = None):
        if Owner != None:
            for i in Owner.inventory:
                if self.addToStack(i, Owner):
                    return True
        else:
            for i in var.getEntity():
                if i.hasFlag('ITEM') and i.x == self.x and i.y == self.y:
                    if self.addToStack(i, Owner):
                        return True

        return False

    def isSameAs(self, other):
        # Now this is going to be long...

        if len(self.inventory) != 0 or len(other.inventory) != 0:
            return False

        if self.type != other.type:
            return False

        if self.prefix != other.prefix:
            return False

        if self.suffix != other.suffix:
            return False

        if self.material != other.material:
            return False

        if self.size != other.size:
            return False

        if self.attack != other.attack:
            return False

        if self.ranged != other.ranged:
            return False

        if self.DefenseValue != other.DefenseValue:
            return False

        if self.ProtectionValue != other.ProtectionValue:
            return False

        if self.Str != other.Str:
            return False

        if self.Dex != other.Dex:
            return False

        if self.End != other.End:
            return False

        if self.Wit != other.Wit:
            return False

        if self.Ego != other.Ego:
            return False

        if self.StrScaling != other.StrScaling:
            return False

        if self.DexScaling != other.DexScaling:
            return False

        if self.beautitude != other.beautitude:
            return False

        if self.enchantment != other.enchantment:
            return False

        if self.acc != other.acc:
            return False

        if self.light != other.light:
            return False

        if len(self.intrinsics) != len(other.intrinsics):
            return False
        else:
            for intrinsic in self.intrinsics:
                if not other.hasIntrinsic(intrinsic.type):
                    return False

        return True

    def addToStack(self, other, Owner = None):
        if self == other:
            return False

        if self.isSameAs(other):
            other.stack += self.stack
            self.getDestroyed(Owner)
            return True
        else:
            return False

    def removeFromStack(self, number = 1):
        number = max(1, number) # We cannot remove less than 1 item from stack.

        if len(self.inventory) != 0:
            return None
        if self.stack <= number:
            return None

        NewItem = spawn(self.x, self.y, self.type, 'ITEM', False)

        NewItem.prefix = self.prefix
        NewItem.suffix = self.suffix
        NewItem.material = self.material
        NewItem.size = self.size
        NewItem.attack = self.attack
        NewItem.ranged = self.ranged
        NewItem.Str = self.Str
        NewItem.Dex = self.Dex
        NewItem.End = self.End
        NewItem.Wit = self.Wit
        NewItem.Ego = self.Ego
        NewItem.DefenseValue = self.DefenseValue
        NewItem.ProtectionValue = self.ProtectionValue
        NewItem.StrScaling = self.StrScaling
        NewItem.DexScaling = self.DexScaling
        NewItem.beautitude = self.beautitude
        NewItem.enchantment = self.enchantment
        NewItem.acc = self.acc
        NewItem.light = self.light

        for intrinsic in self.intrinsics:
            if NewItem.hasIntrinsic(intrinsic.type):
                continue
            else:
                NewItem.addIntrinsic(intrinsic.type, intrinsic.duration, intrinsic.power)

        NewItem.stack = number
        self.stack -= number

        return NewItem

    def getAccuracyValue(self):
        try:
            toHit = self.attack['ToHitBonus']
        except:
            toHit = raw.DummyAttack['ToHitBonus']

        toHit += self.enchantment

        if self.hasFlag('ENCHANT_DOUBLE'):
            toHit += self.enchantment

        return toHit

    def getDefenseValue(self):
        DV = self.DefenseValue

        if self.hasFlag('SHIELD') or self.hasFlag('ENCHANT_DODGE'):
            DV += self.enchantment

            if self.hasFlag('ENCHANT_DOUBLE'):
                DV += self.enchantment

        return DV

    def getProtectionValue(self):
        PV = self.ProtectionValue

        if self.hasFlag('ARMOR') or self.hasFlag('ENCHANT_PROTECTION'):
            PV += self.enchantment

            if self.hasFlag('ENCHANT_DOUBLE'):
                PV += self.enchantment

        return PV

    def getLightValue(self):
        light = self.light

        if self.hasFlag('ENCHANT_LIGHT'):
            light += self.enchantment

        return light

    def getSPCost(self):
        return 5 + self.size

        # The stuff below works nicely, but it results in way too high SP cost
        # for weapons with high StrScaling and low DexScaling. They need to be
        # useable, so we'll use a simpler SP cost for now. Maybe revise later?
        '''
        base = 5
        # Stamina cost of attacks is based on their scaling, as StrScaling attacks
        # are supposed to use the weight of the weapon, requiring heavy blow and
        # momentum, thus much more stamina for the swing, while DexScaling attacks
        # are quick, light and supposed to come again and again until the target
        # dies of a thousand needle wounds.

        # Str Scaling:
        Str = ((raw.Scaling[self.StrScaling] * 100) + 25) / 125
        base *= Str

        # Dex Scaling:
        Dex = 125 / ((raw.Scaling[self.DexScaling] * 100) + 75)
        base *= Dex

        # Two-handers and two-and-a-half-handers get small discout in stamina,
        # as you are using them in both hands and thus each hand is less tired
        # by the attacks.
        if self.size > 0 or self.hasFlag('TWO_AND_HALF'):
            return max(2, int(math.floor(base)))
        else:
            return max(2, int(math.ceil(base)))
        '''

    def getMPCost(self):
        # TODO: For magical weapons and shields blocking magic.
        pass

    def getAttack(self):
        try:
            verb = self.attack['verb']
        except:
            verb = raw.DummyAttack['verb']
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
        try:
            DamageType = self.attack['DamageType']
        except:
            DamageType = raw.DummyAttack['DamageType']
        try:
            AttackRange = self.attack['range']
        except:
            AttackRange = raw.DummyAttack['range']
        try:
            AttackFlags = self.attack['flags']
        except:
            AttackFlags = raw.DummyAttack['flags']
        try:
            inflict = self.attack['inflict']
        except:
            inflict = raw.DummyAttack['inflict']
        try:
            explode = self.attack['explode']
        except:
            explode = raw.DummyAttack['explode']

        return (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
                AttackRange, AttackFlags, inflict, explode)

    def getRanged(self):
        try:
            verb = self.ranged['verb']
        except:
            verb = raw.DummyAttack['verb']
        try:
            ToHitBonus = self.ranged['ToHitBonus']
        except:
            ToHitBonus = raw.DummyAttack['ToHitBonus']
        try:
            DiceNumber = self.ranged['DiceNumber']
        except:
            DiceNumber = raw.DummyAttack['DiceNumber']
        try:
            DiceValue = self.ranged['DiceValue']
        except:
            DiceValue = raw.DummyAttack['DiceValue']
        try:
            DamageBonus = self.ranged['DamageBonus']
        except:
            DamageBonus = raw.DummyAttack['DamageBonus']
        try:
            DamageType = self.ranged['DamageType']
        except:
            DamageType = raw.DummyAttack['DamageType']
        try:
            AttackRange = self.ranged['range']
        except:
            AttackRange = raw.DummyAttack['range']
        try:
            AttackFlags = self.ranged['flags']
        except:
            AttackFlags = raw.DummyAttack['flags']
        try:
            inflict = self.ranged['inflict']
        except:
            inflict = raw.DummyAttack['inflict']
        try:
            explode = self.ranged['explode']
        except:
            explode = raw.DummyAttack['explode']

        return (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
                AttackRange, AttackFlags, inflict, explode)

    def getCoolness(self):
        cool = self.coolness

        cool += self.acc
        cool += self.light
        cool += self.beautitude
        cool += self.enchantment

        if self.hasFlag('WEAPON') or self.hasFlag('SHIELD'):
            weaponBonus = 0

            (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
             AttackRange, AttackFlags, inflict, explode) = self.getAttack()

            weaponBonus += ToHitBonus
            weaponBonus += DiceNumber * DiceValue
            weaponBonus += DamageBonus

            if inflict != None:
                weaponBonus += len(inflict)
            if explode != None:
                weaponBonus += 5

            weaponBonus *= raw.Scaling[self.StrScaling]
            weaponBonus *= raw.Scaling[self.DexScaling]

            cool += weaponBonus
        elif self.hasFlag('ARMOR'):
            armorBonus = 0

            armorBonus += self.DefenseValue
            armorBonus += self.ProtectionValue
            armorBonus += len(self.intrinsics)

            cool += armorBonus

        return cool

    def getSlot(self):
        slot = None          # I has a bug here that made no monsters equip any
                             # gloves or gauntlets. I hate how long it can take to
        for i in self.flags: # find such a minor bug and fix it.
            if i in ['HEAD', 'TORSO', 'GROIN', 'ARM', 'LEG', 'WING', 'TAIL']:
                slot = i
            elif i in ['WEAPON', 'SHIELD']:
                slot = 'GRASP'

        return slot

    def getType(self):
        for i in self.flags:
            if i in ['WEAPON', 'SHIELD', 'ARMOR', 'POTION', 'TOOL', 'FOOD']:
                return i

        return None

    def hasSpecialBonuses(self):
        if self.acc != 0 and not self.hasFlag('WEAPON'):
            return True

        if self.light != 0:
            return True

        if self.Str != 0:
            return True

        if self.Dex != 0:
            return True

        if self.End != 0:
            return True

        if self.Wit != 0:
            return True

        if self.Ego != 0:
            return True

        return False

    def canAttack(self):
        if self.hasFlag('WEAPON'):
            return True

        if self.hasFlag('SHIELD'):
            return False

        if var.rand_chance(50):
            return True
        else:
            return False

    # Various use methods:
    def beApplied(self, User, victim = None):
        if victim == None:
            victim = User

        if self.hasFlag('HORN'):
            effect = "Nothing happens."

            if self.hasFlag('FOO'):
                pass

            ui.message("%s blow&S the %s. %s" % (User.getName(True), self.getName(), effect), actor = User)
            return True
        else:
            if self.hasFlag('BANDAGE'):
                if victim == User:
                    ui.message("%s bandage&S &SELF." % User.getName(True), actor = User)
                else:
                    ui.message("%s bandage&S %s wounds." % (User.getName(True), victim.getName(possessive = True)), actor = User)

                power = self.beautitude + self.enchantment
                User.receiveHeal(power) # Yes, this can theoretically damage us.

                if self.beautitude >= 0:
                    if User.hasIntrinsic('BLEED'):
                        User.removeIntrinsic('BLEED')
                else:
                    if User.hasIntrinsic('BLEED'):
                        User.removeIntrinsic('BLEED', max(1, power))

                for part in User.bodyparts: # And remove all wounds.
                    if part.wounded:
                        part.wounded = False

                self.getDestroyed(User)
                return True

            elif self.hasFlag('FOO'):
                pass

        return False

    def beEaten(self, Eater):
        if not self.material in Eater.diet:
            if Eater.hasFlag('AVATAR'):
                ui.message("You cannot consume that.")
            return False
        # NP+
        # return if too full

        if self.hasFlag('FOOD'):
            pass

        if self.hasFlag('POTION'):
            effect = "Nothing happens."

            if self.hasFlag('HEAL'):
                if Eater.HP >= Eater.maxHP:
                    toHeal = 1 + self.enchantment + self.beautitude
                    Eater.bonusHP += libtcod.random_get_int(0, min(1, toHeal), max(0, toHeal))
                    Eater.recalculateHealth()

                if self.beautitude > 0:
                    toHeal = 20
                    effect = "&SUBC feel&S much better."
                elif self.beautitude == 0:
                    toHeal = var.rand_dice(1, 10, 10)
                    effect = "&SUBC feel&S better."
                else:
                    toHeal = var.rand_dice(1, 10)
                    effect = "&SUBC feel&S somewhat better."

                toHeal += self.enchantment + self.beautitude

                Eater.receiveHeal(toHeal)

                if self.beautitude >= 0:
                    if Eater.hasIntrinsic('BLEED'):
                        Eater.removeIntrinsic('BLEED')

            elif self.hasFlag('MUTATION'):
                # TODO: Good/bad based on BUC.
                mutationMax = max(1, 1 + self.enchantment)
                mutationNo = 0

                while mutationNo < mutationMax:
                    mutation.gain('RANDOM_ANY', Eater)
                    mutationNo += 1

                effect = "&SUBC feel&S weird."

            elif self.hasFlag('STRENGTH'):
                effect = "&SUBC feel&S &POSS muscles grow."

                if self.beautitude >= 0:
                    Eater.Str += 1

                if self.beautitude > 0:
                    duration = 200

                    if Eater.hasIntrinsic('DEBUFF_STRENGTH'):
                        Eater.removeIntrinsic('DEBUFF_STRENGTH')

                elif self.beautitude == 0:
                    duration = var.rand_dice(1, 100, 50)
                else:
                    duration = var.rand_dice(1, 100)

                    if Eater.hasIntrinsic('BUFF_STRENGTH'):
                        Eater.removeIntrinsic('BUFF_STRENGTH')

                toBuff = self.enchantment + self.beautitude

                if toBuff > 0:
                    Eater.addIntrinsic('BUFF_STRENGTH', duration, toBuff)
                elif toBuff < 0:
                    Eater.addIntrinsic('DEBUFF_STRENGTH', duration, -toBuff)

                Eater.recalculateAll()

            elif self.hasFlag('DEXTERITY'):
                effect = "&SUBC feel&S &POSS joints grow flexible."

                if self.beautitude >= 0:
                    Eater.Dex += 1

                if self.beautitude > 0:
                    duration = 200

                    if Eater.hasIntrinsic('DEBUFF_DEXTERITY'):
                        Eater.removeIntrinsic('DEBUFF_DEXTERITY')

                elif self.beautitude == 0:
                    duration = var.rand_dice(1, 100, 50)
                else:
                    duration = var.rand_dice(1, 100)

                    if Eater.hasIntrinsic('BUFF_DEXTERITY'):
                        Eater.removeIntrinsic('BUFF_DEXTERITY')

                toBuff = self.enchantment + self.beautitude

                if toBuff > 0:
                    Eater.addIntrinsic('BUFF_DEXTERITY', duration, toBuff)
                elif toBuff < 0:
                    Eater.addIntrinsic('DEBUFF_DEXTERITY', duration, -toBuff)

                Eater.recalculateAll()

            elif self.hasFlag('ENDURANCE'):
                effect = "&SUBC feel&S &POSS bulk grow."

                if self.beautitude >= 0:
                    Eater.End += 1

                if self.beautitude > 0:
                    duration = 200

                    if Eater.hasIntrinsic('DEBUFF_ENDURANCE'):
                        Eater.removeIntrinsic('DEBUFF_ENDURANCE')

                elif self.beautitude == 0:
                    duration = var.rand_dice(1, 100, 50)
                else:
                    duration = var.rand_dice(1, 100)

                    if Eater.hasIntrinsic('BUFF_ENDURANCE'):
                        Eater.removeIntrinsic('BUFF_ENDURANCE')

                toBuff = self.enchantment + self.beautitude

                if toBuff > 0:
                    Eater.addIntrinsic('BUFF_ENDURANCE', duration, toBuff)
                elif toBuff < 0:
                    Eater.addIntrinsic('DEBUFF_ENDURANCE', duration, -toBuff)

                Eater.recalculateAll()

            elif self.hasFlag('WITS'):
                effect = "&SUBC feel&S &POSS mind sharpen."

                if self.beautitude >= 0:
                    Eater.Wit += 1

                if self.beautitude > 0:
                    duration = 200

                    if Eater.hasIntrinsic('DEBUFF_WITS'):
                        Eater.removeIntrinsic('DEBUFF_WITS')

                elif self.beautitude == 0:
                    duration = var.rand_dice(1, 100, 50)
                else:
                    duration = var.rand_dice(1, 100)

                    if Eater.hasIntrinsic('BUFF_WITS'):
                        Eater.removeIntrinsic('BUFF_WITS')

                toBuff = self.enchantment + self.beautitude

                if toBuff > 0:
                    Eater.addIntrinsic('BUFF_WITS', duration, toBuff)
                elif toBuff < 0:
                    Eater.addIntrinsic('DEBUFF_WITS', duration, -toBuff)

                Eater.recalculateAll()

            elif self.hasFlag('EGO'):
                effect = "&SUBC feel&S &POSS ego grow."

                if self.beautitude >= 0:
                    Eater.Ego += 1

                if self.beautitude > 0:
                    duration = 200

                    if Eater.hasIntrinsic('DEBUFF_EGO'):
                        Eater.removeIntrinsic('DEBUFF_EGO')

                elif self.beautitude == 0:
                    duration = var.rand_dice(1, 100, 50)
                else:
                    duration = var.rand_dice(1, 100)

                    if Eater.hasIntrinsic('BUFF_EGO'):
                        Eater.removeIntrinsic('BUFF_EGO')

                toBuff = self.enchantment + self.beautitude

                if toBuff > 0:
                    Eater.addIntrinsic('BUFF_EGO', duration, toBuff)
                elif toBuff < 0:
                    Eater.addIntrinsic('DEBUFF_EGO', duration, -toBuff)

                Eater.recalculateAll()

            elif self.hasFlag('FOO'):
                pass
            else:
                return False

            ui.message("%s drink&S the %s. %s" % (Eater.getName(True), self.getName(), effect), actor = Eater)
            self.getDestroyed(Eater)
            return True

        return False

    def beLooted(self, Looter):
        if not self.hasFlag('CONTAINER'):
            if Looter.hasFlag('AVATAR'):
                ui.message("You cannot loot the %s." % self.getName())
            return False

        if len(self.inventory) == 0:
            if Looter.hasFlag('AVATAR'):
                ui.message("%s is empty." % self.getName(True))
            return False

        if Looter.getBurdenState() == 3:
            if Looter.hasFlag('AVATAR'):
                ui.message("Your inventory is already full.")
            return False

        if Looter.hasFlag('AVATAR'):
            toLoot = ui.item_menu("Take what?", self.inventory)
        else:
            toLoot = libtcod.random_get_int(0, 0, len(self.inventory))

        if toLoot == None:
            return False
        else:
            try:
                item = self.inventory[toLoot]

                Looter.inventory.append(item)
                item.tryStacking(Looter)
                self.inventory.remove(item)
                Looter.AP -= Looter.getActionAPCost()
            except:
                pass # Out-of-bounds letter was pressed.

        if len(self.inventory) >= 1:
            return True
        else:
            return False

    def beStored(self, Looter):
        if not self.hasFlag('CONTAINER'):
            if Looter.hasFlag('AVATAR'):
                ui.message("You cannot loot the %s." % self.getName())
            return False

        if len(self.inventory) >= self.getCarryingCapacity():
            if Looter.hasFlag('AVATAR'):
                ui.message("%s is full." % self.getName(True))
            return False

        toLoot = ui.item_menu("Put in what?", Looter.inventory)

        if toLoot == None:
            return False
        else:
            try:
                item = Looter.inventory[toLoot]

                if item == self:
                    ui.message("That would be an interesting topological exercise.")
                    return False

                if item.size > self.size and not self.hasFlag('HOLDING'):
                    ui.message("%s is too large to put into %s." % (item.getName(True), self.getName()))
                    return False

                self.inventory.append(item)
                item.tryStacking(self)
                Looter.inventory.remove(item)
                Looter.AP -= Looter.getActionAPCost()
            except:
                pass # Out-of-bounds letter was pressed.

        if len(Looter.inventory) >= 1:
            return True
        else:
            return False

    def beZapped(self, Zapper):
        pass

class BodyPart(Entity):
    def __init__(self, name, type, #These are base Entity arguments.
                 mob, cover, place, size, eyes, attack, StrScaling, DexScaling,
                 addFlags, material = None):
        x = mob.x
        y = mob.y
        char = '~'
        color = libtcod.red

        if material == None:
            material = mob.material

        # Different body parts are differently smaller then mob, plus cannot
        # equip items smaller than the body part.
        size = min(2, max(-2, mob.size + size))

        super(BodyPart, self).__init__(x, y, char, color, name, type, material, size)

        #self.flags.append('ITEM')
        self.flags.append('BODY_PART')
        for i in addFlags:
            self.flags.append(i)

        self.attack = attack
        self.StrScaling = StrScaling
        self.DexScaling = DexScaling
        self.cover = cover
        self.placement = place
        self.eyes = eyes

        # Attribute bonuses:
        # TODO: Limbs should offer some.
        self.Str = 0
        self.Dex = 0
        self.End = 0
        self.Wit = 0
        self.Ego = 0

        self.wounded = False

    def getName(self, capitalize = False, full = False):
        name = self.name

        # Size:
        #size = raw.Sizes[self.size]
        #name = size + ' ' + name

        # Right/left:
        if self.hasFlag('RIGHT'):
            name = 'right ' + name
        if self.hasFlag('LEFT'):
            name = 'left ' + name
        if self.hasFlag('OTHER'):
            name = 'other ' + name

        if full == True:
        #    if self.hasFlag('ARM') and self.hasFlag('MAIN'):
        #        name = name + '*'

            # Wounds:
            if self.wounded:
                name = 'wounded ' + name

            # While severed:
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

                name = self.prefix + " " + name

        #    if len(self.inventory) > 0:
        #        name = name + self.inventory[0].getName()


        if capitalize == True:
            name = name.capitalize()

        return name

    def getCoolness(self):
        cool = 0

        if self.hasFlag('GRASP'):
            (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
             AttackRange, AttackFlags, inflict, explode) = self.getAttack()

            cool += ToHitBonus
            cool += DiceNumber * DiceValue
            cool += DamageBonus

            if inflict != None:
                cool += len(inflict)
            if explode != None:
                cool += 5

            cool *= raw.Scaling[self.StrScaling]
            cool *= raw.Scaling[self.DexScaling]

        return cool

    def getSlot(self):
        slot = None
        for i in self.flags:
            if i in ['HEAD', 'TORSO', 'GROIN', 'ARM', 'HAND', 'LEG', 'WING', 'TAIL', 'GRASP']:
                slot = i # Grasp must be last!
        return slot

    def getPlacement(self):
        slot = None
        for i in self.flags:
            if i in ['RIGHT', 'LEFT', 'OTHER']:
                slot = i
                break

        return slot

    def getDescription(self):
        lines = []
        underscore = "-" * 26

        lines.append("General")
        lines.append(underscore)
        lines.append("Material: %s" % self.material.lower())
        lines.append("Size    : %s" % raw.Sizes[self.size])

        if self.eyes > 0:
            lines.append("Eyes    : %s" % self.eyes)

        lines.append("")

        lines.append("Combat")
        lines.append(underscore)

        (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
         AttackRange, AttackFlags, inflict, explode) = self.getAttack()

        ToHitBonus += self.eyes
        ToHitBonus += self.enchantment
        DamageBonus += self.enchantment

        if ToHitBonus >= 0:
            acc = "+" + str(ToHitBonus)
        else:
            acc = str(ToHitBonus)

        damage = str(DiceNumber) + "d" + str(DiceValue)
        if DamageBonus > 0:
            damage += "+" + str(DamageBonus)
        elif DamageBonus < 0:
            damage += str(DamageBonus)

        lines.append("Melee:")
        lines.append("  to hit: " + acc)
        lines.append("  damage: " + damage + " " + DamageType.lower())
        lines.append("")

        lines.append("Scaling:")
        lines.append("  strength : %s" % self.StrScaling)
        lines.append("  dexterity: %s" % self.DexScaling)
        lines.append("")

        # TODO: Natural armor.

        # TODO
        #lines.append("")
        lines.append(underscore)
        lines.append("Eww! This looks like it belonged to someone!")

        return lines

    def getAttack(self):
        try:
            verb = self.attack['verb']
        except:
            verb = raw.DummyAttack['verb']
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
        try:
            DamageType = self.attack['DamageType']
        except:
            DamageType = raw.DummyAttack['DamageType']
        try:
            AttackRange = self.attack['range']
        except:
            AttackRange = raw.DummyAttack['range']
        try:
            AttackFlags = self.attack['flags']
        except:
            AttackFlags = raw.DummyAttack['flags']
        try:
            inflict = self.attack['inflict']
        except:
            inflict = raw.DummyAttack['inflict']
        try:
            explode = self.attack['explode']
        except:
            explode = raw.DummyAttack['explode']

        return (verb, ToHitBonus, DiceNumber, DiceValue, DamageBonus, DamageType,
                AttackRange, AttackFlags, inflict, explode)

    def doEquip(self, item, actor = None):
        if len(self.inventory) > 0:
            return False

        slot = self.getSlot()

        if slot != None:
            if not (slot in item.flags or slot == 'GRASP'):
                return False
        else:
            return False

        if not slot == 'GRASP':
            if item.size < self.size:
                if actor != None:
                    if actor.hasFlag('AVATAR'):
                        ui.message("%s is too small to fit." % item.getName(True))
                return False
            elif item.size > self.size:
                if actor != None:
                    if actor.hasFlag('AVATAR'):
                        ui.message("%s is too large to fit properly." % item.getName(True))
                return False

        self.inventory.append(item)
        return True

    def doDeEquip(self, actor = None):
        # Remove equipment from a limb. Cursed stuff cannot be removed, of course,
        # unless you are undead.

        if len(self.inventory) == 0:
            return None
        else:
            for item in self.inventory:
                if item != None:
                    if actor != None:
                        if item.beautitude < 0 and not actor.canBreakCurse(item.beautitude):
                            if actor.hasFlag('AVATAR'):
                                ui.message("%s is cursed and you cannot take it off." % item.getName(True))
                            continue

                    self.inventory.remove(item)
                    return item

        return None

#class Cloud(Entity):
#    def __init__(self, x, y, color, name, type, #These are base Entity arguments.
#                 attack, addFlags):
#        char = chr(177)
#        material = 'AIR'
#        size = 2 # Clouds should count as huge.
#
#        super(Cloud, self).__init__(x, y, char, color, name, type, material, size)
#
#        self.flags.append('CLOUD')
#        for i in addFlags:
#            self.flags.append(i)
#
#        self.attack = attack
