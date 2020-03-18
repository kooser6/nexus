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
        new_half_moves = self.half_moves[:]
        new_enpassants = self.enpassants[:]
        if self.board[action[0]] == 5 and not(threat.is_king_threat(action[0], action[1], board)):
            ext_req = move.castle_req_keys[action[0]][action[1]]
            ext_rep = move.castle_rep_keys[action[0]][action[1]]
            new_board[action[1]] = self.board[action[0]]
            new_board[action[0]] = 0
            new_board[req] = 0
            new_board[rep] = [self.color, 3]
            new_castle_rights[self.color][0] = False
            new_castle_rights[self.color][1] = False
            if self.color == 0:
                new_half_moves += 1
            new_enpassants[self.color] = '-'
            skipRest = True
        elif self.board[action[0]] == 0:
            temp_board = self.board[:]
            temp_board[action[0]][1] = 5
            if not(threat.is_king_threat(action[0], action[1], temp_board)):
                if move == 0:
                    new_enpassants[self.color] = action[1] + threat.directions[1]
                elif move == 1:
                    new_enpassants[self.color] = action[1] + threat.directions[2]
                elif move == 2:
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
            if is_promotion_key(to_key, move):
                if valid_promotion(promotion_code):
                    new_board[action[0]][1] = promotion_code
        if skipRest = False
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
                        new_castle_rights[move][1] = False
                    if action[0] == 251:
                        new_castle_rights[move][0] = False
                elif self.color == 1:
                    if action[0] == 193:
                        new_castle_rights[move][1] = False
                    if action[0] == 81:
                        new_castle_rights[move][0] = False
                elif self.color == 2:
                    if action[0] == 43:
                        new_castle_rights[move][1] = False
                    if action[0] == 36:
                        new_castle_rights[move][0] = False
                else:
                    if action[0] == 94:
                        new_castle_rights[move][1] = False
                    if action[0] == 206:
                        new_castle_rights[move][0] = False
            new_board[action[1]] = new_board[action[0]]
            new_board[action[0]] = 0
        new_history.append([self.color, self.board, self.half_moves, self.castle_rights, self.enpassants])
        new_state = GameState(new_color, new_board, new_half_moves, new_castle_rights, new_enpassants, new_history)
        return new_state

    def gameover(self):
        """ Check To See If This Is A Final Position """
        return state.is_gameover(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants)

    def undo_action(self):
        """ Undo The Action """
        prev = move.undo(self.history)
        data = prev[0]
        new_history = prev[1]
        new_state = GameState(data[0], data[1], data[2], data[3], data[4], new_history)
        return new_state