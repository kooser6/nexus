# This file is part of Fisheater, A strong 4 player chess engine,
# and is released under the "GNU General Public License v3.0". Please see the LICENSE
# file that should have been included as part of this package.
#------------------------------------------------------------------------------------

directions = [-16, 16, -1, 1, -15, -17, 15, 17]
valid_keys = [
                   36,  37,  38,  39,  40,  41,  42,  43,
                   52,  53,  54,  55,  56,  57,  58,  59,
                   68,  69,  70,  71,  72,  73,  74,  75,
    81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,
    97,  98,  99,  100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110,
    113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126,
    129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142,
    145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158,
    161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174,
    177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
    193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206,
                   212, 213, 214, 215, 216, 217, 218, 219,
                   228, 229, 230, 231, 232, 233, 234, 235,
                   244, 245, 246, 247, 248, 249, 250, 251
]

def is_threat(from_key, to_key, board):
    """ Detects Piece Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0:
            if data[1] == 0:
                return is_pawn_threat(from_key, to_key, board)
            elif data[1] == 1:
                return is_knight_threat(from_key, to_key, board)
            elif data[1] == 2:
                return is_bishop_threat(from_key, to_key, board)
            elif data[1] == 3:
                return is_rook_threat(from_key, to_key, board)
            elif data[1] == 4:
                return is_queen_threat(from_key, to_key, board)
            else:
                return is_king_threat(from_key, to_key, board)
    return False

def is_pawn_threat(from_key, to_key, board):
    """ Detects Pawn Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0 and data[1] == 0:
            if data[0] == 0:
                direction_one = directions[4]
                direction_two = directions[5]
            elif data[0] == 1:
                direction_one = directions[4]
                direction_two = directions[7]
            elif data[0] == 2:
                direction_one = directions[6]
                direction_two = directions[7]
            else:
                direction_one = directions[5]
                direction_two = directions[6]
            actual_to_key_one = from_key + direction_one
            actual_to_key_two = from_key + direction_two
            if actual_to_key_one == to_key or actual_to_key_two == to_key:
                return True
    return False

def is_knight_threat(from_key, to_key, board):
    """ Detects Knight Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0 and data[1] == 1:
            direction_check = [
                directions[0] + directions[5],
                directions[0] + directions[4],
                directions[3] + directions[4],
                directions[3] + directions[7],
                directions[1] + directions[6],
                directions[1] + directions[7],
                directions[2] + directions[5],
                directions[2] + directions[6]
            ]
            for direct in direction_check:
                actual_to_key = from_key + direct;
                if actual_to_key == to_key:
                    return True
    return False;

def is_bishop_threat(from_key, to_key, board, skip = False):
    """ Detects Bishop Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if skip == True or data != 0 and data[1] == 2:
            direction_check = [
                directions[4],
                directions[5],
                directions[6],
                directions[7]
            ]
            for direct in direction_check:
                res = loop_direction(from_key, to_key, board, direct);
                if res == True:
                    return True
    return False

def is_rook_threat(from_key, to_key, board, skip = False):
    """ Detects Rook Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if skip == True or data != 0 and data[1] == 3:
            direction_check = [
                directions[0],
                directions[1],
                directions[2],
                directions[3]
            ]
            for direct in direction_check:
                res = loop_direction(from_key, to_key, board, direct);
                if res == True:
                    return True
    return False

def is_queen_threat(from_key, to_key, board):
    """ Detects Queen Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0 and data[1] == 4:
            return is_bishop_threat(from_key, to_key, board, True) or is_rook_threat(from_key, to_key, board, True)
    return False

def is_king_threat(from_key, to_key, board):
    """ Detects King Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0 and data[1] == 5:
            direction_check = [
                directions[0],
                directions[1],
                directions[2],
                directions[3],
                directions[4],
                directions[5],
                directions[6],
                directions[7]
            ]
            for direct in direction_check:
                actual_to_key = from_key + direct
                if actual_to_key == to_key:
                    return True
    return False

def is_not_enpassant_pawn_move(from_key, to_key, board):
    """ Detects Enpassant Moves """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0 and data[1] == 0:
            direction_check = [
                directions[0],
                directions[1],
                directions[2],
                directions[3]
            ]
            for direct in direction_check:
                actual_to_key = from_key + direct
                if actual_to_key == to_key:
                    return True
    return False

def loop_direction(from_key, to_key, board, direction):
    """ Loops Directions """
    res = ''
    next = from_key
    while res == '':
        next += direction
        if valid_key(next):
            check = board[next]
            if check != 0:
                if next != to_key:
                    res = False
                    break
            if next == to_key:
                res = True
                break
        else:
            res = False
    return res

def valid_key(key):
    """ Checks An Input Key """
    if key in valid_keys:
        return True
    return False
