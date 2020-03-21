# This file is part of Fisheater, A strong 4 player chess engine,
# and is released under the "GNU General Public License v3.0". Please see the LICENSE
# file that should have been included as part of this package.
#------------------------------------------------------------------------------------

import conversation
import extras
from game_state import GameState
import requests

beta = "https://4player-beta.chess.com"
main = "https://4player.chess.com"

endpoints = {
    'arrow'  : '{}/bot?token={}&arrows={}',
    'chat'   : '{}/bot?token={}&chat={}',
    'clear'  : '{}/bot?token={}&arrows=clear',
    'play'   : '{}/bot?token={}&play={}',
    'resign' : '{}/bot?token={}&play=R',
    'stream' : '{}/bot?token={}&stream=1',
}
