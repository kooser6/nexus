import data.tests.move_tests
from game_state import GameState
import random
import minimax

state = GameState(0, data.tests.move_tests.board_xre, 0, [[True, True], [True, True], [True, True], [True, True]], ['-', '-', '-', '-'], [])

state.render()

depth = 1

print("_______________________________________________________________________________________________________")

for i in range(32):
    best = [[], '-']
    if state.is_maximizer == True:
        best_score = minimax.maximizer
    else:
        best_score = minimax.minimizer
    avaliable_actions = state.get_actions()
    for action in avaliable_actions:
        newState = state.play_action(action)
        if state.is_maximizer == True:
            oppo = False
        else:
            oppo = True
        data = minimax.minimax(newState, depth - 1, oppo)
        score = data[1]
        if best[0] == []:
            best[0] == action
        if state.is_maximizer == True:
            if score > best_score:
                best = [action, score]
        else:
            if score < best_score:
                best = [action, score]
        state = newState.undo_action()
    state = state.play_action(best[0])
    state.render()
    print("_______________________________________________________________________________________________________")
    print("Eval: " + str(best[1]))
    print("_______________________________________________________________________________________________________")
    