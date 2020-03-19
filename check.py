import data.tests.move_tests
from game_state import GameState
import random

state = GameState(0, data.tests.move_tests.board_xre, 0, [[True, True], [True, True], [True, True], [True, True]], ['-', '-', '-', '-'], [])
state.render()

print("_______________________________________________________________________________________________________")

for i in range(32):
    actions = state.get_actions()
    state = state.play_action(actions[random.randint(0, len(actions) - 1)])
    state.render()
    print("_______________________________________________________________________________________________________")
    