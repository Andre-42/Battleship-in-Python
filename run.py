import numpy as np
from pprint import pprint

SHIP_SIZES = [5, 4, 3, 3, 2]
GAME_STATUS = True
BATTLEFIELD_SIZE = (8, 8)
BATTLEFIELD_SIZE_S = (6, 6)
BATTLEFIELD_SIZE_L = (12, 12)
BATTLEFIELD_PLAYER = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
BATTLEFIELD_PC = BATTLEFIELD_PLAYER

battlevector = BATTLEFIELD_PC[1, :]
startpos = 3
ship = SHIP_SIZES[1]


def set_ship_inline(boardvector, startpos, shiplength):
    """
    This function defines the ship position within a column or row.
    numbreaks enables the identification of unique fields within the vector
    """
    numbreaks = np.cumsum(boardvector == True)
    fields, fieldstart, fieldindex, fieldcounts = np.unique(numbreaks, return_index = True, return_inverse = True, return_counts = True)
    #print(f"{fields},sid{fieldstart},{fieldindex},{fieldcounts}")
    if (sum(fields > 0) > 0):
        fieldcounts[fields > 0] = fieldcounts[fields > 0] - 1
        fieldindex[fieldstart[fields > 0]] = -1
    fieldvalid = fieldcounts >= shiplength
    #print(f"{fields},sid{fieldstart},{fieldindex},{fieldcounts},{fieldvalid}")
    if (sum(fieldvalid) > 0):
        fieldwish = fieldindex[startpos]
        getwish = sum(fieldwish == fields[fieldvalid]) > 0
        #print(f"getwish: {getwish},  {fieldindex}")
        if getwish:
            u, poslast = np.unique(np.flip(fieldindex) == fieldwish, 
                return_index=True)
            poslast = len(fieldindex) - poslast - 1
            u, posfirst = np.unique(fieldindex == fieldwish, 
                return_index=True)
            #print(f"{startpos} + {shiplength} -1, {poslast}")
            #posend = [startpos + shiplength - 1]
            #posend.extend(poslast)
            #posend = min(posend)
            #print(posend)
            #posstart = posend - shiplength
        else:
            fieldwish = fields[fieldvalid]
            fieldlen = fieldcounts[fieldvalid]
            fieldwish = fieldwish[fieldlen == max(fieldlen)]
            if len(fieldwish) > 1:
                fieldwish = fieldwish[np.random.randint(len(fieldwish)-1)]
            
            u, poslast = np.unique(np.flip(fieldindex) == fieldwish, 
                return_index=True)
            poslast = len(fieldindex) - poslast - 1
            u, posfirst = np.unique(fieldindex == fieldwish, 
                return_index=True)
        posend = [startpos + shiplength - 1]
        posend.extend(poslast)
        posend = min(posend)
        posfirst = min(posfirst)
        #print(posend)
        posstart = int(posend - shiplength)
        if posstart < 0:
            posstart = int(posfirst)
            posend = (posstart + shiplength)
        print(f"ship: {shiplength}, wish:{fieldwish} , idx: {fieldindex}")
        print(f"start {int(posstart)}, end {int(posend)}")
        for i in range(int(posstart), int(posend)):
            boardvector[i] = True
    return boardvector


def set_ship_random(battlefield, ship):
    """
    This function defines the column or row for a new ship position
    """
    pos_x = np.random.randint(BATTLEFIELD_SIZE[1]-1)
    pos_y = np.random.randint(BATTLEFIELD_SIZE[0]-1)
    row_xy = battlefield[pos_y, :]
    col_xy = battlefield[:, pos_x]
    roworcol = np.random.randint(2)
    if roworcol == 1:
        boardvector = set_ship_inline(row_xy, pos_x, ship)
        if (boardvector != row_xy).all():
            battlefield[pos_y, :] = boardvector
    else:
        boardvector = set_ship_inline(col_xy, pos_y, ship)
        if (boardvector != col_xy).all():
            battlefield[:, pos_x] = boardvector
    return battlefield


def create_battlefield(battlefield):
    for ship in SHIP_SIZES:
        #print(ship)
        tryagain = True
        it = 1
        while tryagain:
            sb = sum(sum(battlefield))
            battlefieldNew = set_ship_random(battlefield, ship)
            sb2 = sum(sum(battlefieldNew))
            isset = (sb2-sb) == ship
            if isset:
                battlefield = battlefieldNew
                tryagain = False
                break
            tryagain = tryagain or it < 100
            #print(f"{sb} and {sb2}, {isset}")
            it += 1

    print(battlefield)
    return battlefield


def startGame():
    # create battlefield for player
    BATTLEFIELD_PLAYER = create_battlefield(BATTLEFIELD_PLAYER)
    # create battlefield for player
    BATTLEFIELD_PC = create_battlefield(BATTLEFIELD_PC)


def endGame()
    break


def playGame()
    """
    user Input for player.
    """
    field = input("Type in your target coordinate:")
    return field


def main()
    """ 
    main game function
    """
    startGame()
    print("Welcome to a game of battleship.")
    print("Your fleet is deployed and ready to hunt.")

    gameon = True
    while gameon:
        command = playGame()

        gameon = False

    
