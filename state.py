# This file is part of Fisheater, A strong 4 player chess engine,
# and is released under the "GNU General Public License v3.0". Please see the LICENSE
# file that should have been included as part of this package.
#------------------------------------------------------------------------------------

import move
import threat

def in_checkmate(color, board, castle_rights, enpassants):
    """ Detect Checkmates """
    if in_check(board, color) != 0 and len(move.get_moves(board, color, castle_rights, enpassants)) == 0:
        return True
    return False

def in_stalemate(color, board, castle_rights, enpassants):
    """ Detect Stalemates """
    if in_check(board, color) == 0 and len(move.get_moves(board, color, castle_rights, enpassants)) == 0:
        return True
    return False

def in_check(board, color):
    """ Checks If A Color Is In Check """
    ret = 0
    for key, square in enumerate(board):
        if square != 0 and square[0] == color and square[1] == 5:
            for key_check, square_check in enumerate(board):
                if square_check != 0 and not(move.is_not_opposite_color(color, square_check[0])) and threat.is_threat(key_check, key, board):
                    ret += 1
    return ret

def is_draw(color, board, half_moves, castle_rights, enpassants, history):
    """ Check To See If The Position Is A Draw """
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
    """ Check To See If The Position Is Over """
    if is_draw(color, board, half_moves, castle_rights, enpassants, history):
        return True
    if in_checkmate(color, board, castle_rights, enpassants):
        return True
    return False
