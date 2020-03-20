import move
import state
import threat

class GameState:
    def __init__(self, color, board, half_moves, castle_rights, enpassants, history):
        """ Construct A New Game State """
        self.board = board
        self.color = color
        self.half_moves = half_moves
        self.castle_rights = castle_rights
        self.enpassants = enpassants
        self.history = history

    def get_actions(self):
        """ Get The Avaliable Actions """
        return move.get_moves(self.board, self.color, self.castle_rights, self.enpassants)

    def play_action(self, action, promotion_code = 4):
        """ Play The Action """
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
                        direct = threat.directions[0]
                    elif self.color == 1:
                        direct = threat.directions[3]
                    elif self.color == 2:
                        direct = threat.directions[1]
                    else:
                        direct = threat.directions[2]
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

    def is_maximizer(self):
        """ Check To See If The Player Is The Maximizer """
        if self.color == 0 or self.color == 2:
            return True
        return False

    def gameover(self):
        """ Check To See If This Is A Final Position """
        return state.is_gameover(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants, self.history)

    def maximizer_winning(self):
        """ Check To See If The Maximizer Player Is Winning """
        if state.is_draw(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants):
            return False
        elif state.in_checkmate(0, self.board, self.castle_rights, self.enpassants) or state.in_checkmate(2, self.board, self.castle_rights, self.enpassants):
            return False
        else:
            return True

    def minimizer_winning(self):
        """ Check To See If The Minimizer Player Is Winning """
        if state.is_draw(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants):
            return False
        elif state.in_checkmate(1, self.board, self.castle_rights, self.enpassants) or state.in_checkmate(3, self.board, self.castle_rights, self.enpassants):
            return False
        else:
            return True

    def undo_action(self):
        """ Undo The Action """
        prev = move.undo(self.history)
        data = prev[0]
        new_history = prev[1]
        new_state = GameState(data[0], data[1], data[2], data[3], data[4], new_history)
        return new_state

    def render(self):
        """ Render The Board State """
        outputa = ""
        outputb = ""
        outputc = ""
        outputd = ""
        outpute = ""
        outputf = ""
        outputg = ""
        outputh = ""
        outputi = ""
        outputj = ""
        outputk = ""
        outputl = ""
        outputm = ""
        outputn = ""
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
        