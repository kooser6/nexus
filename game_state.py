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

    def play_action(self, action):
        """ Play The Action """
        """                       """
        """ Preform New Move Here """
        """                       """
        newState = GameState(newColor, newBoard, newHalfMoves, newCastleRights, newEnpassants)

    def gameover(self):
        """ Check To See If This Is A Final Position """
        return state.is_gameover(self.color, self.board, self.half_moves, self.castle_rights, self.enpassants)