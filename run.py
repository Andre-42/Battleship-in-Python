import numpy as np
import random
import time
from itertools import product

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
    """
    This function uses the template battlefields to create the empty player fields.
    It also creates several lists necessary for the game scoreing with all valid 
    field names on the score board.
    Columns are presentes as letters a,b,c,...
    Rows are numbered 1,...
    """
    # pre requisit for battlefield update
    max_letter = BATTLEFIELD_PLAYER.shape[1]
    col_names = list(map(chr, range(97, max_letter+97)))
    max_number = BATTLEFIELD_PLAYER.shape[0]

    created_scoreboard = create_scoreboards(max_letter, col_names, max_number)
    not_hit_list_player = created_scoreboard[0].copy()
    not_hit_list_pc = not_hit_list_player.copy()

    # Create battlefields
    player = create_battlefield(BATTLEFIELD_PLAYER.copy())
    pc = create_battlefield(BATTLEFIELD_PC.copy())
    
    print("This is your fleet:")
    map_ship_placement = np.full((BATTLEFIELD_SIZE[0] + 1, BATTLEFIELD_SIZE[1] + 1), '~', dtype=str)
    
    # Fill the top row with alphabet letters as column names
    for col_idx, col_label in enumerate(col_names):
        map_ship_placement[0, col_idx + 1] = col_label
    
    # Fill the leftmost column with row numbers
    for row_idx in range(1, BATTLEFIELD_SIZE[0] + 1):
        map_ship_placement[row_idx, 0] = str(row_idx)

    # Mark ships with ^
    for row_idx in range(1, BATTLEFIELD_SIZE[0] + 1):
        for col_idx in range (1, BATTLEFIELD_SIZE[1] + 1):
            if player[row_idx - 1][col_idx - 1]:
                map_ship_placement[row_idx, col_idx] = '^'
                
    # print(map_ship_placement) but neatly
    for row_idx in map_ship_placement:
        print(' '.join(row_idx))
        
    return player, pc, not_hit_list_player, not_hit_list_pc, created_scoreboard

created_scoreboard = create_scoreboards(max_letter, col_names, max_number)
           

# Functions for Playing the Game

def end_game(command_stop):
    """
    This funtion returns True to initiate the end of a game.
    """
    return command_stop.lower() == "stop" or command_stop.lower() == "s"


def play_game():
    """
    Get user Input for player.
    """
    print("Targets should be provided as:")
    print(f" -letters for columns, {col_names[0]}...{col_names[max_letter-1]}")
    print(f" -numbers for rows, max({max_number})")
    print(" -example: a3, d8 or f1")
    print("If you want to retreat say 'stop' or 's'")
    field = input("Type in your target coordinate:")
    return field


def did_i_hit_something(target, player_id):
    """
    The name is the function. Function gets x,y coordinates of target position 
    and checks either the player or pc deployment board if there is a ship a that position.
    It returns True for a valid hit.
    """
    field_index = created_scoreboard[1]
    field_x = created_scoreboard[2]
    field_y = created_scoreboard[3]
    
    target_index = field_index[created_scoreboard[0].index(target)]
    target_x = field_x[target_index]
    target_y = field_y[target_index]
    
    if player_id == 1:
        is_hit = BATTLEFIELD_PC[target_y, target_x]
    else:
        is_hit = BATTLEFIELD_PLAYER[target_y, target_x]
    
    return is_hit


def check_command(command, not_hit_yet):
    """
    This function checks the user input for validity against allowed entries.
    It will return True for valid target positions (inside game bounds) and if 
    game aboard command is given.
    False is returned for gibberish input and already called target positions.
    """
    valid_input = created_scoreboard[0]

    if command in valid_input:
        
        if command in not_hit_yet:
            print(f"New target acquired: {command}")
            print("Fire!")
            time.sleep(1)
            return True
        
        else:
            print("You hit that place already.")
            was_hit = did_i_hit_something(command, 1)
            
            if was_hit:
                print(f"It was a direct hit at {command}")
            else:
                print("We missed.")
            time.sleep(3)
            return False
    
    elif command in ["stop", "s"]:
        print("Retreat command received.")
        print("Game will be closed")
        return True
    
    else:
        print("Your target coordinates are not correct. TRY again")
        time.sleep(3)
        return False


def computer_move(not_hit_rand):
    """
    Choose the computer's move by randomly selecting a target that hasn't been hit yet.
    """
    return random.choice(not_hit_rand)

def generate_map_overview(target_list, not_hit_list):
    """
    Create a nice little display of your shooting efforts. Including '~' waves,
    'x' hits and 'w' sploooosh (miss).
    """
    map_overview = np.full((BATTLEFIELD_SIZE[0] + 1, BATTLEFIELD_SIZE[1] + 1), '~', dtype=str)
    
    # Fill the top row with alphabet letters as column names
    for col_idx, col_label in enumerate(col_names):
        map_overview[0, col_idx + 1] = col_label
    
    # Fill the leftmost column with row numbers
    for row_idx in range(1, BATTLEFIELD_SIZE[0] + 1):
        map_overview[row_idx, 0] = str(row_idx)
    
    # Still empty coordinates get filled with water
    for target in not_hit_list:
        target_y, target_x = get_coordinates_from_target(target)
        map_overview[target_y + 1, target_x + 1] = '~'
    
    # Already shot targets get hit and splash marks
    for target in target_list:
        target_y, target_x = get_coordinates_from_target(target)
        if BATTLEFIELD_PC[target_y, target_x]:
            map_overview[target_y + 1, target_x + 1] = 'x'
        else:
            map_overview[target_y + 1, target_x + 1] = 'w'
        
    return map_overview


def get_coordinates_from_target(target):
    """
    Aquires the x,y coodinates of the requested position to create the overview display.
    """
    field_index = created_scoreboard[1]
    field_x = created_scoreboard[2]
    field_y = created_scoreboard[3]
    
    target_index = field_index[created_scoreboard[0].index(target)]
    target_x = field_x[target_index]
    target_y = field_y[target_index]
    
    return target_y, target_x



# Main Game Loop

def main():
    # global variables that are affected by the function
    global BATTLEFIELD_PLAYER, BATTLEFIELD_PC, BATTLEFIELD_SIZE, SHIP_SIZES, created_scoreboard
    
    # change Field size
    request_gamelevel()
    
    # Create the boards and other necessary variables
    player, pc, not_hit_player, not_hit_pc, created_scoreboard = start_game()
    
    # Update BATTLEFIELD_PLAYER and BATTLEFIELD_PC
    BATTLEFIELD_PLAYER = player.copy()
    BATTLEFIELD_PC = pc.copy()

    score_player = 0
    score_pc = 0
    hitlist_player = []
    hitlist_pc = []
    answer_list = ["My blind grandma could have shot better!",
                   "How much rum did you have for breakfast, Capt'n?",
                   "That one was not quite shooting fish in a barrel..."]

    print("Welcome to a game of Battleship.")
    print("Your fleet is deployed and ready to hunt.")
    print("Be aware of the fogbank. Reports say it is full of enemy ships.")
    
    # the game begins
    game_on = True
    while game_on:
        # get user command and transfer to lower case
        user_command = play_game()
        user_command = user_command.lower()

        # check input and act 
        is_valid_command = check_command(user_command, not_hit_player)
        
        if is_valid_command:
            # check for stop command
            stop_it = end_game(user_command)
            
            if not stop_it:
                # check for hit
                hit = did_i_hit_something(user_command, 1)
                
                # remove command from possible commands
                try:
                    not_hit_player.remove(user_command)
                    hitlist_player.append(user_command)
                except ValueError:
                    pass
                
                # score the shot
                if hit:
                    print(f"Hit! Target confirmed at: {user_command}")
                    score_player += 1
                else:
                    answer = np.random.randint(3)
                    print(f"Sploosh! {answer_list[answer]}")

                # Enemy attack
                pc_command = computer_move(not_hit_pc)
                # check for hit
                hit_pc = did_i_hit_something(pc_command, 2)
                
                # remove command from possible commands
                try:
                    not_hit_pc.remove(pc_command)
                    hitlist_pc.append(pc_command)
                    #print(f"pc shot at: {hitlist_pc}")
                except ValueError:
                    pass

                # score the enemy 
                if hit_pc:
                    print(f"The enemy scored a hit at: {pc_command}")
                    print("Get your swimaids out!")
                    score_pc += 1
                else:
                    print(f"Enemy shot at: {pc_command} and missed, Sir.")
                
                # check if game can be continued, are any ships left floating?
                game_on = not (score_player >= sum(SHIP_SIZES) or score_pc >= sum(SHIP_SIZES))
                # Have you shot all your cannons?
                game_on = game_on and (len(not_hit_player) > 0 or len(not_hit_pc) > 0)
            else:
                game_on = not stop_it

        # Print the current map overview
        map_overview = generate_map_overview(hitlist_player, not_hit_player)

        # Add row names (numbers) and column names (letters) to the map overview
        max_letter = BATTLEFIELD_PC.shape[1]
        col_names = list(map(chr, range(97, max_letter + 97)))
        row_names = list(map(str, range(1, BATTLEFIELD_PC.shape[0] + 1)))

        #map_overview = [[''] + col_names] + [[row_names[i]] + row for i, row in enumerate(map_overview)]

        print("This is how it looks, Capt'n:")
        for row in map_overview:
            print(' '.join(row))

        print(f"Player: {score_player} ({np.ceil((score_player/sum(SHIP_SIZES))*100)}%) vs. Computer: {score_pc} ({np.ceil((score_pc/sum(SHIP_SIZES))*100)}%)")
        #print(f"Player's targets: {hitlist_player}")

    print("Game over!")
    if score_pc > score_player:
        print("It was an honor, Sir...")
        print("but the Capt'n goes down with the ship.")
    elif score_pc == score_player:
        print("Well, wet feet are better than sinking. Ey, Capt'n?")
    else:
        print("A jolly good win Sir. Let's see how the rum is fairing.")
    
    time.sleep(5)
    print("Oh god, I can't stand upright anymore. God night!")
    time.sleep(5)


main()
