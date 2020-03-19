import evaluation

maximizer = 99999
minimizer = -maximizer

def minimax(state, is_maximizer = True, depth = 3):
    if is_maximizer == True:
        best_move = []
        best_score = maximizer
    else:
        best_move = []
        best_score = minimizer
    if depth == 0 or state.gameover:
        if state.maximizer_winning == True:
            return maximizer
        elif state.minimizer_winning == True:
            return minimizer
        else:
            return [[], evaluation.evaluate(state.board)]
    avaliable_actions = state.get_actions()
    for action in avaliable_actions:
        newState = state.play_action(action)
        if is_maximizer == True:
            oppo = False
        else:
            oppo = True
        data = minimax(newState, oppo, depth - 1)
        score = data[1]
        if best_move == []:
            best_move == action
        if is_maximizer == True:
            if score > best_score:
                best_move = action
                best_score = score
        else:
            if score < best[1]:
                best_move = action
                best_score = score
        state = newState.undo_action()
    return [best_move, best_score]