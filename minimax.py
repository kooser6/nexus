import evaluation

def maxi(state, depth, alpha, beta):
    if depth == 0 or state.gameover() == True:
        return evaluation.evaluate(state.board)
    avaliable_actions = state.get_actions()
    doBreak = False
    for action in avaliable_actions:
        newState = state.play_action(action)
        score = mini(newState, depth - 1, alpha, beta)
        if score >= beta:
            alpha = beta
            doBreak = True
        if score > alpha:
            alpha = score
        state = newState.undo_action()
        if doBreak == True:
            break
    return alpha

def mini(state, depth, alpha, beta):
    if depth == 0 or state.gameover() == True:
        return -evaluation.evaluate(state.board)
    avaliable_actions = state.get_actions()
    doBreak = False
    for action in avaliable_actions:
        newState = state.play_action(action)
        score = maxi(newState, depth - 1, alpha, beta)
        if score <= alpha:
            beta = alpha
            doBreak = True
        if score < beta:
            beta = score
        state = newState.undo_action()
        if doBreak == True:
            break
    return beta