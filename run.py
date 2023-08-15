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


created_scoreboard = create_scoreboards(max_letter, col_names, max_number)
not_hit_player = created_scoreboard[0]
not_hit_pc = not_hit_player
hitlist_player = []
hitlist_pc = []
score_player = 0
score_pc = 0


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
    return player, pc, not_hit_player, not_hit_pc, created_scoreboard
            

def endGame(command_stop):
    is_valid = np.isin(command_stop, ["stop", "s"])
    return is_valid


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


def did_i_hit_something(target, player_id):
    valid_input = created_scoreboard[0]
    is_position = np.isin(valid_input, target)
    is_position = np.concatenate(np.nonzero(is_position))
    print((int(is_position)))
    get_field_index = created_scoreboard[1]
    get_field_index = get_field_index[is_position[0]]
    get_x = created_scoreboard[2][get_field_index]
    get_y = created_scoreboard[3][get_field_index]
    if player_id == 1:
        is_hit = BATTLEFIELD_PC[get_y, get_x]
    else:
        is_hit = BATTLEFIELD_PLAYER[get_y, get_x]
    print(f"Hit comfirmed: {is_hit}")
    return is_hit
        

def check_command(command):
    print("check command syntax")
    # try:
    valid_input = created_scoreboard[0]
    print(f"test input: {command},{type(command)} is part of ref{type(valid_input)}")
    is_valid = np.isin(command, valid_input)
    if is_valid == 0:
        is_valid = np.isin(command, ["stop", "s"])
        if is_valid:
            print("Retreat command received.")
            print("Game will be closed")
        else:
            print("Your target coordinates are not correct. TRY again")
            
    else:
        not_hit_yet = not_hit_pc
        is_valid = np.isin(command, not_hit_yet)
        if is_valid == 0:
            print("You hit that place already.")
            isvalid = False
            was_hit = did_i_hit_something(command, 1)
            if was_hit:
                print(f"It was a direct hit at {command}")
            else:
                print("We missed.")
        else:
            print(f"New target aquired: {command}")
            print("Fire!")
    return is_valid


def main():
    """ 
    main game function
    """
    maps = start_game()
    BATTLEFIELD_PLAYER = maps[0]
    BATTLEFIELD_PC = maps[1]
    created_scoreboard = maps[4]
    not_hit_player = maps[2]
    not_hit_pc = maps[3]
    score_player = 0
    score_pc = 0
    print("Welcome to a game of battleship.")
    print("Your fleet is deployed and ready to hunt.")
    print("This is your fleet:")
    print(BATTLEFIELD_PLAYER)
    gameon = True
    while gameon:
        user_command = play_game()
        user_command = user_command.lower()
        validity_result = check_command(user_command)
        if validity_result:
            stop_it = endGame(user_command)
            print(stop_it)
            if not stop_it:
                hit = did_i_hit_something(user_command, 1)
                print(user_command)
                print(not_hit_player)
                try:
                    not_hit_player.remove(user_command)
                    hitlist_player.append(user_command)
                except NameError:
                    print("usercommand failed")
                if hit:
                    print(f"Hit! Target confirmed at: {user_command}")
                    score_player += 1
                else:
                    print("no hit")
                gameon = not (score_player >= sum(SHIP_SIZES) or\
                    score_pc >= sum(SHIP_SIZES))
                
            else:
                gameon = not stop_it
                
        print(f"player: {score_player} vs. pc: {score_pc}")
        print(f"player targted: {hitlist_player}")
main()
