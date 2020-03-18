import threat
import state

pawn_start_keys = [
    52,  53,  54,  55,  56,  57,  58,  59,
    82,  98,  114, 130, 146, 162, 178, 194,
    93,  109, 125, 141, 157, 173, 189, 205,
    228, 229, 230, 231, 232, 233, 234, 235
]
castle_req_keys = {
    129 : { 97  : 81,  161 : 193},
    248 : { 250 : 151, 246 : 244},
    39  : { 37  : 36,  41  : 43},
    158 : { 190 : 206, 126 : 94}
}
castle_rep_keys = {
    129 : { 97  : 113, 161 : 145},
    248 : { 250 : 249, 246 : 247},
    39  : { 37  : 38,  41  : 40},
    158 : { 190 : 174, 126 : 142}
}
valid_promotion_codes = [1, 2, 3, 4]
promotion_keys = [
    [81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94],
    [43,  59,  75,  91,  107, 123, 139, 155, 171, 187, 203, 219, 235, 251],
    [193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206],
    [36,  52,  68,  84,  100, 116, 132, 148, 164, 180, 196, 212, 228, 244]
]

def undo(history):
    """ Returns The Last Position Data """
    pos = history.pop()
    return [pos, history]

def get_moves(board, move, castle_rights, enpassants):
    """ Gets A List Of Avaliable Moves """
    ret = []
    for key, square in enumerate(board):
        if square != 0 and square[0] == move:
            if pawn_start_square(key) and square[1] == 0:
                if move == 0:
                    directone = key + (threat.directions[0] * 2)
                    directtwo = key + threat.directions[0]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                        if board[directone] == 0:
                            temp_board = board[:]
                            temp_board[directone] = temp_board[key]
                            temp_board[key] = 0
                            if state.in_check(temp_board, move) == 0:
                                ret.append([key, directone])
                elif move == 1:
                    directone = key + (threat.directions[3] * 2)
                    directtwo = key + threat.directions[3]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                        if board[directone] == 0:
                            temp_board = board[:]
                            temp_board[directone] = temp_board[key]
                            temp_board[key] = 0
                            if state.in_check(temp_board, move) == 0:
                                ret.append([key, directone])
                elif move == 2:
                    directone = key + (threat.directions[1] * 2)
                    directtwo = key + threat.directions[1]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                        if board[directone] == 0:
                            temp_board = board[:]
                            temp_board[directone] = temp_board[key]
                            temp_board[key] = 0
                            if state.in_check(temp_board, move) == 0:
                                ret.append([key, directone])
                else:
                    directone = key + (threat.directions[2] * 2)
                    directtwo = key + threat.directions[2]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                        if board[directone] == 0:
                            temp_board = board[:]
                            temp_board[directone] = temp_board[key]
                            temp_board[key] = 0
                            if state.in_check(temp_board, move) == 0:
                                ret.append([key, directone])
            elif square[1] == 0:
                if move == 0:
                    directtwo = key + threat.directions[0]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                elif move == 1:
                    directtwo = key + threat.directions[3]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                elif move == 2:
                    directtwo = key + threat.directions[1]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
                else:
                    directtwo = key + threat.directions[2]
                    if board[directtwo] == 0:
                        temp_board = board[:]
                        temp_board[directtwo] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) == 0:
                            ret.append([key, directtwo])
            if square[1] == 5 and state.in_check(board, move) == 0:
                if castle_rights[move][0] == True:
                    if move == 0:
                        local_a = 249
                        local_b = 250
                    elif move == 1:
                        local_a = 113
                        local_b = 97
                    elif move == 2:
                        local_a = 38
                        local_b = 37
                    else:
                        local_a = 174
                        local_b = 190
                    if board[local_a] == 0 and board[local_b] == 0:
                        allow = True
                        for key_check, square_check in enumerate(board):
                            if square_check != 0 and not(is_not_opposite_color(move, square_check[0])):
                                if threat.is_threat(key_check, local_a, board) or threat.is_threat(key_check, local_b, board):
                                    allow = False
                        if allow == True:
                            ret.append([key, local_b])
                if castle_rights[move][1] == True:
                    if move == 0:
                        local_a = 247
                        local_b = 246
                        local_c = 245
                    elif move == 1:
                        local_a = 145
                        local_b = 161
                        local_c = 177
                    elif move == 2:
                        local_a = 40
                        local_b = 41
                        local_c = 42
                    else:
                        local_a = 142
                        local_b = 126
                        local_c = 110
                    if board[local_a] == 0 and board[local_b] == 0:
                        allow = True
                        for key_check, square_check in enumerate(board):
                            if square_check != 0 and not(is_not_opposite_color(move, square_check[0])):
                                if threat.is_threat(key_check, local_a, board) or threat.is_threat(key_check, local_b, board) or threat.is_threat(key_check, local_c, board):
                                    allow = False
                        if allow == True:
                            ret.append([key, local_b])
            for key_check, square_check in enumerate(board):
                if threat.is_threat(key, key_check, board):
                    if square_check == 0:
                        if square[1] == 0:
                            for enpassant_key, enpassant_check in enumerate(enpassants):
                                if key_check == enpassant_check and not(is_not_opposite_color(enpassant_key, move)):
                                    if move == 0:
                                        hasOpposingPawnKey = key + threat.directions[0]
                                    elif move == 1:
                                        hasOpposingPawnKey = key + threat.directions[3]
                                    elif move == 2:
                                        hasOpposingPawnKey = key + threat.directions[1]
                                    else:
                                        hasOpposingPawnKey = key + threat.directions[2]
                                    accessKey = board[hasOpposingPawnKey]
                                    if accessKey != 0 and accessKey[0] == enpassant_key and accessKey[1] == 0:
                                        ret.append([key, key_check])
                            continue
                    if square_check != 0:
                        if is_not_opposite_color(square[0], square_check[0]):
                            continue
                    skipSection = False
                    if square[1] == 5:
                        for threat_key_check in threat.valid_keys:
                            if board[threat_key_check] == 0:
                                continue
                            check_opposite = board[threat_key_check]
                            if not(is_not_opposite_color(square[0], check_opposite[0])):
                                if threat.is_threat(threat_key_check, key_check, board):
                                    skipSection = True
                    if skipSection == False:
                        temp_board = board[:]
                        temp_board[key_check] = temp_board[key]
                        temp_board[key] = 0
                        if state.in_check(temp_board, move) != 0:
                            continue
                        ret.append([key, key_check])
    return ret

def is_not_opposite_color(color_one, color_two):
    """ Checks If The Colors Are Opposite """
    if color_one == 0 and color_two == 0 or color_one == 0 and color_two == 2:
        return True
    if color_one == 1 and color_two == 1 or color_one == 1 and color_two == 3:
        return True
    if color_one == 2 and color_two == 2 or color_one == 2 and color_two == 0:
        return True
    if color_one == 3 and color_two == 3 or color_one == 3 and color_two == 1:
        return True
    return False

def pawn_start_square(key):
    """ Checks If The Pawn Is On Starting Square """
    if key in pawn_start_keys:
        return True
    return False

def next_move(color):
    """ Get The Next Color To Move """
    return (color + 1) % 4

def is_promotion_key(key, move):
    """ Checks An promotion Key """
    if key in promotion_keys[move]:
        return True
    return False

def valid_promotion(code):
    """ Checks An promotion Code """
    if code in valid_promotion_codes:
        return True
    return False
