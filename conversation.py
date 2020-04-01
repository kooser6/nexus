import random
import requests
import nexus

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

def in_checkmate(color, board, castle_rights, enpassants):
    """ Detects Checkmates """
    if in_check(board, color) != 0 and len(get_moves(board, color, castle_rights, enpassants)) == 0:
        return True
    return False

    """ Detects Stalemates """
def in_stalemate(color, board, castle_rights, enpassants):
    if in_check(board, color) == 0 and len(get_moves(board, color, castle_rights, enpassants)) == 0:
        return True
    return False

def in_check(board, color):
    """ Detects Checks """
    ret = 0
    for key, square in enumerate(board):
        if square != 0 and square[0] == color and square[1] == 5:
            for key_check, square_check in enumerate(board):
                if square_check != 0 and not(is_not_opposite_color(color, square_check[0])) and is_threat(key_check, key, board):
                    ret += 1
    return ret

def is_draw(color, board, half_moves, castle_rights, enpassants, history):
    """ Detects Draws """
    if half_moves == 50:
        return True
    if in_stalemate(color, board, castle_rights, enpassants):
        return True
    start = 0
    for pos in history:
        if pos[0] == color and pos[1] == board:
            start += 1
    if start == 2:
        return True
    return False

def is_gameover(color, board, half_moves, castle_rights, enpassants, history):
    """ Detects A Final Position """
    if is_draw(color, board, half_moves, castle_rights, enpassants, history):
        return True
    if in_checkmate(color, board, castle_rights, enpassants):
        return True
    return False

pawn_start_keys = [
    52,  53,  54,  55,  56,  57,  58,  59,  82,  98,  114, 130, 146, 162, 178, 194,
    93,  109, 125, 141, 157, 173, 189, 205, 228, 229, 230, 231, 232, 233, 234, 235
]
castle_req_keys = {
    129 : { 97  : 81,  161 : 193}, 248 : { 250 : 151, 246 : 244},
    39  : { 37  : 36,  41  : 43},  158 : { 190 : 206, 126 : 94}
}
castle_rep_keys = {
    129 : { 97  : 113, 161 : 145}, 248 : { 250 : 249, 246 : 247},
    39  : { 37  : 38,  41  : 40},  158 : { 190 : 174, 126 : 142}
}
valid_promotion_codes = [1, 2, 3, 4]
promotion_keys = [
    [81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94],
    [43,  59,  75,  91,  107, 123, 139, 155, 171, 187, 203, 219, 235, 251],
    [193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206],
    [36,  52,  68,  84,  100, 116, 132, 148, 164, 180, 196, 212, 228, 244]
]

def undo(history):
    """ Undo The Position """
    pos = history.pop()
    return [pos, history]

def get_moves(board, move, castle_rights, enpassants, priorityPiece = False):
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

def is_not_opposite_color(color_one, color_two):
    """ Checks The Opposite Colors """
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
    """ Check To See If This Is A Pawn Start Key """
    if key in pawn_start_keys:
        return True
    return False

def next_move(color):
    """ Return Who's Next To Move """
    return (color + 1) % 4

def is_promotion_key(key, move):
    """ Check To See If This Is A Promotion Key """
    if key in promotion_keys[move]:
        return True
    return False

def valid_promotion(code):
    """ Check To See If This Is A Valid Promotion Code """
    if code in valid_promotion_codes:
        return True
    return False

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
        return move.get_moves(self.board, self.color, self.castle_rights, self.enpassants, priority)

    def play_action(self, action, promotion_code = 4):
        """ Plays The Action And Returns The New Game State """
        skipRest = False
        new_board = self.board[:]
        new_color = move.next_move(self.color)
        new_castle_rights = self.castle_rights[:]
        new_half_moves = self.half_moves
        new_enpassants = self.enpassants[:]
        new_history = self.history
        if self.board[action[0]][1] == 5 and not(threat.is_king_threat(action[0], action[1], self.board)):
            ext_req = move.castle_req_keys[action[0]][action[1]]
            ext_rep = move.castle_rep_keys[action[0]][action[1]]
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
            if not(threat.is_not_enpassant_pawn_move(action[0], action[1], self.board)):
                if self.color == 0:
                    new_enpassants[self.color] = action[1] + threat.directions[1]
                elif self.color == 1:
                    new_enpassants[self.color] = action[1] + threat.directions[2]
                elif self.color == 2:
                    new_enpassants[self.color] = action[1] + threat.directions[0]
                else:
                    new_enpassants[self.color] = action[1] + threat.directions[3]
            for enpassant_check in new_enpassants:
                if action[1] == enpassant_check:
                    if self.color == 0:
                        direct = action[1] + threat.directions[0]
                    elif self.color == 1:
                        direct = action[1] + threat.directions[3]
                    elif self.color == 2:
                        direct = action[1] + threat.directions[1]
                    else:
                        direct = action[1] + threat.directions[2]
                    new_board[direct] = 0
            if move.is_promotion_key(action[1], self.color):
                if move.valid_promotion(promotion_code):
                    new_board[action[0]][1] = promotion_code
        if skipRest == False:
            if self.board[action[1]] != 0:
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
        return state.is_gameover(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants, self.history)

    def undo_action(self):
        """ Undo The Action And Return The Old Game State """
        prev = move.undo(self.history)
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

coordinates = [[
                         'd14', 'e14', 'f14', 'g14', 'h14', 'i14', 'j14', 'k14',
                         'd13', 'e13', 'f13', 'g13', 'h13', 'i13', 'j13', 'k13',
                         'd12', 'e12', 'f12', 'g12', 'h12', 'i12', 'j12', 'k12',
    'a11', 'b11', 'c11', 'd11', 'e11', 'f11', 'g11', 'h11', 'i11', 'j11', 'k11', 'l11', 'm11', 'n11',
    'a10', 'b10', 'c10', 'd10', 'e10', 'f10', 'g10', 'h10', 'i10', 'j10', 'k10', 'l10', 'm10', 'n10',
    'a9',  'b9',  'c9',  'd9',  'e9',  'f9',  'g9',  'h9',  'i9',  'j9',  'k9',  'l9',  'm9',  'n9',
    'a8',  'b8',  'c8',  'd8',  'e8',  'f8',  'g8',  'h8',  'i8',  'j8',  'k8',  'l8',  'm8',  'n8',
    'a7',  'b7',  'c7',  'd7',  'e7',  'f7',  'g7',  'h7',  'i7',  'j7',  'k7',  'l7',  'm7',  'n7',
    'a6',  'b6',  'c6',  'd6',  'e6',  'f6',  'g6',  'h6',  'i6',  'j6',  'k6',  'l6',  'm6',  'n6',
    'a5',  'b5',  'c5',  'd5',  'e5',  'f5',  'g5',  'h5',  'i5',  'j5',  'k5',  'l5',  'm5',  'n5',
    'a4',  'b4',  'c4',  'd4',  'e4',  'f4',  'g4',  'h4',  'i4',  'j4',  'k4',  'l4',  'm4',  'n4',
                         'd3',  'e3',  'f3',  'g3',  'h3',  'i3',  'j3',  'k3',
                         'd2',  'e2',  'f2',  'g2',  'h2',  'i2',  'j2',  'k2',
                         'd1',  'e1',  'f1',  'g1',  'h1',  'i1',  'j1',  'k1',
], {
                                           'd14' : 36,  'e14' : 37,  'f14' : 38,  'g14' : 39,  'h14' : 40,  'i14' : 41,  'j14' : 42,  'k14' : 43,
                                           'd13' : 52,  'e13' : 53,  'f13' : 54,  'g13' : 55,  'h13' : 56,  'i13' : 57,  'j13' : 58,  'k13' : 59,
                                           'd12' : 68,  'e12' : 69,  'f12' : 70,  'g12' : 71,  'h12' : 72,  'i12' : 73,  'j12' : 74,  'k12' : 75,
    'a11' : 81,  'b11' : 82,  'c11' : 83,  'd11' : 84,  'e11' : 85,  'f11' : 86,  'g11' : 87,  'h11' : 88,  'i11' : 89,  'j11' : 90,  'k11' : 91,  'l11' : 92,  'm11' : 93,  'n11' : 94,
    'a10' : 97,  'b10' : 98,  'c10' : 99,  'd10' : 100, 'e10' : 101, 'f10' : 102, 'g10' : 103, 'h10' : 104, 'i10' : 105, 'j10' : 106, 'k10' : 107, 'l10' : 108, 'm10' : 109, 'n10' : 110,
    'a9'  : 113, 'b9'  : 114, 'c9'  : 115, 'd9'  : 116, 'e9'  : 117, 'f9'  : 118, 'g9'  : 119, 'h9'  : 120, 'i9'  : 121, 'j9'  : 122, 'k9'  : 123, 'l9'  : 124, 'm9'  : 125, 'n9'  : 126,
    'a8'  : 129, 'b8'  : 130, 'c8'  : 131, 'd8'  : 132, 'e8'  : 133, 'f8'  : 134, 'g8'  : 135, 'h8'  : 136, 'i8'  : 137, 'j8'  : 138, 'k8'  : 139, 'l8'  : 140, 'm8'  : 141, 'n8'  : 142,
    'a7'  : 145, 'b7'  : 146, 'c7'  : 147, 'd7'  : 148, 'e7'  : 149, 'f7'  : 150, 'g7'  : 151, 'h7'  : 152, 'i7'  : 153, 'j7'  : 154, 'k7'  : 155, 'l7'  : 156, 'm7'  : 157, 'n7'  : 158,
    'a6'  : 161, 'b6'  : 162, 'c6'  : 163, 'd6'  : 164, 'e6'  : 165, 'f6'  : 166, 'g6'  : 167, 'h6'  : 168, 'i6'  : 169, 'j6'  : 170, 'k6'  : 171, 'l6'  : 172, 'm6'  : 173, 'n6'  : 174,
    'a5'  : 177, 'b5'  : 178, 'c5'  : 179, 'd5'  : 180, 'e5'  : 181, 'f5'  : 182, 'g5'  : 183, 'h5'  : 184, 'i5'  : 185, 'j5'  : 186, 'k5'  : 187, 'l5'  : 188, 'm5'  : 189, 'n5'  : 190,
    'a4'  : 193, 'b4'  : 194, 'c4'  : 195, 'd4'  : 196, 'e4'  : 197, 'f4'  : 198, 'g4'  : 199, 'h4'  : 200, 'i4'  : 201, 'j4'  : 202, 'k4'  : 203, 'l4'  : 204, 'm4'  : 205, 'n4'  : 206,
                                           'd3'  : 212, 'e3'  : 213, 'f3'  : 214, 'g3'  : 215, 'h3'  : 216, 'i3'  : 217, 'j3'  : 218, 'k3'  : 219,
                                           'd2'  : 228, 'e2'  : 229, 'f2'  : 230, 'g2'  : 231, 'h2'  : 232, 'i2'  : 233, 'j2'  : 234, 'k2'  : 235,
                                           'd1'  : 244, 'e1'  : 245, 'f1'  : 246, 'g1'  : 247, 'h1'  : 248, 'i1'  : 249, 'j1'  : 250, 'k1'  : 251
}]
board_xre = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, [2, 3], [2, 1], [2, 2], [2, 5], [2, 4], [2, 2], [2, 1], [2, 3], 0, 0, 0, 0,
    0, 0, 0, 0, [2, 0], [2, 0], [2, 0], [2, 0], [2, 0], [2, 0], [2, 0], [2, 0], 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, [1, 3], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 3], 0,
    0, [1, 1], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 1], 0,
    0, [1, 2], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 2], 0,
    0, [1, 5], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 4], 0,
    0, [1, 4], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 5], 0,
    0, [1, 2], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 2], 0,
    0, [1, 1], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 1], 0,
    0, [1, 3], [1, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, [3, 0], [3, 3], 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], 0, 0, 0, 0,
    0, 0, 0, 0, [0, 3], [0, 1], [0, 2], [0, 4], [0, 5], [0, 2], [0, 1], [0, 3], 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

def represents_int(the_int):
    """ Check To See If A Variable Represents An Int """
    try: 
        int(the_int)
        return True
    except ValueError:
        return False

def parseFenAndReturnGameState(fen = ""):
    """ Parse The Fen And Get The Game State """
    parts = fen.split("-")
    castle_rt = [[], [], [], []]
    cl = parts[0]
    ks = parts[2]
    qs = parts[3]
    ks = ks.split(",")
    qs = qs.split(",")
    sc_ks = sc_qs = hf_mv = board_arr_key = start = 0
    for c_state_ks in ks:
        if c_state_ks == "0":
            castle_rt[sc_ks].append(False)
        else:
            castle_rt[sc_ks].append(True)
        sc_ks = move.next_move(sc_ks)
    for c_state_qs in qs:
        if c_state_qs == "0":
            castle_rt[sc_qs].append(False)
        else:
            castle_rt[sc_qs].append(True)
        sc_qs = next_move(sc_qs)
    enpa = history = []
    chmk = parts[6]
    chep = chmk.split(":")
    if chep[0] == "{'enPassant'":
        enpy = chmk.split("(")
        enpy = enpy[1].split(")")
        enpy = enpy[0]
        enpy = enpy.split(",")
        if enpy[0] == "''":
            enpa.append("-")
        else:
            enpa.append(coordinates[1][enpy[0].strip("'")])
        if enpy[1] == "''":
            enpa.append("-")
        else:
            enpa.append(coordinates[1][enpy[1].strip("'")])
        if enpy[2] == "''":
            enpa.append("-")
        else:
            enpa.append(coordinates[1][enpy[2].strip("'")])
        if enpy[3] == "''":
            enpa.append("-")
        else:
            enpa.append(coordinates[1][enpy[3].strip("'")])
        board_arr_key = 7
    else:
        board_arr_key = 6
    board = parts[board_arr_key]
    ranks = board.split("/")
    rank_locator = 0
    for rank in ranks:
        sqrss = rank.split(",")
        if rank_locator == 0 or rank_locator == 1 or rank_locator == 2 or rank_locator == 11 or rank_locator == 12 or rank_locator == 13:
            last = len(sqrss) - 1
            addi = int(sqrss[last]) - 3
            sqrss[last] = addi
            addi = int(sqrss[0]) - 3
            sqrss[0] = addi
        for key, squar in enumerate(sqrss):
            if represents_int(squar) == True:
                for i in range(int(squar)):
                    board_xre[valid_keys[start]] = 0
                    start += 1
            else:
                piece_col = [0, 0]
                if squar[0] == 'r':
                    piece_col[0] = 0
                elif squar[0] == 'b':
                    piece_col[0] = 1
                elif squar[0] == 'y':
                    piece_col[0] = 2
                else:
                    piece_col[0] = 3
                if squar[1] == 'P':
                    piece_col[1] = 0
                elif squar[1] == 'N':
                    piece_col[1] = 1
                elif squar[1] == 'B':
                    piece_col[1] = 2
                elif squar[1] == 'R':
                    piece_col[1] = 3
                elif squar[1] == 'Q':
                    piece_col[1] = 4
                else:
                    piece_col[1] = 5
                board_xre[valid_keys[start]] = piece_col
                start += 1
        rank_locator += 1
    state = GameState(cl, board_xre, hf_mv, castle_rt, enpa, history)
    return state

import nexus