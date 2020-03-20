import data.tests.move_tests
import data.tests.threat_tests
from game_state import GameState
import random
import minimax

state = GameState(0, data.tests.move_tests.board_xre, 0, [[True, True], [True, True], [True, True], [True, True]], ['-', '-', '-', '-'], [])

state.render()

depth = 3

print("_______________________________________________________________________________________________________")

for i in range(20):
    max = -99999
    min = 99999
    best_action = []
    avaliable_actions = state.get_actions()
    for action in avaliable_actions:
        newState = state.play_action(action)
        if state.color == 0 or state.color == 2:
            score = minimax.maxi(newState, depth - 1, -99999, 99999)
            if score > max:
                best_action = action
                max = score
        else:
            score = minimax.mini(newState, depth - 1, -99999, 99999)
            if score < min:
                best_action = action
                max = score
        state = newState.undo_action()
    state = state.play_action(best_action)
    state.render()
    print("_______________________________________________________________________________________________________")
    