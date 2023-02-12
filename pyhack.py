import random
import sys,os
import curses
import math

def diceroll(number, dx, bonus):
    total = bonus
    loop = number
    while loop > 0:
        total += random.randint(1,dx)
        loop -= 1
    return total

##classes for monsters
monsters = []

class monster:
    def __init__(self, id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid):
        self.id = id
        self.x = x
        self.y = y
        self.HP = HP
        self.HPMax = HPMax
        self.AC = AC
        self.dred = dred
        self.number = number
        self.dx = dx
        self.bonus = bonus
        self.ai = ai
        self.speed = speed
        self.symbol = symbol
        self.display = display
        self.rarity = rarity
        self.power = power
        self.alignment = alignment
        self.effects = effects
        self.peacefuls = peacefuls
        self.chats = chats
        self.stuff= stuff
        self.color = color
        self.intel = intel
        self.humanoid = humanoid

    def chat(self):
        messageappend(self.chats[random.randint(1, len(self.chats))-1])

    def attack(self, target):
        specialusers = [rust, highwayman, watchman, vampire, kingrat, gremlin, flamingskeleton, imp, somethingcubus, demon, goldbug]
        flag = 0
        special = 0
        for it in self.stuff:
            if isinstance(it, weapon):
                if it.number*it.dx > self.number*self.dx:
                    weaponchoice = it
                    flag = 1
        for sp in specialusers:
            if isinstance(self, sp):
                special = 1
        if flag == 0 or special == 1:
            if diceroll(1, 20, self.bonus) >= target.AC:
                if special == 1:
                    self.special(target)
                damage = diceroll(self.number, self.dx, int(self.bonus/4))- target.dred
                if damage > 0:
                    messageappend("The " + self.display + " attacks " + target.display + "!")
                    target.HP -= damage
                else:
                    messageappend("The " + self.display + "'s attack doesn't seem to harm " + target.display + "!")
            else:
                messageappend("The " + self.display + "'s attack missed " + target.display + "!")
        else:
            weapon.attack(weaponchoice, self, target, 0)
            return
 
    def act(self):
        ##Things every move will need
        findpoint(self.x, self.y).monster = 0
        eligiblemoves = []
        eligibleloop = [".", "#", "+", "<", ">", "^"]
        for x in eligibleloop:
            eligiblemoves += checkadj(findpoint(self.x, self.y), x, 0)
        killlist = []

        if pc.clss in self.peacefuls or pc.race in self.peacefuls:
            for x in eligiblemoves:
                if x.monster == pc:
                    killlist.append(x)

        eligibletargets = vision(self, 8)

        ##To be fair, you need to have a very high IQ to find items
        finaltarget = 0
        flag = 0
        flagger = 0
        treligible = []
        if self.intel == 1:
            if len(findpoint(self.x, self.y).items) > 0:
                if len(check4(self.stuff, weapon)) > 0:
                    myweapon = check4(self.stuff, weapon)[0]
                else:
                    myweapon = 0
                for we in findpoint(self.x, self.y).items:
                    if (myweapon != 0 and isinstance(we, weapon) and myweapon.number*myweapon.dx < we.number*we.dx):
                       flagger = 1
                    if (len(check4(self.stuff, weapon)) == 0 and isinstance(we, weapon) == True and self.number*self.dx < we.number*we.dx):
                        flagger = 1
                    if flagger == 1:
                        if isinstance(myweapon, weapon):
                            findpoint(self.x, self.y).items.append(myweapon)
                            self.stuff.remove(myweapon)
                            if findpoint(self.x, self.y) in vision(pc, 6):
                                messageappend("The " + self.display + " drops its " + myweapon.display)
                        self.stuff.append(we)
                        myweapon = we
                        findpoint(self.x, self.y).items.remove(myweapon)
                        if findpoint(self.x, self.y) in vision(pc, 6):
                            messageappend("The " + self.display + " wields a " + myweapon.display)
            else:
                flag = 1

            if flag == 1:
                for el in eligibletargets:
                    for eli in el.items:
                        if eli.monsterusable == 1 and el.monster == 0 and eli not in purchasable:
                            if isinstance(eli, armor) == False and isinstance(eli, weapon) == False:
                                treligible.append(el)
                                break
                            if self.humanoid == 1:
                                if len(check4(self.stuff, weapon)) > 0:
                                    myweapon = check4(self.stuff, weapon)[0]
                                    if isinstance(eli, weapon) and myweapon.number*myweapon.dx < eli.number*eli.dx:
                                        treligible.append(el)
        if self.alignment == "evil" and flagger == 0:
            for el in eligibletargets:
                if el.monster == pc:
                    finaltarget = el
                    break

        if finaltarget == 0 and len(treligible) > 0:
            finaltarget = treligible[random.randint(1, len(treligible)) - 1]

        ##TEAM EVIL YEAH
        if self.alignment == "evil":
            for x in eligiblemoves:
                if isinstance(x.monster, monster) is True:
                    if x.monster.alignment == "evil":
                        killlist.append(x)

        for x in killlist:
            eligiblemoves.remove(x)

        ##Random AI, choose completely random moves        
        if self.ai == "random":
            if len(eligiblemoves) == 1:
                target = eligiblemoves[0]
            if len(eligiblemoves) == 0:
                target = findpoint(self.x, self.y)
            if len(eligiblemoves) > 1:
                target = eligiblemoves[random.randint(1, len(eligiblemoves))-1]

        ##Targeted AI, seek and destroy the player
        if self.ai == "primitive":
            flag = 0
            if finaltarget == 0:
                flag = 1
            dorandom = 1
            moveables = []
            if flag == 0 and pc.clss not in self.peacefuls and pc.race not in self.peacefuls:
                if self.x < finaltarget.x and findpoint(self.x+1, self.y) in eligiblemoves:
                    moveables.append(findpoint(self.x+1, self.y))
                    dorandom = 0
                if self.x > finaltarget.x and findpoint(self.x-1, self.y) in eligiblemoves:
                    moveables.append(findpoint(self.x-1, self.y))
                    dorandom = 0
                if self.y < finaltarget.y and findpoint(self.x, self.y+1) in eligiblemoves:
                    moveables.append(findpoint(self.x, self.y+1))
                    dorandom = 0
                if self.y > finaltarget.y and findpoint(self.x, self.y-1) in eligiblemoves:
                    moveables.append(findpoint(self.x, self.y-1))
                    dorandom = 0
                for x in self.effects:
                    if "stunned" in x:
                        dorandom = 1

            if dorandom == 1:
                self.ai = "random"
                self.act()
                self.ai = "primitive"
                return
            else:
                target = moveables[random.randint(1, len(moveables))-1]

        ##Shopkeeping AI
        if self.ai == "shopkeep":
            killlist = []
            for po in eligiblemoves:
                if po.type == "door" or abs(po.x - self.anchor.x) >= 2 or abs(po.y - self.anchor.y) >= 2:
                    killlist.append(po)
            for hit in killlist:
                eligiblemoves.remove(hit)
            flag = 0
            for it in pc.debts:
                if it in self.protective:
                    flag = 1
            if flag == 0:
                target = eligiblemoves[random.randint(1, len(eligiblemoves))-1]
            else:
                target = self.anchor

        ##Movement
        if target.monster == 0:
            self.x = target.x
            self.y = target.y
            target.monster = self
        else:
            findpoint(self.x, self.y).monster = self
            self.attack(target.monster)

    def anger(self):
        flag = 0
        if pc.clss in self.peacefuls:
            self.peacefuls.remove(pc.clss)
            flag = 1
        if pc.race in self.peacefuls:
            self.peacefuls.remove(pc.race)
            flag = 1
        if flag == 1:
            self.ai = "primitive"
            self.alignment = "evil"
        return flag

##classes for objects
class weapon:
    def __init__(self, id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol = ")", color = 2, monsterusable = 1):
        self.id = id
        self.weight = weight
        self.number = number
        self.dx = dx
        self.ability = ability
        self.attributes = attributes
        self.value = value
        self.rarity = rarity
        self.display = display
        self.skill = skill
        self.symbol = symbol
        self.color = color
        self.monsterusable = monsterusable
    
    def attack(self, origin, target, tpoint):
        bonus = 0
        atkbonus = 0
        for x in self.attributes:
            if x is int:
                bonus += x
        
        counter = -1        
        if origin == pc:
            if self.ability == "DEX":
                bonus += mod(pc.DEX)
            else:
                bonus += mod(pc.STR)
            counter = 0
            for x in weaponskills:
                if self.skill == x:
                    skillselect = pc.skills[counter]
                    break
                else:
                    counter += 1
            atkbonus += (-4/(skillselect+1)) + 2*skillselect
            if monster.anger(target) == 1:
                messageappend("'Hey, what's the big idea?' the " + target.display + " shouts")
                for x in vision(pc, 6):
                    if type(x.monster) == type(target) and x.monster != 0 and x.monster != target:
                        monster.anger(x.monster)
                        messageappend("The " + x.monster.display + " looks angry!")       
            monster.anger(target)
            displaynames = ["Your attack does no damage!", "You strike the " + target.display +"!", "You kill the " + target.display + "!", "Your attack missed!", int(5*target.power)]
        else:
            counter = -1
            atkbonus += origin.bonus
            bonus = int(origin.bonus/4)
            messageappend("The " + origin.display + " swings its " + self.display)
            displaynames = ["The " + origin.display + "'s attack does no damage!", "The " + origin.display + " hits!", "The " + origin.display + " kills the " + target.display + "!", "The " + origin.display + "'s attack missed!", 0]
            if target == pc:
                displaynames[2] = "The " + origin.display + " kills you..."
        

        if diceroll(1, 20, (round(pc.LVL/4, 1)+1+atkbonus+bonus)) >= target.AC:
            if counter > -1:
                pc.training[counter] += 1
                if pc.training[counter] >= 20 + (30 + 10*pc.skills[counter]-1) * pc.skills[counter] and pc.skills[counter] < pc.clss.maxskills[counter]:
                    messageappend("You feel more dangerous!")
                    
                    pc.skills[counter] += 1

            sus = diceroll(self.number, self.dx, bonus)
            if sus <= target.dred:
                messageappend(displaynames[0])
            else:
                target.HP -= sus - target.dred
                messageappend(displaynames[1])
                if target.HP <= 0:
                    messageappend(displaynames[2])
                    pc.XP += displaynames[4]
        else:
            messageappend(displaynames[3])

class wand:
    def __init__(self, id, charges, display, rarity, value, equivalentspell, caneffect, color, monsterusable, symbol = "/", weight = 5):
        self.id = id
        self.charges = charges
        self.display = display
        self.rarity = rarity
        self.value = value
        self.equivalentspell = equivalentspell
        self.caneffect = caneffect
        self.symbol = symbol
        self.weight = weight
        self.color = color
        self.monsterusable = monsterusable

        self.charges = diceroll(2, round(self.value/20, 1), 2)

    def zap(self, zapper, stdscr):
        if self.charges <= 0:
            messageappend("But nothing happened")
            return
        else:
            self.charges -= 1
        if self.equivalentspell != 0:
            direction = [0, 0]
            if self.equivalentspell.shape != "nil":
                direction = determinedirection(stdscr)
            spellbook.cast(self.equivalentspell, direction, "wand", zapper, stdscr)
            return

class armor:
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol = "]", color = 2, monsterusable = 0):
        self.id = id
        self.weight = weight
        self.ACbase = ACbase
        self.dred = dred
        self.attributes = attributes
        self.value = value
        self.rarity = rarity
        self.display = display
        self.material = material
        self.symbol = symbol
        self.color = color
        self.monsterusable = monsterusable

class spellbook:
    def __init__(self, id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol = "+", weight = 20, color = 3, monsterusable = 0):
        self.id = id
        self.display = display
        self.level = level
        self.range = range
        self.rarity = rarity
        self.value = value
        self.targets = targets
        self.caneffect = caneffect
        self.shape = shape
        self.actions = actions
        self.school = school
        self.symbol = symbol
        self.weight = weight
        self.color = color
        self.monsterusable = monsterusable
    
    def read(self, user, stdscr):
        if user == pc:
            if diceroll(1, 20, mod(pc.INT)) >= 17 - (pc.LVL*(1 + 2*pc.clss.spellskill)) + (self.level/2):
                turn = 0
                while turn < self.actions:
                    flag = 0
                    for x in vision(pc, 10):
                        if x.monster != 0:
                            flag = 1
                    if flag == 1:
                        messageappend("You spy a monster out of the corner of your eye while reading!")
                        return
                    turnup(stdscr)
                    turn += 1

                self.checkfail(None)

                spellname = ""
                loop = len(self.display) - 12
                while loop > 0:
                    spellname += self.display[len(self.display) - loop]
                    loop -= 1

                messageappend("You have learned the " + spellname + " spell!")
            else:
                messageappend("The spellbook's incomprehensible runes burn your eyes!")
                pc.HP -= diceroll(2, 3+pc.LVL, 5-mod(pc.clss.spell))

    def checkfail(self, recall):
        if recall == None:
            recall = 1500+mod(pc.INT)*200
        skill = 0
        loop = 0
        for sp in spellskills:
            if spellskills[loop] == self.school:
                skill = loop
                break
            loop += 1
        odds = 5.5*pc.clss.spell
        difficulty = (self.level*4) - (pc.clss.spellstart[skill]*6) - (pc.LVL/3) - 5
        if difficulty > 0:
            odds -= math.sqrt((900*difficulty) + 2000)
        penalty = 10*(1-pc.clss.spellskill)-pc.clss.spellstart[skill]
        for it in [pc.helm, pc.chest, pc.boots]:
            if isinstance(it, int) == False and it.material == "metal":
                penalty += it.ACbase
        chance = ((odds*(20-penalty))/15)-penalty
        if chance < 0:
            chance = 0
        if chance > 100:
            chance = 100
        pc.spells.append([self, recall, chance])

    def cast(self, direction, user, origin, stdscr):
        if user == pc:
            totalrange = self.range + int(mod(pc.clss.spell)**0.5)
        else:
            totalrange = self.range + 1

        findpoint(pc.x, pc.y).monster = pc
        targets = []
        ##direction should be [x, y]
        if self.shape == "line":
            loop = 0
            tpoint = findpoint(origin.x + direction[0], origin.y + direction[1])
            while loop < totalrange:
                if tpoint.type in nomove:
                    break
                flag = 0
                while True:
                    if isinstance(tpoint.monster, monster) and monster in self.caneffect:
                        flag = 1
                        break
                    if isinstance(tpoint.type, self.caneffect[0]):
                        flag = 1
                        break
                    if tpoint.monster == pc and monster in self.caneffect:
                        flag = 1
                        break
                    break
                if flag == 1:
                    if tpoint not in targets:
                        targets.append(tpoint)
                    if len(targets) >= self.targets:
                        break
                if 0 < tpoint.x+direction[0] < 71 and 0 < tpoint.y+direction[1] < 21:
                    tpoint = findpoint(tpoint.x + direction[0], tpoint.y + direction[1])
                loop += 1
        else:
            ##direction should be "up" etc
            if self.shape == "cone":
                if direction[0] == 1:
                    direction = "right"
                if direction[0] == -1:
                    direction = "left"
                if direction[1] == 1:
                    direction = "up"
                if direction[1] == -1:
                    direction = "down"
                for target in triangle(origin, 1, direction, round(totalrange, 2)):
                    targets.append(target)
            else:
                targets = [point(0, 0, 0, 0, 0, 0, 0, 0, 0)]
        if user != pc:
            for x in targets:
                self.effect(x, user, stdscr)
            return

        if pc.MP >= self.level*5 and user == pc:
            pc.MP -= self.level*5
            for x in targets:
                if isinstance(x.monster, monster) == True and monster in self.caneffect:
                    if self.school != "healing":
                        monster.anger(x.monster)
                    else:
                        messageappend("'Hey thanks buddy!' the " + x.monster.display + " says")
                self.effect(x, user, stdscr)
                if x.monster != 0:
                    if x.monster.HP <= 0 and user == pc:
                        messageappend("You kill the " + x.monster.display + "!")
                        pc.XP += 5*x.monster.power
                        x.monster = 0
        else:
            messageappend("You do not have the energy to cast this spell!")
            return

class scroll:
    def __init__(self, id, display, rarity, value, equivalentspell, caneffect, monsterusable, symbol = "?", weight = 10, color = 2):
        self.id = id
        self.display = display
        self.rarity = rarity
        self.value = value
        self.equivalentspell = equivalentspell
        self.caneffect = caneffect
        self.monsterusable = monsterusable
        self.symbol = symbol
        self.weight = weight
        self.color = color

    def read(self, reader, stdscr):
        if self.equivalentspell != 0:
            spellbook.cast(self.equivalentspell, [0,0], "scroll", findpoint(reader.x, reader.y), stdscr)
            reader.stuff.remove(self)
        else:
            if isinstance(self, map):
                for x in points:
                    if x not in pc.memory:
                        pc.memory.append(x)
                reader.stuff.remove(self)
                return

class potion:
    def __init__(self, id, display, rarity, value, equivalentspell, color, monsterusable, symbol = "!", weight = 12):
        self.id = id
        self.display = display
        self.rarity = rarity
        self.value = value
        self.equivalentspell = equivalentspell
        self.symbol = symbol
        self.weight = weight
        self.color = color
        self.monsterusable = monsterusable
    
    def drink(self, drinker, stdscr):
        if self.equivalentspell != 0:
            self.equivalentspell.effect(findpoint(drinker.x, drinker.y), "scroll", stdscr)
        else: 
            if isinstance(self, phaste):
                if drinker == pc:
                    pc.statuses.append(["haste", random.randint(10, 30)])
                    messageappend("The world seems to slow down around you")
                    return
            if isinstance(self, pskill):
                if drinker == pc:
                    counter = 0
                    forupgrade = []
                    for x in pc.clss.maxskills:
                        if x > 0 and x > pc.skills[counter]:
                            forupgrade.append(counter)
                        counter += 1
                    pc.skills[forupgrade[random.randint(1, len(forupgrade))-1]] += 1
                    messageappend("You feel more dangerous!")
                    return

class point:
    def __init__(self, x, y, type, symbol, display, isroom, monster, items, color):
        self.x = x
        self.y = y
        self.type = type
        self.symbol = symbol
        self.display = display
        self.isroom = isroom
        self.monster = monster
        self.items = items
        self.color = color

class trap:
    def __init__(self, fdc, adc, rarity, severity, color, display):
        self.fdc = fdc
        self.adc = adc
        self.color = color
        self.rarity = rarity
        self.severity = severity
        self.display = display

weapons = []
armors = []
spellbooks = []
scrolls = []
potions = []
wands = []

class hand(weapon):
    def __init__(self, id, weight = 0, number = 1, dx = 2, ability = "STR", attributes = [], value = 0, rarity = 0, display = "hand", skill = "boxing", symbol = "hand"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class knuckle(weapon):
    def __init__(self, id, weight = 0, number = 1, dx = 3, ability = "STR", attributes = [], value = 15, rarity = 2, display = "knuckleduster", skill = "boxing", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class gauntlet(weapon):
    def __init__(self, id, weight = 0, number = 1, dx = 4, ability = "STR", attributes = [], value = 25, rarity = 4, display = "gauntlet", skill = "boxing", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)    

class knife(weapon):
    def __init__(self, id, weight = 1, number = 1, dx = 3, ability = "DEX", attributes = [], value = 3, rarity = 10, display = "knife", skill = "knife", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class dagger(weapon):
    def __init__(self, id, weight = 1, number = 1, dx = 4, ability = "DEX", attributes = [], value = 5, rarity = 5, display = "dagger", skill = "knife", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class rapier(weapon):
    def __init__(self, id, weight = 4, number = 1, dx = 6, ability = "DEX", attributes = [], value = 25, rarity = 7, display = "rapier", skill = "rapier", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class duelingsword(weapon):
    def __init__(self, id, weight = 5, number = 1, dx = 8, ability = "DEX", attributes = [], value = 30, rarity = 10, display = "dueling sword", skill = "rapier", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class bastardsword(weapon):
    def __init__(self, id, weight = 12, number = 1, dx = 7, ability = "STR", attributes = [], value = 40, rarity = 8, display = "bastard sword", skill = "longsword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class longsword(weapon):
    def __init__(self, id, weight = 12, number = 1, dx = 8, ability = "STR", attributes = [], value = 50, rarity = 5, display = "longsword", skill = "longsword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class greatsword(weapon):
    def __init__(self, id, weight = 20, number = 2, dx = 6, ability = "STR", attributes = [], value = 100, rarity = 3, display = "greatsword", skill = "two-handed sword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class mace(weapon):
    def __init__(self, id, weight = 8, number = 1, dx = 6, ability = "STR", attributes = [], value = 10, rarity = 10, display = "mace", skill = "mace", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class morningstar(weapon):
    def __init__(self, id, weight = 18, number = 2, dx = 5, ability = "STR", attributes = [], value = 15, rarity = 4, display = "morningstar", skill = "mace", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)    

class cudgel(weapon):
    def __init__(self, id, weight = 6, number = 1, dx = 4, ability = "STR", attributes = [], value = 8, rarity = 7, display = "cudgel", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)  

class shillelagh(weapon):
    def __init__(self, id, weight = 6, number = 1, dx = 5, ability = "STR", attributes = [], value = 9, rarity = 3, display = "shillelagh", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)  

class nightstick(weapon):
    def __init__(self, id, weight = 4, number = 1, dx = 5, ability = "STR", attributes = [], value = 10, rarity = 0, display = "nightstick", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class greatclub(weapon):
    def __init__(self, id, weight = 11, number = 2, dx = 4, ability = "STR", attributes = [], value = 18, rarity = 2, display = "greatclub", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class quarterstaff(weapon):
    def __init__(self, id, weight = 5, number = 1, dx = 6, ability = "STR", attributes = [], value = 8, rarity = 6, display = "quarterstaff", skill = "staff", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class crook(weapon):
    def __init__(self, id, weight = 4, number = 1, dx = 5, ability = "STR", attributes = [], value = 12, rarity = 2, display = "crook", skill = "staff", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

weaponskills = ["boxing", "knife", "rapier", "longsword", "two-handed sword", "mace", "club", "staff"]

class chest(armor):
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)
        self.MaxDex = MaxDex

class robe(chest):
    def __init__(self, id, weight = 2, ACbase = 1, dred = 0, attributes = [], value = 15, rarity = 5, display = "robe", material = "cloth", symbol = "]", MaxDex = 6):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)

class leather(chest):
    def __init__(self, id, weight = 20, ACbase = 1, dred = 0, attributes = [], value = 15, rarity = 20, display = "leather armor", material = "leather", symbol = "]", MaxDex = 8):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)

class studdedleather(chest):
    def __init__(self, id, weight = 30, ACbase = 3, dred = 0, attributes = [], value = 20, rarity = 15, display = "studded leather armor", material = "leather", symbol = "]", MaxDex = 7):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)    

class cuirass(chest):
    def __init__(self, id, weight = 35, ACbase = 4, dred = 0, attributes = [], value = 25, rarity = 10, display = "cuirass", material = "metal", symbol = "]", MaxDex = 5):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)  

class scalemail(chest):
    def __init__(self, id, weight = 55, ACbase = 4, dred = 1, attributes = [], value = 50, rarity = 15, display = "scale mail", material = "metal", symbol = "]", MaxDex = 2):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)

class ringmail(chest):
    def __init__(self, id, weight = 60, ACbase = 3, dred = 1, attributes = [], value = 30, rarity = 20, display = "ring mail", material = "metal", symbol = "]", MaxDex = 1):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)

class chain(chest):
    def __init__(self, id, weight = 65, ACbase = 5, dred = 2, attributes = [], value = 70, rarity = 12, display = "chainmail", material = "metal", symbol = "]", MaxDex = 1):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)

class fieldplate(chest): 
    def __init__(self, id, weight = 80, ACbase = 5, dred = 2, attributes = [], value = 120, rarity = 8, display = "field plate", material = "metal", symbol = "]", MaxDex = 2):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)

class plate(chest):
    def __init__(self, id, weight = 95, ACbase = 6, dred = 3, attributes = [], value = 150, rarity = 5, display = "plate mail", material = "metal", symbol = "]", MaxDex = 0):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol, MaxDex)


class helm(armor):
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)

class cone(helm):
    def __init__(self, id, weight = 1, ACbase = 0, dred = 0, attributes = [], value = 5, rarity = 3, display = "cone", material = "cloth", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)

class jestercap(helm):
    def __init__(self, id, weight = 1, ACbase = 0, dred = 0, attributes = [], value = 8, rarity = 1, display = "jester's cap", material = "cloth", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)

class cap(helm):
    def __init__(self, id, weight = 2, ACbase = 1, dred = 0, attributes = [], value = 10, rarity = 5, display = "cap", material = "leather", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol) 

class pot(helm):
    def __init__(self, id, weight = 5, ACbase = 1, dred = 0, attributes = [], value = 5, rarity = 7, display = "cookpot", material = "metal", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol) 

class plume(helm):
    def __init__(self, id, weight = 5, ACbase = 1, dred = 0, attributes = [], value = 12, rarity = 4, display = "plumed helm", material = "metal", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)


class boots(armor):
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)

class cowboyboots(boots):
    def __init__(self, id, weight = 3, ACbase = 1, dred = 0, attributes = [], value = 15, rarity = 2, display = "cowboy boots", material = "leather", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol) 

class slippers(boots):
    def __init__(self, id, weight = 1, ACbase = 0, dred = 0, attributes = [], value = 3, rarity = 1, display = "slippers", material = "cloth", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol) 

class greaves(boots):
    def __init__(self, id, weight = 10, ACbase = 2, dred = 0, attributes = [], value = 30, rarity = 2, display = "greaves", material = "metal", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol)    


##############
##Spellbooks##
##############
spellskills = ["attack", "divination", "enchantment", "escape", "faith", "healing", "matter"]

##Enchantment Spells
class stunmonster(spellbook):
    def __init__(self, id, display = "spellbook of stun monster", level = 1, range = 2, rarity = 30, value = 100, targets = 1, caneffect = [monster], shape = "line", actions = 12, school = "enchantment", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)
    
    def effect(self, target, user, stdscr):
        if user == pc:
            bonus = mod(pc.clss.spell)
            block = 8+target.monster.power
        else: 
            if user == "wand":
                bonus = 2
            else:
                bonus = int(user.power/2)
            if isinstance(target, monster):
                block = 8+target.monster.power
            else:
                block = 8+mod(pc.CON)
        if diceroll(1, 20, bonus) >= block:
            flag = 0
            for x in target.monster.effects:
                if "stunned" in x:
                    x[1] += random.randint(2, bonus)
                    flag = 1
            if flag == 0:
                target.monster.effects.append(["stunned", random.randint(2, bonus)+1])
            messageappend("The " + target.monster.display + " seems dazed!")
        else:
            messageappend("The " + target.monster.display + " resists!")
        return        

class slow(spellbook):
    def __init__(self, id, display = "spellbook of slow", level = 2, range = 3, rarity = 15, value = 200, targets = 2, caneffect = [monster], shape = "line", actions = 22, school = "enchantment", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)  

    def effect(self, target, user, stdscr):
        if user == pc:
            if diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                flag = 0
                for x in target.monster.effects:
                    if "slow" in x:
                        x[1] += random.randint(2, mod(pc.clss.spell))
                        flag = 1
                if flag == 0:
                    target.monster.effects.append(["slow", random.randint(2, mod(pc.clss.spell))+1])
                messageappend("The", target.monster.display, "seems to be moving slower!")
            else:
                messageappend("The", target.monster.display, "resists!")
        return


##Clerical Spells
class turnundead(spellbook):
    def __init__(self, id, display = "spellbook of turn undead", level = 2, range = 4, rarity = 12, value = 200, targets = 16, caneffect = [monster], shape = "cone", actions = 24, school = "faith", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol) 

    def effect(self, target, user, stdscr):
        undead = ["Z", "S", "V", "W"]
        if target.monster != 0:
            if target.monster.symbol in undead and diceroll(1, 20, mod(pc.clss.spell)) >= 8 + target.monster.power:
                target.monster.HP -= diceroll(1,6,mod(pc.clss.spell))
                target.monster.effects.append(["stunned", random.randint(mod(pc.clss.spell), mod(pc.clss.spell)+3)])
                messageappend("The " + target.monster.display + " recoils!")
            return

##Attack Spells
class mortonaloysiussaintclairjunior(spellbook):
    def __init__(self, id, display = "spellbook of e. barrage", level = 1, range = 4, rarity = 40, value = 100, targets = 3, caneffect = [monster], shape = "line", actions = 20, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        if user == pc:
            maxdice = int(pc.LVL/3)
        else:
            maxdice = 1

        if diceroll(1, 20, 6) >= target.monster.AC:
            target.monster.HP -= diceroll(1, 6 + maxdice, 4)
            messageappend("The glob of energy strikes the " + target.monster.display + "!")
        else:
            messageappend("The " + target.monster.display + " resists!")
        return

class magicmissile(spellbook):
    def __init__(self, id, display = "spellbook of magic missile", level = 2, range = 5, rarity = 25, value = 200, targets = 4, caneffect = [monster], shape = "line", actions = 24, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        if user == pc:
            bonus = int(mod(pc.clss.spell))
            maxdice = int(pc.LVL/3)
        else:
            bonus = 4
            maxdice = 1

        if diceroll(1,20, bonus) >= target.monster.AC:
            target.monster.HP -= diceroll(2, 6 + maxdice, bonus)
            messageappend("The magic missle strikes the " + target.monster.display + "!")
        else:
            target.monster.HP -= diceroll(1, 6 + maxdice, 0)
            messageappend("The " + target.monster.display + " resists!")
        return

class vampirictouch(spellbook):
    def __init__(self, id, display = "spellbook of vampiric touch", level = 2, range = 1, rarity = 10, value = 200, targets = 1, caneffect = [monster], shape = "line", actions = 18, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol) 

    def effect(self, target, user, stdscr):
        if user == pc:
            if diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                drainage = diceroll(2, 4, 0)
                target.monster.HP -= drainage
                pc.HP += drainage
                if pc.HP > pc.HPMax:
                    pc.HP = pc.HPMax
                messageappend("The", target.monster.display, "looks weaker!")
            else:
                messageappend("The", target.monster.display, "resists!")
        return

class coneofcold(spellbook):
    def __init__(self, id, display = "spellbook of cone of cold", level = 4, range = 4, rarity = 3, value = 400, targets = 16, caneffect = [monster], shape = "cone", actions = 42, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)    

    def effect(self, target, user, stdscr):
        if user == pc:
            if isinstance(target.monster, monster):
                if diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                    target.monster.HP -= diceroll(3, 6, 2)
                    target.monster.speed -= mod(pc.clss.spell)/2.5*target.monster.power - 0.5*pc.clss.spellskill
                    messageappend("The", target.monster.display, "is chilled out!")
                else:
                    target.monster.HP -= diceroll(2, 4, 0)
                    messageappend("The", target.monster.display, "resists!")
        return

##Divination
class detectmo(spellbook):
    def __init__(self, id, display = "spellbook of detect monsters", level = 1, range = 0, rarity = 14, value = 100, targets = 0, caneffect = [], shape = "nil", actions = 20, school = "divination", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)  

    def effect(self, target, user, stdscr):
        symbollog = []
        for po in points:
            if po.monster != 0 and po.monster != pc:
                symbollog.append(po.symbol)
                po.symbol = po.monster.symbol
                pc.memory.append(po)
        display(stdscr)
        pause = chr(stdscr.getch())
        counter = 0
        for x in points:
            if x.monster != 0 and x.monster != pc:
                x.symbol = symbollog[counter]
                counter += 1
                pc.memory.remove(x)
        return

class detecttr(spellbook):
    def __init__(self, id, display = "spellbook of detect treasure", level = 1, range = 0, rarity = 10, value = 100, targets = 0, caneffect = [], shape = "nil", actions = 20, school = "divination", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        symbollog = []
        for po in points:
            if len(po.items) > 0:
                symbollog.append(po.symbol)
                po.symbol = po.items[len(po.items)-1].symbol
                pc.memory.append(po)
        display(stdscr)
        pause = chr(stdscr.getch())
        counter = 0
        for x in points:
            if len(x.items) > 0:
                x.symbol = symbollog[counter]
                counter += 1
                pc.memory.remove(x)
        return

class insight(spellbook):
    def __init__(self, id, display = "spellbook of insight", level = 2, range = 3, rarity = 7, value = 200, targets = 1, caneffect = [monster], shape = "line", actions = 36, school = "divination", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        stdscr.addstr(6, 71, target.monster.display, WHITE_ON_BLACK)
        stdscr.addstr(7, 71, "AC: " + str(target.monster.AC), WHITE_ON_BLACK)
        stdscr.addstr(8, 71, "HP: " + str(target.monster.HP) + "/" + str(target.monster.HPMax), WHITE_ON_BLACK)
        stdscr.addstr(9, 71, "Damage: " + str(target.monster.number + int(target.monster.bonus/4)) + "-" + str(target.monster.number*target.monster.dx + int(target.monster.bonus/4)), WHITE_ON_BLACK)
        return

##Escape
class teleport(spellbook):
    def __init__(self, id, display = "spellbook of teleport", level = 4, range = 2 , rarity = 4, value = 400, targets = 1, caneffect = [monster], shape = "line", actions = 76, school = "escape", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        teligible = []
        flagerino = 0
        if target.monster == pc:
            for x in shopkeeps:
                if findpoint(target.x, target.y).isroom == x.shopid:
                    angeredshop = x
                    flagerino = 1
            if flagerino == 1:
                flag = 0
                for it in pc.stuff:
                    if it in purchasable:
                        if it in angeredshop.protective:
                            monster.anger(angeredshop)
                        flag = 1

                if flag == 1:
                    soundthealarm(target)
        for po in points:
            if po.type not in nomove and po.monster == 0:
                teligible.append(po)
        poggers = target.monster
        tpoint = teligible[random.randint(1, len(teligible))-1]
        if poggers == pc:
            pc.memory.append(tpoint)
        poggers.x = tpoint.x
        poggers.y = tpoint.y
        tpoint.monster = poggers
        target.monster = 0
        return

##Healing
class cure(spellbook):
    def __init__(self, id, display = "spellbook of cure", level = 1, range = 3, rarity = 30, value = 100, targets = 2, caneffect = [monster], shape = "line", actions = 20, school = "healing", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        if user == pc:
            bonus = int(mod(pc.clss.spell)/2)
        else:
            bonus = 4
        target.monster.HP += diceroll(2, 6, bonus)
        if target.monster.HP > target.monster.HPMax:
            target.monster.HP = target.monster.HPMax
        if target.monster == pc:
            messageappend("You feel better")
        return

class cure2(spellbook):
    def __init__(self, id, display = "spellbook of heal", level = 3, range = 3, rarity = 12, value = 300, targets = 2, caneffect = [monster], shape = "line", actions = 54, school = "healing", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        if user == pc:
            bonus = int(mod(pc.clss.spell))
        else:
            bonus = 4
        target.monster.HP += diceroll(4, 6, bonus)
        if target.monster.HP > target.monster.HPMax:
            target.monster.HP = target.monster.HPMax
        return

##Matter
class antitrap(spellbook):
    def __init__(self, id, display = "spellbook of disable trap", level = 1, range = 2, rarity = 25, value = 100, targets = 1, caneffect = [trap], shape = "line", actions = 22, school = "matter", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

    def effect(self, target, user, stdscr):
        global presenttraps
        presenttraps.remove(target)
        if target.symbol == "^":
            messageappend("The " + target.type.display + " suddenly disappears!")
        else:
            messageappend("You feel safer")
        target.type = "floor"
        target.symbol = "."

##Scrolls
tpp = teleport(0)
class tp(scroll):
    def __init__(self, id, display = "scroll of teleportation", rarity = 50, value = 30, equivalentspell = tpp, caneffect = [], monsterusable = 1):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect, monsterusable)
    
class map(scroll):
    def __init__(self, id, display = "scroll of magic mapping", rarity = 10, value = 65, equivalentspell = 0, caneffect = [], monsterusable = 0):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect, monsterusable)

detectmoo = detectmo(0)
class detectm(scroll):
    def __init__(self, id, display = "scroll of detect monsters", rarity = 20, value = 40, equivalentspell = detectmoo, caneffect = [], monsterusable = 0):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect, monsterusable)

detecttrr = detecttr(0)
class detectt(scroll):
    def __init__(self, id, display = "scroll of detect treasure", rarity = 20, value = 35, equivalentspell = detecttrr, caneffect = [], monsterusable = 0):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect, monsterusable)


##Potions
ppheal = cure(0)
class pheal(potion):
    def __init__(self, id, display = "potion of healing", rarity = 30, value = 50, equivalentspell = ppheal, color = 4, monsterusable = 1):
        super().__init__(id, display, rarity, value, equivalentspell, color, monsterusable)

class phaste(potion):
    def __init__(self, id, display = "potion of haste", rarity = 5, value = 70, equivalentspell = 0, color = 7, monsterusable = 0):
        super().__init__(id, display, rarity, value, equivalentspell, color, monsterusable)

class pskill(potion):
    def __init__(self, id, display = "potion of skillfulness", rarity = 3, value = 80, equivalentspell = 0, color = 6, monsterusable = 0):
        super().__init__(id, display, rarity, value, equivalentspell, color, monsterusable)


##Wands
stunmo = stunmonster(0)
class baffling(wand):
    def __init__(self, id, charges = 1, display = "wand of baffling", rarity = 30, value = 75, equivalentspell = stunmo, caneffect = [monster], color = 6, monsterusable = 0):
        super().__init__(id, charges, display, rarity, value, equivalentspell, caneffect, color, monsterusable)

insit = insight(0)
class statview(wand):
    def __init__(self, id, charges = 1, display = "wand of insight", rarity = 10, value = 55, equivalentspell = insit, caneffect = [monster], color = 2, monsterusable = 0):
        super().__init__(id, charges, display, rarity, value, equivalentspell, caneffect, color, monsterusable)

arcmis = magicmissile(0)
class wagicwissile(wand):
    def __init__(self, id, charges = 1, display = "wand of magic missile", rarity = 15, value = 50, equivalentspell = arcmis, caneffect = [monster], color = 5, monsterusable = 0):
        super().__init__(id, charges, display, rarity, value, equivalentspell, caneffect, color, monsterusable)

##Gold
class gold:
    def __init__(self, value, symbol = "$", display = "gold", weight = 0, color = 6, monsterusable = 0):
        self.value = value
        self.symbol = symbol
        self.display = display
        self.weight = weight
        self.color = color
        self.monsterusable = monsterusable

##Item Lists
armorlist = [robe, leather, studdedleather, cuirass, scalemail, ringmail, fieldplate, chain, plate, cap, cone, jestercap, plume, pot, cowboyboots, slippers, greaves]
weaponlist = [hand, knuckle, nightstick, gauntlet, knife, dagger, bastardsword ,longsword, greatsword, mace, morningstar, rapier, duelingsword, cudgel, greatclub, shillelagh, crook, quarterstaff]
spellbooklist = [stunmonster, slow, mortonaloysiussaintclairjunior ,magicmissile, coneofcold, vampirictouch, turnundead, detectmo, detecttr, insight, teleport, cure, cure2, antitrap] ##, protection]
scrolllist = [tp, map, detectm, detectt]
potionlist = [pheal, phaste, pskill]
wandlist = [baffling, statview, wagicwissile]

stuff = armorlist + weaponlist + spellbooklist + scrolllist + potionlist + wandlist


##classes for pc and map
class warp(trap):
    def __init__(self, fdc = 16, adc = 15, rarity = 40, severity = 5, color = 7, display = "teleportation trap"):
        super().__init__(fdc, adc, rarity, severity, color, display)
    
    def trigger(self, target, stdscr):
        global messages
        if target.monster == pc:
            messageappend("You feel a wrenching sensation")
        teleport.effect(teleport(0), target, "scroll", stdscr)

class trapdoor(trap):
    def __init__(self, fdc = 10, adc = 14, rarity = 30, severity = 7, color = 6, display = "trapdoor"):
        super().__init__(fdc, adc, rarity, severity, color, display)
    
    def trigger(self, target, stdscr):
        global DLVL
        global messages
        if target.monster == pc:
            messageappend("A trap door opens beneath you!")
            DLVL += 1
            dungeonlayout()
            pc.memory.remove(findpoint(pc.x, pc.y))
            teleport.effect(teleport(0), findpoint(pc.x, pc.y), "scroll", stdscr)    

class rusttrap(trap):
    def __init__(self, fdc = 12, adc = 15, rarity = 70, severity = 4, color = 5, display = "rust trap"):
        super().__init__(fdc, adc, rarity, severity, color, display)
    
    def trigger(self, target, stdscr):
        global messages
        if target.monster == pc:
            messageappend("You are struck by a jet of water!")
            rust.special(rust(0, 0, 0), pc)

class rocksfall(trap):
    def __init__(self, fdc = 12, adc = 15, rarity = 40, severity = 3, color = 2, display = "falling rock trap"):
        super().__init__(fdc, adc, rarity, severity, color, display)
    
    def trigger(self, target, stdscr):
        global messages
        if target.monster == pc:
            if pc.helm != 0 and pc.helm.material == "metal":
                messageappend("You are struck by a falling rock! Fortunately, you have a solid helmet on")
                pc.HP -= random.randint(1, 2)
            else:
                messageappend("You are struck by a falling rock!")
                pc.HP -= diceroll(2, 4, 2)

traps = [warp, trapdoor, rusttrap, rocksfall]

nomove = ["wall", "infill"]

class player:
    def __init__(self, HP, HPMax, MP, MPMax, carry, AC, dred, XP, STR, DEX, CON, INT, WIS, CHA, clss, race, name, LVL, x, y, stuff, weapon, helm, chest, boots, statuses, display, memory, skills, training, spells, wealth, debts, wizard101):
        self.HP = HP
        self.HPMax = HPMax
        self.MP = MP
        self.MPMax = MPMax
        self.carry = carry
        self.AC = AC
        self.dred = dred
        self.XP = XP
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.clss = clss
        self.race = race
        self.name = name
        self.LVL = LVL
        self.x = x
        self.y = y
        self.stuff = stuff
        self.weapon = weapon
        self.helm = helm
        self.chest = chest
        self.boots = boots
        self.statuses = statuses
        self.display = display
        self.memory = memory
        self.skills = skills
        self.training = training
        self.spells = spells
        self.wealth = wealth
        self.debts = debts
        self.wizard101 = wizard101

pc = player(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [], hand, 0, 0, 0, [], "you", [], [], [0, 0, 0, 0, 0, 0, 0, 0], [], 0, [], [0, 0, 0, 0, 0, 0, 0])

class race:
    def __init__(self, display, STR, DEX, CON, INT, WIS, CHA):
        self.display = display
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA

human = race("human", 0, 0, +1, 0, 0, +1)
elf = race("elf", 0, +2, -2, +2, 0, 0)
halfling = race("halfling", -2, +2, 0, 0, 0, +2)
gnome = race("gnome", -2, +2, +1, +1, 0, 0)
dwarf = race("dwarf", +2, -2, +2, 0, 0, 0)
orc = race("orc", +2, 0, +2, -2, 0, 0)
oni = race("oni", +4, 0, 0, -2, -1, -1)

eligibleraces = [human, elf, halfling, gnome, dwarf, orc]

class clss:
    def __init__(self, display, STR, DEX, CON, INT, WIS, CHA, spell, spellskill, baseHP, startinventory, startskills, maxskills, spellstart, spellmax):
        self.display = display
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.spell = spell
        self.spellskill = spellskill
        self.baseHP = baseHP
        self.startinventory = startinventory
        self.startskills = startskills
        self.maxskills = maxskills
        self.spellstart = spellstart
        self.spellmax = spellmax

wizard = clss("wizard", diceroll(1, 4, 8), diceroll(1, 4, 8), diceroll(1, 4, 10), diceroll(1, 4, 16), diceroll(1, 4, 10), diceroll(1, 4, 10), 1, 1, 6, [quarterstaff, robe, slippers, tp, map, mortonaloysiussaintclairjunior, magicmissile, wagicwissile], [0, 0, 0, 0, 0, 0, 0, 1], [1, 2, 0, 1, 0, 0, 1, 3], [1, 0, 1, 0, 0, 0, 0], [3, 3, 3, 3, 1, 2, 3])
priest = clss("priest", diceroll(1, 4, 10), diceroll(1, 4, 8), diceroll(1, 4, 10), diceroll(1, 4, 12), diceroll(1, 4, 16), diceroll(1, 4, 10), 2, 0.75, 8, [mace, robe, slippers, cure, turnundead, pheal], [0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 0, 3, 2, 3], [0, 0, 0, 0, 1, 1, 0], [2, 3, 1, 2, 3, 3, 3])
rogue = clss("rogue", diceroll(1, 4, 8), diceroll(1, 4, 16), diceroll(1, 4, 8), diceroll(1, 4, 8), diceroll(1, 4, 10), diceroll(1, 4, 10), 3, 0.25, 8, [dagger, leather, cowboyboots, phaste, detectt], [1, 1, 0, 0, 0, 0, 0, 0], [2, 3, 2, 1, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 1, 2, 0, 0, 1])
knight = clss("knight", diceroll(1, 4, 14), diceroll(1, 4, 10), diceroll(1, 4, 14), diceroll(1, 4, 6), diceroll(1, 4, 8), diceroll(1, 4, 8), 3, 0.25, 10, [longsword, ringmail, greaves, plume], [0, 0, 0, 1, 0, 0, 0, 0], [1, 1, 2, 3, 3, 2, 3, 1], [0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 1, 0])
bard = clss("bard", diceroll(1, 4, 8), diceroll(1, 4, 12), diceroll(1, 4, 10), diceroll(1, 4, 10), diceroll(1, 4, 8), diceroll(1, 4, 16), 3, 0.5, 8, [rapier, leather, jestercap, stunmonster, pskill, pheal], [0, 0, 1, 0, 0, 0, 0, 0], [1, 2, 3, 2, 0, 0, 2, 1], [0, 0, 1, 0, 0, 0, 0], [0, 1, 3, 2, 0, 1, 0])
redmage = clss("red mage", diceroll(1, 4, 10), diceroll(1, 4, 10), diceroll(1, 4, 12), diceroll(1, 4, 14), diceroll(1, 4, 10), diceroll(1, 4, 12), 1, 0.5, 8, [rapier, leather, cowboyboots, stunmonster, mortonaloysiussaintclairjunior], [0, 1, 1, 0, 0, 0, 0, 0], [1, 2, 3, 2, 0, 0, 1, 2], [0, 0, 1, 0, 0, 0, 0], [2, 2, 2, 2, 1, 1, 2])
investigator = clss("investigator", diceroll(1, 4, 10), diceroll(1, 4, 10), diceroll(1, 4, 10), diceroll(1, 4, 14), diceroll(1, 4, 12), diceroll(1, 4, 8), 1, 0.5, 8, [knuckle, dagger, leather, cap, map, detectmo], [1, 1, 0, 0, 0, 0, 0, 0], [2, 3, 0, 1, 0, 0, 3, 1], [0, 1, 0, 0, 0, 0, 0], [0, 2, 1, 2, 0, 0, 1])

leper = clss("leper", diceroll(1, 4, 6), diceroll(1, 4, 6), diceroll(1, 4, 4), diceroll(1, 4, 8), diceroll(1, 4, 8), diceroll(1, 4, 2), 1, 0.33, 4, [knife, slippers], [0, 1, 0, 0, 0, 0, 0, 0],[2, 2, 0, 0, 0, 1, 2, 1], [0, 0, 0, 0, 0, 0, 0], [1, 0, 1, 0, 1, 1, 0])

eligibleclasses = [wizard, priest, knight, rogue, bard, redmage, investigator, leper]
##Initialization

##Shopkeepers (ඞ)
class shopkeep(monster):
        def __init__(self, id, x, y, HP = 55, HPMax = 55, AC = 15, dred = 2, number = 4, dx = 4 , bonus = 10, ai = "shopkeep", speed = 1.5, symbol = "@", display = "shopkeep", rarity = 0, power = 15, alignment = "evil", effects = None, peacefuls = None, chats = ["'Like you, I used to be poor. So very poor'", "'Piracy is not a victimless crime!'", "'Shoplifting is wrong m'kay?'"], stuff = None, protective = None, anchor = 0, shopid = 0, color = 6, intel = 1, humanoid = 1):
            peacefuls = eligibleclasses
            effects = []
            stuff = [[100, [wagicwissile, 100, 1, 1]]]
            protective = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

##Watchmen (w)
class watchman(monster):
        def __init__(self, id, x, y, HP = 19, HPMax = 19, AC = 14, dred = 1, number = 1, dx = 5, bonus = 6, ai = "primitive", speed = 0.9, symbol = "w", display = "watchman", rarity = 0, power = 4, alignment = "evil", effects = None, peacefuls = None, chats = ["'But who watches us watchmen, man?'", "You spot a glimmer on the watchman's wrist and become transfixed watching the watchman's watch"], stuff = None, color = 2, intel = 1, humanoid = 1):
            peacefuls = eligibleclasses
            effects = []
            stuff = [[100, [nightstick, 100, 1, 1]], [60, [leather, 100, 1, 1], 20, [ringmail, 100, 1, 1], 20, [studdedleather, 100, 1, 1]]]
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
        
        def special(self, target):
            if target == pc:
                if isinstance(pc.weapon, hand) == False:
                    if random.randint(1, 15) >= mod(pc.STR) + mod(pc.DEX):
                        messageappend("The watchman's nightstick slaps your weapon from your hand!")
                        findpoint(pc.x, pc.y).items.append(pc.weapon)
                        pc.stuff.remove(pc.weapon)
                        pc.weapon = hand(0)

##Rats (r/K)
class smallrat(monster):
        def __init__(self, id, x, y, HP = 4, HPMax = 4,AC = 10, dred = 0, number = 1, dx = 3, bonus = 2, ai = "primitive", speed = 1, symbol = "r", display = "small rat", rarity = 10, power = 1, alignment = "evil", effects = None, peacefuls = None, chats = ["'Squeak squeak'"], stuff = None, color = 2, intel = 0, humanoid = 0):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class giantrat(monster):
        def __init__(self, id, x, y, HP = 8, HPMax = 8, AC = 11, dred = 0, number = 1, dx = 6, bonus = 4, ai = "primitive", speed = 1, symbol = "r", display = "giant rat", rarity = 6, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["Now that is a rodent of unusual size"], stuff = None, color = 4, intel = 0, humanoid = 0):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
            
class kingrat(monster):
        def __init__(self, id, x, y, HP = 45, HPMax = 45, AC = 14, dred = 2, number = 3, dx = 6, bonus = 10, ai = "primitive", speed = 1.2, symbol = "K", display = "rat king", rarity = 0, power = 10, alignment = "evil", effects = None, peacefuls = None, chats = ["'I actually knew the fat rat in high school'", "'I don't like em putting chemicals in the water that turn my rats ogey!'"], stuff = None, color = 7, intel = 1, humanoid = 0):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
        def special(self, target):
            spawnable = []
            rats = [smallrat, smallrat, giantrat]
            for x in checkadj(self, ".", 1):
                if x.monster == 0:
                    spawnable.append(x)
            if len(spawnable) > 0 and random.randint(1, 10) >= 4:
                tpoint = spawnable[random.randint(1, len(spawnable))-1]
                tpoint.monster = mintmonster(rats[random.randint(1, 3)-1], tpoint.x, tpoint.y)

##Plants (F)
class lichen(monster):
        def __init__(self, id, x, y, HP = 2, HPMax = 2, AC = 7, dred = 0, number = 1, dx = 2, bonus = 0, ai = "random", speed = 0.1, symbol = "F", display = "lichen", rarity = 6, power = 0.2, alignment = "neutral", effects = None, peacefuls = None, chats = ["It's a plant dummy, it can't talk"], stuff = None, color = 3, intel = 0, humanoid = 0):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

##Doglikes (d)
class coyote(monster):
        def __init__(self, id, x, y, HP = 8, HPMax = 8, AC = 12, dred = 0, number = 1, dx = 4, bonus = 4, ai = "primitive", speed = 1.25, symbol = "d", display = "coyote", rarity = 15, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'Yip yip!'"], stuff = None, color = 6, intel = 0, humanoid = 0):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

##bandit (b)
class badman(monster):
        def __init__(self, id, x, y, HP = 20, HPMax = 20, AC = 16, dred = 0, number = 3, dx = 5, bonus = 9, ai = "primitive", speed = 1.6, symbol = "b", display = "badman", rarity = 2, power = 11, alignment = "evil", effects = None, peacefuls = None, chats = [], stuff = None, color = 7, intel = 1, humanoid = 1):
            peacefuls = []
            effects = []
            stuff = []          
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class highwayman(monster):
        def __init__(self, id, x, y, HP = 15, HPMax = 15, AC = 14, dred = 0, number = 2, dx = 5, bonus = 5, ai = "primitive", speed = 1.4, symbol = "b", display = "highwayman", rarity = 4, power = 5, alignment = "evil", effects = None, peacefuls = None, chats = ["'I'm the highwayman!'", "'I make ends meet, just like any man'", "'I work with my hands'"], stuff = None, color = 4, intel = 1, humanoid = 1):
            peacefuls = [rogue]
            effects = []
            stuff = []           
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
        
        def special(self, target):
            if target == pc and pc.boots != 0:
                if random.randint(1, 5) >= 4:
                    messageappend("The highwayman steals your shoes from off your feet!")
                    self.stuff.append(pc.boots)
                    pc.stuff.remove(pc.boots)
                    pc.boots = 0

class bandit(monster):
        def __init__(self, id, x, y, HP = 7, HPMax = 7, AC = 12, dred = 0, number = 1, dx = 5, bonus = 3, ai = "primitive", speed = 1.2, symbol = "b", display = "bandit", rarity = 9, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'Why pay for things you can just steal?'"], stuff = None, color = 5, intel = 1, humanoid = 1):
            peacefuls = [rogue]
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
        
##humanoids (h/G)
class hobbit(monster):
    def __init__(self, id, x, y, HP = 6, HPMax = 6, AC = 12, dred = 0, number = 1, dx = 3, bonus = 4, ai = "primitive", speed = 0.75, symbol = "h", display = "halfling", rarity = 7, power = 1, alignment = "evil", effects = None, peacefuls = None, chats = ["'Have you seen my ring?'", "'Did you just call me a hobbit?'", "The halfling inquires about fireworks"], stuff = None, color = 3, intel = 1, humanoid = 1):
        peacefuls = [halfling, wizard, dwarf]
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class gnelf(monster):
    def __init__(self, id, x, y, HP = 7, HPMax = 7, AC = 14, dred = 0, number = 1, dx = 2, bonus = 4, ai = "primitive", speed = 0.9, symbol = "G", display = "gnome", rarity = 11, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'I'm gnot a gnelf'", "'I'm gnot a gnoblin'", "'You've been gnomed!'"], stuff = None, color = 4, intel = 1, humanoid = 1):
        peacefuls = [gnome]
        effects = []
        stuff = [[50, [cudgel, 100, 1, 1], 30, [dagger, 100, 1, 1], 20]]
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

##Undead (Z/S/V/W)
class zombie(monster):
        def __init__(self, id, x, y, HP = 15, HPMax = 15, AC = 11, dred = 1, number = 2, dx = 3, bonus = 3, ai = "primitive", speed = 0.5, symbol = "Z", display = "zombie", rarity = 15, power = 3, alignment = "evil", effects = None, peacefuls = None, chats = ["The zombie groans"], stuff = None, color = 2, intel = 0, humanoid = 1):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class skeleton(monster):
    def __init__(self, id, x, y, HP = 15, HPMax = 15, AC = 13, dred = 1, number = 1, dx = 5, bonus = 5, ai = "primitive", speed = 0.75, symbol = "S", display = "skeleton", rarity = 8, power = 5, alignment = "evil", effects = None, peacefuls = None, chats = ["The skeleton rattles"], stuff = None, color = 2, intel = 0, humanoid = 1):
        peacefuls = []
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class flamingskeleton(monster):
    def __init__(self, id, x, y, HP = 21, HPMax = 21, AC = 14, dred = 2, number = 2, dx = 4, bonus = 5, ai = "primitive", speed = 0.6, symbol = "S", display = "flaming skeleton", rarity = 6, power = 7, alignment = "evil", effects = None, peacefuls = None, chats = ["'WHERE'S MY MOTORCYCLE?'", "'NOT THE BEES, ANYTHING BUT THE BEES'"], stuff = None, color = 4, intel = 0, humanoid = 1):
        peacefuls = []
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
    
    def special(self, target):
        if target == pc:
            for it in pc.stuff:
                if isinstance(it, spellbook) or isinstance(it, scroll) or isinstance(it, armor) and it.material == "cloth":
                    if random.randint(1, 6) == 6:
                        messageappend("Your " + it.display + " burns to cinders!")
                        pc.stuff.remove(it)

class catacombsaint(monster):
    def __init__(self, id, x, y, HP = 25, HPMax = 25, AC = 16, dred = 1, number = 1, dx = 3, bonus = 8, ai = "primitive", speed = 0.8, symbol = "S", display = "catacomb saint", rarity = 3, power = 5, alignment = "evil", effects = None, peacefuls = None, chats = ["''"], stuff = None, color = 6, intel = 0, humanoid = 1):
        peacefuls = [priest]
        effects = []
        stuff = [[50, [mace, 100, 1, 1], 20, [crook, 100, 1, 1], 20, [longsword, 100, 1, 1], 10, [morningstar, 100, 1, 1]], [90, [robe, 100, 1, 1], 10, [chain, 100, 1, 1]]]
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class vampire(monster):
        def __init__(self, id, x, y, HP = 25, HPMax = 25, AC = 15, dred = 1, number = 2, dx = 8, bonus = 9, ai = "primitive", speed = 1.1, symbol = "V", display = "Vampire", rarity = 2, power = 13, alignment = "evil", effects = None, peacefuls = None, chats = ["1 wasted turn! Ah ah ah!"], stuff = None, color = 4, intel = 1, humanoid = 1):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
        
        def special(self, target):
            if target == pc:
                if random.randint(1, 20) >= pc.CON:
                    messageappend("You feel your strength draining away!")
                    pc.STR -= random.randint(1, 2)
                    pc.HPMax -= random.randint(2, 4)
                    if pc.STR <= 0:
                        pc.HP = -2

##goblins (o)
class goblin(monster):
    def __init__(self, id, x, y, HP = 7, HPMax = 7, AC = 11, dred = 0, number = 1, dx = 3, bonus = 3, ai = "primitive", speed = 1, symbol = "o", display = "goblin", rarity = 16, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'Mind goblin' deez nuts?'"], stuff = None, color = 3, intel = 1, humanoid = 1):
        peacefuls = [orc]
        effects = []
        stuff = [[20, [cudgel, 100, 1, 1], 60, [dagger, 100, 1, 1], 20]]
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

##demons (i/&)
class gremlin(monster):
    def __init__(self, id, x, y, HP = 11, HPMax = 11, AC = 12, dred = 0, number = 1, dx = 4, bonus = 6, ai = "primitive", speed = 1.25, symbol = "i", display = "gremlin", rarity = 7, power = 4, alignment = "evil", effects = None, peacefuls = None, chats = ["'Feed me after midnight'", "'Have you seen any water around here?'"], stuff = None, color = 3, intel = 1, humanoid = 0):
        peacefuls = []
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
    
    def special(self, target):
        if target == pc:
            if random.randint(1, 20) >= mod(pc.DEX):
                for x in pc.stuff:
                    if isinstance(x, potion):
                        messageappend("The gremlin drinks your " + x.display + "!")
                        pc.stuff.remove(x)
                        greligible = checkadj(findpoint(self.x, self.y), ".", 1) + checkadj(findpoint(self.x, self.y), "#", 1)
                        tgreligible = []
                        for gr in greligible:
                            if gr.monster == 0:
                                tgreligible.append(gr)
                        if len(tgreligible) > 0:
                            gremlinized = tgreligible[random.randint(1, len(tgreligible))-1]
                            gremlinized.monster = mintmonster(gremlin, gremlinized.x, gremlinized.y)
                            messageappend("You hear the great garbled groan of a greedy gremlin")

class imp(monster):
    def __init__(self, id, x, y, HP = 14, HPMax = 14, AC = 15, dred = 0, number = 1, dx = 6, bonus = 8, ai = "primitive", speed = 1.2, symbol = "i", display = "imp", rarity = 12, power = 8, alignment = "evil", effects = None, peacefuls = None, chats = ["'I'm a man of wealth and taste'", "'Who killed the Kennedys?'", "'Have some sympathy, and some taste'"], stuff = None, color = 4, intel = 1, humanoid = 0):
        peacefuls = []
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

    def special(self, target):
        if target == pc:
            if random.randint(1, 20) + mod(pc.CON) < 13:
                messageappend("The imp's sting was poisoned!")
                pc.HP -= random.randint(1, 6)
                pc.CON -= 1
                if pc.CON <= 0:
                    pc.HP = -2

class IMP(monster):
    def __init__(self, id, x, y, HP = 24, HPMax = 24, AC = 15, dred = 0, number = 1, dx = 3, bonus = 8, ai = "primitive", speed = 1.1, symbol = "i", display = "IMP", rarity = 1, power = 8, alignment = "evil", effects = None, peacefuls = None, chats = ["'The media is covering up Ozzie's part 2'", "'I need to kill you to pay for horseriding lessons'", "'No, I didn't mean that awful cough syrup soda!'"], stuff = None, color = 4, intel = 1, humanoid = 1):
        peacefuls = []
        effects = []
        stuff = [[80, [longsword, 100, 1, 1], 20, [morningstar, 100, 1, 1], 0], [100, [studdedleather, 100, 1, 1]], [34, [teleport, 100, 0, 0], 66]]
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

class somethingcubus(monster):
    def __init__(self, id, x, y, HP = 35, HPMax = 35, AC = 14, dred = 1, number = 1, dx = 6, bonus = 10, ai = "primitive", speed = 1.3, symbol = "&", display = "somethingcubus", rarity = 4, power = 10, alignment = "evil", effects = None, peacefuls = None, chats = ["'Did it hurt when you fell from heaven? It did for me'"], stuff = None, color = 2, intel = 1, humanoid = 1):
        peacefuls = []
        effects = []
        stuff = [[100, [robe, 100, 1, 1]]]
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

    def special(self, target):
        if target == pc:
            if random.randint(1, 20) + mod(pc.WIS) < 14 and len([pc.helm, pc.chest, pc.boots]) > 0:
                messageappend("The demon of questionable gender begins to undress you!")
                if pc.clss != priest:
                    wearing = []
                    for t in [pc.helm, pc.chest, pc.boots]:
                        if t != 0:
                            wearing.append(t)
                    if len(wearing) > 0:
                        removal = wearing[random.randint(1, len(wearing))-1]
                        messageappend("The demon takes your " + removal.display)
                        self.stuff.append(removal)
                        pc.stuff.remove(removal)
                        teleport.effect(teleport(0), findpoint(self.x, self.y), "scroll", 0)
                    else:
                        messageappend("However, you find you are not wearing anything")
                        if pc.CHA < 11:
                            messageappend("The somethingcubus gives you a look of disgust")
                else:
                    messageappend("Fortunately, you took an oath of celibacy upon joining the clergy")

class demon(monster):
    def __init__(self, id, x, y, HP = 80, HPMax = 80, AC = 16, dred = 3, number = 5, dx = 6, bonus = 15, ai = "primitive", speed = 0.8, symbol = "&", display = "demon", rarity = 3, power = 24, alignment = "evil", effects = None, peacefuls = None, chats = ["'Use all your well learned politesse, or I'll lay your soul to waste'"], stuff = None, color = 4, intel = 1, humanoid = 0):
        peacefuls = []
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)

    def special(self, target):
        for it in target.stuff:
            if isinstance(it, scroll) or isinstance(it, spellbook):
                if random.randint(1, 2) == 2:
                    messageappend("Your " + it.display + " burns into sulfuric cinders!")

##Rust Monster (R)
class goldbug(monster):
    def __init__(self, id, x, y, HP = 5, HPMax = 5, AC = 12, dred = 0, number = 1, dx = 2, bonus = 4, ai = "primitive", speed = 1.6, symbol = "R", display = "gold bug", rarity = 8, power = 6, alignment = "evil", effects = None, peacefuls = None, chats = ["The bug itself is actually a mottled brown color"], stuff = None, color = 6, intel = 0, humanoid = 0):
        peacefuls = []
        effects = []
        stuff = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
    
    def special(self, target):
        if target == pc:
            if pc.wealth >= 8:
                pc.wealth -= random.randint(int(pc.wealth/8), int(pc.wealth/4))
            else:
                pc.wealth = 0
            messageappend("Your wallet feels lighter!")

class rust(monster):
        def __init__(self, id, x, y, HP = 22, HPMax = 22, AC = 14, dred = 2, number = 1, dx = 2, bonus = 8, ai = "primitive", speed = 1.1, symbol = "R", display = "rust monster", rarity = 5, power = 6, alignment = "evil", effects = None, peacefuls = None, chats = ["A rust monster, programmed in python. Ironic"], stuff = None, color = 4, intel = 0, humanoid = 0):
            peacefuls = []
            effects = []
            stuff = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats, stuff, color, intel, humanoid)
        def special(self, target):
            if target == pc:
                piece = random.randint(1,3)-1
                listicle = [pc.helm, pc.chest, pc.boots]
                armored = listicle[piece]
                if isinstance(armored, armor):
                    if armored.material == "metal":
                        messageappend("Your " + armored.display + " looks rusted!")
                        armored.ACbase -= 1
                        if armored.dred >= 1:
                            armored.dred -= 1
                        if armored.ACbase <= 0:
                            messageappend("Your " + armored.display + " rusts away completely!")
                            [pc.helm, pc.chest, pc.boots][piece] == 0
                            pc.stuff.remove(armored)


monsterlist = [shopkeep, smallrat, giantrat, kingrat, coyote, bandit, highwayman, zombie, skeleton, rust, goldbug, vampire, hobbit, gnelf, goblin, gremlin, flamingskeleton, imp, IMP, somethingcubus, demon, catacombsaint]


##Mapmaker
def createpoints():
    global points
    points = []
    loopy = 1
    while loopy <= 20:
        loopx = 1
        while loopx <= 70:
            points.append(point(loopx, loopy, "infill", " ", " ", 0, 0, [], 2))
            loopx += 1
        loopy += 1

def room(maxx, maxy, minx, miny, door, id, distribution):
    global points
    issue = 0

    loopx = maxx
    while loopx >= minx:
        loopy = maxy
        while loopy >= miny:
            tpoint = findpoint(loopx, loopy)
            tpoint.isroom = id
            if loopx == maxx or loopx == minx:
                tpoint.type = "wall"
                tpoint.symbol = "|"
            if loopy == maxy or loopy == miny:
                tpoint.type = "wall"
                tpoint.symbol = "-"                
            if door != 0:
                findpoint(door[0], door[1]).type = "door"
                findpoint(door[0], door[1]).symbol = "+"
            loopy -= 1
        loopx -= 1

    if door != 0 and distribution != 0:
        if len(checkadj(findpoint(door[0], door[1]), "-", 0)) == 2:
            issue = 2
        else:
            issue = 1

    stuffnthangs = []
    loopx = maxx - 1
    while loopx >= minx+1:
        loopy = maxy - 1
        while loopy >= miny+1:
            tpoint = findpoint(loopx, loopy)
            tpoint.isroom = id

            tpoint.type = "floor"
            tpoint.symbol = "."
            if issue != 0:
                if issue == 1:
                    dif = abs(tpoint.x - door[0])
                if issue == 2:
                    dif = abs(tpoint.y - door[1])
                if dif >= 2:
                    chance = random.randint(1,100)
                    reducer = 0
                    counter = 0
                    things = [weaponlist, armorlist, spellbooklist, scrolllist, potionlist, wandlist]
                    for x in distribution:
                        if reducer + x >= chance:
                            sus = things[counter]
                            while True:
                                item = mintitem(sus[random.randint(1, len(sus))-1](0))
                                if item.rarity > 0:
                                    break
                            tpoint.items.append(item)
                            stuffnthangs.append(item)
                            break
                        else:
                            reducer += distribution[counter]
                            counter += 1
                if dif == 1 and tpoint.x == door[0] or dif == 1 and tpoint.y == door[1]:
                    tpoint.monster = mintmonster(shopkeep, tpoint.x, tpoint.y)
                    tpoint.monster.protective = stuffnthangs
                    tpoint.monster.anchor = tpoint
                    tpoint.monster.shopid = id
            loopy -= 1
        loopx -= 1

def findpoint(x,y):
    tpoint = 70*(y-1)+x-1
    if 1 <= y <= 20 and 1 <= x <= 70:
        return points[tpoint]
    else:
        return 0

def thebigroom():
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            findpoint(loopx, loopy).type = "floor"
            findpoint(loopx, loopy).symbol = "."
            if findpoint(loopx, loopy).x == 1 or findpoint(loopx, loopy).x == 70:
                findpoint(loopx, loopy).type = "wall"
                findpoint(loopx, loopy).symbol = "|"
            if findpoint(loopx, loopy).y == 1 or findpoint(loopx, loopy).y == 20:
                findpoint(loopx, loopy).type = "wall"
                findpoint(loopx, loopy).symbol = "-"
            if findpoint(loopx, loopy).y == 13 and findpoint(loopx, loopy).x == 13:
                findpoint(loopx, loopy).type = "stairup"
                findpoint(loopx, loopy).symbol = "<"
            if findpoint(loopx, loopy).y == 18 and findpoint(loopx, loopy).x == 68:
                findpoint(loopx, loopy).type = "stairdown"
                findpoint(loopx, loopy).symbol = ">"
            if 5 <= findpoint(loopx, loopy).y <= 14 and findpoint(loopx, loopy).x == 35:
                findpoint(loopx, loopy).type = "wall"
                findpoint(loopx, loopy).symbol = "|"
            
            loopy -= 1
        loopx -= 1

def adelaide():
    room(59, 19, 11, 2, 0, 0, 0)
    findpoint(13, 4).type = "stairup"
    findpoint(13, 4).symbol = "<"
    findpoint(57, 17).type = "stairdown"
    findpoint(57, 17).symbol = ">"

    room(20, 19, 13, 15, [19, 15], 11, [37, 24, 4, 12, 18, 5])

    room(17, 12, 14, 9, [16, 12], 1, 0)
    room(20, 12, 17, 9, [18, 12], 1, 0)
    room(23, 13, 20, 10, [22, 13], 1, 0)
    room(26, 17, 23, 13, [23, 15], 1, 0)

    room(19, 6, 16, 2, [18, 6], 2, 0)
    room(25, 10, 22, 6, [24, 6], 2, 0)
    room(26, 13, 23, 10, [26, 11], 2, 0)
    room(32, 15, 29, 12, [32, 13], 2, 0)
            
    room(32, 8, 29, 5, [32, 7], 3, 0)
    room(34, 5, 31, 2, [33, 5], 3, 0)
    room(37, 5, 34, 2, [36, 5], 3, 0)
    room(40, 6, 37, 2, [39, 6], 3, 0)
    room(45, 10, 41, 6, [41, 8], 3, 0)

    room(46, 6, 40, 2, [46, 5], 12, [10, 90, 0, 0, 0, 0])

    room(44, 17, 39, 13, [44, 15], 666, 0)
    findpoint(40, 15).type = "altar"
    findpoint(40, 15).symbol = "_"

    room(36, 19, 30, 15, [35, 15], 7, 0)
    room(30, 19, 28, 15, [30, 18], 7, 0)

    room(58, 9, 54, 2, [54, 7], 13, [0, 0, 10, 90, 0, 0, 0])
    room(51, 19, 47, 14, [48, 14], 4, 0)
    room(53, 19, 51, 17, [51, 18], 7, 0)
    room(58, 13, 55, 9, [56, 13], 4, 0)
    room(55, 12, 52, 9, [52, 11], 4, 0)

    findpoint(52, 18).items.append(mintitem(wandlist[random.randint(1, len(wandlist))-1](0)))
    findpoint(29, 16).items.append(mintitem(potionlist[random.randint(1, len(wandlist))-1](0)))

    ##Adelaide Monsters
    findpoint(35, 11).monster = mintmonster(watchman, 35, 11)
    findpoint(39, 9).monster = mintmonster(watchman, 39, 9)
    findpoint(57, 17).monster = mintmonster(watchman, 57, 17)
    findpoint(50, 8).monster = mintmonster(watchman, 50, 8)
    findpoint(26, 4).monster = mintmonster(watchman, 26, 4)
    findpoint(40, 15).monster = mintmonster(somethingcubus, 40, 15)

    loop = 1
    while loop <= 4:
        specificmonsters(loop, [40, 40, 10, 10], [[gnelf, goblin, gremlin], [hobbit], [bandit, highwayman], [smallrat, giantrat, giantrat]], random.randint(2, 4))

        loop += 1

def standardfloor(roomnumber, mindimension, maxdimension):
    looprooms = roomnumber
    while looprooms > 0:
        roomstart = findpoint(random.randint(3,68-maxdimension), random.randint(3,18-maxdimension))
        roommaxx = roomstart.x + random.randint(mindimension, maxdimension)
        roommaxy = roomstart.y + random.randint(mindimension, maxdimension)
        loopy = roommaxy + 1
        redflag = 0
        while loopy >= roomstart.y - 1 and redflag == 0:
            loopx = roommaxx + 1
            while loopx >= roomstart.x - 1 and redflag == 0:
                if findpoint(loopx, loopy).isroom != 0:
                    redflag = 1
                loopx -= 1
            loopy -= 1
        if redflag == 0:
            loopy = roommaxy
            while loopy >= roomstart.y:
                loopx = roommaxx
                while loopx >= roomstart.x:
                    findpoint(loopx, loopy).isroom = looprooms
                    if loopx == roommaxx or loopx == roomstart.x:
                        findpoint(loopx, loopy).type = "wall"
                        findpoint(loopx, loopy).symbol = "|"
                    if loopy == roommaxy or loopy == roomstart.y:
                        findpoint(loopx, loopy).type = "wall"
                        findpoint(loopx, loopy).symbol = "-"
                    if roomstart.x < loopx < roommaxx and roomstart.y < loopy < roommaxy:
                        findpoint(loopx, loopy).type = "floor"
                        findpoint(loopx, loopy).symbol = "."       
                    loopx -= 1
                loopy -= 1              
            looprooms -= 1   
    staireligible = []
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if findpoint(loopx, loopy).type == "floor":
                staireligible.append(findpoint(loopx, loopy))
            loopy -=1
        loopx -=1
    stairup = staireligible[random.randint(1, len(staireligible))-1]
    stairup.symbol = "<"
    stairup.type = "stairup"
    staireligible.remove(stairup)
    loop = len(staireligible)
    killlist = []
    while loop > 0:
        if staireligible[loop-1].isroom == stairup.isroom:
            killlist.append(staireligible[loop-1])
        loop -= 1
    loop = len(staireligible)
    while loop > 0:
        if staireligible[loop-1] in killlist:
            staireligible.remove(staireligible[loop-1])
        loop -=1

    stairdown = staireligible[random.randint(1, len(staireligible))-1]
    stairdown.symbol = ">"
    stairdown.type = "stairdown"
    staireligible.remove(stairdown)

def ratkingslair():
    room(17, 12, 12, 8, [17, 10], 1, 0)
    findpoint(13, 10).symbol = "<"
    findpoint(13, 10).type = "stairup"
    findpoint(14, 12).symbol = "+"
    findpoint(14, 12).type = "door"
    findpoint(14, 8).symbol = "+"
    findpoint(14, 8).type = "door"

    room(25, 14, 17, 6, [17, 10], 3, 0)
    room(21, 12, 19, 8, [21, 10], 0, 0)
    findpoint(20, 11).items.append(mintitem(scrolllist[random.randint(1, len(scrolllist)- 1)](0)))
    findpoint(20, 9).items.append(mintitem(potionlist[random.randint(1, len(potionlist)- 1)](0)))

    room(30, 8, 27, 3, [27, 4], 1, 0)
    findpoint(30, 7).symbol = "+"
    findpoint(30, 7).type = "door"
    room(30, 17, 27, 12, [27, 16], 1, 0)
    findpoint(30, 13).symbol = "+"
    findpoint(30, 13).type = "door"

    loopx = 26
    while loopx >= 14:
        loopy = 16
        while loopy >= 13:
            if loopy == 16 or loopx == 14:
                findpoint(loopx, loopy).type = "hall"
                findpoint(loopx, loopy).symbol = "#"
            loopy -= 1
        loopx -= 1

    loopx = 26
    while loopx >= 14:
        loopy = 7
        while loopy >= 4:
            if loopy == 4 or loopx == 14:
                findpoint(loopx, loopy).type = "hall"
                findpoint(loopx, loopy).symbol = "#"
            loopy -= 1
        loopx -= 1

    room(44, 15, 32, 5, [32, 13], 2, 0)
    findpoint(32, 7).symbol = "+"
    findpoint(32, 7).type = "door"
    findpoint(31, 7).symbol = "#"
    findpoint(31, 7).type = "hall"
    findpoint(31, 13).symbol = "#"
    findpoint(31, 13).type = "hall"

    specificmonsters(1, [60, 20, 20], [[smallrat, giantrat, giantrat], [bandit, highwayman], [zombie, skeleton]], 4)
    findpoint(43, 10).monster = mintmonster(kingrat, 43, 10)
    findpoint(43, 10).type = "stairdown"
    findpoint(43, 10).symbol = ">"
    specificmonsters(2, [90, 10], [[giantrat], [bandit, highwayman, highwayman]], 6)
    specificmonsters(3, [60, 20, 20], [[giantrat], [bandit, highwayman, highwayman], [zombie, skeleton]], 3)

def checkadj(basepoint, typecheck, corners):
    hits = []
    if findpoint(basepoint.x, (basepoint.y+1)).type == typecheck or findpoint(basepoint.x, (basepoint.y+1)).symbol == typecheck:
        hits.append(findpoint(basepoint.x, (basepoint.y+1)))
    if findpoint(basepoint.x, (basepoint.y-1)).type == typecheck or findpoint(basepoint.x, (basepoint.y-1)).symbol == typecheck:
        hits.append(findpoint(basepoint.x, (basepoint.y-1)))
    if findpoint((basepoint.x+1), basepoint.y).type == typecheck or findpoint((basepoint.x+1), basepoint.y).symbol == typecheck:
        hits.append(findpoint((basepoint.x+1), basepoint.y))
    if findpoint((basepoint.x-1), basepoint.y).type == typecheck or findpoint((basepoint.x-1), basepoint.y).symbol == typecheck:
        hits.append(findpoint((basepoint.x-1), basepoint.y))
    if corners == 1:
        if findpoint((basepoint.x+1), (basepoint.y+1)).type == typecheck or findpoint((basepoint.x+1), (basepoint.y+1)).symbol == typecheck:
            hits.append(findpoint((basepoint.x+1), (basepoint.y+1)))
        if findpoint((basepoint.x-1), (basepoint.y-1)).type == typecheck or findpoint((basepoint.x-1), (basepoint.y-1)).symbol == typecheck:
            hits.append(findpoint((basepoint.x-1), (basepoint.y-1)))
        if findpoint((basepoint.x+1), (basepoint.y-1)).type == typecheck or findpoint((basepoint.x+1), (basepoint.y-1)).symbol == typecheck:
            hits.append(findpoint((basepoint.x+1), (basepoint.y-1)))
        if findpoint((basepoint.x-1), (basepoint.y+1)).type == typecheck or findpoint((basepoint.x-1), (basepoint.y+1)).symbol == typecheck:
            hits.append(findpoint((basepoint.x-1), (basepoint.y+1)))
    return hits

def canmakeprogress(spoint, tpoint):
    global yissue
    global xissue
    yissue = 0
    xissue = 0
    if spoint.y > tpoint.y and findpoint(spoint.x, spoint.y-1).type == "wall" or findpoint(spoint.x, spoint.y-1).type == "door":
        yissue = 1
    if spoint.y < tpoint.y and findpoint(spoint.x, spoint.y+1).type == "wall" or findpoint(spoint.x, spoint.y+1).type == "door":
        yissue = 1
    if spoint.x > tpoint.x and findpoint(spoint.x-1, spoint.y).type == "wall" or findpoint(spoint.x-1, spoint.y).type == "door":
        xissue = 1
    if spoint.x < tpoint.x and findpoint(spoint.x+1, spoint.y).type == "wall" or findpoint(spoint.x+1, spoint.y).type == "door":
        xissue = 1

def doordash(roomnumber, extraconnections):
    dooreligible = []
    loopy = 1
    while loopy <= 20:
        loopx = 1
        while loopx <= 70:
            if findpoint(loopx, loopy).isroom == 1 and findpoint(loopx, loopy).type == "wall":
                if len(checkadj(findpoint(loopx, loopy), "|", 0)) != 0 and len(checkadj(findpoint(loopx, loopy), "-", 0)) != 0:
                    sus = 1
                else:
                    dooreligible.append(findpoint(loopx, loopy))
            loopx += 1
        loopy += 1
    cringe = dooreligible[random.randint(1, len(dooreligible))-1]
    cringe.type = "door"
    cringe.symbol = "+"
    if random.randint(1, 3) >= 2:
        cringe.closed = 1
        if random.randint(1, 2) == 2:
            cringe.locked = 1

    chain = [1]
    unchained = []
    loop = roomnumber
    while loop > 1:
        unchained.append(loop)
        loop -= 1
    macroloop = roomnumber
    while macroloop > 1:
        dooreligible = []
        troom = unchained[random.randint(1, len(unchained))-1]
        unchained.remove(troom)                                           
        loopy = 1
        sussy = 0
        while loopy <= 20:
            loopx = 1
            while loopx <= 70:
                if findpoint(loopx, loopy).isroom == troom and findpoint(loopx, loopy).type == "wall":
                    if len(checkadj(findpoint(loopx, loopy), "|", 0)) != 0 and len(checkadj(findpoint(loopx, loopy), "-", 0)) != 0:
                        sus = 0
                    else:
                        dooreligible.append(findpoint(loopx, loopy))
                        sussy += 1
                loopx += 1
            loopy += 1
        
        cringe = dooreligible[random.randint(1, len(dooreligible))-1]                                                                                       ##starting door is the highest room number
        cringe.type = "door"
        cringe.symbol = "+"
        if len(checkadj(cringe, " ", 0)) != 0:
            spoint = checkadj(cringe, " ", 0)[0]
        else:
            spoint = checkadj(cringe, "#", 0)[0]
        spoint.symbol = "#"
        spoint.type = "hall"

        chainconnector = chain[random.randint(1, len(chain)) - 1]                                                                                            ##select a random room on the chain to connect to
        loopx = 70
        while loopx > 0:
            loopy = 20
            while loopy > 0:
                if findpoint(loopx, loopy).isroom == chainconnector and findpoint(loopx, loopy).symbol == "+":
                    tdoor = findpoint(loopx, loopy)
                loopy -= 1
            loopx -= 1
        
        if len(checkadj(tdoor, " ", 0)) == 1:
            tpoint = checkadj(tdoor, " ", 0)[0]
        else:
            tpoint = checkadj(tdoor, "#", 0)[0]

        while spoint != tpoint:
            canmakeprogress(spoint, tpoint)
            spoint.type = "hall"
            spoint.symbol = "#"
            if spoint.y > tpoint.y and yissue == 0:
                spoint = findpoint(spoint.x, spoint.y -1)
                continue
            if spoint.y < tpoint.y and yissue == 0:
                spoint = findpoint(spoint.x, spoint.y +1)
                continue

            if spoint.x > tpoint.x and xissue == 0:
                spoint = findpoint(spoint.x -1, spoint.y)
                continue
            if spoint.x < tpoint.x and xissue == 0:
                spoint = findpoint(spoint.x +1, spoint.y)
                continue

            if spoint.x != tpoint.x and xissue == 1:
                chance = random.randint(1,2)
                while xissue == 1:
                    if chance == 1:
                        spoint = findpoint(spoint.x, spoint.y+1)
                    if chance == 2:
                        spoint = findpoint(spoint.x, spoint.y-1)
                    spoint.type = "hall"
                    spoint.symbol = "#"
                    canmakeprogress(spoint, tpoint)
                if spoint.x > tpoint.x:
                    spoint = findpoint(spoint.x-1, spoint.y)
                else:
                    spoint = findpoint(spoint.x+1, spoint.y)
                continue
            if spoint.y != 1 and yissue == 1:
                chance = random.randint(1,2)
                while yissue == 1:
                    if chance == 1:
                        spoint = findpoint(spoint.x+1, spoint.y)
                    if chance == 2:
                        spoint = findpoint(spoint.x-1, spoint.y)
                    spoint.type = "hall"
                    spoint.symbol = "#"
                    canmakeprogress(spoint, tpoint)
                if spoint.y > tpoint.y:
                    spoint = findpoint(spoint.x, spoint.y-1)
                else:
                    spoint = findpoint(spoint.x, spoint.y+1)
                continue
        spoint.type = "hall"
        spoint.symbol = "#"

        chain.append(troom)   ##after the connection is made
        macroloop -= 1

def checkmap():
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            tpoint = findpoint(loopx, loopy)
            tpoint.display = tpoint.symbol
            tpoint.color = 2
            if tpoint.items != []:
                findpoint(loopx, loopy).display = tpoint.items[len(tpoint.items)-1].symbol
            if tpoint.monster != 0:
                if tpoint.monster == pc:
                    tpoint.display = "@"
                else:
                    tpoint.display = tpoint.monster.symbol
            if len(tpoint.display) > 1:
                tpoint.display = "}"
            loopy -= 1
        loopx -= 1

def intitialize(floor, type):
    global purchasable
    global shopkeeps
    global presenttraps
    presenttraps = []
    monsters.clear
    createpoints()
    if type == "standard":
        standardfloor(6, 4, 8)
        doordash(6, 0)
        distributeloot(150+(floor-1)*30, [30, 25, 10, 15, 10, 10])
        distributemonsters(5+(floor-1)*2 + (3*pc.LVL), round(floor/3, 1), 3+round(floor-1, 1))
        ithoughtthatwasanormalsquare(random.randint(3, 6))
    if type == "bigroom":
        thebigroom()
    if type == "adelaide":
        adelaide()
    if type == "rrat":
        ratkingslair()
        traps.remove(trapdoor)
        ithoughtthatwasanormalsquare(6)
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if findpoint(loopx, loopy).type == "stairup":
                pc.x = loopx
                pc.y = loopy
                findpoint(loopx, loopy).monster = pc
                pc.memory.append(findpoint(loopx, loopy))
            loopy -= 1
        loopx -= 1
    purchasable = []
    shopkeeps = []
    for mo in monsters:
        if isinstance(mo, shopkeep):
            purchasable += mo.protective
            shopkeeps.append(mo)

def ithoughtthatwasanormalsquare(number):
    global presenttraps
    presenttraps = []
    treligible = []
    for po in points:
        if po.type == "floor" and len(checkadj(po, "door", 0)) == 0:
            treligible.append(po)
    
    trapslist= []
    for tr in traps:
        trp = tr()
        loop = 0
        while loop < trp.rarity and trp.severity <= DLVL*5 + pc.LVL:
            trapslist.append(tr)
            loop += 1

    loop = 0
    while loop < number:
        realtrap = trapslist[random.randint(1, len(trapslist))-1]
        tpoint = treligible[random.randint(1, len(treligible))-1]
        treligible.remove(tpoint)
        presenttraps.append(tpoint)
        tpoint.type = realtrap()
        loop += 1

##Item/loot functions
def mintitem(item):
    if isinstance(item, weapon):
        thelist = weapons
    if isinstance(item, armor):
        thelist = armors
    if isinstance(item, spellbook):
        thelist = spellbooks
    if isinstance(item, scroll):
        thelist = scrolls
    if isinstance(item, potion):
        thelist = potions
    if isinstance(item, wand):
        thelist = wands
    thelist.append(item)
    thelist[len(thelist)-1].color = thelist[len(thelist)-1].color
    return(thelist[len(thelist)-1])

def itemdistribution(totalvalue, list, macrolist, distributionnumber):
    value = totalvalue
    raritybuilder = []
    for x in list:
        loop = x(0).rarity
        while loop > 0:
            if x(0).value <= value:
                raritybuilder.append(x)
                loop -= 1
            else:
                break
    if len(raritybuilder) == 0:
        return "popeet"
    returner = 0
    returner = raritybuilder[random.randint(1, len(raritybuilder))-1]
    return mintitem(returner(0))

def distributeloot(totalvalue, distribution):
    looteligible = []
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if findpoint(loopx, loopy).type == "floor":
                looteligible.append(findpoint(loopx, loopy))
            loopy -=1
        loopx -=1

    cringe = [weaponlist, armorlist, spellbooklist, scrolllist, potionlist, wandlist]
    cringier = [weapons, armors, spellbooks, scrolls, potions, wands]
    while True:
        chance = random.randint(1, sum(distribution))
        breaker = 0
        while True:
            chance -= distribution[breaker]
            if chance <= 0:
                cringin = itemdistribution(totalvalue, cringe[breaker], 0, distribution[breaker])
                if cringin != "popeet":
                    looteligible[random.randint(1, len(looteligible)) - 1].items.append(cringin)
                    totalvalue -= cringin.value
                else:
                    cringe.remove(cringe[breaker])
                    distribution.remove(distribution[breaker])
                break
            breaker += 1
        if sum(distribution) == 0:
            break

    totalvalue += random.randint(3*DLVL, 6*DLVL) + 15
    while totalvalue > 0:
        pool = gold(random.randint(1, totalvalue))
        pool.display = str(pool.value) + " gold"
        looteligible[random.randint(1, len(looteligible))-1].items.append(pool)
        totalvalue -= pool.value

def call(item):
    while True:
        if isinstance(item, gold):
            message = "You see here " + str(item.value) + " gold"
            break
        if isinstance(item, boots) == False:
            message = "You see here a " + item.display
            break
        else:
            message = "You see here some " + item.display
            break
    for mo in monsters:
        if isinstance(mo, shopkeep) and item in mo.protective:
            message += " ($" + str(int((item.value*1.15)/(1+(0.05*mod(pc.CHA))))) + ")"
    messageappend(message)


##Monster Functions
def mintmonster(type, x, y):
    x = type(0, x, y)
    monsters.append(x)
    monsters[len(monsters)-1].id = len(monsters)
    monsters[len(monsters)-1].color = monsters[len(monsters)-1].color
    setventory(monsters[len(monsters)-1], monsters[len(monsters)-1].stuff)
    return monsters[len(monsters)-1]

def distributemonsters(totalvalue, minimumpower, maximumpower):
    monstereligible = []
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if findpoint(loopx, loopy).type == "floor" or findpoint(loopx, loopy).type == "hall":
                monstereligible.append(findpoint(loopx, loopy))
            loopy -=1
        loopx -=1

    raritybuilder = []
    for x in monsterlist:
        sus = x(0, 0, 0)
        loop = sus.rarity
        while loop > 0:
            if maximumpower >= sus.power >= minimumpower:
                raritybuilder.append(x)
                loop -= 1
            else:
                break
    loop = totalvalue
    while loop > 0:
        targetblock = monstereligible[random.randint(1, len(monstereligible))-1]
        targetblock.monster = mintmonster(raritybuilder[random.randint(1, len(raritybuilder))-1], targetblock.x, targetblock.y)
        monstereligible.remove(targetblock)
        loop -= monsters[len(monsters)-1].power

def soundthealarm(crook):
    messageappend("You hear the alarm blare!")
    for mo in monsters:
        if isinstance(mo, watchman):
            monster.anger(mo)

def specificmonsters(id, distribution, monstahs, number):
    eligiblespawn = []
    for po in points:
        if po.isroom == id and po.type not in nomove:
            eligiblespawn.append(po)
    
    loop = 0
    while loop < number:
        chance = random.randint(1, 100)
        counter = 0
        while True:
            chance -= distribution[counter]
            if chance <= 0:
                tpoint = eligiblespawn[random.randint(1, len(eligiblespawn))-1]
                tpoint.monster = mintmonster(monstahs[counter][random.randint(1, len(monstahs[counter]))-1], tpoint.x, tpoint.y)
                eligiblespawn.remove(tpoint)
                break
            else:
                counter += 1
        loop += 1

def setventory(monstah, odds):
    ##odds should look like: [[item, chance, minnumber, maxnumber].. per each item]
    ##[[10, [100, cudgel, 1, 1], 10, [100, dagger, 1, 4], 80]]
    monstah.stuff = []
    for od in odds:
        chance = random.randint(1, 100)
        counter = 0
        while chance > 0:
            chance -= od[counter]
            if chance > 0:
                counter += 2
        if len(od) >= counter + 2:
            odd = od[counter + 1]
        else:
            return
        if random.randint(1, 100) <= odd[1]:
            loop = random.randint(odd[2], odd[3])
            while loop > 0:
                monstah.stuff.append(mintitem(odd[0](0)))
                loop -= 1


##General Functions
messages = []
def messageappend(message):
    global messages
    messages.append(message)

def im(message, stdscr):
    stdscr.addstr(28, 0, " "*100, WHITE_ON_BLACK)
    stdscr.addstr(28, 0, message, WHITE_ON_BLACK)
    messages.clear
    stdscr.refresh()

def determinedirection(stdscr):
    im("In what direction (h, j, k, l, .)? ", stdscr)
    clarification = chr(stdscr.getch())
    if clarification in ["j", "h", "k", "l", "."]:
            if clarification == "j":
                return [0, -1]
            if clarification == "h":
                return [-1, 0]
            if clarification == "k":
                return [0, 1]
            if clarification == "l":
                return [1, 0]      
            if clarification == ".":
                return [0, 0]     
    else:
        messageappend("Choose a movement direction! (h, j, k, l, .)")

def round(input, tox):
    excess = input
    while excess >= tox:
        excess -= tox
    lowbar  = 0
    while lowbar <= input:
        lowbar += tox
        if lowbar > input:
            lowbar -= tox
            break
    highbar = 0
    while highbar < input:
        highbar += tox
    if excess >= (tox/2):
        return highbar
    else:
        return lowbar

def isdivis(number, by):
    divis = number/by
    if int(divis) == 0:
        return 0
    divis /= int(divis)
    if divis * number == number:
        return 1
    else:
        return 0

def circle(origin, radius):
    incircle = []
    loopx = origin.x - radius
    while loopx <= origin.x + radius:
        loopy = origin.y - radius
        while loopy <= origin.y + radius:
            if findpoint(loopx, loopy) != 0:
                if ((findpoint(loopx, loopy).x - origin.x)**2 + (findpoint(loopx, loopy).y - origin.y)**2) <= radius**2:
                    incircle.append(findpoint(loopx, loopy))
            loopy += 1
        loopx += 1
    return incircle

def triangle(origin, slope, direction, range):
    intriangle =[]
    if direction == "up":
        right = [int(range/slope), range]
        left = [int(-range/slope), 0]
        reye = findpoint(origin.x+1, origin.y)
        leye = findpoint(origin.x-1, origin.y)
    if direction == "left":
        right = [-1, int(range/slope)]
        left = [-range, int(-range/slope)-1]
        reye = findpoint(origin.x, origin.y+1)
        leye = findpoint(origin.x, origin.y-1)
    if direction == "right":
        right = [range, int(range/slope)]
        left = [1, int(-range/slope)-1]
        reye = findpoint(origin.x, origin.y-1)
        leye = findpoint(origin.x, origin.y+1)
    if direction == "down":
        right = [int(range/slope), -1]
        left = [int(-range/slope), -range-1]
        reye = findpoint(origin.x-1, origin.y)
        leye = findpoint(origin.x+1, origin.y)
    eyes = [leye, reye]

    loopx = origin.x + right[0]
    while loopx >= origin.x + left[0]:
        loopy = origin.y + right[1]
        while loopy > origin.y + left[1]:
            if findpoint(loopx, loopy) != 0 and 0 < loopx < 71 and 0< loopy < 21:
                intriangle.append(findpoint(loopx, loopy))
            loopy -= 1
        loopx -= 1

    killlist =  []
    obstructions = []
    for coord in intriangle:
        if direction == "up" or direction == "down":
            if slope*abs(origin.x-coord.x) > abs(origin.y-coord.y):
                killlist.append(coord)
        if direction == "right" or direction == "left":
            if slope*abs(origin.y-coord.y) > abs(origin.x-coord.x):
                killlist.append(coord)
        if coord.type in nomove:
            obstructions.append(coord)
    
    for x in killlist:
        if x in intriangle:
            intriangle.remove(x)
        if x in obstructions:
            obstructions.remove(x)
    killlist.clear

    
    for ob in obstructions:
        id = 1   
        for eye in eyes:
            if ob.x == eye.x:
                slope = "infinite"
            else:
                slope = abs((ob.y-eye.y)/(eye.x-ob.x))

            nblocks = []
            blocks = []

            if ob.y > eye.y:
                ymodifier = 1
            else:
                ymodifier = -1
            if ob.x > eye.x:
                xmodifier = 1
            else:
                xmodifier = -1


            if slope != "infinite":
                if slope > 1:
                    loop = abs(eye.y - ob.y)
                    looper = 1
                    while looper <= loop:
                        slopepick = (looper)/slope
                        if isdivis(slopepick, 1) == 1:
                            blocks.append(findpoint(eye.x + int(slopepick) * xmodifier, eye.y + looper*ymodifier))
                        else:
                            if isdivis(slopepick, 0.5) == 0 or len(blocks) == 0:
                                blocks.append(findpoint(eye.x + int(round(slopepick, 1)) * xmodifier, eye.y + looper * ymodifier))
                            else:
                                blocks.append(findpoint(blocks[looper-2].x + xmodifier, eye.y + looper * ymodifier))
                        looper += 1

                else:
                    loop = abs(eye.x - ob.x)
                    looper = 1
                    while looper <= loop:
                        slopepick = slope*looper
                        if isdivis(slopepick, 1) == 1 or slopepick == 0:
                            blocks.append(findpoint(eye.x + looper * xmodifier, eye.y + int(slopepick)*ymodifier))
                        else:
                            if isdivis(slopepick, 0.5) == 0 or len(blocks) == 0:
                                blocks.append(findpoint(eye.x + looper * xmodifier, eye.y + int(round(slopepick, 1))*ymodifier))
                            else:
                                blocks.append(findpoint(eye.x + looper * xmodifier, blocks[looper-2].y + ymodifier))
                        looper += 1
            else:
                loop = abs(eye.y - ob.y)
                looper = 1
                while looper <= loop:
                    blocks.append(findpoint(eye.x, eye.y + looper*ymodifier))
                    looper += 1
                
            for bl in blocks:    
                nblocks.append([bl.x - eye.x, bl.y - eye.y])

            if direction == "up" or direction == "down":
                continuation = range - abs(ob.y - origin.y)
                counter = 1
            else:
                continuation = range - abs(ob.x - origin.x)
                counter = 0
            start = ob
            looper = 0
            listcrawler = 0
            toberemoved = []

            while looper < continuation:
                if 0 < start.x + nblocks[listcrawler][0] < 71 and 0 < start.y + nblocks[listcrawler][1] < 21:
                    tpoint = findpoint(start.x + nblocks[listcrawler][0], start.y + nblocks[listcrawler][1])
                    toberemoved.append(tpoint)
                else:
                    break

                if listcrawler != 0:
                    looper += abs(nblocks[listcrawler][counter] - nblocks[listcrawler - 1][counter])
                else:
                    looper += abs(nblocks[listcrawler][counter])

                if listcrawler + 1 == len(nblocks):
                    listcrawler = 0
                    start = toberemoved[len(toberemoved) - 1]
                else:
                    listcrawler += 1

            if eye == reye:
                reyemoval = toberemoved
                sloper = slope
            else:
                leyemoval = toberemoved
                slopel = slope

        garbageman = leyemoval
        

        for trash in reyemoval:
            checker = 0
            if direction == "left" or direction == "right":
                check = "y"
            else:
                check = "x"
            while True:
                if check == "y":
                    tpoint = findpoint(trash.x, trash.y + checker)
                else:
                    tpoint = findpoint(trash.x + checker, trash.y)
                if tpoint in leyemoval:
                    break
                else:
                    garbageman.append(tpoint)
                if direction == "right" or direction == "down":
                    checker -= 1
                if direction == "left" or direction == "up":
                    checker += 1

        for trash in garbageman:
            if trash in intriangle:
                intriangle.remove(trash)

    return intriangle

def mod(input):
    return round((input-10)/2, 1)

def healthbar(current, max, blocks):
    bar = "["
    percent = round(current/max, 0.01)*100
    blockmaker = round(percent/(100/blocks),1)
    if blockmaker > blocks:
        blockmaker = blocks
    counter = 0
    while counter < blockmaker:
        bar += "#"
        counter += 1
    counter = 0
    while counter < blocks-blockmaker:
        bar += " "
        counter += 1
    bar += "]"
    return bar

def display(stdscr):
    global BLACK_ON_WHITE
    global WHITE_ON_BLACK
    global GREEN_ON_BLACK
    global RED_ON_BLACK
    global BLUE_ON_BLACK
    global YELLOW_ON_BLACK
    global PURPLE_ON_BLACK
    global messages

    title = pc.name + " the " + pc.clss.display
    stdscr.addstr(0, 0, title, WHITE_ON_BLACK)
    
    hpline = "HP %4d / %-4d  " % (pc.HP, pc.HPMax) + healthbar(pc.HP, pc.HPMax, 20)
    stdscr.addstr(1 ,0 , hpline, WHITE_ON_BLACK)

    mpline = "MP %4d / %-4d  " % (pc.MP, pc.MPMax) + healthbar(pc.MP, pc.MPMax, 20)
    stdscr.addstr(2 ,0 , mpline, WHITE_ON_BLACK)

    stdscr.addstr(3, 0, "Carry Capacity: " + healthbar(weight, pc.carry, 20), WHITE_ON_BLACK)

    checkmap()
    invision = vision(pc, 6)
    loopy = 20
    while loopy > 0:
        printy = 25 - loopy
        loopx = 1
        while loopx <= 70:
            yprinter = ""
            tpoint = findpoint(loopx, loopy)
            if tpoint in pc.memory:
                if tpoint in invision or tpoint.monster == pc:
                    yprinter = tpoint.display
                    color = curses.color_pair(tpoint.color)
                    if isinstance(tpoint.type, trap) and tpoint.symbol == "^" and tpoint.monster != pc:
                        color = curses.color_pair(tpoint.type.color)
                    if len(tpoint.items) > 0 and tpoint.monster != pc:
                        color = curses.color_pair(tpoint.items[len(tpoint.items)-1].color)
                    if isinstance(tpoint.monster, monster):
                        color = curses.color_pair(tpoint.monster.color)
                else:
                    yprinter = tpoint.symbol
                    color = WHITE_ON_BLACK
            else:
                yprinter += " "
                color = WHITE_ON_BLACK
            stdscr.addstr(printy, loopx, yprinter, color)
            loopx += 1
        loopy -=1
    stdscr.addstr(26, 0, "STR: %s DEX: %s CON: %s INT: %s WIS: %s CHA: %s" % (pc.STR, pc.DEX, pc.CON, pc.INT, pc.WIS, pc.CHA), WHITE_ON_BLACK)
    stdscr.addstr(27, 0, "Level: %s AC: %s XP: %s DLVL: %s Turn: %s $: %s" % (pc.LVL, pc.AC, pc.XP, DLVL, turn-100, pc.wealth), WHITE_ON_BLACK)

    counter = 1
    for me in messages:
        stdscr.addstr(28, 0, " "*80, WHITE_ON_BLACK)
        stdscr.addstr(28, 0, me, WHITE_ON_BLACK)
        stdscr.refresh()
        if len(messages) > 1 and counter != len(messages):
            stdscr.addstr(28, len(me)+1, "cont...", WHITE_ON_BLACK)
            cont = chr(stdscr.getch())
        counter += 1

    messages = []
    stdscr.refresh()

def turnup(stdscr):
    global turn
    turn += 1
    tomove = []
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if isinstance(findpoint(loopx, loopy).monster, monster):
                if findpoint(loopx, loopy).monster.HP >= 1:
                    tomove.append(findpoint(loopx, loopy).monster)
                else:
                    if len(findpoint(loopx, loopy).monster.stuff) > 0:
                        findpoint(loopx, loopy).items += findpoint(loopx, loopy).monster.stuff
                    findpoint(loopx, loopy).monster = 0
            loopy -= 1
        loopx -=1
    for x in tomove:
        loop = 0
        if "slow" in x.effects:
            reducer = 2*x.speed/3
        else:
            reducer = x.speed
        if "burdened" in pc.statuses:
            reducer += 1/3
        for eff in pc.statuses:
            if "haste" in eff:
                reducer = 3*reducer/5
        naturalspeed = 0
        while reducer > 1:
            naturalspeed += 1
            reducer -= 1
        chance = int(reducer*100)
        if random.randint(1, 100) <= chance:
            loop += 1
        loop += naturalspeed
        while loop > 0:
            x.act()
            loop -= 1
        for ef in x.effects:
            if isinstance(ef, list) == True:
                ef[1] -= 1
                if ef[1] == 0:
                    x.effects.remove(ef)

    removal = []
    for x in pc.spells:
        x[1] -= 1
        if x[1] <= 0:
            removal.append(x)
    for x in removal:
        pc.spells.remove(x)

    for tr in presenttraps:
        if tr.monster != 0:
            user = tr.monster
            if user == pc and command in ["h", "j", "k", "l"]:
                if random.randint(1, 20) + mod(pc.DEX) >= tr.type.adc:
                    tr.type.trigger(tr, stdscr)
                else:
                    messageappend("You narrowly avoid a " + tr.type.display)
                if tr not in pc.memory:
                    pc.memory.append(tr)
                tr.symbol = "^"
    
def dungeonlayout():
    if DLVL in [6, 9]:
        if DLVL == 6:
            intitialize(DLVL, "adelaide")
        if DLVL == 9:
            intitialize(DLVL, "rrat")
    else:
        intitialize(DLVL, "standard")

def check4(listicle, type):
    pogchamps = []
    for li in listicle:
        if isinstance(li, type):
            pogchamps.append(li)
    return pogchamps

def cutscene(number, stdscr):
    opening = ["Welcome to Rrat Killing Simulator " + pc.name + "!", "The great lamp is dying, and without it the world is sinking into chaos", "and strife. You have been chosen as the light bearer, the one prophecied", "to delve into Carceri and recover the stolen flame of the world!"]
    scenes = [opening]
    counter = 0
    for x in scenes[number]:
        stdscr.addstr(6+counter, 71, x, WHITE_ON_BLACK)
        counter += 1
    stdscr.refresh()
    passer = chr(stdscr.getch())

##PC Functions
def createpc():
    select = 1
    pc.LVL = 1
    pc.stuff = []
    while select == 1:
        print("Choose a class: ")
        loop = 1
        while loop <= len(eligibleclasses):
            print(eligibleclasses[loop-1].display, loop)
            loop += 1
        while True:
            try:
                classchoice = int(input("Selection: "))
                classchoice += 0
            except ValueError:
                print("Please pick a number in the listed range!")
            else:
                if 0 < classchoice <= len(eligibleclasses):
                    pc.clss = eligibleclasses[classchoice-1]
                    break
        loop = 1
        while loop <= len(eligibleraces):
            print(eligibleraces[loop-1].display, loop)
            loop += 1
        while True:
            try:
                racechoice = int(input("Selection: "))
                racechoice += 0
            except ValueError:
                print("Please pick a number in the listed range!")
            else:
                if 0 < racechoice <= len(eligibleraces):
                    pc.race = eligibleraces[racechoice-1]
                    break
        pc.STR = pc.clss.STR + pc.race.STR
        pc.DEX = pc.clss.DEX + pc.race.DEX
        pc.CON = pc.clss.CON + pc.race.CON
        pc.INT = pc.clss.INT + pc.race.INT
        pc.WIS = pc.clss.WIS + pc.race.WIS
        pc.CHA = pc.clss.CHA + pc.race.CHA
        
        pc.skills = pc.clss.startskills

        skills = [pc.INT, pc.WIS, pc.CHA]
        pc.clss.spell = skills[pc.clss.spell-1]

        pc.HPMax = mod(pc.CON) + pc.clss.baseHP
        pc.HP = pc.HPMax
        pc.MPMax = int((6+mod(pc.clss.spell))*pc.clss.spellskill)
        pc.MP = pc.MPMax
        for x in pc.clss.startinventory:
            pc.stuff.append(mintitem(x(0)))
            if isinstance(pc.stuff[len(pc.stuff)-1], spellbook):
                spellbook.checkfail(x(0), 2500)
            if isinstance(pc.stuff[len(pc.stuff)-1], weapon):
                pc.weapon = pc.stuff[len(pc.stuff)-1]
            if isinstance(pc.stuff[len(pc.stuff)-1], chest):
                pc.chest = pc.stuff[len(pc.stuff)-1]
            if isinstance(pc.stuff[len(pc.stuff)-1], helm):
                pc.helm = pc.stuff[len(pc.stuff)-1]
            if isinstance(pc.stuff[len(pc.stuff)-1], boots):
                pc.boots = pc.stuff[len(pc.stuff)-1]
        pc.name = input("What is your name, brave adventurer? ")

        while 1 == 1:
            print(pc.name, "the ", pc.race.display, pc.clss.display)
            confirmation = input("is this correct (y/n)? ")
            if confirmation == "y":
                select = 0
                break
            if confirmation == "n":
                break
            print("Please reply either y or n!")

def lvlup():
    pc.LVL += 1
    pc.XP = 0
    oldmax = pc.HPMax
    oldmaxm = pc.MPMax
    pc.HPMax = int(pc.clss.baseHP + mod(pc.CON)*pc.LVL + 0.5*(pc.LVL-1)*(pc.clss.baseHP + 1))
    pc.HP += pc.HPMax - oldmax
    pc.MPMax = int((6+mod(pc.clss.spell)*pc.LVL)*pc.clss.spellskill)
    pc.MP += pc.MPMax - oldmaxm

def checkup():
    global weight

    if isdivis(turn, 8) == 1 and pc.HP < pc.HPMax:
        pc.HP += 1

    if isdivis(turn, round(10/2*pc.clss.spellskill, 1)) == 1 and pc.MP < pc.MPMax:
        pc.MP += 1

    XPtoNXT = 100 + 100*float(pc.LVL-1)**(1+0.04*(pc.LVL^2)-0.33*pc.LVL)
    if pc.XP >= XPtoNXT:
        lvlup()

    DEXbonus = mod(pc.DEX)
    pc.AC = 10
    ACsources = [pc.boots, pc.chest, pc.helm]
    for x in ACsources:
        if x != 0:
            pc.AC += x.ACbase
            if x == pc.chest and DEXbonus >= x.MaxDex:
                DEXbonus = x.MaxDex
    pc.AC += DEXbonus

    pc.dred = 0
    for x in ACsources:
        if x != 0:
            pc.dred += x.dred

    pc.carry = 60 + 4*pc.STR
    weight = 0
    for x in pc.stuff:
        weight += x.weight
    if weight > pc.carry and "burdened" not in pc.statuses:
        pc.statuses.append("burdened")
    if weight <= pc.carry and "burdened" in pc.statuses:
        pc.statuses.remove("burdened")

    if pc.weapon not in pc.stuff:
        pc.weapon = hand(0)
    if pc.boots not in pc.stuff:
        pc.boots = 0
    if pc.chest not in pc.stuff:
        pc.chest = 0
    if pc.helm not in pc.stuff:
        pc.helm = 0

    killlist = []
    for x in pc.statuses:
        if isinstance(x, list) == True:
            x[1] -= 1
            if x[1] <= 0:
                killlist.append(x)
    for x in killlist:
        pc.statuses.remove(x)
        if "haste" in x:
            messageappend("You feel yourself begin to slow down")

    cringe = []
    cringe += pc.spells
    pc.spells = []
    for sp in cringe:
        spellbook.checkfail(sp[0], sp[1])

def vision(origin, sight):
    invision = triangle(origin, 1, "up", sight) + triangle(origin, 1, "right", sight) + triangle(origin, 1, "down", sight) + triangle(origin, 1, "left", sight)
    return invision

def inventorycheck(useitem, action, types, stdscr):
    global pc
    global BLACK_ON_WHITE
    global WHITE_ON_BLACK
    global GREEN_ON_BLACK
    global RED_ON_BLACK
    global BLUE_ON_BLACK
    weaponsi = []
    armorsi = []
    spellbooksi = []
    scrollsi = []
    potionsi = []
    wandsi = []
    stdscr.addstr(5, 71, "----------------Inventory----------------", WHITE_ON_BLACK)
    for item in pc.stuff:
        if isinstance(item, weapon) == True:
            weaponsi.append(item)
        if isinstance(item, armor) == True:
            armorsi.append(item)
        if isinstance(item, spellbook) == True:
            spellbooksi.append(item)
        if isinstance(item, scroll) == True:
            scrollsi.append(item)
        if isinstance(item, potion) == True:
            potionsi.append(item)
        if isinstance(item, wand) == True:
            wandsi.append(item)
    stdscr.addstr(6, 71, "| Weapons:                              |", WHITE_ON_BLACK)    
    counter = 1
    for x in weaponsi:
        if x is pc.weapon:
            stdscr.addstr(6+counter, 71, "| " + str(counter) + ": " + x.display + " "*(25-len(x.display)-len(str(counter))) + " -equipped |", WHITE_ON_BLACK)
        else:
            stdscr.addstr(6+counter, 71, "| " + str(counter) + ": " + x.display + " "*(35-len(x.display)-len(str(counter))) + " |", WHITE_ON_BLACK)
        counter += 1
    stdscr.addstr(6+counter, 71, "| Armors:                               |", WHITE_ON_BLACK)    
    counter += 1
    for x in armorsi:
        if x is pc.chest or x is pc.helm or x is pc.boots:
            stdscr.addstr(6+counter, 71, "| " + str(counter-1) + ": " + x.display + " "*(25-len(x.display)-len(str(counter-1))) + " -equipped |", WHITE_ON_BLACK)
        else:
            stdscr.addstr(6+counter, 71, "| " + str(counter-1) + ": " + x.display + " "*(35-len(x.display)-len(str(counter-1))) + " |", WHITE_ON_BLACK)
        counter += 1
    stdscr.addstr(6+counter, 71, "| Spellbooks:                           |", WHITE_ON_BLACK)    
    counter += 1
    for x in spellbooksi:
        stdscr.addstr(6+counter, 71, "| " + str(counter-2) + ": " + x.display + " "*(35-len(x.display)-len(str(counter-2))) + " |")
        counter += 1
    stdscr.addstr(6+counter, 71, "| Scrolls:                              |", WHITE_ON_BLACK)    
    counter += 1
    for x in scrollsi:
        stdscr.addstr(6+counter, 71, "| " + str(counter-3) + ": " + x.display + " "*(35-len(x.display)-len(str(counter-3))) + " |")
        counter += 1
    stdscr.addstr(6+ counter, 71, "| Potions:                              |", WHITE_ON_BLACK)   
    counter += 1 
    for x in potionsi:
        stdscr.addstr(6+counter, 71, "| " + str(counter-4) + ": " + x.display + " "*(35-len(x.display)-len(str(counter-4))) + " |")
        counter += 1
    stdscr.addstr(6+counter, 71, "| Wands:                                |", WHITE_ON_BLACK)    
    counter += 1
    for x in wandsi:
        stdscr.addstr(6+counter, 71, "| " + str(counter-5) + ": " + x.display + " "*(35-len(x.display)-len(str(counter-5))) + " |")
        counter += 1

    stdscr.addstr(6+counter, 71, "-----------------------------------------", WHITE_ON_BLACK)
    pc.stuff = weaponsi + armorsi + spellbooksi + scrollsi + potionsi + wandsi

    if useitem != 0:
        try:
            im(action + " which item (number -> enter)?", stdscr)
            clarification = int(stdscr.getstr())
            clarification += 0
        except ValueError:
            im("Pick a number please!", stdscr)
        else:
            if 1 <= clarification <= len(pc.stuff):
                if type(pc.stuff[clarification -1]) in types:
                    return pc.stuff[clarification - 1]
                else:
                    im("That is a silly thing to " + action + " !", stdscr)
                    return
            else:
                im("Please pick a number within the shown range!", stdscr)
                return


##Primary Loop
def cursesdraw(stdscr):
    global DLVL
    global turn
    global command
    global BLACK_ON_WHITE
    global WHITE_ON_BLACK
    global GREEN_ON_BLACK
    global RED_ON_BLACK
    global BLUE_ON_BLACK
    global YELLOW_ON_BLACK
    global PURPLE_ON_BLACK

    key_pressed = 0
    cursor_x = 0
    cursor_y = 0

    stdscr.clear()
    stdscr.refresh()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    BLACK_ON_WHITE = curses.color_pair(1)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    WHITE_ON_BLACK = curses.color_pair(2)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_ON_BLACK = curses.color_pair(3)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    RED_ON_BLACK = curses.color_pair(4)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    BLUE_ON_BLACK = curses.color_pair(5)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    YELLOW_ON_BLACK = curses.color_pair(6)
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    PURPLE_ON_BLACK = curses.color_pair(7)
    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)
    PURPLE_ON_BLACK = curses.color_pair(8)

    checkup()
    intitialize(DLVL, "standard")

    messages = []
    truecommands = ["h", "j", "k", "l", ">", ",", ".", "Z", "s"]
    freecommands = ["d", "i", "w", "W", "S", "C", "r", "R", "q", "z", "p", "*"]
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for pos in vision(pc, 6):
            if pos not in pc.memory:
                pc.memory.append(pos)
        display(stdscr)
        viablecommands = [".", "r", "S", "C", "s", "*"]
        if findpoint(pc.x-1, pc.y).type not in nomove:
            viablecommands.append("h")
        if findpoint(pc.x, pc.y-1).type not in nomove:
            viablecommands.append("j")
        if findpoint(pc.x, pc.y+1).type not in nomove:
            viablecommands.append("k")
        if findpoint(pc.x+1, pc.y).type not in nomove:
            viablecommands.append("l")
        if findpoint(pc.x, pc.y).type == "stairdown":
            viablecommands.append(">")
        if findpoint(pc.x, pc.y).items != []:
            viablecommands.append(",")
        if pc.spells != []:
            viablecommands.append("Z")
        if pc.stuff != []:
            viablecommands.append("i")
            viablecommands.append("d")
            viablecommands.append("w")
            viablecommands.append("W")
            viablecommands.append("q")
            viablecommands.append("z")
        if pc.debts != []:
            viablecommands.append("p")
        if pc.helm != 0 or pc.chest != 0 or pc.boots != 0:
            viablecommands.append("R")
        while 1 == 1:
            command = chr(stdscr.getch())
            if command in truecommands and command in viablecommands:
                startpoint = findpoint(pc.x, pc.y)
                startpoint.monster = 0
                tpoint = findpoint(pc.x, pc.y)
                if command == "h":
                    tpoint = findpoint(pc.x - 1, pc.y)
                if command == "j":
                    tpoint = findpoint(pc.x, pc.y-1)
                if command == "k":
                    tpoint = findpoint(pc.x, pc.y+1)
                if command == "l":
                    tpoint = findpoint(pc.x+1, pc.y)
                if tpoint.monster == 0:
                    pc.x = tpoint.x
                    pc.y = tpoint.y
                else:
                    weapon.attack(pc.weapon, pc, tpoint.monster, tpoint)
                if command == "s":
                    for el in checkadj(startpoint, ".", 1):
                        if isinstance(el.type, trap):
                            if random.randint(1, 20) + mod(pc.WIS) >= el.type.fdc or pc.clss == investigator:
                                el.symbol = "^"
                                messageappend("You find a trap!")
                if command == ">":
                    DLVL += 1
                    dungeonlayout()

                if command == ",":
                    if len(findpoint(pc.x, pc.y).items) == 1:
                        if isinstance(findpoint(pc.x, pc.y).items[0], gold):
                            pc.wealth += findpoint(pc.x, pc.y).items[0].value
                        else:
                            pc.stuff.append(findpoint(pc.x, pc.y).items[0])
                            if findpoint(pc.x, pc.y).items[0] in purchasable:
                                pc.debts.append(findpoint(pc.x, pc.y).items[0])

                        findpoint(pc.x, pc.y).items.remove(findpoint(pc.x, pc.y).items[0])
                    else:
                        loop = 0
                        while loop < len(findpoint(pc.x, pc.y).items):
                            stdscr.addstr(6+loop, 71, str(loop + 1) + ": " + findpoint(pc.x, pc.y).items[loop].display, WHITE_ON_BLACK)
                            loop += 1
                        try:
                            im("take which item (number -> enter)?", stdscr)
                            clarification = int(stdscr.getstr())
                            clarification += 0
                        except ValueError:
                            messageappend("Type a number please!")
                        else:
                            if 0 < clarification <= len(findpoint(pc.x, pc.y).items):
                                if isinstance(findpoint(pc.x, pc.y).items[clarification-1], gold):
                                    pc.wealth += findpoint(pc.x, pc.y).items[clarification-1].value
                                else:
                                    pc.stuff.append(findpoint(pc.x, pc.y).items[clarification-1])
                                    if findpoint(pc.x, pc.y).items[clarification-1] in purchasable:
                                        pc.debts.append(findpoint(pc.x, pc.y).items[clarification-1])
                                findpoint(pc.x, pc.y).items.remove(findpoint(pc.x, pc.y).items[clarification-1])
                                break
                            else:
                                    messageappend("Please type a number within the acceptable range")
                if command == "Z":
                    counter = 1
                    stdscr.addstr(6, 71, "-------Name----------LVL-Recall-Fail-", WHITE_ON_BLACK)
                    for x in pc.spells:
                        spellname = ""
                        loop = len(x[0].display) - 12
                        while loop > 0:
                            spellname += x[0].display[len(x[0].display) - loop]
                            loop -= 1
                        stdscr.addstr(6+counter, 71, "| %1d:%-16s  %-2d  %-4d   %-3d|" % (counter, spellname, x[0].level, x[1], 100-x[2]), WHITE_ON_BLACK)
                        counter += 1
                    stdscr.addstr(6+counter, 71, "-------------------------------------", WHITE_ON_BLACK)
                    try:
                        im("Cast which spell? (number -> enter)?", stdscr)
                        choice = int(stdscr.getstr())
                        choice += 0
                    except ValueError:
                        messageappend("Type a number please!")
                    else:
                        if 1 <= choice <= counter:
                            if random.randint(1, 100) > pc.spells[choice-1][2]:
                                messageappend("You fail to cast the spell correctly!")
                                pc.MP -= 5*pc.spells[choice-1][0].level
                                if pc.MP > 0:
                                    pc.MP = 0
                                break
                            counter = 0
                            for skil in spellskills:
                                if pc.spells[choice-1][0].school == skil:
                                    pc.wizard101[counter] += 1
                                    if pc.wizard101[counter] >= 20 + (30 + 10*pc.clss.spellstart[counter]-1) * pc.clss.spellstart[counter] and pc.clss.spellstart[counter] < pc.clss.spellmax[counter]:
                                        pc.clss.spellstart += 1
                                        messageappend("You feel more dangerous!")
                                    break
                                counter += 1
                            if pc.spells[choice-1][0].shape == "nil":
                                spellbook.cast(pc.spells[choice-1][0], 0, pc, tpoint, stdscr)
                            else:
                                dir = determinedirection(stdscr)
                                if dir != None:
                                    spellbook.cast(pc.spells[choice-1][0], dir, pc, tpoint, stdscr)
                        else:
                            if choice != "c":
                                messageappend("Select a number within the shown range!")
                            else:
                                break

                findpoint(pc.x, pc.y).monster = pc
                break

            if command in viablecommands and command in freecommands:
                if command == "*":
                    pc.HP = 0
                    break

                if command == "p":
                    for it in pc.debts:
                        cost = int((it.value*1.15)/(1 + 0.05*mod(pc.CHA)))
                        stdscr.addstr(6, 71, "wallet- " + str(pc.wealth), WHITE_ON_BLACK)
                        stdscr.addstr(7, 71, it.display + "- " + str(cost), WHITE_ON_BLACK)
                        while True:
                            stdscr.addstr(28, 0, "Buy this item? (y/n) ", WHITE_ON_BLACK)
                            checkout = str(chr(stdscr.getch()))
                            if checkout not in ["y", "n"]:
                                im("Please answer y or n!", stdscr)
                            else:
                                if checkout == "y":
                                    if pc.wealth >= cost:
                                        pc.wealth -= cost
                                        pc.debts.remove(it)
                                        purchasable.remove(it)
                                        for shit in shopkeeps:
                                            if it in shit.protective:
                                                shit.protective.remove(it)
                                        im("Thank you for your purchase!", stdscr)
                                    else:
                                        im("You are too broke to buy this item!", stdscr)
                                break

                if command == "R":
                    sus = inventorycheck(1, "Remove", armorlist, stdscr)
                    if sus != None:
                        messageappend("You remove your", sus.display)
                        if  sus == pc.helm:
                            pc.helm = 0
                        if  sus == pc.chest:
                            pc.chest = 0
                        if  sus == pc.boots:
                            pc.boots = 0
                        break

                if command == "r":
                    sus = inventorycheck(1, "read", spellbooklist + scrolllist, stdscr)
                    if sus != None:
                        if isinstance(sus, spellbook):
                            flag = 0
                            for x in pc.spells:
                                if isinstance(sus, type(x[0])):
                                    flag = 1
                            
                            if flag == 0:
                                spellbook.read(sus, pc, stdscr)
                            else:
                                messageappend("You already know " + sus.display + "!")
                        else:
                            scroll.read(sus, pc, stdscr)
                        break

                if command == "d":
                    dropped = inventorycheck(1, "drop", stuff, stdscr)
                    if dropped != None:
                        messageappend("You drop your " + dropped.display)
                        pc.stuff.remove(dropped)
                        findpoint(pc.x, pc.y).items.append(dropped)
                        for sho in shopkeeps:
                            if findpoint(pc.x, pc.y).isroom == sho.shopid and len(checkadj(findpoint(pc.x, pc.y), "door", 0)) == 0:
                                if dropped in pc.debts and dropped in sho.protective:
                                    pc.debts.remove(dropped)
                                else:
                                    while True:
                                        im("Sell your " + dropped.display + " for " + str(int(0.75*dropped.value/(1-mod(pc.CHA)*0.05))) + "? (y/n) ", stdscr)
                                        yeeep = chr(stdscr.getch())
                                        if yeeep in ["y", "n"]:
                                            if yeeep == "y":
                                                sho.protective.append(dropped)
                                                pc.wealth += int(0.8*dropped.value/(1-mod(pc.CHA)*0.05))
                                            break
                                        else:
                                            print("please reply y or n!")
                        break

                if command == "q":
                    drinkup = inventorycheck(1, "quaff", potionlist, stdscr)
                    if drinkup != None:
                        potion.drink(drinkup, pc, stdscr)
                        pc.stuff.remove(drinkup)
                        break

                if command == "z":
                    zaperino = inventorycheck(1, "zap", wandlist, stdscr)
                    if zaperino != None:
                        wand.zap(zaperino, pc, stdscr)
                        break

                if command == "C":
                    sus = determinedirection(stdscr)
                    impasta = findpoint(pc.x + sus[0], pc.y + sus[1])
                    if impasta.monster != 0:
                        monster.chat(impasta.monster)
                        break
                    else:
                        messageappend("You are overwhelmed by lonliness realizing there is no one to talk to")
                if command == "i":
                    inventorycheck(0, 0, 0, stdscr)
                
                if command == "S":
                    stdscr.addstr(5, 71, "-------------Skills-------------", WHITE_ON_BLACK)
                    counter = 0
                    for skil in weaponskills:
                        stdscr.addstr(6+counter, 71, "| " + skil + " "*(25-len(skil)) + str(pc.skills[counter]) + "/" + str(pc.clss.maxskills[counter]) + " |", WHITE_ON_BLACK)
                        counter += 1
                    stdscr.addstr(6+counter, 71, "|------------Spells------------|", WHITE_ON_BLACK)
                    counter += 1
                    weaponnum = counter
                    for skil in spellskills:
                        stdscr.addstr(6+counter, 71, "| " + skil + " "*(25-len(skil)) + str(pc.clss.spellstart[counter-weaponnum]) + "/" + str(pc.clss.spellmax[counter-weaponnum]) + " |", WHITE_ON_BLACK)
                        counter += 1
                    stdscr.addstr(6+counter, 71, "--------------------------------", WHITE_ON_BLACK)
                
                if command == "w":
                    decision = inventorycheck(1, "wield", weaponlist, stdscr)
                    if decision != None:
                        pc.weapon = decision
                        messageappend("You are now wielding your " + decision.display)
                        break

                if command == "W":
                    choice = inventorycheck(1, "Equip", armorlist, stdscr)
                    if choice != None:
                        messageappend("You are now wearing your " + choice.display)
                        if isinstance(choice, chest):
                            pc.chest = choice
                            break
                        if isinstance(choice, helm):
                            pc.helm = choice
                            break
                        if isinstance(choice, boots):
                            pc.boots = choice
                            break
            else:
                pass
        if findpoint(pc.x, pc.y).items != [] and startpoint != findpoint(pc.x, pc.y):
            call(findpoint(pc.x, pc.y).items[len(findpoint(pc.x, pc.y).items)-1])
        checkup()
        turnup(stdscr)

        if pc.HP <= 0:
            display(stdscr)
            stdscr.addstr(28, 0, " "*80, RED_ON_BLACK)
            stdscr.addstr(28, 0, "RIP " + pc.name + " the " + pc.clss.display, RED_ON_BLACK)
            stdscr.refresh()
            cont = chr(stdscr.getch())
            break

def main():
    createpc()
    global DLVL
    DLVL = 1
    global turn
    turn = 100
    curses.wrapper(cursesdraw)

main()

##Thanks for playing