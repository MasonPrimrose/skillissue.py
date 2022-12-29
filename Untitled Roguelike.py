import random

def diceroll(number, dx, bonus):
    total = bonus
    loop = number
    while loop > 0:
        total += random.randint(1,dx)
        loop -= 1
    return total

##classes for objects
class weapon:
    def __init__(self, id, weight, number, dx, ability, attributes, value, rarity, display, symbol = ")"):
        self.id = id
        self.weight = weight
        self.number = number
        self.dx = dx
        self.ability = ability
        self.attributes = attributes
        self.value = value
        self.rarity = rarity
        self.display = display
        self.symbol = symbol
    
    def attack(self):
        bonus = 0
        for x in self.attributes:
            if x is int:
                bonus += x
        if self.ability == "DEX":
            atkbonus = mod(pc.DEX)
        else:
            atkbonus = mod(pc.STR)
        return [diceroll(1, 20, 1)+round(pc.LVL/4) +atkbonus+bonus, diceroll(self.number, self.dx) + bonus]
    
    def call(self):
        print("You see here a ", self.display)

weapons = []
armors = []

class dagger(weapon):
    def __init__(self, id, weight = 1, number = 1, dx = 4, ability = "DEX", attributes = [], value = 5, rarity = 50, display = "dagger", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, symbol)

class longsword(weapon):
    def __init__(self, id, weight = 10, number = 1, dx = 10, ability = "STR", attributes = [], value = 50, rarity = 5, display = "longsword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, symbol)

class greatsword(weapon):
    def __init__(self, id, weight = 20, number = 2, dx = 6, ability = "STR", attributes = [], value = 100, rarity = 2, display = "greatsword", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, symbol)

class mace(weapon):
    def __init__(self, id, weight = 8, number = 1, dx = 6, ability = "STR", attributes = [], value = 10, rarity = 10, display = "mace", symbol = ")"):
        super().__init__(id, weight, number, dx, ability, attributes, value, rarity, display, symbol)


class armor:
    def __init__(self, id, weight, ACbase, MaxDex, dred, attributes, value, rarity, display, symbol):
        self.id = id
        self.weight = weight
        self.ACbase = ACbase
        self.MaxDex = MaxDex
        self.dred = dred
        self.attributes = attributes
        self.value = value
        self.rarity = rarity
        self.display = display
        self.symbol = symbol

class robe(armor):
    def __init__(self, id, weight = 2, ACbase = 1, MaxDex = 10, dred = 0, attributes = [], value = 5, rarity = 15, display = "robe", symbol = "]"):
        super().__init__(id, weight, ACbase, MaxDex, dred, attributes, value, rarity, display, symbol)

class leather(armor):
    def __init__(self, id, weight = 10, ACbase = 2, MaxDex = 8, dred = 0, attributes = [], value = 15, rarity = 20, display = "leather armor", symbol = "]"):
        super().__init__(id, weight, ACbase, MaxDex, dred, attributes, value, rarity, display, symbol)

class chain(armor):
    def __init__(self, id, weight = 50, ACbase = 6, MaxDex = 1, dred = 2, attributes = [], value = 70, rarity = 10, display = "chainmail", symbol = "]"):
        super().__init__(id, weight, ACbase, MaxDex, dred, attributes, value, rarity, display, symbol)


armorlist = [robe, leather, chain]
weaponlist = [dagger, longsword, greatsword, mace]

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
    def __init__(self, HP, HPMax, MP, MPMax, AC, STR, DEX, CON, INT, WIS, CHA, clss, race, name, LVL, xpos, ypos, stuff, weapon, helm, chest, boots):
        self.HP = HP
        self.HPMax = HPMax
        self.MP = MP
        self.MPMax = MPMax
        self.AC = AC
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
        self.xpos = xpos
        self.ypos = ypos
        self.stuff = stuff
        self.weapon = weapon
        self.helm = helm
        self.chest = chest
        self.boots = boots

pc = player(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [], 0, 0, 0, 0)

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
dwarf = race("dwarf", +2, -2, +2, 0, 0, 0)

class clss:
    def __init__(self, display, STR, DEX, CON, INT, WIS, CHA, spell, baseHP, startinventory):
        self.display = display
        self.STR = STR
        self.DEX = DEX
        self.CON = CON
        self.INT = INT
        self.WIS = WIS
        self.CHA = CHA
        self.spell = spell
        self.baseHP = baseHP
        self.startinventory = startinventory

wizard = clss("wizard", diceroll(2, 6, 4), diceroll(2, 6, 6), diceroll(2, 6, 4), diceroll(2, 6, 10), diceroll(2, 8, 4), diceroll(2, 8, 4), 1, 6, [dagger])
priest = clss("priest", diceroll(2, 8, 4), diceroll(2, 8, 4), diceroll(2, 6, 6), diceroll(2, 6, 6), diceroll(2, 8, 8), diceroll(2, 6, 6), 2, 8, [mace, robe])
rogue = clss("rogue", diceroll(2, 6, 4), diceroll(2, 6, 10), diceroll(2, 6, 6), diceroll(2, 6, 6), diceroll(2, 8, 4), diceroll(2, 6, 8), 3, 8, [dagger, leather])
knight = clss("knight", diceroll(2, 6, 10), diceroll(2, 6, 4), diceroll(2, 6, 10), diceroll(2, 6, 4), diceroll(2, 6, 4), diceroll(2, 6, 6), 2, 10, [longsword])

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
    tpoint = points[70*(y-1)+x-1]
    return tpoint

def createrooms(roomnumber, mindimension, maxdimension):
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
                if findpoint(loopx, loopy).monster == "pc":
                    findpoint(loopx, loopy).display = "@"
                else:
                    findpoint(loopx, loopy).display = findpoint(loopx, loopy).monster.symbol
            loopy -= 1
        loopx -= 1

def printmap():
    checkmap()
    yprinter = ""
    loopy = 20
    while loopy > 0:
        loopx = 1
        while loopx <= 70:
            yprinter += findpoint(loopx, loopy).display
            loopx += 1
        loopy -=1
        print(yprinter)
        yprinter = ""

def intitialize(floor):
    createpoints()
    createrooms(6, 4, 8)
    doordash(6, 0)
    distributeloot(60+(floor-1)*20, [0.6, 0.4])
    loopx = 70
    while loopx > 0:
        loopy = 20
        while loopy > 0:
            if findpoint(loopx, loopy).type == "stairup":
                pc.xpos = loopx
                pc.ypos = loopy
                findpoint(loopx, loopy).monster = "pc"
            loopy -= 1
        loopx -= 1


##Item/loot functions
def mintitem(item):
    if isinstance(item, weapon):
        thelist = weapons
    if isinstance(item, armor):
        thelist = armors
    thelist.append(item)
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

def mod(input):
    return round((input-10)/2, 1)

def healthbar(current, max, blocks):
    bar = "["
    percent = round(current/max, 0.01)*100
    blockmaker = round(percent/(100/blocks),1)
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
    print(pc.name, "the", pc.clss.display)
    print(pc.HP, "/", pc.HPMax, healthbar(pc.HP, pc.HPMax, 20))

    printmap()

    print("STR: ", pc.STR, "DEX: ", pc.DEX, "CON: ", pc.CON, "INT: ", pc.INT, "WIS: ", pc.WIS, "CHA: ", pc.CHA)
    print("Level:", pc.LVL, "AC:", pc.AC)


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
        eligibleraces = [human, elf, halfling, dwarf]
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
        pc.HPMax = mod(pc.CON) + pc.clss.baseHP
        pc.HP = pc.HPMax
        for x in pc.clss.startinventory:
            pc.stuff.append(mintitem(x(0)))
            if isinstance(pc.stuff[len(pc.stuff)-1], weapon):
                pc.weapon = pc.stuff[len(pc.stuff)-1]
            if isinstance(pc.stuff[len(pc.stuff)-1], armor):
                pc.chest = pc.stuff[len(pc.stuff)-1]
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

def checkup():
    DEXbonus = mod(pc.DEX)
    pc.AC = 10
    ACsources = [pc.boots, pc.chest, pc.helm]
    for x in ACsources:
        if x != 0:
            pc.AC += x.ACbase
            if x == pc.chest and DEXbonus >= x.MaxDex:
                DEXbonus = x.MaxDex
    pc.AC +=  DEXbonus



##Primary Loop
createpc()
DLVL = 1
intitialize(DLVL)

truecommands = ["h", "j", "k", "l", ">", ","]
freecommands = ["i"]
while 1 == 1:
    checkup()
    display()
    viablecommands = []
    if findpoint(pc.xpos-1, pc.ypos).type not in nomove:
        viablecommands.append("h")
    if findpoint(pc.xpos, pc.ypos-1).type not in nomove:
        viablecommands.append("j")
    if findpoint(pc.xpos, pc.ypos+1).type not in nomove:
        viablecommands.append("k")
    if findpoint(pc.xpos+1, pc.ypos).type not in nomove:
        viablecommands.append("l")
    if findpoint(pc.xpos, pc.ypos).type == "stairdown":
        viablecommands.append(">")
    if findpoint(pc.xpos, pc.ypos).items != []:
        viablecommands.append(",")
    if pc.stuff != []:
        viablecommands.append("i")
    while 1 == 1:
        if findpoint(pc.xpos, pc.ypos).items != []:
            weapon.call(findpoint(pc.xpos, pc.ypos).items[len(findpoint(pc.xpos, pc.ypos).items)-1])
        command = input("Do what? ")
        if command in truecommands and command in viablecommands:
            findpoint(pc.xpos, pc.ypos).monster = 0
            if command == "h":
                pc.xpos -= 1
            if command == "j":
                pc.ypos -= 1
            if command == "k":
                pc.ypos += 1
            if command == "l":
                pc.xpos += 1
            if command == ">":
                intitialize(DLVL+1)
            if command == ",":
                if len(findpoint(pc.xpos, pc.ypos).items) == 1:
                    pc.stuff.append(findpoint(pc.xpos, pc.ypos).items[0])
                    findpoint(pc.xpos, pc.ypos).items.remove(findpoint(pc.xpos, pc.ypos).items[0])
                else:
                    loop = 0
                    while loop < len(findpoint(pc.xpos, pc.ypos).items):
                        print(loop + 1, ":", findpoint(pc.xpos, pc.ypos).items[loop].display)
                        loop += 1
                    while 1 == 1:
                        try:
                            clarification = int(input("Take which (number): "))
                            clarification += 0
                        except ValueError:
                            print("Type a number please!")
                        else:
                            if 0 < clarification <= len(findpoint(pc.xpos, pc.ypos).items):
                                    pc.stuff.append(findpoint(pc.xpos, pc.ypos).items[clarification-1])
                                    findpoint(pc.xpos, pc.ypos).items.remove(findpoint(pc.xpos, pc.ypos).items[clarification-1])
                                    break
                            else:
                                    print("Please type a number within the acceptable range")
            findpoint(pc.xpos, pc.ypos).monster = "pc"
            break
        if command in viablecommands and command in freecommands:
            if command == "i":
                print("~~Inventory~~")
                for x in pc.stuff:
                    if x is pc.chest or x is pc.weapon or x is pc.helm or x is pc.boots:
                        print("A", x.display, "-equipped")
                    else:
                        print("A", x.display)

        else:
            print("Invalid command")