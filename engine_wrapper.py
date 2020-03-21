# This file is part of Fisheater, A strong 4 player chess engine,
# and is released under the "GNU General Public License v3.0". Please see the LICENSE
# file that should have been included as part of this package.
#------------------------------------------------------------------------------------

class EngineWrapper:
    def __init__(self, board, commands, options = None, silence_stderr = False):
        pass

    def first_search(self, board):
        pass

    def search(self, board, winc, binc):
        pass

    def print_stats(self):
        pass

    def name(self):
        return self.engine.name

    def quit(self):
        self.engine.quit()

    def print_handler_stats(self, info, stats):
        for stat in stats:
            if stat in info:
                print("    {}: {}".format(stat, info[stat]))

    def get_handler_stats(self, info, stats):
        stats_str = []
        for stat in stats:
            if stat in info:
                stats_str.append("{}: {}".format(stat, info[stat]))

        return stats_str
