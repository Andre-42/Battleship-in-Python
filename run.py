"""
This is a game of battleship.
"""
import random
import time
import numpy as np

# Global Constants and Variables
SHIP_SIZES = [5, 4, 3, 3, 2]
BATTLEFIELD_SIZE = (8, 8)

BATTLEFIELD_PLAYER = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
BATTLEFIELD_PC = BATTLEFIELD_PLAYER.copy()

max_letter = BATTLEFIELD_PLAYER.shape[1]
col_names = list(map(chr, range(97, max_letter+97)))
max_number = BATTLEFIELD_PLAYER.shape[0]

# Functions for Setting Up the Game

def change_fieldsize(size_xbyx):
    """
    This function adjusts the fieldsize of the game 
    and related reference variables in the global space.
    """
    # global variable declaration to effect changes
    global BATTLEFIELD_SIZE, BATTLEFIELD_PLAYER, BATTLEFIELD_PC
    global max_letter, col_names, max_number
    # change global variables
    BATTLEFIELD_SIZE = (size_xbyx, size_xbyx)
    BATTLEFIELD_PLAYER = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
    BATTLEFIELD_PC = BATTLEFIELD_PLAYER.copy()
    # ... other variable changes ...
    max_letter = BATTLEFIELD_PLAYER.shape[1]
    col_names = list(map(chr, range(97, max_letter+97)))
    max_number = BATTLEFIELD_PLAYER.shape[0]


def check_answer(fieldvalue):
    """
    Here you confirm your answer again. It will return a True value if you confirm.
    Every false input or decline will return False.
    """
    # chose appropriate request text
    if fieldvalue == 6:
        print("You want to shoot fish in a barrel?")
    elif fieldvalue == 8:
        print("You want to go hunting in the North Sea?")
    else:
        print("You want to go out on the really big blue yonder?")
    # user decision
    choice = input("Say Yea (Y) or Nei (N): \n")
    choice = choice.lower()
    choice = choice[0]
    return choice == "y"


def request_gamelevel():
    """
    This function enables you to select a game size. The default value after 3 wrong inputs is 8x8.
    """
    strikes = 0
    ask = True
    while ask:
        # get user input
        print("Welcome to Battleship!")
        print("How big an ocean do you want to sail on today, Capt'n?")
        print("1. Shoot fish in a barrel (type: 6 / small)")
        print("2. The North Sea sounds like good waters (type: 8 / medium)")
        print("3. Let's go on the big ocean! (type: 12 / large)")
        choice = input("The man are ready, tell me your choice: \n")
        choice = choice.lower()
        # check input
        if choice in ["1","6","small","barrel"]:
            fieldsize = 6
            confirm = check_answer(fieldsize)
        elif choice in ["2","8","medium","sea"]:
            fieldsize = 8
            confirm = check_answer(fieldsize)
        elif choice in ["3","12","large","ocean"]:
            fieldsize = 12
            confirm = check_answer(fieldsize)
        else:
            print("You are talking nonsense, Capt'n.")
            print("Did you have to much to drink?")
            confirm = False
        # check if question needs repeat
        if confirm:
            ask = False
        else:
            strikes += 1
        # default setting after 3 tries
        if strikes >= 3:
            ask = False
            fieldsize = 8
    change_fieldsize(fieldsize)


def set_ship_inline(boardvector, startpos, shiplength):
    """
    This function defines the ship position within a column or row.
    It identifies already used positions and finds the gaps.
    It identifies gaps that are large enough for the ship (shiplength) and
    tries to place the ship in a gap as close as possible to the prefered
    startpos.
    If the ship cannot be place it will not change the boardvector.
    """
    # check out boardvector for spaces
    boardvector_old = boardvector.copy()
    initial_sum = np.sum(boardvector)
    num_breaks = np.cumsum(boardvector)
    if initial_sum > 0:
        num_breaks[np.where(boardvector)[0]] = -1
    unique_breaks, break_index, break_counts = np.unique(num_breaks, 
        return_index=True, return_counts=True)
    # prepare placement
    valid_counts = break_counts[unique_breaks >= 0]
    valid_indices = break_index[unique_breaks >= 0]
    valid_ends = valid_indices + valid_counts - 1
    valid_positions = valid_indices[valid_counts >= shiplength]
    valid_n = len(valid_positions)
    # ship placement procedure
    try:
        if valid_n > 0:
            # find region fitting to suggested position
            if valid_n > 1:
                start_idx = np.searchsorted(np.append(valid_positions, valid_ends), startpos)
            else:
                start_idx = 0
            if start_idx > valid_n:
                start_idx = start_idx - valid_n
            # determine position
            ship_min = valid_positions[start_idx]
            ship_max = valid_ends[start_idx]
            ship_end = startpos + shiplength - 1
            ship_end = min(ship_end, ship_max)
            ship_start = ship_end - shiplength + 1
            # place ship
            if ship_start >= ship_min and ship_end <= ship_max:
                boardvector[ship_start:ship_end + 1] = True
        else:
            # not sure if ever gets executed observed error may abort beforehand
            ship_start = startpos
            ship_end = ship_start + shiplength - 1
            ship_end = min(ship_end, len(boardvector) - 1)
            ship_start = ship_end - shiplength + 1
            boardvector[ship_start:ship_end + 1] = True
    except:
        # error fix in try statement
        ship_start = startpos
        ship_end = ship_start + shiplength - 1
        ship_end = min(ship_end, len(boardvector) - 1)
        ship_start = ship_end - shiplength + 1
        boardvector[ship_start:ship_end + 1] = True
        print("Error ship placement line 44")
    # check if ship is properly placed
    end_sum = np.sum(boardvector) - initial_sum
    if not end_sum == shiplength:
        boardvector = boardvector_old
    return boardvector


def set_ship_random(set_battlefield, ship):
    """
    This function defines the column or row for a new ship position.
    It converts every row or column selection into a vector and
    calls the set_ship_inline function to place a ship in the vector.
    After ship placement the vector is put back into the correct 
    column or row.
    """
    # find random deployment position
    max_x = BATTLEFIELD_SIZE[1] - 1
    max_y = BATTLEFIELD_SIZE[0] - 1
    pos_x = np.random.randint(max_x)
    pos_y = np.random.randint(max_y)
    # select row or column for ship placement
    roworcol = np.random.randint(2)
    if roworcol == 1:
        boardvector = set_battlefield[pos_y, :]
    else:
        boardvector = set_battlefield[:, pos_x]
    # place ship in vector
    boardvector = set_ship_inline(boardvector, pos_x if roworcol == 1 else pos_y, ship)
    # set boardvector back into the battlefield
    if roworcol == 1:
        set_battlefield[pos_y, :] = boardvector
    else:
        set_battlefield[:, pos_x] = boardvector
    return set_battlefield


def create_battlefield(battlefield):
    """
    This is a iterative approach to deploy a fleet of ships. It will deploy from largest
    to smallest ship in descending order. Attention this is a double while loop!!!
    This is just the shell function for the actual ship placement in 'set_ship_random'.
    It will check if the ship was actually deployed and if not it will retry the deployment
    until success or an aboard condition is reached (99 tries).
    """
    # deploy fleet
    redo = True
    while redo:
        # iterade through ship sizes
        for ship_size in SHIP_SIZES:
            max_sum = sum(SHIP_SIZES)
            tryagain = True
            it = 1
            # try ship placement
            while tryagain:
                initial_sum = np.sum(battlefield)
                battlefield_new = set_ship_random(battlefield.copy(), ship_size)
                new_sum = np.sum(battlefield_new)
                is_ship_set = (new_sum - initial_sum == ship_size) and (new_sum <= max_sum)
                # check ship placement or try again
                if is_ship_set:
                    battlefield = battlefield_new
                    tryagain = False
                else:
                    tryagain = tryagain and it < 100 and new_sum < max_sum
                it += 1
            # check if complete overhaul
            redo = not is_ship_set
            if redo:
                battlefield = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
    return battlefield


def create_scoreboards(max_letter_x, col_name_x, max_number_y):
    """
    This function creates a list with all valid target entries available on the board.
    not_hit: stringlist: a1, a2, ...
    field_index: numerical index of board matrix: 0..number of fields-1
    field_x: column coordinates for not_hit elements
    field_y: row coordinates for not_hit elements
    """
    n_el = max_letter_x * max_number_y
    not_hit = [None] * n_el
    field_index = [None] * n_el
    field_x = [None] * n_el
    field_y = [None] * n_el
    it_list = 0
    for j in range(max_letter_x):
        for i in range(max_number_y):
            not_hit[it_list] = col_name_x[j] + str(i+1)
            field_index[it_list] = it_list
            field_x[it_list] = j
            field_y[it_list] = i
            it_list += 1
    return not_hit, field_index, field_x, field_y


def start_game():
    """
    This function uses the template battlefields to create the empty player fields.
    It also creates several lists necessary for the game scoreing with all valid 
    field names on the score board.
    Columns are presentes as letters a,b,c,...
    Rows are numbered 1,...
    """
    # pre requisit for battlefield update
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
    field = input("Type in your target coordinate: \n")
    return field


def did_i_hit_something(target, player_id):
    """
    The name is the function. Function gets x,y coordinates of target position 
    and checks either the player or pc deployment board if there is a ship a that position.
    It returns True for a valid hit.
    """
    # get indices
    field_index = created_scoreboard[1]
    field_x = created_scoreboard[2]
    field_y = created_scoreboard[3]
    target_index = field_index[created_scoreboard[0].index(target)]
    target_x = field_x[target_index]
    target_y = field_y[target_index]
    # get placement information at target
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
    # get valid input options
    valid_input = created_scoreboard[0]
    if command in valid_input:
        # check command regarding target coordinates
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
        # check for stop command
        print("Retreat command received.")
        print("Game will be closed")
        return True
    else:
        # false input handling
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
    # get field coordinate reference data
    field_index = created_scoreboard[1]
    field_x = created_scoreboard[2]
    field_y = created_scoreboard[3]
    # get target related information
    target_index = field_index[created_scoreboard[0].index(target)]
    target_x = field_x[target_index]
    target_y = field_y[target_index]
    return target_y, target_x


# Main Game Loop

def main():
    """
    This is the main function controlling gaming and setup
    """
    # global variables that are affected by the function
    global BATTLEFIELD_PLAYER, BATTLEFIELD_PC, BATTLEFIELD_SIZE, SHIP_SIZES, created_scoreboard
    # change Field size
    request_gamelevel()
    # Create the boards and other necessary variables
    player, enemy, not_hit_player, not_hit_pc, created_scoreboard = start_game()
    # Update BATTLEFIELD_PLAYER and BATTLEFIELD_PC
    BATTLEFIELD_PLAYER = player.copy()
    BATTLEFIELD_PC = enemy.copy()
    # initiate scoring variables
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
                    answer = random.randint(0, 2)
                    print(f"Sploosh! {answer_list[answer]}")
                # Enemy attack
                pc_command = computer_move(not_hit_pc)
                # check for hit
                hit_pc = did_i_hit_something(pc_command, 2)
                # remove command from possible commands
                try:
                    not_hit_pc.remove(pc_command)
                    hitlist_pc.append(pc_command)
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
        print("This is how it looks, Capt'n:")
        for row in map_overview:
            print(' '.join(row))
        print(f"Player: {score_player} ({np.ceil((score_player/sum(SHIP_SIZES))*100)}%) vs. Computer: {score_pc} ({np.ceil((score_pc/sum(SHIP_SIZES))*100)}%)")
    # end game
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
