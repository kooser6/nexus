# This file is part of Fisheater, A strong 4 player chess engine,
# and is released under the "GNU General Public License v3.0". Please see the LICENSE
# file that should have been included as part of this package.
#------------------------------------------------------------------------------------

from game_state import GameState
import move
import threat

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
        if c_state_ks == "0":
            castle_rt[sc_qs].append(False)
        else:
            castle_rt[sc_qs].append(True)
        sc_qs = move.next_move(sc_qs)
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
                    board_xre[threat.valid_keys[start]] = 0
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
                board_xre[threat.valid_keys[start]] = piece_col
                start += 1
        rank_locator += 1
    state = GameState(cl, board_xre, hf_mv, castle_rt, enpa, history)
    return state
