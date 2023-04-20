import numpy as np
from hex.HexGame import HexGame as Game


class RandomPlayer():
    def __init__(self, game: Game):
        self.game = game

    def play(self, board):
        valids = np.argwhere(self.game.getValidMoves(board, 1) == 1)
        r = np.random.randint(valids.size)
        return valids[r][0]


class StupidPlayer():
    def __init__(self, game: Game):
        self.game = game

    def play(self, board):
        valids = self.game.getValidMoves(board, 1)
        return np.argwhere(valids == 1)[0][0]

class DirectPlayer():
    def __init__(self, game: Game):
        self.game = game
        self.iter = 0

    def play(self, board):
        while (board[self.iter % self.game.n, self.iter // self.game.n] != 0):
            self.iter += 1
            self.iter %= board.size
        return (self.iter % self.game.n) * self.game.n + self.iter // self.game.n


class HumanPlayer():
    def __init__(self, game: Game):
        self.game = game

    def play(self, board):
        Game.display(board, True)
        valid = self.game.getValidMoves(board, 1)
        while True:
            input_move = input("Enter a move (R B e.g. 1 1):")
            input_a = input_move.split(" ")
            if len(input_a) == 2:
                try:
                    x, y = [int(i) for i in input_a]
                    if not self.game.isOutOfMap((x, y)):
                        a = self.game.n * x + y
                        if valid[a]:
                            break
                except:
                    pass

            print('Invalid move')
        return a
