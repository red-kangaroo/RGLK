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
            attack = BluePrint['BaseAttack']
        except:
            attack = raw.DummyMonster['BaseAttack']
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
                     Str, Dex, End, Wit, Ego, speed, sight, addFlags)

        New.BaseAttack = attack
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
                   addFlags)
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
            libtcod.console_set_default_foreground(var.MapConsole, self.color)
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

    def isBlocked(self, x, y, DungeonLevel = var.DungeonLevel):
        if (x < 0 or x > var.MapWidth - 1 or
            y < 0 or y > var.MapHeight - 1):
            return True

        if var.Maps[DungeonLevel][x][y].BlockMove:
            return True

        for i in var.Entities[DungeonLevel]:
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
                 Str, Dex, End, Wit, Ego, speed = 1.0, FOVRadius = 6, addFlags = []):
        BlockMove = True # All mobs block movement, but not all entities,
                         # so pass this to Entity __init__
        super(Mob, self).__init__(x, y, char, color, name, material, BlockMove)

        # Attributes:
        self.Str = Str
        self.Dex = Dex
        self.End = End
        self.Wit = Wit
        self.Ego = Ego
        self.speed = speed

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
        self.carry = self.recalculateCarryingCapacity()
        self.BaseAttack = None # Special case this as a slam attack in attack code.
        self.givenName = None

        self.flags.append('MOB')
        for i in addFlags:
            self.flags.append(i)

        self.bodyparts = []
        self.gainBody()

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
                addFlags = part['flags']
            except:
                addFlags = raw.DummyPart['flags']

            New = BodyPart(name, self, cover, addFlags)

            self.bodyparts.append(New)

        for part in self.bodyparts:
            if part.hasFlag('ARM'):
                part.flags.append('MAIN')
                break

    def recalculateFOV(self):
        libtcod.map_compute_fov(var.FOVMap, self.x, self.y, self.FOVRadius, True, 0)

    def recalculateCarryingCapacity(self):
        return max(0, 10 + (2 * self.Str))

    def recalculateHealth(self):
        return (20 * (1.2 ** self.End)) + self.bonusHP

    def recalculateMana(self):
        return (20 * (1.2 ** self.Ego)) + self.bonusMP

    def recalculateStamina(self):
        return (20 * (1.2 ** self.Str))

    def regainHealth(self):
        if not self.hasFlag('DEAD') and self.HP < self.maxHP:
            self.HP += 0.2

    def regainMana(self):
        if not self.hasFlag('DEAD') and self.MP < self.maxMP:
            self.MP += 0.3

    def regainStamina(self):
        if not self.hasFlag('DEAD') and self.SP < self.maxSP:
            self.SP += 0.5

    def regainActions(self):
        # This works even when dead, because items can have actions, too.
        self.AP += self.speed

        # Energy randomization:
        #if var.rand_chance(5):
        #    self.AP += 0.1
        #elif var.rand_chance(5):
        #    self.AP -= 0.1

    def getAccuracyBonus(self):
        # TODO
        toHit = self.Dex

        if toHit >= 1:
            return libtcod.random_get_int(0, 0, toHit)
        else:
            return toHit

    def getDodgeBonus(self):
        # TODO:
        # Penalty for adjacent walls.
        # Bonus after move.
        # Unarmored / Light Armor

        toDodge = self.Dex

        if toDodge >= 1:
            return libtcod.random_get_int(0, 0, toDodge)
        else:
            return toDodge


    def getRelation(self, Other):
        # TODO: Add factions, pets etc.
        #       Special cases for golden beetle, vampire bat, ...
        if (self.hasFlag('AVATAR') or Other.hasFlag('AVATAR')):
            return 0
        else:
            return 1

    def getActionAPCost(self):
        return 1

    def getAttackAPCost(self):
        return 1

    def getMoveAPCost(self):
        return 1

    def getName(self, capitalize = False, full = False):
        name = self.name

        # TODO:
        # full should make the function return whole name and title

        if self.givenName != None:
            name = self.givenName + ' the ' + name

        if self.hasFlag('AVATAR'):
            name = 'you'

        if capitalize == True:
            name = name.capitalize()

        return name

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

    def receiveAttack(self, attacker, multiplier = 0):
        self.target = attacker
        # TODO

    def receiveDamage(self, damage, type = None):
        # TODO
        if damage > 0:
            self.HP -= damage

        self.checkDeath()

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

            self.actionDrop(True)

            self.flags.remove('MOB')
            self.flags.append('ITEM')
            self.flags.append('DEAD')

            if self.hasFlag('AVATAR'):
                game.save() # No savescumming for you! (Unless you prepare for this, of course.)
                ai.waitForMore(self)
                var.WizModeTrueSight = True
                ui.message("You have failed in your quest!")

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

        if self.AP < 1:
            return False

        # TODO
        if self.SP <= 0:
            if self.hasFlag('AVATAR'):
                ui.message("You are too exhausted to fight.")
            return False
        if not victim.hasFlag('MOB'):
            if self.hasFlag('AVATAR'):
                ui.message("You can only attack creatures.")
            return False

        victim.receiveAttack(self)

        forcedHit = False
        forcedMiss = False
        toHit = var.rand_gaussian_d20()
        toDodge = var.rand_gaussian_d20()

        if toHit == 20:
            forcedHit = True
        elif (toHit == 1 or toDodge == 20):
            forcedMiss = True

        # Debug:
        #print "-" * 10
        #print "%s to hit roll: %s; %s to dodge roll: %s" % (self.name, toHit,
        #                                                    victim.name, toDodge)

        toHit += self.getAccuracyBonus()
        toDodge += victim.getDodgeBonus()

        #print "modified hit chance: %s vs %s" % (toHit, toDodge)

        if forcedMiss == False or forcedHit == True:
            if (forcedHit == True or toHit > toDodge):
                if forcedHit == True:
                    ui.message("%s easily hit&S %s." % (self.getName(True), victim.getName()), actor = self)
                else:
                    ui.message("%s hit&S %s." % (self.getName(True), victim.getName()), actor = self)

                # TODO:
                # Different attacks, crits.
                damage = libtcod.random_get_int(0, 1, 6) + self.Str
                victim.receiveDamage(damage)
                #print "%s receives %s damage" % (victim.name, damage)
            else:
                ui.message("%s miss&ES %s." % (self.getName(True), victim.getName()), actor = self)
        else:
            ui.message("%s completely miss&ES %s." % (self.getName(True), victim.getName()), actor = self)
            # TODO: if toHit + bonus < 0, fumble

        self.AP -= self.getAttackAPCost()
        self.SP -= 2 # TODO
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
                    ui.message("%s clos&ES the door." % self.getName(True), actor = self)
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

    def actionInventory(self):
        if len(self.inventory) == 0:
            ui.message("You carry no items.")
            return False
        else:
            ui.option_menu("You carry the following:", self.inventory)
            return True

    def actionEquipment(self):
        if len(self.bodyparts) == 0:
            ui.message("You should be dead.", actor = self)
            self.checkDeath()
            return False
        else:
            ui.option_menu("Your equipment:", self.bodyparts)
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

        if (not self.isBlocked(nx, ny) and not self.isBlocked(nnx, nny) and
            libtcod.map_is_in_fov(var.FOVMap, nnx, nny)):
            ui.message("%s leap&S." % self.getName(True), actor = self)
            self.move(dx * 2, dy * 2)
            moved = True
        else:
            ui.message("%s balk&S at the leap." % self.getName(True), actor = self)

        self.AP -= self.getMoveAPCost()
        self.SP -= 5
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
        if self.AP < 1:
            return False

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
            for i in options:
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
            ui.message("%s attempt&S to swap with &OBJself and fails." % self.getName(True), actor = self)
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

        if (not self.isBlocked(self.x + dx, self.y + dy) or
           (self.hasFlag('AVATAR') and var.WizModeNoClip)):
            self.move(dx, dy)
            moved = True
        else:
            if self.hasFlag('AVATAR'):
                ui.message("You cannot go there.")

        # Take a turn even if we walk into a wall.
        self.AP -= self.getMoveAPCost()
        return moved

class Item(Entity):
    def __init__(self, x, y, char, color, name, material, size, BlockMove, #These are base Entity arguments.
                 addFlags):
        super(Item, self).__init__(x, y, char, color, name, material, size, BlockMove)

        self.beautitude = 0 # Negative for cursed/doomed, positive for blessed/holy.

        self.flags.append('ITEM')
        for i in addFlags:
            self.flags.append(i)

    def getName(self, capitalize = False, full = True):
        name = self.name

        # TODO:
        # all different stuff
        # if full == False, show only base name

        if capitalize == True:
            name = name.capitalize()

        return name

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
                 mob, cover, addFlags):
        x = mob.x
        y = mob.y
        char = '~'
        color = libtcod.red
        material = mob.material
        size = min(2, max(-2, mob.size))

        super(BodyPart, self).__init__(x, y, char, color, name, material, size)

        self.flags.append('ITEM')
        self.flags.append('BODY_PART')
        for i in addFlags:
            self.flags.append(i)

        self.cover = cover
        self.wounded = False

    def getName(self, capitalize = False, full = True):
        name = self.name

        if self.hasFlag('ARM') and self.hasFlag('MAIN'):
            name = 'main ' + name

        if self.wounded == True:
            name = 'wounded ' + name

        #if full == True:
        #    if len(self.inventory) > 0:
        #        name = name + self.inventory[0].getName()

        if capitalize == True:
            name = name.capitalize()

        return name

#    def __init__(self, x, y, char, color, name, #These are base Entity arguments.
#                 ):
#        super(Mob, self).__init__(x, y, char, color, name)
#
#        self.flags.append('FEATURE')
