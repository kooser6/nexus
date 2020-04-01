from cpython cimport array
from cpython cimport bool

piece_val = [100, 375, 475, 600, 1275, 26000]
pawn_start_keys = [  52, 53, 54, 55, 56, 57, 58, 59, 82, 98, 114, 130, 146, 162, 178, 194, 93, 109, 125, 141, 157, 173, 189, 205, 228, 229, 230, 231, 232, 233, 234, 235]
castle_req_keys = {
    129 : { 97 : 81, 161 : 193}, 248 : { 250 : 151, 246 : 244},
    39  : { 37 : 36, 41  : 43},  158 : { 190 : 206, 126 : 94}
}
castle_rep_keys = {
    129 : { 97 : 113, 161 : 145}, 248 : { 250 : 249, 246 : 247},
    39  : { 37 : 38,  41  : 40},  158 : { 190 : 174, 126 : 142}
}
valid_promotion_codes = [1, 2, 3, 4]
promotion_keys = [
    [81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94],  [43,  59,  75,  91,  107, 123, 139, 155, 171, 187, 203, 219, 235, 251],
    [193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206], [36,  52,  68,  84,  100, 116, 132, 148, 164, 180, 196, 212, 228, 244]
]
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

cdef is_threat(from_key, to_key, board):
    """ Detects Piece Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0:
            if data[1] == 0:
                return bool(is_pawn_threat(from_key, to_key, board))
            elif data[1] == 1:
                return bool(is_knight_threat(from_key, to_key, board))
            elif data[1] == 2:
                return bool(is_bishop_threat(from_key, to_key, board))
            elif data[1] == 3:
                return bool(is_rook_threat(from_key, to_key, board))
            elif data[1] == 4:
                return bool(is_queen_threat(from_key, to_key, board))
            else:
                return bool(is_king_threat(from_key, to_key, board))
    return bool(False)

cdef is_pawn_threat(from_key, to_key, board):
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
                return bool(True)
    return bool(False)

cdef is_knight_threat(from_key, to_key, board):
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
                actual_to_key = from_key + direct
                if actual_to_key == to_key:
                    return bool(True)
    return bool(False)

cdef is_bishop_threat(from_key, to_key, board, skip = False):
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
                res = loop_direction(from_key, to_key, board, direct)
                if res == True:
                    return bool(True)
    return bool(False)

cdef is_rook_threat(from_key, to_key, board, skip = False):
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
                res = loop_direction(from_key, to_key, board, direct)
                if res == True:
                    return bool(True)
    return bool(False)

cdef is_queen_threat(from_key, to_key, board):
    """ Detects Queen Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if data != 0 and data[1] == 4:
            return bool(is_bishop_threat(from_key, to_key, board, True) or is_rook_threat(from_key, to_key, board, True))
    return bool(False)

cdef is_king_threat(from_key, to_key, board, enpassants = False):
    """ Detects King Threats """
    if valid_key(from_key) and valid_key(to_key):
        data = board[from_key]
        if enpassants == True or data != 0 and data[1] == 5:
            direction_check = [
                directions[0],
                directions[1],
                directions[2],
                directions[3]
            ]
            if enpassants != True:
                direction_check.append(directions[4])
                direction_check.append(directions[5])
                direction_check.append(directions[6])
                direction_check.append(directions[7])
            for direct in direction_check:
                actual_to_key = from_key + direct
                if actual_to_key == to_key:
                    return bool(True)
    return bool(False)

cdef loop_direction(from_key, to_key, board, direction):
    """ Loops Directions """
    while True:
        from_key += direction
        if valid_key(from_key):
            check = board[from_key]
            if check != 0:
                if from_key != to_key:
                    return False
            if from_key == to_key:
                return bool(True)
        else:
            return bool(False)

cdef get_moves(board, move, castle_rights, enpassants, priorityPiece = False):
    """ Gets A List Of Avaliable Moves """
    ret = []
    for key, square in enumerate(board):
        if square != 0 and square[0] == move:
            if priorityPiece == False or priorityPiece == 0:
                if pawn_start_square(key) and square[1] == 0:
                    if move == 0:
                        directone = key + (directions[0] * 2)
                        directtwo = key + directions[0]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                            if board[directone] == 0:
                                temp_board = board[:]
                                temp_board[directone] = temp_board[key]
                                temp_board[key] = 0
                                if in_check(temp_board, move) == 0:
                                    ret.append([key, directone])
                    elif move == 1:
                        directone = key + (directions[3] * 2)
                        directtwo = key + directions[3]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                            if board[directone] == 0:
                                temp_board = board[:]
                                temp_board[directone] = temp_board[key]
                                temp_board[key] = 0
                                if in_check(temp_board, move) == 0:
                                    ret.append([key, directone])
                    elif move == 2:
                        directone = key + (directions[1] * 2)
                        directtwo = key + directions[1]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                            if board[directone] == 0:
                                temp_board = board[:]
                                temp_board[directone] = temp_board[key]
                                temp_board[key] = 0
                                if in_check(temp_board, move) == 0:
                                    ret.append([key, directone])
                    else:
                        directone = key + (directions[2] * 2)
                        directtwo = key + directions[2]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                            if board[directone] == 0:
                                temp_board = board[:]
                                temp_board[directone] = temp_board[key]
                                temp_board[key] = 0
                                if in_check(temp_board, move) == 0:
                                    ret.append([key, directone])
                elif square[1] == 0:
                    if move == 0:
                        directtwo = key + directions[0]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                    elif move == 1:
                        directtwo = key + directions[3]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                    elif move == 2:
                        directtwo = key + directions[1]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
                    else:
                        directtwo = key + directions[2]
                        if board[directtwo] == 0:
                            temp_board = board[:]
                            temp_board[directtwo] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) == 0:
                                ret.append([key, directtwo])
            if priorityPiece == False or priorityPiece == 5:
                if square[1] == 5 and in_check(board, move) == 0:
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
                                    if is_threat(key_check, local_a, board) or is_threat(key_check, local_b, board):
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
                                    if is_threat(key_check, local_a, board) or is_threat(key_check, local_b, board) or is_threat(key_check, local_c, board):
                                        allow = False
                            if allow == True:
                                ret.append([key, local_b])
            for key_check, square_check in enumerate(board):
                if is_threat(key, key_check, board):
                    if priorityPiece == False or priorityPiece == 0:
                        if square_check == 0:
                            if square[1] == 0:
                                for enpassant_key, enpassant_check in enumerate(enpassants):
                                    if key_check == enpassant_check and not(is_not_opposite_color(enpassant_key, move)):
                                        if move == 0:
                                            hasOpposingPawnKey = key + directions[0]
                                        elif move == 1:
                                            hasOpposingPawnKey = key + directions[3]
                                        elif move == 2:
                                            hasOpposingPawnKey = key + directions[1]
                                        else:
                                            hasOpposingPawnKey = key + directions[2]
                                        accessKey = board[hasOpposingPawnKey]
                                        if accessKey != 0 and accessKey[0] == enpassant_key and accessKey[1] == 0:
                                            ret.append([key, key_check])
                                continue
                    if square_check != 0:
                        if is_not_opposite_color(square[0], square_check[0]):
                            continue
                    skipSection = False
                    if priorityPiece == False or priorityPiece == 5:
                        if square[1] == 5:
                            for threat_key_check in valid_keys:
                                if board[threat_key_check] == 0:
                                    continue
                                check_opposite = board[threat_key_check]
                                if not(is_not_opposite_color(square[0], check_opposite[0])):
                                    if is_threat(threat_key_check, key_check, board):
                                        skipSection = True
                    if priorityPiece == False or square[1] == priorityPiece:
                        if skipSection == False:
                            temp_board = board[:]
                            temp_board[key_check] = temp_board[key]
                            temp_board[key] = 0
                            if in_check(temp_board, move) != 0:
                                continue
                            ret.append([key, key_check])
    return ret

cdef undo(history):
    """ Undo The Position """
    pos = history.pop()
    return [pos, history]

cdef in_checkmate(color, board, castle_rights, enpassants):
    """ Detects Checkmates """
    if in_check(board, color) != 0 and len(get_moves(board, color, castle_rights, enpassants)) == 0:
        return bool(True)
    return bool(False)

cdef in_stalemate(color, board, castle_rights, enpassants):
    """ Detects Stalemates """
    if in_check(board, color) == 0 and len(get_moves(board, color, castle_rights, enpassants)) == 0:
        return bool(True)
    return bool(False)

cdef int in_check(board, color):
    """ Detects Checks """
    ret = 0
    for key, square in enumerate(board):
        if square != 0 and square[0] == color and square[1] == 5:
            for key_check, square_check in enumerate(board):
                if square_check != 0 and not(is_not_opposite_color(color, square_check[0])) and is_threat(key_check, key, board):
                    ret += 1
    return ret

cdef is_draw(color, board, half_moves, castle_rights, enpassants, history):
    """ Detects Draws """
    if half_moves > 49:
        return bool(True)
    if in_stalemate(color, board, castle_rights, enpassants):
        return bool(True)
    start = 0
    for pos in history:
        if pos[0] == color and pos[1] == board:
            start += 1
    if start == 2:
        return bool(True)
    return bool(False)

cdef is_gameover(color, board, half_moves, castle_rights, enpassants, history):
    """ Detects A Final Position """
    if is_draw(color, board, half_moves, castle_rights, enpassants, history):
        return bool(True)
    if in_checkmate(color, board, castle_rights, enpassants):
        return bool(True)
    return bool(False)

cdef valid_key(key):
    """ Checks An Input Key """
    if key in valid_keys:
        return bool(True)
    return bool(False)

cdef is_not_opposite_color(color_one, color_two):
    """ Checks The Opposite Colors """
    if color_one == 0 and color_two == 0 or color_one == 0 and color_two == 2:
        return bool(True)
    if color_one == 1 and color_two == 1 or color_one == 1 and color_two == 3:
        return bool(True)
    if color_one == 2 and color_two == 2 or color_one == 2 and color_two == 0:
        return bool(True)
    if color_one == 3 and color_two == 3 or color_one == 3 and color_two == 1:
        return bool(True)
    return bool(False)

cdef pawn_start_square(key):
    """ Check To See If This Is A Pawn Start Key """
    if key in pawn_start_keys:
        return bool(True)
    return bool(False)

cdef int next_move(color):
    """ Return Who's Next To Move """
    return (color + 1) % 4

cdef is_promotion_key(key, move):
    """ Check To See If This Is A Promotion Key """
    if key in promotion_keys[move]:
        return bool(True)
    return bool(False)

cdef valid_promotion(code):
    """ Check To See If This Is A Valid Promotion Code """
    if code in valid_promotion_codes:
        return bool(True)
    return bool(False)

cdef int evaluate_material(board):
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

cdef int maxi(state, depth, alpha, beta):
    if depth == 0 or state.gameover() == True:
        return evaluate_material(state.board)
    avaliable_actions = state.get_actions()
    doBreak = False
    for action in avaliable_actions:
        newState = state.play_action(action)
        score = mini(newState, depth - 1, alpha, beta)
        if score >= beta:
            alpha = beta
            doBreak = True
        if score > alpha:
            alpha = score
        state = newState.undo_action()
        if doBreak == True:
            break
    return alpha

cdef int mini(state, depth, alpha, beta):
    if depth == 0 or state.gameover() == True:
        return -evaluate_material(state.board)
    avaliable_actions = state.get_actions()
    doBreak = False
    for action in avaliable_actions:
        newState = state.play_action(action)
        score = maxi(newState, depth - 1, alpha, beta)
        if score <= alpha:
            beta = alpha
            doBreak = True
        if score < beta:
            beta = score
        state = newState.undo_action()
        if doBreak == True:
            break
    return beta

class GameState:
    def __init__(self, color, board, half_moves, castle_rights, enpassants, history):
        """ Constructs A New Game State """
        self.board = board
        self.color = color
        self.half_moves = half_moves
        self.castle_rights = castle_rights
        self.enpassants = enpassants
        self.history = history

    def get_actions(self, priority = False):
        """ Gets The Avaliable Actions For This State """
        return get_moves(self.board, self.color, self.castle_rights, self.enpassants, priority)

    def get_best_action(self, depth):
        max = -99999
        min = 99999
        best_action = []
        avaliable_actions = self.get_actions()
        for action in avaliable_actions:
            newState = self.play_action(action)
            if self.color == 0 or self.color == 2:
                score = maxi(newState, depth - 1, -99999, 99999)
                if score > max:
                    best_action = action
                    max = score
            else:
                score = mini(newState, depth - 1, -99999, 99999)
                if score < min:
                    best_action = action
                    min = score
            self = newState.undo_action()
        return best_action

    def play_action(self, action, promotion_code = 4):
        """ Plays The Action And Returns The New Game State """
        skipRest = False
        new_board = self.board[:]
        new_color = next_move(self.color)
        new_castle_rights = self.castle_rights[:]
        new_half_moves = self.half_moves
        new_enpassants = self.enpassants[:]
        new_history = self.history
        if self.board[action[0]][1] == 5 and not(is_king_threat(action[0], action[1], self.board)):
            ext_req = castle_req_keys[action[0]][action[1]]
            ext_rep = castle_rep_keys[action[0]][action[1]]
            new_board[action[1]] = self.board[action[0]]
            new_board[action[0]] = 0
            new_board[ext_req] = 0
            new_board[ext_rep] = [self.color, 3]
            new_castle_rights[self.color][0] = False
            new_castle_rights[self.color][1] = False
            if self.color == 0:
                new_half_moves += 1
            new_enpassants[self.color] = '-'
            skipRest = True
        elif self.board[action[0]][1] == 0:
            if not(is_king_threat(action[0], action[1], self.board, True)):
                if self.color == 0:
                    new_enpassants[self.color] = action[1] + directions[1]
                elif self.color == 1:
                    new_enpassants[self.color] = action[1] + directions[2]
                elif self.color == 2:
                    new_enpassants[self.color] = action[1] + directions[0]
                else:
                    new_enpassants[self.color] = action[1] + directions[3]
            for enpassant_check in new_enpassants:
                if action[1] == enpassant_check:
                    if self.color == 0:
                        direct = action[1] + directions[0]
                    elif self.color == 1:
                        direct = action[1] + directions[3]
                    elif self.color == 2:
                        direct = action[1] + directions[1]
                    else:
                        direct = action[1] + directions[2]
                    new_board[direct] = 0
            if is_promotion_key(action[1], self.color):
                if valid_promotion(promotion_code):
                    new_board[action[0]][1] = promotion_code
        if skipRest == False:
            if self.board[action[1]] != 0 or in_check(self.board, self.color) > 0:
                new_half_moves = 0
            elif self.color == 0:
                new_half_moves += 1
            if self.board[action[0]][1] != 0:
                new_enpassants[self.color] = '-'
            if self.board[action[0]][1] == 5:
                new_castle_rights[self.color][1] = False
                new_castle_rights[self.color][0] = False
            if self.board[action[0]][1] == 3:
                if self.color == 0:
                    if action[0] == 244:
                        new_castle_rights[self.color][1] = False
                    if action[0] == 251:
                        new_castle_rights[self.color][0] = False
                elif self.color == 1:
                    if action[0] == 193:
                        new_castle_rights[self.color][1] = False
                    if action[0] == 81:
                        new_castle_rights[self.color][0] = False
                elif self.color == 2:
                    if action[0] == 43:
                        new_castle_rights[self.color][1] = False
                    if action[0] == 36:
                        new_castle_rights[self.color][0] = False
                else:
                    if action[0] == 94:
                        new_castle_rights[self.color][1] = False
                    if action[0] == 206:
                        new_castle_rights[self.color][0] = False
            new_board[action[1]] = new_board[action[0]]
            new_board[action[0]] = 0
        new_history.append([self.color, self.board, self.half_moves, self.castle_rights, self.enpassants])
        new_state = GameState(new_color, new_board, new_half_moves, new_castle_rights, new_enpassants, new_history)
        return new_state

    def gameover(self):
        """ Checks To See If This Game State Is Final """
        return is_gameover(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants, self.history)

    def undo_action(self):
        """ Undo The Action And Return The Old Game State """
        prev = undo(self.history)
        data = prev[0]
        new_history = prev[1]
        new_state = GameState(data[0], data[1], data[2], data[3], data[4], new_history)
        return new_state

    def render(self):
        """ Render The Board To The Console """
        outputa = outputb = outputc = outputd = outpute = outputf = outputg = outputh = outputi = outputj = outputk = outputl = outputm = outputn = ""
        start_one = "|"
        start_two = "|-----|-----|-----|"
        renderBoard = iter(self.board[:])
        for i in range(36):
            next(renderBoard)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(8):
            value = next(renderBoard)
            if value == 0:
                outputa += "     |"
            else:
                outputa += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_two + outputa + "-----|-----|-----|\n")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(8):
            next(renderBoard)
        for i in range(8):
            value = next(renderBoard)
            if value == 0:
                outputb += "     |"
            else:
                outputb += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_two + outputb + "-----|-----|-----|\n")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(8):
            next(renderBoard)
        for i in range(8):
            value = next(renderBoard)
            if value == 0:
                outputc += "     |"
            else:
                outputc += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_two + outputc + "-----|-----|-----|")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(5):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputd += "     |"
            else:
                outputd += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputd)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outpute += "     |"
            else:
                outpute += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outpute)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputf += "     |"
            else:
                outputf += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputf)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputg += "     |"
            else:
                outputg += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputg)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputh += "     |"
            else:
                outputh += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputh)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputi += "     |"
            else:
                outputi += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputi)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputj += "     |"
            else:
                outputj += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputj)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(2):
            next(renderBoard)
        for i in range(14):
            value = next(renderBoard)
            if value == 0:
                outputk += "     |"
            else:
                outputk += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_one + outputk)
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(5):
            next(renderBoard)
        for i in range(8):
            value = next(renderBoard)
            if value == 0:
                outputl += "     |"
            else:
                outputl += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_two + outputl + "-----|-----|-----|\n")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(8):
            next(renderBoard)
        for i in range(8):
            value = next(renderBoard)
            if value == 0:
                outputm += "     |"
            else:
                outputm += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_two + outputm + "-----|-----|-----|\n")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")
        for i in range(8):
            next(renderBoard)
        for i in range(8):
            value = next(renderBoard)
            if value == 0:
                outputn += "     |"
            else:
                outputn += " " + str(value[0]) + "." + str(value[1]) + " |"
        print(start_two + outputn + "-----|-----|-----|\n")
        print("+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+\n")