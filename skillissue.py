import random

class point:
    def __init__(self, x, y, type, symbol, isroom):
        self.x = x
        self.y = y
        self.type = type
        self.symbol = symbol
        self.isroom = isroom

def createpoints():
    global points
    points = []
    loopy = 1
    while loopy <= 20:
        loopx = 1
        while loopx <= 70:
            points.append(point(loopx, loopy, "infill", "_", 0))
            loopx += 1
        loopy += 1

def findpoint(x,y):
    tpoint = points[70*(y-1)+x-1]
    return tpoint

def createrooms(roomnumber, mindimension, maxdimension):
    looprooms = roomnumber
    while looprooms > 0:
        roomstart = findpoint(random.randint(2,69-maxdimension), random.randint(2,19-maxdimension))
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
            looprooms -= 1
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
    spoint = checkadj(cringe, "infill", 0)[0]
    spoint.type = "hall"
    spoint.symbol = "#"
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
        chain.append(troom)                                              ##Temporary
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
        print(sussy)
        cringe = dooreligible[random.randint(1, len(dooreligible))-1]
        cringe.type = "door"
        cringe.symbol = "+"
        ##connect troom to random room on the chain

        macroloop -= 1




def printmap():
    yprinter = ""
    loopy = 20
    while loopy > 0:
        loopx = 1
        while loopx <= 70:
            yprinter += findpoint(loopx, loopy).symbol
            loopx += 1
        loopy -=1
        print(yprinter)
        yprinter = ""

createpoints()
createrooms(5, 5, 10)
findpoint(70,20).symbol = "C"
findpoint(1,20).symbol = "C"
findpoint(70,1).symbol = "C"
findpoint(1,1).symbol = "C"
doordash(5, 0)
printmap()