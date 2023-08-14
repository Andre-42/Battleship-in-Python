import numpy as np
import random
from pprint import pprint

SHIP_SIZES = [5,4,3,3,2]
GAME_STATUS = True
BATTLEFIELD_SIZE = (8,8)
BATTLEFIELD_PLAYER = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
BATTLEFIELD_PC = BATTLEFIELD_PLAYER

def start_game():
    GAME_STATUS = True
    return GAME_STATUS

def pause_game():
    GAME_STATUS = False
    return GAME_STATUS

def reset_gameboard():
    BATTLEFIELD_PLAYER = np.zeros(BATTLEFIELD_SIZE, dtype=bool)
    BATTLEFIELD_PC = BATTLEFIELD_PLAYER

def set_ship_random(battlefield,ship)
    pos_x = np.random.randint(BATTLEFIELD_SIZE(2))
    pos_y = np.random.randint(BATTLEFIELD_SIZE(1))

    row_xy = battlefield[pos_y,:]
    col_xy = battlefield[:,pos_x]

    set_ship_inline(row_xy,pos_x,ship)

def set_ship_inline(boardvector,startpos,shiplength)
    """
    This function defines the ship position within a column or row.
    numbreaks enables the identification of unique fields within the vector
    """
    freespace = sum(boardvector==False)
    numbreaks = np.cumsum(boardvector==True)
    fields, fieldstart, fieldindex, fieldcounts = np.unique(numbreaks, return_index = True, return_inverse = True, return_counts = True)
    if sum(fields>0)>0:
        fieldcounts[fields>0] = fieldcounts[fields>0]-1
        fieldindex[fieldstart[fields>0]] = -1
    fieldvalid = fieldcounts>=shiplength
    if sum(fieldvalid)>0:
        fieldwish = fieldindex(startpos)
        getwish = fieldwish == fields(fieldvalid)
        if getwish:
            u, poslast = np.unique(np.flip(fieldindex)==fieldwish, return_index = True)
            u, posfirst = np.unique(fieldindex==fieldwish, return_index = True)
            posend = min([startpos+shiplength-1,poslast])
            posstart = posend - shiplength
        else:
            fieldwish = fields(fieldvalid)
            fieldlen = fieldcounts(fieldvalid)
            fieldwish = fieldwish(fieldlen == max(fieldlen))
            if len(fieldwish)>1:
                fieldwish = fieldwish[np.random.randint(len(fieldwish)-1)]
            
            u, poslast = np.unique(np.flip(fieldindex)==fieldwish, return_index = True)
            u, posfirst = np.unique(fieldindex==fieldwish, return_index = True)
            posend = min([startpos+shiplength-1,poslast])
            posstart = posend - shiplength

