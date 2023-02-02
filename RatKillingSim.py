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
    def __init__(self, id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats):
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

    def chat(self):
        print(self.chats[random.randint(1, len(self.chats))-1])

    def attack(self, target):
        print("The",self.display,"attacks",target.display,"!")
        if diceroll(1,20, self.bonus) >= target.AC:
            specialusers = [rust, highwayman, watchman, vampire, kingrat, gremlin, flamingskeleton]
            for sp in specialusers:
                if isinstance(self, sp):
                    self.special(target)
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

        if pc.clss in self.peacefuls or pc.race in self.peacefuls:
            for x in eligiblemoves:
                if x.monster == pc:
                    killlist.append(x)

        ##TEAM EVIL YEAH
        if self.alignment == "evil":
            for x in eligiblemoves:
                if isinstance(x.monster, monster) is True:
                    if x.monster.alignment == "evil":
                        killlist.append(x)
            finaltarget = findpoint(pc.x, pc.y)

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

            dorandom = 1
            if abs(pc.x-self.x) <= 10 and abs(pc.y-self.y) <= 10 and pc.clss not in self.peacefuls and pc.race not in self.peacefuls:
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
                for x in self.effects:
                    if "stunned" in x:
                        dorandom = 1

            if dorandom == 1:
                self.ai = "random"
                self.act()
                self.ai = "primitive"
                return

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
            monster.anger(target)
            if monster.anger(target) == 1:
                print("'Hey, what's the big idea?' the", target.display, "shouts")
                for x in vision(pc, 6):
                    if type(x.monster) == type(target) and x.monster != 0 and x.monster != target:
                        monster.anger(x.monster)
                        print("The", x.monster.display, "looks angry!")                 
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

class shillelagh(weapon):
    def __init__(self, id, weight = 6, number = 1, dx = 5, ability = "STR", attributes = [], value = 9, rarity = 3, display = "shillelagh", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)  

class nightstick(weapon):
    def __init__(self, id, weight = 4, number = 1, dx = 5, ability = "STR", attributes = [], value = 10, rarity = 0, display = "nightstick", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

class greatclub(weapon):
    def __init__(self, id, weight = 11, number = 2, dx = 4, ability = "STR", attributes = [], value = 18, rarity = 2, display = "greatclub", skill = "club", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, skill, symbol)

weaponskills = ["boxing", "knife", "rapier", "longsword", "two-handed sword", "mace", "club"]

class armor:
    def __init__(self, id, weight, ACbase, dred, attributes, value, rarity, display, material, symbol = "]"):
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

class scalemail(chest):
    def __init__(self, id, weight = 55, ACbase = 4, dred = 1, attributes = [], value = 50, rarity = 15, display = "scale mail", material = "metal", symbol = "]", MaxDex = 3):
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
class spellbook():
    def __init__(self, id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol = "+", weight = 20):
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
            if diceroll(1, 20, mod(pc.INT)) >= 16 - (pc.LVL/2) + (self.level/2):
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
                pc.spells.append([self, 1500+mod(pc.INT)*200])
                print("You have learned the", self.display, "spell!")
            else:
                print("The spellbook's incomprehensible runes burn your eyes!")
                pc.HP -= diceroll(2, 3+pc.LVL, 10-mod(pc.clss.spell))

    def cast(self, direction, user, origin):
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
                if isinstance(tpoint.monster, monster) and monster in self.caneffect or tpoint.type in self.caneffect or tpoint.monster == pc and monster in self.caneffect:
                    targets.append(tpoint)
                    if len(targets) >= self.targets:
                        break
                if 0 < tpoint.x+direction[0] < 71 and 0 < tpoint.y+direction[1] < 21:
                    tpoint = findpoint(tpoint.x + direction[0], tpoint.y + direction[1])
                loop += 1
        else:
            ##direction should be "up" etc
            if direction == "cone":
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
                targets = [point(0, 0, 0, 0, 0, 0, 0, 0)]
        if user != pc:
            for x in targets:
                self.effect(x, user)
            return

        if pc.MP >= self.level*5 and user == pc:
            pc.MP -= self.level*5
            for x in targets:
                if isinstance(x.monster, monster) == True and monster in self.caneffect:
                    if self.school != "healing":
                        monster.anger(x.monster)
                    else:
                        print("'Hey thanks buddy!' the", x.monster.display, "says")
                self.effect(x, user)
        else:
            print("You do not have the energy to cast this spell!")
            return
    
    def effect(self, target, user):
        ##Enchantments
        if self.display == "stun monster":
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
                print("The", target.monster.display, "seems dazed!")
            else:
                print("The", target.monster.display, "resists!")
            return
        if self.display == "slow":
            if user == pc:
                if diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                    flag = 0
                    for x in target.monster.effects:
                        if "slow" in x:
                            x[1] += random.randint(2, mod(pc.clss.spell))
                            flag = 1
                    if flag == 0:
                        target.monster.effects.append(["slow", random.randint(2, mod(pc.clss.spell))+1])
                    print("The", target.monster.display, "seems to be moving slower!")
                else:
                    print("The", target.monster.display, "resists!")
            return
        ##Attacks
        if self.display == "magic missile":
            if user == pc:
                bonus = int(mod(pc.clss.spell))
                maxdice = int(pc.LVL/4)
            else:
                bonus = 4
                maxdice = 1

            if diceroll(1,20, bonus) >= target.monster.AC:
                target.monster.HP -= diceroll(2, 6 + maxdice, bonus)
                print("The magic missle strikes the", target.monster.display,"!")
            else:
                print("The", target.monster.display, "resists!")
            if target.monster.HP <= 0:
                target.monster = 0
            return
        if self.display == "vampiric touch":
            if user == pc:
                if diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                    drainage = diceroll(2, 4, 0)
                    target.monster.HP -= drainage
                    pc.HP += drainage
                    if pc.HP > pc.HPMax:
                        pc.HP = pc.HPMax
                    print("The", target.monster.display, "looks weaker!")
                else:
                    print("The", target.monster.display, "resists!")
                if target.monster.HP <= 0:
                    target.monster = 0
            return
        if self.display == "cone of cold":
            if user == pc:
                if diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                    target.monster.HP -= diceroll(3, 6, 2)
                    target.monster.speed -= mod(pc.clss.spell)/2.5*target.monster.power - 0.5*pc.clss.spellskill
                    print("The", target.monster.display, "is chilled out!")
                else:
                    target.monster.HP -= diceroll(2, 4, 0)
                    print("The", target.monster.display, "resists!")
                if target.monster.HP <= 0:
                    target.monster = 0
            return
        ##clerical
        if self.display == "turn undead" and user == pc:
            if target.monster.symbol in ["Z", "S", "V"] and diceroll(1, 20, mod(pc.clss.spell)) >= 10 + target.monster.power:
                target.monster.HP -= diceroll(1,6,mod(pc.clss.spell))
                target.monster.effects.append(["stunned", random.randint(2, mod(pc.clss.spell)+1)])
            return
        ##divination
        if self.display == "detect monsters":
            symbollog = []
            for po in points:
                if po.monster != 0 and po.monster != pc:
                    symbollog.append(po.symbol)
                    po.symbol = po.monster.symbol
                    pc.memory.append(po)
            display()
            pause = input("Press any button to continue ")
            counter = 0
            for x in points:
                if x.monster != 0 and x.monster != pc:
                    x.symbol = symbollog[counter]
                    counter += 1
                    pc.memory.remove(x)
            return
        if self.display == "detect treasure":
            symbollog = []
            for po in points:
                if len(po.items) > 0:
                    symbollog.append(po.symbol)
                    po.symbol = po.items[len(po.items)-1].symbol
                    pc.memory.append(po)
            display()
            pause = input("Press any button to continue ")
            counter = 0
            for x in points:
                if len(x.items) > 0:
                    x.symbol = symbollog[counter]
                    counter += 1
                    pc.memory.remove(x)
            return
        if self.display == "insight":
            print(target.monster.display)
            print("AC:",target.monster.AC)
            print("HP:",target.monster.HP, "/", target.monster.HPMax)
            print("Damage:",target.monster.number + target.monster.bonus, "-", target.monster.number*target.monster.dx + target.monster.bonus)
            return

        ##escape
        if self.display == "teleport":
            teligible = []
            flagerino = 0
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
            poggers.x = tpoint.x
            poggers.y = tpoint.y
            tpoint.monster = poggers
            target.monster = 0
            return

        ##healing
        if self.display == "cure":
            if user == pc:
                bonus = int(mod(pc.clss.spell)/2)
            else:
                bonus = 4
            target.monster.HP += diceroll(2, 6, bonus)
            if target.monster.HP > target.monster.HPMax:
                target.monster.HP = target.monster.HPMax
            return
        if self.display == "heal":
            if user == pc:
                bonus = int(mod(pc.clss.spell))
            else:
                bonus = 4
            target.monster.HP += diceroll(4, 6, bonus)
            if target.monster.HP > target.monster.HPMax:
                target.monster.HP = target.monster.HPMax
            return

##Enchantment Spells
class stunmonster(spellbook):
    def __init__(self, id, display = "stun monster", level = 1, range = 2, rarity = 30, value = 100, targets = 1, caneffect = [monster], shape = "line", actions = 12, school = "enchantment", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

class slow(spellbook):
    def __init__(self, id, display = "slow", level = 2, range = 3, rarity = 15, value = 200, targets = 2, caneffect = [monster], shape = "line", actions = 22, school = "enchantment", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)     

##Clerical Spells
class turnundead(spellbook):
    def __init__(self, id, display = "turn undead", level = 2, range = 4, rarity = 12, value = 200, targets = 16, caneffect = [monster], shape = "cone", actions = 24, school = "clerical", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol) 

##Attack Spells
class magicmissile(spellbook):
    def __init__(self, id, display = "magic missile", level = 2, range = 5, rarity = 25, value = 200, targets = 3, caneffect = [monster], shape = "line", actions = 24, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

class vampirictouch(spellbook):
    def __init__(self, id, display = "vampiric touch", level = 2, range = 1, rarity = 10, value = 200, targets = 1, caneffect = [monster], shape = "line", actions = 18, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol) 

class coneofcold(spellbook):
    def __init__(self, id, display = "cone of cold", level = 4, range = 4, rarity = 3, value = 400, targets = 16, caneffect = [monster], shape = "cone", actions = 42, school = "attack", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)    

##Divination
class detectmo(spellbook):
    def __init__(self, id, display = "detect monsters", level = 1, range = 0, rarity = 14, value = 100, targets = 0, caneffect = [], shape = "nil", actions = 20, school = "divination", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)  

class detecttr(spellbook):
    def __init__(self, id, display = "detect treasure", level = 1, range = 0, rarity = 10, value = 100, targets = 0, caneffect = [], shape = "nil", actions = 20, school = "divination", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)  

class insight(spellbook):
    def __init__(self, id, display = "insight", level = 2, range = 3, rarity = 7, value = 200, targets = 2, caneffect = [monster], shape = "line", actions = 36, school = "divination", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

##Escape
class teleport(spellbook):
    def __init__(self, id, display = "teleport", level = 4, range = 2 , rarity = 4, value = 400, targets = 1, caneffect = [monster], shape = "line", actions = 76, school = "escape", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

##Healing
class cure(spellbook):
    def __init__(self, id, display = "cure", level = 1, range = 3, rarity = 30, value = 100, targets = 2, caneffect = [monster], shape = "line", actions = 20, school = "healing", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

class cure2(spellbook):
    def __init__(self, id, display = "heal", level = 3, range = 3, rarity = 12, value = 300, targets = 2, caneffect = [monster], shape = "line", actions = 54, school = "healing", symbol = "+"):
        super().__init__(id, display, level, range, rarity, value, targets, caneffect, shape, actions, school, symbol)

##Scrolls
class scroll:
    def __init__(self, id, display, rarity, value, equivalentspell, caneffect, symbol = "?", weight = 10):
        self.id = id
        self.display = display
        self.rarity = rarity
        self.value = value
        self.equivalentspell = equivalentspell
        self.caneffect = caneffect
        self.symbol = symbol
        self.weight = weight

    def read(self, reader):
        if self.equivalentspell != 0:
            spellbook.cast(self.equivalentspell, [0,0], "scroll", findpoint(reader.x, reader.y))
            reader.stuff.remove(self)
        else:
            if isinstance(self, map):
                for x in points:
                    if x not in pc.memory:
                        pc.memory.append(x)
                reader.stuff.remove(self)
                return

tpp = teleport(0)
class tp(scroll):
    def __init__(self, id, display = "teleportation", rarity = 50, value = 30, equivalentspell = tpp, caneffect = []):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect)
    
class map(scroll):
    def __init__(self, id, display = "magic mapping", rarity = 10, value = 65, equivalentspell = 0, caneffect = []):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect)

detectmoo = detectmo(0)
class detectm(scroll):
    def __init__(self, id, display = "detect monsters", rarity = 20, value = 40, equivalentspell = detectmoo, caneffect = []):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect)

detecttrr = detecttr(0)
class detectt(scroll):
    def __init__(self, id, display = "detect treasure", rarity = 20, value = 35, equivalentspell = detecttrr, caneffect = []):
        super().__init__(id, display, rarity, value, equivalentspell, caneffect)


##Potions
class potion:
    def __init__(self, id, display, rarity, value, equivalentspell, symbol = "!", weight = 12):
        self.id = id
        self.display = display
        self.rarity = rarity
        self.value = value
        self.equivalentspell = equivalentspell
        self.symbol = symbol
        self.weight = weight
    
    def drink(self, drinker):
        if self.equivalentspell != 0:
            spellbook.effect(self.equivalentspell, findpoint(drinker.x, drinker.y), "potion")
        else: 
            if isinstance(self, phaste):
                if drinker == pc:
                    pc.statuses.append(["haste", random.randint(10, 30)])
                    print("The world seems to slow down around you")
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
                    print("You feel more dangerous!")
                    return

ppheal = cure(0)
class pheal(potion):
    def __init__(self, id, display = "healing", rarity = 30, value = 50, equivalentspell = ppheal):
        super().__init__(id, display, rarity, value, equivalentspell)

class phaste(potion):
    def __init__(self, id, display = "haste", rarity = 5, value = 70, equivalentspell = 0):
        super().__init__(id, display, rarity, value, equivalentspell)

class pskill(potion):
    def __init__(self, id, display = "skillfulness", rarity = 3, value = 80, equivalentspell = 0):
        super().__init__(id, display, rarity, value, equivalentspell)


##Wands
class wand:
    def __init__(self, id, charges, display, rarity, value, equivalentspell, caneffect, symbol = "/", weight = 5):
        self.id = id
        self.charges = charges
        self.display = display
        self.rarity = rarity
        self.value = value
        self.equivalentspell = equivalentspell
        self.caneffect = caneffect
        self.symbol = symbol
        self.weight = weight

        self.charges = diceroll(2, round(self.value/20, 1), 2)

    def zap(self, zapper):
        if self.charges <= 0:
            print("But nothing happened")
            return
        else:
            self.charges -= 1
        if self.equivalentspell != 0:
            direction = 0
            if self.equivalentspell.shape != "nil":
                direction = determinedirection()
            spellbook.cast(self.equivalentspell, direction, "wand", zapper)
            return
        
stunmo = stunmonster(0)
class baffling(wand):
    def __init__(self, id, charges = 1, display = "baffling", rarity = 30, value = 75, equivalentspell = stunmo, caneffect = [monster]):
        super().__init__(id, charges, display, rarity, value, equivalentspell, caneffect)

insit = insight(0)
class statview(wand):
    def __init__(self, id, charges = 1, display = "insight", rarity = 10, value = 55, equivalentspell = insit, caneffect = [monster]):
        super().__init__(id, charges, display, rarity, value, equivalentspell, caneffect)

arcmis = magicmissile(0)
class wagicwissile(wand):
    def __init__(self, id, charges = 1, display = "magic missile", rarity = 15, value = 50, equivalentspell = arcmis, caneffect = [monster]):
        super().__init__(id, charges, display, rarity, value, equivalentspell, caneffect)

##Gold
class gold:
    def __init__(self, value, symbol = "$", display = "gold", weight = 0):
        self.value = value
        self.symbol = symbol
        self.display = display
        self.weight = weight

##Item Lists
armorlist = [robe, leather, studdedleather, scalemail, ringmail, fieldplate, chain, plate, cap, cone, jestercap, plume, pot, cowboyboots, slippers, greaves]
weaponlist = [hand, knuckle, nightstick, gauntlet, knife, dagger, longsword, greatsword, mace, morningstar, rapier, duelingsword, cudgel, greatclub, shillelagh]
spellbooklist = [stunmonster, slow, magicmissile, coneofcold, vampirictouch, turnundead, detectmo, detecttr, insight, teleport, cure, cure2] ##, protection]
scrolllist = [tp, map, detectm, detectt]
potionlist = [pheal, phaste, pskill]
wandlist = [baffling, statview, wagicwissile]

stuff = armorlist + weaponlist + spellbooklist + scrolllist + potionlist + wandlist


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
    def __init__(self, HP, HPMax, MP, MPMax, carry, AC, dred, XP, STR, DEX, CON, INT, WIS, CHA, clss, race, name, LVL, x, y, stuff, weapon, helm, chest, boots, statuses, display, memory, skills, training, spells, wealth, debts):
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

pc = player(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [], hand, 0, 0, 0, [], "you", [], [], [0, 0, 0, 0, 0, 0, 0], [], 0, [])

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

eligibleraces = [human, elf, halfling, gnome, dwarf]

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

wizard = clss("wizard", diceroll(3, 4, 2), diceroll(3, 4, 6), diceroll(3, 4, 4), diceroll(3, 4, 10), diceroll(2, 8, 4), diceroll(2, 8, 4), 1, 1, 6, [dagger, robe, slippers, tp, map, stunmonster, magicmissile, wagicwissile], [0, 1, 0, 0, 0, 0, 0], [1, 2, 0, 1, 0, 0, 1])
priest = clss("priest", diceroll(3, 4, 6), diceroll(3, 4, 4), diceroll(3, 4, 6), diceroll(3, 4, 6), diceroll(3, 4, 10), diceroll(3, 4, 6), 2, 0.75, 8, [mace, robe, slippers, cure, turnundead, pheal], [0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 3, 2])
rogue = clss("rogue", diceroll(3, 4, 4), diceroll(3, 4, 10), diceroll(3, 4, 6), diceroll(3, 4, 6), diceroll(2, 8, 4), diceroll(3, 4, 8), 3, 0.25, 8, [dagger, leather, cowboyboots, phaste, detectt], [1, 1, 0, 0, 0, 0, 0], [2, 3, 2, 1, 0, 0, 1])
knight = clss("knight", diceroll(3, 4, 10), diceroll(3, 4, 4), diceroll(3, 4, 10), diceroll(3, 4, 4), diceroll(3, 4, 4), diceroll(3, 4, 6), 3, 0.25, 10, [longsword, ringmail, greaves, plume], [0, 0, 0, 1, 1, 0, 1], [1, 1, 2, 3, 3, 2, 3])
bard = clss("bard", diceroll(3, 4, 4), diceroll(3, 5, 4), diceroll(3, 4, 4), diceroll(3, 5, 4), diceroll(3, 4, 4), diceroll(3, 4, 10), 3, 0.5, 8, [rapier, leather, jestercap, stunmonster, pskill, pheal], [0, 0, 1, 0, 0, 0, 0], [1, 2, 3, 2, 0, 0, 2])
redmage = clss("red mage", diceroll(3, 4, 6), diceroll(3, 4, 6), diceroll(3, 4, 6), diceroll(3, 4, 8), diceroll(3, 4, 4), diceroll(3, 4, 6), 1, 0.5, 8, [rapier, leather, cowboyboots, detectmo, cure], [0, 1, 1, 0, 0, 0, 0], [1, 2, 3, 2, 0, 0, 1])

eligibleclasses = [wizard, priest, knight, rogue, bard, redmage]
##Initialization 
global monsterlist

##Shopkeepers (ඞ)
class shopkeep(monster):
        def __init__(self, id, x, y, HP = 40, HPMax = 40, AC = 15, dred = 2, number = 2, dx = 3, bonus = 6, ai = "shopkeep", speed = 1.5, symbol = "ඞ", display = "shopkeep", rarity = 0, power = 15, alignment = "good", effects = None, peacefuls = None, chats = ["'Like you, I used to be poor. So very poor'", "'Piracy is not a victimless crime!'", "'Shoplifting is wrong m'kay?'"], protective = None, anchor = 0, shopid = 0):
            if peacefuls is None:
                peacefuls = [rogue, bard, wizard, knight, priest]
            if effects is None:
                effects = []
            if protective is None:
                protective = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

##Watchmen
class watchman(monster):
        def __init__(self, id, x, y, HP = 17, HPMax = 17, AC = 14, dred = 1, number = 1, dx = 3, bonus = 4, ai = "random", speed = 0.9, symbol = "w", display = "watchman", rarity = 0, power = 4, alignment = "evil", effects = None, peacefuls = None, chats = ["'But who watches us watchmen, man?'", "You spot a glimmer on the watchman's wrist and become transfixed watching the watchman's watch"]):
            if peacefuls is None:
                peacefuls = [priest, wizard, knight, rogue, bard]
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
        
        def special(self, target):
            if target == pc:
                if isinstance(pc.weapon, hand) == False:
                    if random.randint(1, 15) >= mod(pc.STR) + mod(pc.DEX):
                        print("The watchman's nightstick slaps your weapon from your hand!")
                        findpoint(pc.x, pc.y).items.append(pc.weapon)
                        pc.stuff.remove(pc.weapon)
                        pc.weapon = hand(0)

##Rats (r)
class smallrat(monster):
        def __init__(self, id, x, y, HP = 4, HPMax = 4,AC = 10, dred = 0, number = 1, dx = 3, bonus = 1, ai = "primitive", speed = 1, symbol = "r", display = "small rat", rarity = 10, power = 1, alignment = "evil", effects = None, peacefuls = None, chats = ["'Squeak squeak'"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

class giantrat(monster):
        def __init__(self, id, x, y, HP = 8, HPMax = 8, AC = 11, dred = 0, number = 1, dx = 6, bonus = 2, ai = "primitive", speed = 1, symbol = "r", display = "giant rat", rarity = 6, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["Now that is a rodent of unusual size"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []    
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
            
class kingrat(monster):
        def __init__(self, id, x, y, HP = 45, HPMax = 45, AC = 14, dred = 2, number = 1, dx = 6, bonus = 7, ai = "primitive", speed = 1.2, symbol = "K", display = "rat king", rarity = 0, power = 10, alignment = "evil", effects = None, peacefuls = None, chats = ["'I actually knew the fat rat in high school'", "'I don't like em putting chemicals in the water that turn my rats ogey!'"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
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
        def __init__(self, id, x, y, HP = 2, HPMax = 2, AC = 7, dred = 0, number = 1, dx = 2, bonus = 0, ai = "random", speed = 0.1, symbol = "F", display = "lichen", rarity = 6, power = 0.2, alignment = "neutral", effects = None, peacefuls = None, chats = ["It's a plant dummy, it can't talk"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

##Doglikes (d)
class coyote(monster):
        def __init__(self, id, x, y, HP = 8, HPMax = 8, AC = 12, dred = 0, number = 1, dx = 5, bonus = 1, ai = "primitive", speed = 1.25, symbol = "d", display = "coyote", rarity = 15, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'Yip yip!'"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []  
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

##bandit (b)
class badman(monster):
        def __init__(self, id, x, y, HP = 20, HPMax = 20, AC = 16, dred = 0, number = 1, dx = 6, bonus = 5, ai = "primitive", speed = 1.6, symbol = "b", display = "badman", rarity = 2, power = 11, alignment = "evil", effects = None, peacefuls = None, chats = []):
            if peacefuls is None:
                peacefuls = [rogue]
            if effects is None:
                effects = []            
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

class highwayman(monster):
        def __init__(self, id, x, y, HP = 15, HPMax = 15, AC = 14, dred = 0, number = 2, dx = 3, bonus = 3, ai = "primitive", speed = 1.4, symbol = "b", display = "highwayman", rarity = 4, power = 5, alignment = "evil", effects = None, peacefuls = None, chats = ["'I'm the highwayman!'", "'I make ends meet, just like any man'", "'I work with my hands'"]):
            if peacefuls is None:
                peacefuls = [rogue]
            if effects is None:
                effects = []            
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
        
        def special(self, target):
            if target == pc and pc.boots != 0:
                if random.randint(1, 5) >= 4:
                    print("The highwayman steals your shoes from off your feet!")
                    findpoint(self.x, self.y).items.append(pc.boots)
                    pc.stuff.remove(pc.boots)
                    pc.boots = 0

class bandit(monster):
        def __init__(self, id, x, y, HP = 7, HPMax = 7, AC = 12, dred = 0, number = 1, dx = 4, bonus = 2, ai = "primitive", speed = 1.2, symbol = "b", display = "bandit", rarity = 9, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'Why pay for things you can just steal?'"]):
            if peacefuls is None:
                peacefuls = [rogue]
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
        
##humanoids (h)
class hobbit(monster):
    def __init__(self, id, x, y, HP = 6, HPMax = 6, AC = 12, dred = 0, number = 1, dx = 3, bonus = 2, ai = "primitive", speed = 0.75, symbol = "h", display = "halfling", rarity = 7, power = 1, alignment = "evil", effects = None, peacefuls = None, chats = ["'Have you seen my ring?'", "'Did you just call me a hobbit?'", "The halfling inquires about fireworks"]):
        if peacefuls is None:
            peacefuls = [halfling, wizard, dwarf]
        if effects is None:
            effects = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

class gnelf(monster):
    def __init__(self, id, x, y, HP = 7, HPMax = 7, AC = 15, dred = 0, number = 1, dx = 2, bonus = 2, ai = "primitive", speed = 0.9, symbol = "G", display = "gnome", rarity = 11, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'I'm gnot a gnelf'", "'I'm gnot a gnoblin'", "'You've been gnomed!'"]):
        if peacefuls is None:
            peacefuls = [gnome]
        if effects is None:
            effects = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

##Undead (Z/S/V)
class zombie(monster):
        def __init__(self, id, x, y, HP = 18, HPMax = 18, AC = 11, dred = 1, number = 1, dx = 4, bonus = 3, ai = "primitive", speed = 0.5, symbol = "Z", display = "zombie", rarity = 15, power = 3, alignment = "evil", effects = None, peacefuls = None, chats = ["The zombie groans"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

class skeleton(monster):
    def __init__(self, id, x, y, HP = 15, HPMax = 15, AC = 13, dred = 1, number = 1, dx = 3, bonus = 5, ai = "primitive", speed = 0.75, symbol = "S", display = "skeleton", rarity = 8, power = 5, alignment = "evil", effects = None, peacefuls = None, chats = ["The skeleton rattles"]):
        if peacefuls is None:
            peacefuls = []
        if effects is None:
            effects = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

class flamingskeleton(monster):
    def __init__(self, id, x, y, HP = 21, HPMax = 21, AC = 14, dred = 2, number = 1, dx = 3, bonus = 5, ai = "primitive", speed = 0.6, symbol = "S", display = "flaming skeleton", rarity = 5, power = 7, alignment = "evil", effects = None, peacefuls = None, chats = ["'WHERE'S MY MOTORCYCLE?'", "'NOT THE BEES, ANYTHING BUT THE BEES'"]):
        if peacefuls is None:
            peacefuls = []
        if effects is None:
            effects = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
    
    def special(self, target):
        if target == pc:
            for it in pc.stuff:
                if isinstance(it, spellbook) or isinstance(it, scroll) or isinstance(it, armor) and it.material == "cloth":
                    if random.randint(1, 6) == 6:
                        print("Your " + it.display + " burns to cinders!")
                        pc.stuff.remove(it)

class vampire(monster):
        def __init__(self, id, x, y, HP = 25, HPMax = 25, AC = 15, dred = 1, number = 1, dx = 7, bonus = 7, ai = "primitive", speed = 1.1, symbol = "V", display = "Vampire", rarity = 2, power = 10, alignment = "evil", effects = None, peacefuls = None, chats = ["1 wasted turn! Ah ah ah!"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
        
        def special(self, target):
            if target == pc:
                if random.randint(1, 20) >= pc.CON:
                    print("You feel your strength draining away!")
                    pc.STR -= random.randint(1, 2)
                    pc.HPMax -= random.randint(2, 4)
                    if pc.STR <= 0:
                        pc.HP = 0

##goblins (g)
class goblin(monster):
    def __init__(self, id, x, y, HP = 7, HPMax = 7, AC = 11, dred = 0, number = 1, dx = 3, bonus = 3, ai = "primitive", speed = 1, symbol = "g", display = "goblin", rarity = 13, power = 2, alignment = "evil", effects = None, peacefuls = None, chats = ["'Mind goblin' deez nuts?'"]):
        if peacefuls is None:
            peacefuls = []
        if effects is None:
            effects = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)

class gremlin(monster):
    def __init__(self, id, x, y, HP = 11, HPMax = 11, AC = 12, dred = 0, number = 1, dx = 2, bonus = 6, ai = "primitive", speed = 1.25, symbol = "g", display = "gremlin", rarity = 7, power = 5, alignment = "evil", effects = None, peacefuls = None, chats = ["'Feed me after midnight'", "'Have you seen any water around here?'"]):
        if peacefuls is None:
            peacefuls = []
        if effects is None:
            effects = []
        super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
    
    def special(self, target):
        if target == pc:
            if random.randint(1, 20) >= mod(pc.DEX):
                if pc.helm != 0:
                    print("The gremlin snatches your " + pc.helm.display + "!")
                    findpoint(self.x, self.y).items.append(pc.helm)
                    pc.stuff.remove(pc.helm)
                    pc.helm = 0
                else:
                    print("The gremlin scratches at your head!")
                    pc.HP -= random.randint(2, 3)


##Rust Monster (R)
class rust(monster):
        def __init__(self, id, x, y, HP = 22, HPMax = 22, AC = 14, dred = 2, number = 1, dx = 2, bonus = 4, ai = "primitive", speed = 1.1, symbol = "R", display = "rust monster", rarity = 5, power = 7, alignment = "evil", effects = None, peacefuls = None, chats = ["A rust monster, programmed in python. Ironic"]):
            if peacefuls is None:
                peacefuls = []
            if effects is None:
                effects = []
            super().__init__(id, x, y, HP, HPMax, AC, dred, number, dx, bonus, ai, speed, symbol, display, rarity, power, alignment, effects, peacefuls, chats)
        def special(self, target):
            if target == pc:
                piece = random.randint(1,3)-1
                listicle = [pc.helm, pc.chest, pc.boots]
                armored = listicle[piece]
                if isinstance(armored, armor):
                    if armored.material == "metal":
                        print("Your " + armored.display + " looks rusted!")
                        armored.ACbase -= 1
                        if armored.dred >= 1:
                            armored.dred -= 1
                        if armored.ACbase <= 0:
                            print("Your " + armored.display + " rusts away completely!")
                            [pc.helm, pc.chest, pc.boots][piece] == 0
                            pc.stuff.remove(armored)


monsterlist = [shopkeep, smallrat, giantrat, kingrat, lichen, coyote, bandit, highwayman, zombie, skeleton, rust, vampire, hobbit, gnelf, goblin, gremlin, flamingskeleton]


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

    loop = 1
    while loop <= 4:
        specificmonsters(loop, [40, 40, 10, 10], [[gnelf, gremlin], [hobbit], [bandit, highwayman], [smallrat, giantrat, giantrat]], random.randint(2, 4))

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
            if len(findpoint(loopx, loopy).display) > 1:
                findpoint(loopx, loopy).display = "}"
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
    global purchasable
    global shopkeeps
    monsters.clear
    createpoints()
    if type == "standard":
        standardfloor(6, 4, 8)
        doordash(6, 0)
        distributeloot(100+(floor-1)*30, [30, 25, 5, 2, 10, 10])
        distributemonsters(5+(floor-1)*2 + (3*pc.LVL), round(floor/3, 1), 3+round(floor-1, 1))
    if type == "bigroom":
        thebigroom()
    if type == "adelaide":
        adelaide()
    if type == "rrat":
        ratkingslair()
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
        if isinstance(item, spellbook) == True:
            message = "You see here a spellbook of " + item.display
            break
        if isinstance(item, scroll):
            message = "You see here a scroll of " + item.display
            break
        if isinstance(item, potion):
            message = "You see here a potion of " + item.display
            break
        if isinstance(item, wand):
            message = "You see here a wand of " + item.display
            break
        if isinstance(item, gold):
            message = "You see here " + item.display
            break
        if item.display[len(item.display)-1] != "s":
            message = "You see here a " + item.display
            break
        else:
            message = "You see here some " + item.display
            break
    for mo in monsters:
        if isinstance(mo, shopkeep) and item in mo.protective:
            message += " ($" + str(int((item.value*1.15)/(1+(0.05*mod(pc.CHA))))) + ")"
    print(message)


##Monster Functions
def mintmonster(type, x, y):
    x = type(0, x, y)
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
        targetblock.monster = mintmonster(raritybuilder[random.randint(1, len(raritybuilder))-1], targetblock.x, targetblock.y)
        monstereligible.remove(targetblock)
        loop -= monsters[len(monsters)-1].power

def soundthealarm(crook):
    print("You hear the alarm blare!")
    for mo in monsters:
        if isinstance(mo, watchman):
            mo.ai = "primitive"
            mo.peacefuls.remove(pc.clss)

def specificmonsters(id, distribution, monstahs, number):
    eligiblespawn = []
    for po in points:
        if po.isroom == id:
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


##General Functions
def determinedirection():
    clarification = input("In what direction? ")
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
        print("Choose a movement direction! (h, j, k, l)")

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
    print("Level:", pc.LVL, "AC:", pc.AC, "XP:", pc.XP, "DLVL:", DLVL, "Turn:", turn-100, "$: " + str(pc.wealth))

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
                pc.spells.append([pc.stuff[len(pc.stuff)-1], 2500])
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
            print("You feel yourself begin to slow down")

def vision(origin, sight):
    invision = triangle(origin, 1, "up", sight) + triangle(origin, 1, "right", sight) + triangle(origin, 1, "down", sight) + triangle(origin, 1, "left", sight)
    return invision

def inventorycheck(useitem, action, types):
    global pc
    weaponsi = []
    armorsi = []
    spellbooksi = []
    scrollsi = []
    potionsi = []
    wandsi = []
    print("----------------Inventory----------------")
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
    print("| Weapons:                              |")    
    counter = 1
    for x in weaponsi:
        if x is pc.weapon:
            print("|",counter,":",x.display, " "*(23-len(x.display)-len(str(counter))), "-equipped |")
        else:
            print("|",counter,":",x.display, " "*(33-len(x.display)-len(str(counter))),"|")
        counter += 1
    print("| Armors:                               |")    
    for x in armorsi:
        if x is pc.chest or x is pc.helm or x is pc.boots:
            print("|",counter,":",x.display, " "*(23-len(x.display)-len(str(counter))), "-equipped |")
        else:
            print("|",counter,":",x.display, " "*(33-len(x.display)-len(str(counter))),"|")
        counter += 1
    print("| Spellbooks:                           |")    
    for x in spellbooksi:
        print("|",counter,": spellbook of",x.display, " "*(20-len(x.display)-len(str(counter))),"|")
        counter += 1
    print("| Scrolls:                              |")    
    for x in scrollsi:
        print("|",counter,": scroll of",x.display, " "*(23-len(x.display)-len(str(counter))),"|")
        counter += 1
    print("| Potions:                              |")    
    for x in potionsi:
        print("|",counter,": potion of",x.display, " "*(23-len(x.display)-len(str(counter))),"|")
        counter += 1
    print("| Wands:                                |")    
    for x in wandsi:
        print("|",counter,": wand of",x.display, " "*(25-len(x.display)-len(str(counter))),"|")
        counter += 1

    print("-----------------------------------------")
    pc.stuff = weaponsi + armorsi + spellbooksi + scrollsi + potionsi + wandsi

    if useitem != 0:
        try:
            clarification = int(input(action + " which item? "))
            clarification += 0
        except ValueError:
            print("Pick a number please!")
        else:
            if 1 <= clarification < counter:
                if type(pc.stuff[clarification -1]) in types:
                    return pc.stuff[clarification - 1]
                else:
                    print("That is a silly thing to", action,"!")
                    return
            else:
                print("Please pick a number within the shown range!")
                return


##Primary Loop
createpc()
##initializemonsters()
cutscene(0)
DLVL = 1
turn = 100
checkup()
intitialize(DLVL, "standard")

truecommands = ["h", "j", "k", "l", ">", ",", ".", "Z"]
freecommands = ["d", "i", "w", "W", "S", "C", "r", "R", "q", "z", "p"]
while 1 == 1:
    for pos in vision(pc, 6):
        if pos not in pc.memory:
            pc.memory.append(pos)
    display()
    viablecommands = [".", "r", "S", "C"]
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
        if findpoint(pc.x, pc.y).items != []:
            call(findpoint(pc.x, pc.y).items[len(findpoint(pc.x, pc.y).items)-1])
        command = input("Do what? ")
        if command in truecommands and command in viablecommands:
            findpoint(pc.x, pc.y).monster = 0
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
            if command == ">":
                DLVL += 1
                intitialize(DLVL, "standard")
                if DLVL == 6:
                    intitialize(DLVL, "adelaide")
                if DLVL == 9:
                    intitialize(DLVL, "rrat")
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
                                if isinstance(findpoint(pc.x, pc.y).items[clarification-1], gold):
                                    pc.wealth += findpoint(pc.x, pc.y).items[clarification-1].value
                                else:
                                    pc.stuff.append(findpoint(pc.x, pc.y).items[clarification-1])
                                    if findpoint(pc.x, pc.y).items[clarification-1] in purchasable:
                                        pc.debts.append(findpoint(pc.x, pc.y).items[clarification-1])
                                findpoint(pc.x, pc.y).items.remove(findpoint(pc.x, pc.y).items[clarification-1])
                                break
                            else:
                                    print("Please type a number within the acceptable range")
            if command == "Z":
                counter = 1
                for x in pc.spells:
                    print(counter,":", x[0].display, " "*(15-len(x[0].display)) + "LVL:", x[0].level," "*(5-len(str(x[1]))) + "Recollection:" , x[1])
                    counter += 1
                try:
                    choice = int(input("Cast which spell (number)? "))
                    choice += 0
                except ValueError:
                    print("Type a number please!")
                else:
                    if 1 <= choice <= counter:
                        if pc.spells[choice-1][0].shape == "nil":
                            spellbook.cast(pc.spells[choice-1][0], 0, pc, tpoint)
                        else:
                            dir = determinedirection()
                            if dir != None:
                                spellbook.cast(pc.spells[choice-1][0], dir, pc, tpoint)
                    else:
                        if choice != "c":
                            print("Select a number within the shown range!")
                        else:
                            break

            findpoint(pc.x, pc.y).monster = pc
            break

        if command in viablecommands and command in freecommands:

            if command == "p":
                for it in pc.debts:
                    cost = int((it.value*1.15)/(1 + 0.05*mod(pc.CHA)))
                    print("wallet-", pc.wealth)
                    print(it.display,"-", cost)
                    while True:
                        checkout = input("Buy this item? (y/n) ")
                        if checkout not in ["y", "n"]:
                            print("Please answer y or n!")
                        else:
                            if checkout == "y":
                                if pc.wealth >= cost:
                                    pc.wealth -= cost
                                    pc.debts.remove(it)
                                    purchasable.remove(it)
                                    for shit in shopkeeps:
                                        if it in shit.protective:
                                            shit.protective.remove(it)
                                    print("Thank you for your purchase!")
                                else:
                                    print("You are too broke to buy this item!")
                            break

            if command == "R":
                sus = inventorycheck(1, "Remove", armorlist)
                if sus != None:
                    print("You remove your", sus.display)
                    if  sus == pc.helm:
                        pc.helm = 0
                    if  sus == pc.chest:
                        pc.chest = 0
                    if  sus == pc.boots:
                        pc.boots = 0
                    break

            if command == "r":
                sus = inventorycheck(1, "read", spellbooklist + scrolllist)
                if sus != None:
                    if isinstance(sus, spellbook):
                        flag = 0
                        for x in pc.spells:
                            if x[0] == sus:
                                flag = 1
                        
                        if flag == 0:
                            spellbook.read(sus, pc)
                        else:
                            print("You already know", sus.display,"!")
                    else:
                        scroll.read(sus, pc)
                    break

            if command == "d":
                dropped = inventorycheck(1, "drop", stuff)
                if dropped != None:
                    print("You drop your", dropped.display)
                    pc.stuff.remove(dropped)
                    findpoint(pc.x, pc.y).items.append(dropped)
                    for sho in shopkeeps:
                        if findpoint(pc.x, pc.y).isroom == sho.shopid and len(checkadj(findpoint(pc.x, pc.y), "door", 0)) == 0:
                            if dropped in pc.debts and dropped in sho.protective:
                                pc.debts.remove(dropped)
                            else:
                                while True:
                                    yeeep = input("Sell your " + dropped.display + " for " + str(int(0.75*dropped.value/(1-mod(pc.CHA)*0.05))) + "? (y/n) ")
                                    if yeeep in ["y", "n"]:
                                        if yeeep == "y":
                                            sho.protective.append(dropped)
                                            pc.wealth += int(0.8*dropped.value/(1-mod(pc.CHA)*0.05))
                                        break
                                    else:
                                        print("please reply y or n!")
                    break

            if command == "q":
                drinkup = inventorycheck(1, "quaff", potionlist)
                if drinkup != None:
                    potion.drink(drinkup, pc)
                    pc.stuff.remove(drinkup)
                    break

            if command == "z":
                zaperino = inventorycheck(1, "zap", wandlist)
                if zaperino != None:
                    wand.zap(zaperino, pc)
                    break

            if command == "C":
                sus = determinedirection()
                impasta = findpoint(pc.x + sus[0], pc.y + sus[1])
                if impasta.monster != 0:
                    monster.chat(impasta.monster)
                    break
                else:
                    print("You are overwhelmed by lonliness realizing there is no one to talk to")
            if command == "i":
                inventorycheck(0, 0, 0)
            
            if command == "S":
                print("-------------Skills-------------")
                counter = 0
                for skil in weaponskills:
                    print("|",skil, " "*(21-len(skil)), pc.skills[counter],"/",pc.clss.maxskills[counter],"|")
                    counter += 1
                print("--------------------------------")
            
            if command == "w":
                decision = inventorycheck(1, "wield", weaponlist)
                if decision != None:
                    pc.weapon = decision
                    print("You are now wielding your", decision.display)
                    break

            if command == "W":
                choice = inventorycheck(1, "Equip", armorlist)
                if choice != None:
                    print("You are now wearing your", choice.display)
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
            print("Invalid command")
    checkup()
    turnup()
    if pc.HP <= 0:
        print("RIP", pc.name, "the", pc.clss.display)
        print("So long space cowboy...")
        break
##Thanks for playing