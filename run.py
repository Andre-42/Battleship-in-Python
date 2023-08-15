import numpy as np
from pprint import pprint

SHIP_SIZES = [5, 4, 3, 3, 2]
GAME_STATUS = True
BATTLEFIELD_SIZE = (8, 8)
BATTLEFIELD_SIZE_S = (6, 6)
BATTLEFIELD_SIZE_L = (12, 12)
BATTLEFIELD_PLAYER = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
BATTLEFIELD_PC = BATTLEFIELD_PLAYER

max_letter = BATTLEFIELD_PLAYER.shape[1]
col_names = list(map(chr, range(97, max_letter+97)))
max_number = BATTLEFIELD_PLAYER.shape[0]


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
        if (posstart < 0) or (fieldindex[posstart] < 0):
            posstart = int(posfirst)
            posend = (posstart + shiplength)
        print(f"ship: {shiplength}, wish:{fieldwish} , idx: {fieldindex}")
        print(f"start {int(posstart)}, end {int(posend)}")
        for i in range(int(posstart), int(posend)):
            boardvector[i] = True
    return boardvector


def set_ship_random(set_battlefield, ship):
    """
    This function defines the column or row for a new ship position
    """
    pos_x = np.random.randint(BATTLEFIELD_SIZE[1]-1)
    pos_y = np.random.randint(BATTLEFIELD_SIZE[0]-1)
    row_xy = set_battlefield[pos_y, :]
    col_xy = set_battlefield[:, pos_x]
    roworcol = np.random.randint(2)
    if roworcol == 1:
        boardvector = set_ship_inline(row_xy, pos_x, ship)
        if (boardvector != row_xy).all():
            set_battlefield[pos_y, :] = boardvector
    else:
        boardvector = set_ship_inline(col_xy, pos_y, ship)
        if (boardvector != col_xy).all():
            set_battlefield[:, pos_x] = boardvector
    return set_battlefield


def create_battlefield(battlefield):
    redo = True
    while redo:
        for idship in range(len(SHIP_SIZES)):
            # print(ship)
            ship = SHIP_SIZES[idship]
            maxSum = np.cumsum(SHIP_SIZES)
            maxSum = maxSum[idship]
            tryagain = True
            it = 1
            while tryagain:
                sb = sum(sum(battlefield))
                battlefield_new = set_ship_random(battlefield, ship)
                sb2 = sum(sum(battlefield_new))
                isset = ((sb2-sb) == ship) and (sb2 == maxSum)
                print(f"ship {ship} is deployed: {isset}")
                if isset:
                    battlefield = battlefield_new
                    tryagain = False
                else:
                    tryagain = tryagain and it < 100 and maxSum < sb
                # print(f"{sb} and {sb2}, {isset}")
                it += 1
                print(it)
            redo = not (isset)
            if redo:
                battlefield = np.zeros(BATTLEFIELD_SIZE, dtype=bool)

    print(battlefield)
    return battlefield


def create_scoreboards(max_letter, col_names, max_number):
    n_el = max_letter * max_number
    not_hit = [None] * n_el
    field_index = [None] * n_el
    field_x = [None] * n_el
    field_y = [None] * n_el
    it_list = 0
    for j in range(max_letter):
        for i in range(max_number):
            # print(it_list)
            not_hit[it_list] = col_names[j] + str(i+1)
            field_index[it_list] = it_list
            field_x[it_list] = j
            field_y[it_list] = i
            it_list += 1
    return not_hit, field_index, field_x, field_y


def start_game():
    player = BATTLEFIELD_PLAYER
    pc = BATTLEFIELD_PC
    # create battlefield for player
    player = create_battlefield(player)
    # create battlefield for player
    pc = create_battlefield(pc)
    print("This is your fleet:")
    print(pc)

    max_letter = BATTLEFIELD_PLAYER.shape[1]
    col_names = list(map(chr, range(97, max_letter+97)))
    max_number = BATTLEFIELD_PLAYER.shape[0]

    created_scoreboard = create_scoreboards(max_letter, col_names, max_number)
    not_hit_player = created_scoreboard[0]
    not_hit_pc = not_hit_player
    hitlist_player = []
    hitlist_pc = []
    print(not_hit_pc)
    return player, pc
            

def endGame():
    print("stop game")


def play_game():
    """
    user Input for player.
    """
    print("Targets should be provided as:")
    print(f" -letters for columns, {col_names[0]}...{col_names[max_letter-1]}")
    print(f" -numbers for rows, max({max_number})")
    print(" -example: a3, d8 or f1")
    field = input("Type in your target coordinate:")
    return field


def check_command(command):
    print("check command syntax")
    # try
    #    col_command = 


def main():
    """ 
    main game function
    """
    maps = start_game()
    BATTLEFIELD_PLAYER = maps[0]
    BATTLEFIELD_PC = maps[1]
    print("Welcome to a game of battleship.")
    print("Your fleet is deployed and ready to hunt.")
    print("This is your fleet:")
    print(BATTLEFIELD_PLAYER)
    gameon = True
    while gameon:
        command = play_game()

        gameon = False

main()
