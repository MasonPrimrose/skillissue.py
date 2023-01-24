import random

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
    def __init__(self, id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls):
        self.id = id
        self.x = x
        self.y = y
        self.HP = HP
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

    def attack(self, target):
        print("The",self.display,"attacks",target.display,"!")
        if diceroll(1,20, self.bonus) >= target.AC:
            damage = diceroll(self.number, self.dx, self.bonus)- target.dred
            if damage > 0:
                target.HP -= damage
            else:
                print("But the",self.display,"'s attack doesn't seem to harm",target.display,"!")
        else:
            print("But the",self.display,"'s attack missed",target.display,"!")
        
    def act(self):
        ##Things every move will need
        findpoint(self.x, self.y).monster = 0
        eligiblemoves = []
        eligibleloop = [".", "#", "+", "<", ">"]
        for x in eligibleloop:
            eligiblemoves += checkadj(findpoint(self.x, self.y), x, 0)
        killlist = []

        ##TEAM EVIL YEAH
        if self.alignment == "evil":
            for x in eligiblemoves:
                if isinstance(x.monster, monster) is True:
                    if x.monster.alignment == "evil":
                        killlist.append(x)
            for x in killlist:
                eligiblemoves.remove(x)

            finaltarget = findpoint(pc.x, pc.y)


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
            dorandom = 1
            if -10 <= (pc.x-self.x) <= 10 and -10 <= (pc.y-self.y) <= 10:
                if self.x < finaltarget.x and findpoint(self.x+1, self.y) in eligiblemoves:
                    target = findpoint(self.x+1, self.y)
                    dorandom = 0
                if self.x > finaltarget.x and findpoint(self.x-1, self.y) in eligiblemoves:
                    target = findpoint(self.x-1, self.y)
                    dorandom = 0
                if self.y < finaltarget.y and findpoint(self.x, self.y+1) in eligiblemoves:
                    target = findpoint(self.x, self.y+1)
                    dorandom = 0
                if self.y > finaltarget.y and findpoint(self.x, self.y-1) in eligiblemoves:
                    target = findpoint(self.x, self.y-1)
                    dorandom = 0

            if dorandom == 1:
                self.ai = "random"
                self.act()
                self.ai = "primitive"
                return

        ##Movement
        if target.monster == 0:
            self.x = target.x
            self.y = target.y
            target.monster = self
        else:
            findpoint(self.x, self.y).monster = self
            self.attack(target.monster)

##Rats (r/R)
class smallrat(monster):
    def __init__(self, id, x, y, HP = 4, AC = 10, dred = 0, number = 1, dx = 3, bonus = 1, ai = "primitive", speed = 1, symbol = "r", display = "small rat", rarity = 10, power = 1, alignment = "evil", effects = [], peacefuls = []):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

class giantrat(monster):
    def __init__(self, id, x, y, HP = 8, AC = 11, dred = 0, number = 1, dx = 6, bonus = 2, ai = "primitive", speed = 1, symbol = "R", display = "giant rat", rarity = 6, power = 2, alignment = "evil", effects = [], peacefuls = []):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

class kingrat(monster):
    def __init__(self, id, x, y, HP = 22, AC = 14, dred = 1, number = 2, dx = 6, bonus = 4, ai = "primitive", speed = 1, symbol = "K", display = "rat king", rarity = 6, power = 10, alignment = "evil", effects = [], peacefuls = []):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

##Plants (F)
class lichen(monster):
    def __init__(self, id, x, y, HP = 2, AC = 7, dred = 0, number = 1, dx = 2, bonus = 0, ai = "random", speed = 0.1, symbol = "F", display = "lichen", rarity = 6, power = 0.2, alignment = "neutral", effects = [], peacefuls = []):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

##Doglikes (d)
class coyote(monster):
    def __init__(self, id, x, y, HP = 8, AC = 12, dred = 0, number = 1, dx = 5, bonus = 1, ai = "primitive", speed = 1.25, symbol = "d", display = "coyote", rarity = 15, power = 2, alignment = "evil", effects = [], peacefuls = []):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

##Humanoids (h)
class highwayman(monster):
    def __init__(self, id, x, y, HP = 13, AC = 14, dred = 0, number = 2, dx = 3, bonus = 3, ai = "primitive", speed = 1.4, symbol = "h", display = "highwayman", rarity = 5, power = 6, alignment = "evil", effects = [], peacefuls = [rogue]):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

class bandit(monster):
    def __init__(self, id, x, y, HP = 7, AC = 12, dred = 0, number = 1, dx = 4, bonus = 2, ai = "primitive", speed = 1.2, symbol = "h", display = "bandit", rarity = 8, power = 2, alignment = "evil", effects = [], peacefuls = [rogue]):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

##Undead (Z/S)
class zombie(monster):
    def __init__(self, id, x, y, HP = 13, AC = 11, dred = 1, number = 1, dx = 4, bonus = 3, ai = "primitive", speed = 0.66, symbol = "Z", display = "zombie", rarity = 15, power = 3, alignment = "evil", effects = []):
        super().__init__(id, x, y, HP, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls)

monsterlist = [smallrat, giantrat, kingrat, lichen, coyote, bandit, highwayman, zombie]


##classes for objects
class weapon:
    def __init__(self, id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol = ")"):
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
    
    def attack(self, origin, target, tpoint):
        bonus = 0
        for x in self.attributes:
            if x is int:
                bonus += x
        if self.ability == "DEX":
            bonus += mod(pc.DEX)
        else:
            bonus += mod(pc.STR)
        
        counter = -1
        if origin == pc:
            counter = 0
            displaynames = ["Your", "You", "", ""]
            for x in weaponskills:
                if self.skill == x:
                    skillselect = pc.skills[counter]
                    break
                else:
                    counter += 1
        else:
            skillselect = 1
            displaynames = ["The " + origin.display + "'s", "The " + origin.display, "s", "with its " + self.display]
        
        atkbonus = 0
        atkbonus += (-4/(skillselect+1)) + 2*skillselect

        if diceroll(1, 20, (round(pc.LVL/4, 1)+1+atkbonus+bonus)) >= target.AC:
            if counter >= 0:
                pc.training[counter] += 1
                if pc.training[counter] >= 20 + (30 + 10*pc.skills[counter]-1) * pc.skills[counter] and pc.skills[counter] < pc.clss.maxskills[counter]:
                    print("You feel more dangerous!")
                    
                    pc.skills[counter] += 1

            sus = diceroll(self.number, self.dx, bonus)
            if sus <= target.dred:
                print(displaynames[0], "attack does no damage!")
            else:
                target.HP -= sus
                print(displaynames[1], "strike", displaynames[2], "the", target.display,"!")
                if target.HP <= 0:
                    print(displaynames[1], "kill", displaynames[2], "the", target.display,"!")
                    pc.XP += int(5*target.power)
                    tpoint.monster = 0
        else:
            print("Your attack missed!")

weapons = []
armors = []
spellbooks = []

class hand(weapon):
    def __init__(self, id, weight = 0, number = 1, dx = 2, ability = "STR", attributes = [], value = 0, rarity = 0, display = "hand", skill = "boxing", symbol = "hand"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class gauntlet(weapon):
    def __init__(self, id, weight = 0, number = 1, dx = 4, ability = "STR", attributes = [], value = 25, rarity = 2, display = "hand", skill = "boxing", symbol = ")"):
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

class longsword(weapon):
    def __init__(self, id, weight = 10, number = 1, dx = 10, ability = "STR", attributes = [], value = 50, rarity = 5, display = "longsword", skill = "longsword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class greatsword(weapon):
    def __init__(self, id, weight = 20, number = 2, dx = 6, ability = "STR", attributes = [], value = 100, rarity = 3, display = "greatsword", skill = "two-handed sword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class mace(weapon):
    def __init__(self, id, weight = 8, number = 1, dx = 6, ability = "STR", attributes = [], value = 10, rarity = 10, display = "mace", skill = "mace", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class morningstar(weapon):
    def __init__(self, id, weight = 14, number = 2, dx = 4, ability = "STR", attributes = [], value = 15, rarity = 4, display = "morningstar", skill = "mace", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)    

class cudgel(weapon):
    def __init__(self, id, weight = 6, number = 1, dx = 5, ability = "STR", attributes = [], value = 8, rarity = 7, display = "cudgel", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)  

class nightstick(weapon):
    def __init__(self, id, weight = 4, number = 1, dx = 5, ability = "STR", attributes = [], value = 10, rarity = 0, display = "cudgel", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class greatclub(weapon):
    def __init__(self, id, weight = 11, number = 2, dx = 4, ability = "STR", attributes = [], value = 18, rarity = 2, display = "cudgel", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

weaponskills = ["boxing", "knife", "rapier", "longsword", "two-handed sword", "mace", "club"]

class armor:
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, symbol):
        self.id = id
        self.weight = weight
        self.ACbase = ACbase
        self.dred = dred
        self.attributes = attributes
        self.value = value
        self.rarity = rarity
        self.display = display
        self.symbol = symbol

class chest(armor):
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol)
        self.MaxDex = MaxDex

class robe(chest):
    def __init__(self, id, weight = 2, ACbase = 1, dred = 0, attributes = [], value = 15, rarity = 5, display = "robe", symbol = "]", MaxDex = 10):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)

class leather(chest):
    def __init__(self, id, weight = 10, ACbase = 2, dred = 0, attributes = [], value = 15, rarity = 20, display = "leather armor", symbol = "]", MaxDex = 8):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)

class studdedleather(chest):
    def __init__(self, id, weight = 20, ACbase = 3, dred = 0, attributes = [], value = 20, rarity = 15, display = "studded leather armor", symbol = "]", MaxDex = 7):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)    

class scalemail(chest):
    def __init__(self, id, weight = 40, ACbase = 5, dred = 1, attributes = [], value = 50, rarity = 15, display = "scale mail", symbol = "]", MaxDex = 3):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)

class ringmail(chest):
    def __init__(self, id, weight = 45, ACbase = 3, dred = 1, attributes = [], value = 30, rarity = 20, display = "ring mail", symbol = "]", MaxDex = 1):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)

class chain(chest):
    def __init__(self, id, weight = 50, ACbase = 6, dred = 2, attributes = [], value = 70, rarity = 10, display = "chainmail", symbol = "]", MaxDex = 1):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)

class fieldplate(chest):
    def __init__(self, id, weight = 65, ACbase = 5, dred = 2, attributes = [], value = 120, rarity = 8, display = "field plate", symbol = "]", MaxDex = 2):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)

class plate(chest):
    def __init__(self, id, weight = 90, ACbase = 6, dred = 3, attributes = [], value = 150, rarity = 5, display = "plate mail", symbol = "]", MaxDex = 0):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol, MaxDex)


class helm(armor):
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, symbol):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol)

class cone(helm):
    def __init__(self, id, weight = 1, ACbase = 0, dred = 0, attributes = [], value = 5, rarity = 2, display = "cone", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol)

class cap(helm):
    def __init__(self, id, weight = 2, ACbase = 1, dred = 0, attributes = [], value = 10, rarity = 5, display = "cap", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol) 

class pot(helm):
    def __init__(self, id, weight = 5, ACbase = 1, dred = 0, attributes = [], value = 5, rarity = 7, display = "cookpot", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol) 


class boots(armor):
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, symbol):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol)

class cowboyboots(boots):
    def __init__(self, id, weight = 3, ACbase = 1, dred = 0, attributes = [], value = 15, rarity = 2, display = "cowboy boots", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol) 

class slippers(boots):
    def __init__(self, id, weight = 1, ACbase = 0, dred = 0, attributes = [], value = 3, rarity = 1, display = "slippers", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol) 

class greaves(boots):
    def __init__(self, id, weight = 10, ACbase = 2, dred = 0, attributes = [], value = 30, rarity = 2, display = "greaves", symbol = "]"):
        super().__init__(id, weight, ACbase, dred, attributes, value, rarity, display, symbol)    




class spellbook():
    def __init__(self, id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol = "+", weight = 15):
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
    
    def read(self, user):
        if user == pc:
            if diceroll(1, 20, pc.INT) >= 16 - (pc.LVL/2) + (self.level/2):
                turn = 0
                while turn < self.actions:
                    flag = 0
                    for x in vision(pc, 10):
                        if x.monster != 0:
                            flag = 1
                    if flag == 1:
                        print("You spy a monster out of the corner of your eye while reading!")
                        return
                    turnup()
                    turn += 1
                pc.spells.append([self, 200+mod(pc.INT)*20])
                print("You have learned the", self.display, "spell!")
            else:
                print("The spellbook's incomprehensible runes burn your eyes!")
                pc.HP -= diceroll(2, 3+pc.LVL, 10-mod(pc.clss.spell))

    def cast(self, direction, user, origin):
        if user == pc:
            totalrange = self.range + int(mod(pc.clss.spell)**0.5)
        else:
            totalrange = self.range

        targets = []
        ##direction should be [x, y]
        if self.shape != "cone":
            loop = 0
            while loop < totalrange:
                tpoint = findpoint(origin.x + direction[0], origin.y + direction[1])
                if tpoint.monster != 0 and monster in self.caneffect or tpoint.type in self.caneffect:
                    targets.append(tpoint)
                    if len(targets) >= self.targets:
                        break
                loop += 1
        else:
            ##direction should be "up" etc
            for target in triangle(origin, 1, direction, round(totalrange, 2)):
                targets.append(target)
        
        if pc.MP >= self.level*5:
            pc.MP -= self.level*5
            for x in targets:
                self.effect(x, user)
        else:
            print("You do not have the energy to cast this spell!")
            return
    
    def effect(self, target, user):
        if self.display == "stun monster":
            if user == pc:
                if diceroll(1, 20, mod(pc.clss.spell)) >= 8 + target.monster.power:
                    flag = 0
                    for x in target.monster.effects:
                        if "stunned" in x:
                            x[1] += random.randint(1, mod(pc.clss.spell))
                            flag = 1
                    if flag == 0:
                        target.monster.effects.append(["stunned", random.randint(1, mod(pc.clss.spell))])
                        target.monster.ai = "random"
                    print("The", target.monster.display, "seems dazed!")
                else:
                    print("The", target.monster.display, "resists!")
        if self.display == "slow":
            if user == pc:
                if diceroll(1, 20, mod(pc.clss.spell)) >= 8 + target.monster.power:
                    target.monster.speed -= mod(pc.clss.spell)/target.monster.power + 0.35*pc.clss.spellskill
                    if target.monster.speed <= 0.1:
                        target.monster.speed = 0.1
                    flag = 0
                    for x in target.monster.effects:
                        if "slow" in x:
                            x[1] += random.randint(1, mod(pc.clss.spell))
                            flag = 1
                    if flag == 0:
                        target.monster.effects.append(["slow", random.randint(1, mod(pc.clss.spell))])
                    print("The", target.monster.display, "seems to be moving slower!")
                else:
                    print("The", target.monster.display, "resists!")

class stunmonster(spellbook):
    def __init__(self, id, display = "stun monster", level = 1, range = 3, rarity = 40, value = 100, targets = 1, caneffect = [monster], shape = "line", actions = 12, school = "enchantment", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)     

class slow(spellbook):
    def __init__(self, id, display = "slow", level = 2, range = 5, rarity = 20, value = 200, targets = 2, caneffect = [monster], shape = "line", actions = 22, school = "enchantment", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)     


##Item Lists
armorlist = [robe, leather, studdedleather, scalemail, ringmail, fieldplate, chain, plate, cap, cone, pot, cowboyboots, slippers, greaves]
weaponlist = [gauntlet, knife, dagger, longsword, greatsword, mace, morningstar, rapier, duelingsword, cudgel, nightstick, greatclub]
spellbooklist = [stunmonster, slow]

##classes for pc and map
class point:
    def __init__(self, x, y, type, symbol, display, isroom, monster, items):
        self.x = x
        self.y = y
        self.type = type
        self.symbol = symbol
        self.display = display
        self.isroom = isroom
        self.monster = monster
        self.items = items

nomove = ["wall", "infill"]

class player:
    def __init__(self, HP, HPMax, MP, MPMax, carry, AC, dred, XP, STR, DEX, CON, INT, WIS, CHA, clss, race, name, LVL, x, y, stuff, weapon, helm, chest, boots, statuses, display, memory, skills, training, spells):
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

pc = player(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [], hand, 0, 0, 0, [], "you", [], [], [0, 0, 0, 0, 0, 0], [])

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

class clss:
    def __init__(self, display, STR, DEX, CON, INT, WIS, CHA, spell, spellskill, baseHP, startinventory, startskills, maxskills):
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

wizard = clss("wizard", diceroll(3, 4, 2), diceroll(3, 4, 6), diceroll(3, 4, 4), diceroll(3, 4, 10), diceroll(2, 8, 4), diceroll(2, 8, 4), 1, 1, 6, [dagger, robe, stunmonster, slow], [0, 1, 0, 0, 0, 0, 0], [1, 2, 0, 1, 0, 0, 1])
priest = clss("priest", diceroll(2, 8, 4), diceroll(3, 4, 4), diceroll(3, 4, 6), diceroll(3, 4, 6), diceroll(2, 8, 8), diceroll(3, 4, 6), 2, 0.75, 8, [mace, robe, slippers], [0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 3, 2])
rogue = clss("rogue", diceroll(3, 4, 4), diceroll(3, 4, 10), diceroll(3, 4, 6), diceroll(3, 4, 6), diceroll(2, 8, 4), diceroll(3, 4, 8), 3, 0.25, 8, [dagger, leather, cowboyboots], [1, 1, 0, 0, 0, 0, 0], [2, 3, 2, 1, 0, 0, 1])
knight = clss("knight", diceroll(3, 4, 10), diceroll(3, 4, 4), diceroll(3, 4, 10), diceroll(3, 4, 4), diceroll(3, 4, 4), diceroll(3, 4, 6), 3, 0.25, 10, [longsword, ringmail], [0, 0, 0, 1, 1, 0, 1], [1, 1, 2, 3, 3, 2, 3])

##Mapmaker

def createpoints():
    global points
    points = []
    loopy = 1
    while loopy <= 20:
        loopx = 1
        while loopx <= 70:
            points.append(point(loopx, loopy, "infill", " ", " ", 0, 0, []))
            loopx += 1
        loopy += 1

def findpoint(x,y):
    tpoint = 70*(y-1)+x-1
    if y <= 20 and x <= 70:
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
    pass

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
            findpoint(loopx, loopy).display = findpoint(loopx, loopy).symbol
            if findpoint(loopx, loopy).items != []:
                findpoint(loopx, loopy).display = findpoint(loopx, loopy).items[len(findpoint(loopx, loopy).items)-1].symbol
            if findpoint(loopx, loopy).monster != 0:
                if findpoint(loopx, loopy).monster == pc:
                    findpoint(loopx, loopy).display = "@"
                else:
                    findpoint(loopx, loopy).display = findpoint(loopx, loopy).monster.symbol
            loopy -= 1
        loopx -= 1

def printmap():
    checkmap()
    yprinter = ""
    invision = vision(pc, 6)
    loopy = 20
    while loopy > 0:
        loopx = 1
        while loopx <= 70:
            if findpoint(loopx, loopy) in pc.memory:
                if findpoint(loopx, loopy) in invision or findpoint(loopx, loopy).monster == pc:
                    yprinter += findpoint(loopx, loopy).display
                else:
                    yprinter += findpoint(loopx, loopy).symbol
            else:
                yprinter += " "
            loopx += 1
        loopy -=1
        print(yprinter)
        yprinter = ""

def intitialize(floor, type):
    createpoints()
    if type == "standard":
        standardfloor(6, 4, 8)
        doordash(6, 0)
        distributeloot(100+(floor-1)*20, [0.4, 0.4, 0.2])
        distributemonsters(5+(floor-1)*2 + (3*pc.LVL), round(floor/3, 1), 3+round(floor/2, 1))
    if type == "bigroom":
        thebigroom()
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


##Item/loot functions
def mintitem(item):
    if isinstance(item, weapon):
        thelist = weapons
    if isinstance(item, armor):
        thelist = armors
    if isinstance(item, spellbook):
        thelist = spellbooks
    thelist.append(item)
    if thelist == armors or thelist == weapons:
        loop = 3
        while loop > 0:
            chance = random.randint(1,10)
            if chance == 1:
                thelist[len(thelist)-1].attributes.append(-1)
            if chance == 10:
                thelist[len(thelist)-1].attributes.append(1)
            loop -= 1
        thelist[len(thelist)-1].id = len(thelist)

    return(thelist[len(thelist)-1])

def itemdistribution(totalvalue, list, macrolist, distributionnumber):
    value = round(totalvalue*distributionnumber, 1)
    raritybuilder = []
    for x in list:
        sus = x(0)
        loop = sus.rarity
        while loop > 0:
            if sus.value <= value:
                raritybuilder.append(x)
                loop -= 1
            else:
                break
    returnlist = []
    while raritybuilder != []:
        returnlist.append(raritybuilder[random.randint(1, len(raritybuilder))-1])
        sus = mintitem(returnlist[len(returnlist)-1](0))
        value -= sus.value
        newlist = []
        for x in raritybuilder:
            sus = x(0)
            if sus.value <= value:
                newlist.append(x)
        raritybuilder = newlist
    return returnlist

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

    for x in itemdistribution(totalvalue, weaponlist, weapons, distribution[0]):
        looteligible[random.randint(1, len(looteligible))-1].items.append(mintitem(x(0)))
    for x in itemdistribution(totalvalue, armorlist, armors, distribution[1]):
        looteligible[random.randint(1, len(looteligible))-1].items.append(mintitem(x(0)))
    for x in itemdistribution(totalvalue, spellbooklist, spellbooks, distribution[2]):
        looteligible[random.randint(1, len(looteligible))-1].items.append(mintitem(x(0)))

def call(item):
    if item.display[len(item.display)-1] != "s":
        if isinstance(item, spellbook) != True:
            print("You see here a", item.display)
        else:
            print("You see here a spellbook of", item.display)
    else:
        print("You see here some", item.display)

##Monster Functions
def mintmonster(type):
    x = type(0, 0, 0)
    monsters.append(x)
    monsters[len(monsters)-1].id = len(monsters)
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
        targetblock.monster = mintmonster(raritybuilder[random.randint(1, len(raritybuilder))-1])
        monsters[len(monsters)-1].x = targetblock.x
        monsters[len(monsters)-1].y = targetblock.y 
        monstereligible.remove(targetblock)
        loop -= monsters[len(monsters)-1].power


##General Functions
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

def display():
    print("")
    print(pc.name, "the", pc.clss.display)
    bufferspace = " "
    loop = 0
    while loop < 6 -len(str(pc.HP))-len(str(pc.HPMax)):
        bufferspace += " "
        loop += 1
    print("HP:", pc.HP, "/", pc.HPMax, bufferspace, healthbar(pc.HP, pc.HPMax, 20))
    bufferspace = " "
    loop = 0
    while loop < 6-len(str(pc.MP))-len(str(pc.MPMax)):
        bufferspace += " "
        loop += 1
    print("MP:", pc.MP, "/", pc.MPMax, bufferspace, healthbar(pc.MP, pc.MPMax, 20))
    print("Carry Capacity:", healthbar(weight, pc.carry, 20))

    printmap()

    print("STR: ", pc.STR, "DEX: ", pc.DEX, "CON: ", pc.CON, "INT: ", pc.INT, "WIS: ", pc.WIS, "CHA: ", pc.CHA)
    print("Level:", pc.LVL, "AC:", pc.AC, "XP:", pc.XP, "DLVL:", DLVL, "Turn:", turn-100)

def turnup():
    global turn
    turn += 1
    tomove = []

    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if isinstance(findpoint(loopx, loopy).monster, monster):
                tomove.append(findpoint(loopx, loopy).monster)
            loopy -= 1
        loopx -=1
    for x in tomove:
        loop = 0
        reducer = x.speed
        if "burdened" in pc.statuses:
            reducer += 1/3
        naturalspeed = 0
        while reducer > 1:
            naturalspeed += 1
            reducer -= 1
        if reducer != 0 and isdivis(turn, 1/reducer) == 1:
            loop += 1
        loop += naturalspeed
        while loop > 0:
            x.act()
            loop -= 1

    removal = []
    for x in pc.spells:
        x[1] -= 1
        if x[1] <= 0:
            removal.append(x)
    for x in removal:
        pc.spells.remove(x)


def cutscene(number):
    opening = ["Welcome to Rrat Killing Simulator " + pc.name + "!", "The great lamp is dying, and without it the world is sinking into chaos", "and strife. You have been chosen as the light bearer, the one prophecied", "to delve into Carceri and recover the stolen flame of the world!"]
    scenes = [opening]
    for x in scenes[number]:
        print(x)

##PC Functions
def createpc():
    select = 1
    pc.LVL = 1
    pc.stuff = []
    while select == 1:
        eligibleclasses = [wizard, priest, knight, rogue]
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
        eligibleraces = [human, elf, halfling, gnome, dwarf]
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
        pc.MPMax = int((5+mod(pc.clss.spell))*pc.clss.spellskill)
        pc.MP = pc.MPMax
        for x in pc.clss.startinventory:
            pc.stuff.append(mintitem(x(0)))
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
    pc.HPMax = int(pc.clss.baseHP + mod(pc.CON)*pc.LVL + 0.5*(pc.LVL-1)*pc.clss.baseHP)
    pc.HP += pc.HPMax - oldmax
    pc.MPMax = int((5+mod(pc.clss.spell)*pc.LVL)*pc.clss.spellskill)
    pc.MP += pc.MPMax - oldmaxm

def checkup():
    global weight

    if isdivis(turn, 5) == 1 and pc.HP < pc.HPMax:
        pc.HP += 1

    if isdivis(turn, round(10/3*pc.clss.spellskill, 1)) == 1 and pc.MP < pc.MPMax:
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

    pc.carry = 75 + 4*pc.STR
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

def vision(origin, sight):
    invision = triangle(origin, 1, "up", sight) + triangle(origin, 1, "right", sight) + triangle(origin, 1, "down", sight) + triangle(origin, 1, "left", sight)
    return invision

def returnlist(action, type):
    listicle = []
    for x in pc.stuff:
        if isinstance(x, type):
            listicle.append(x)
    loop = 1
    while loop <= len(listicle):
        print(loop, ":", listicle[loop-1].display)
        loop += 1
    try:
        inputbuilder = action + " which item (number)? "
        clarification = int(input(inputbuilder))
        clarification += 0
    except ValueError:
        print("Please choose a number within the shown range!")
    else:
        if 0 < clarification <= len(listicle):
            return listicle[clarification-1]
        else:
            print("Please choose an item in the list!")

##Primary Loop
createpc()
##cutscene(0)
DLVL = 1
turn = 100
checkup()
intitialize(DLVL, "standard")

truecommands = ["h", "j", "k", "l", ">", ",", "d", "R", "r", ".", "Z", "ogey"]
freecommands = ["i", "w", "W", "S"]
while 1 == 1:
    for pos in vision(pc, 6):
        pc.memory.append(pos)
    display()
    viablecommands = [".", "r", "S", "ogey"]
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
    if pc.helm != 0 or pc.chest != 0 or pc.boots != 0:
        viablecommands.append("R")
    while 1 == 1:
        if findpoint(pc.x, pc.y).items != []:
            call(findpoint(pc.x, pc.y).items[len(findpoint(pc.x, pc.y).items)-1])
        command = input("Do what? ")
        if command in truecommands and command in viablecommands:
            findpoint(pc.x, pc.y).monster = 0
            tpoint = findpoint(pc.x, pc.y)
            if command == "ogey":
                for x in triangle(pc, 1, "right", 8):
                    x.symbol = "$"
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
            if command == ">":
                DLVL += 1
                intitialize(DLVL, "standard")
            if command == ",":
                if len(findpoint(pc.x, pc.y).items) == 1:
                    pc.stuff.append(findpoint(pc.x, pc.y).items[0])
                    findpoint(pc.x, pc.y).items.remove(findpoint(pc.x, pc.y).items[0])
                else:
                    loop = 0
                    while loop < len(findpoint(pc.x, pc.y).items):
                        print(loop + 1, ":", findpoint(pc.x, pc.y).items[loop].display)
                        loop += 1
                    while 1 == 1:
                        try:
                            clarification = int(input("Take which (number): "))
                            clarification += 0
                        except ValueError:
                            print("Type a number please!")
                        else:
                            if 0 < clarification <= len(findpoint(pc.x, pc.y).items):
                                    pc.stuff.append(findpoint(pc.x, pc.y).items[clarification-1])
                                    findpoint(pc.x, pc.y).items.remove(findpoint(pc.x, pc.y).items[clarification-1])
                                    break
                            else:
                                    print("Please type a number within the acceptable range")
            if command == "d":
                loop = 1
                while loop <= len(pc.stuff):
                    print(loop, ":", pc.stuff[loop-1].display)
                    loop += 1
                try:
                    clarification = int(input("Drop which item (number)? "))
                    clarification += 0
                except ValueError:
                    print("Type a number please!")
                else:
                    if 0 < clarification <= len(pc.stuff):
                        print("You drop the", pc.stuff[clarification-1].display)
                        findpoint(pc.x, pc.y).items.append(pc.stuff[clarification-1])
                        pc.stuff.remove(pc.stuff[clarification-1])
                    else:
                        print("Please type a number within the acceptable range")
            if command == "R":
                sus = returnlist("Remove", armor)
                if  sus == pc.helm:
                    pc.helm = 0
                if  sus == pc.chest:
                    pc.chest = 0
                if  sus == pc.boots:
                    pc.boots = 0
            if command == "r":
                spellbook.read(returnlist("Read", spellbook), pc)
            if command == "Z":
                counter = 1
                for x in pc.spells:
                    print(counter,":", x[0].display, " "*(15-len(x[0].display)) + "LVL:", x[0].level)
                    counter += 1
                try:
                    choice = int(input("Cast which spell (number)? "))
                    choice += 0
                except TypeError:
                    print("Type a number please!")
                else:
                    if 1 <= choice <= counter:
                        while True:
                            clarification = input("In what direction? ")
                            if clarification in ["j", "h", "k", "l"]:
                                if clarification == "j":
                                    spellbook.cast(pc.spells[choice-1][0], [0, -1], pc, tpoint)
                                if clarification == "h":
                                    spellbook.cast(pc.spells[choice-1][0], [-1, 0], pc, tpoint)
                                if clarification == "k":
                                    spellbook.cast(pc.spells[choice-1][0], [0, 1], pc, tpoint)
                                if clarification == "l":
                                    spellbook.cast(pc.spells[choice-1][0], [1, 0], pc, tpoint)
                                break
                            else:
                                print("Choose a movement direction! (h, j, k, l)")
                    else:
                        if choice != "c":
                            print("Select a number within the shown range!")
                        else:
                            break

            findpoint(pc.x, pc.y).monster = pc
            break

        if command in viablecommands and command in freecommands:
            if command == "i":
                weaponsi = []
                armorsi = []
                spellbooksi = []
                print("--------------Inventory--------------")
                for item in pc.stuff:
                    if isinstance(item, weapon) == True:
                        weaponsi.append(item)
                    if isinstance(item, armor) == True:
                        armorsi.append(item)
                    if isinstance(item, spellbook) == True:
                        spellbooksi.append(item)
                print("| Weapons:                          |")    
                for x in weaponsi:
                    if x is pc.weapon:
                        print("|",x.display, " "*(22-len(x.display)), "-equipped |")
                    else:
                        print("|",x.display, " "*(32-len(x.display)),"|")
                print("| Armors:                           |")    
                for x in armorsi:
                    if x is pc.chest or x is pc.helm or x is pc.boots:
                        print("|",x.display, " "*(22-len(x.display)), "-equipped |")
                    else:
                        print("|",x.display, " "*(32-len(x.display)),"|")
                print("| Spellbooks:                       |")    
                for x in spellbooksi:
                    print("| spellbook of",x.display, " "*(19-len(x.display)),"|")
                print("-------------------------------------")
                pc.stuff = weaponsi + armorsi
            
            if command == "S":
                print("-------------Skills-------------")
                counter = 0
                for skil in weaponskills:
                    print("|",skil, " "*(21-len(skil)), pc.skills[counter],"/",pc.clss.maxskills[counter],"|")
                    counter += 1
                print("--------------------------------")
            
            if command == "w":
                decision = 0
                if isinstance(pc.weapon, hand) != True:
                    print("You are currently wielding a", pc.weapon.display)
                    while True:
                        inputbuilder = "Unequip your " + pc.weapon.display + " and select a different weapon (y/n)? "
                        confirmation = input(inputbuilder)
                        if confirmation == "y":
                            pc.weapon = returnlist("Equip", weapon)
                            decision = 1
                            break
                        if confirmation == "n":
                            break
                        print("Please reply either y or n!")
                else:
                    pc.weapon = returnlist("Equip", weapon)
                    break
                if decision == 1:
                    break

            if command == "W":
                choice = returnlist("Equip", armor)
                if isinstance(choice, chest):
                    if pc.chest != 0:
                        print("You must remove your", pc.chest.display, "before you can equip new armor!")
                    else:
                        pc.chest = choice
                        break
                if isinstance(choice, helm):
                    if pc.helm != 0:
                        print("You must remove your", pc.helm.display, "before you can equip new armor!")
                    else:
                        pc.helm = choice
                        break
                if isinstance(choice, boots):
                    if pc.boots != 0:
                        print("You must remove your", pc.boots.display, "before you can equip new armor!")
                    else:
                        pc.boots = choice
                    

        else:
            print("Invalid command")
    checkup()
    turnup()
    if pc.HP <= 0:
        print("RIP", pc.name, "the", pc.clss.display)
        print("So long space cowboy...")
        break
##Thanks for playing