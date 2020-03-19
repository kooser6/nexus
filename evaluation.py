import math

piece_val = [100, 300, 400, 500, 1025, 20000]
push_pieces_to_center = [
                   -20, -10, -10, -10, -10, -10, -10, -20,
                   -10, 0,   0,   0,   0,   0,   0,   -10,
                   0,   10,  10,  10,  10,  10,  10,  0,
    -20, -10, 0,   10,  20,  20,  30,  30,  20,  20,  10, 0,  -10, -20,
    -10, 0,   10,  20,  30,  30,  35,  35,  30,  30,  20, 10, 0,   -10,
    -10, 0,   10,  20,  30,  35,  35,  35,  35,  30,  20, 10, 0,   -10,
    -10, 0,   10,  30,  35,  35,  40,  40,  35,  35,  30, 10, 0,   -10,
    -10, 0,   10,  30,  35,  35,  40,  40,  35,  35,  30, 10, 0,   -10,
    -10, 0,   10,  20,  30,  35,  35,  35,  35,  30,  20, 10, 0,   -10,
    -10, 0,   10,  20,  30,  30,  35,  35,  30,  30,  20, 10, 0,   -10,
    -20, -10, 0,   10,  20,  20,  30,  30,  20,  20,  10, 0,  -10, -20,
                   0,   10,  10,  10,  10,  10,  10,  0,
                   -10, 0,   0,   0,   0,   0,   0,   -10,
                   -20, -10, -10, -10, -10, -10, -10, -20
]

def evaluate_material(board):
    """ Evaluate The Material """
    sum = 0
    for square in board:
        if square == 0:
            continue
        if square[0] == 0 or square[0] == 2:
            sum += piece_val[square[1]]
        else:
            sum += -piece_val[square[1]]
    return sum

def evaluate_material_balance(board):
    """ Evaluate The Material Balance """
    sum = aa = bb = cc = dd = 0
    for square in board:
        if square == 0 or square == 1:
            continue
        if square[0] == 0:
            val = piece_val[square[1]]
            val /= 5
            aa += val
        elif square[0] == 1:
            val = piece_val[square[1]]
            val /= 5
            bb += -val
        elif square[0] == 2:
            val = piece_val[square[1]]
            val /= 5
            cc += val
        else:
            val = piece_val[square[1]]
            val /= 5
            dd += -val
    if aa > cc:
        sum += -(aa - cc)
    if cc > aa:
        sum += -(cc - aa)
    if bb > dd:
        sum += bb - dd
    if dd > bb:
        sum += dd - bb
    return sum
