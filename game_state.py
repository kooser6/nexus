import move
import state
import threat

class GameState:
    def __init__(self, color, board, half_moves, castle_rights, enpassants):
		self.board = board
		self.color = color
        self.half_moves = half_moves
        self.castle_rights = castle_rights
        self.enpassants = enpassants

    def get_actions(self):
		return move.get_moves(self.color, self.board, self.castle_rights, self.enpassants)