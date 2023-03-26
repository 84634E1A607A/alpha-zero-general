from __future__ import print_function
import numpy as np
from Game import Game
import sys
from collections import deque
sys.path.append('..')

'''
Author: Ajax Dong
Board class.
Board data:
  1=Red, -1=Blue, 0=Empty

    y
   /
R /
 /
o------> x
   B

board[x][y]
'''

_RED = 1
_BLUE = -1
_EMPTY = 0


_HEX_ADJACENT = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, -1),
    (-1, 1)
]


class HexGame(Game):
    square_content = {
        -1: "b",
        +0: "-",
        +1: "r"
    }

    @staticmethod
    def getSquarePiece(piece):
        return HexGame.square_content[piece]

    def __init__(self, n: int = 11):
        self.n = n
        self.sz = n * n

    def getInitBoard(self):
        # return initial board (numpy board)
        return np.zeros((self.n, self.n), dtype=np.int8)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.sz

    def getNextState(self, board: np.ndarray, player: int, action: int):
        assert board[action // self.n, action % self.n] == 0
        new_board: np.ndarray = np.copy(board)
        new_board[action // self.n, action % self.n] = player
        return (new_board, -player)

    def getValidMoves(self, board: np.ndarray, player: int):
        return np.where(board == _EMPTY, 1, 0).ravel()

    def _out_of_map(self, p: tuple):
        return p[0] < 0 or p[0] >= self.n or p[1] < 0 or p[1] >= self.n

    def _red_player_won(self, board: np.ndarray) -> int:
        # Red won?
        red_queue = deque([(0, y)
                          for y in range(self.n) if board[0, y] == _RED])

        red_visited = np.zeros((11, 11), dtype=np.int8)

        while len(red_queue) > 0:
            r_x, r_y = red_queue.popleft()

            red_visited[r_x, r_y] = 1

            for a_x, a_y in _HEX_ADJACENT:
                p = (r_x + a_x, r_y + a_y)
                if (self._out_of_map(p) or red_visited[p]):
                    continue

                if (board[p] == _RED):
                    if (p[0] == self.n - 1):
                        return 1

                    red_queue.append(p)

        # Blue won?
        blue_queue = deque([(x, 0)
                           for x in range(self.n) if board[x, 0] == _BLUE])

        blue_visited = np.zeros((11, 11), dtype=np.int8)

        while len(blue_queue) > 0:
            b_x, b_y = blue_queue.popleft()

            blue_visited[b_x, b_y] = 1

            for a_x, a_y in _HEX_ADJACENT:
                p = (b_x + a_x, b_y + a_y)
                if (self._out_of_map(p) or blue_visited[p]):
                    continue

                if (board[p] == _BLUE):
                    if (p[1] == self.n - 1):
                        return -1

                    blue_queue.append(p)

        return 0

    def _player_won(self, board: np.ndarray, player: int) -> int:
        # return 0 if not ended, 1 if player won, -1 if player lost
        return player * self._red_player_won(board)

    def getGameEnded(self, board: np.ndarray, player: int):
        # return 0 if not ended, 1 if player won, -1 if player lost
        e = self._player_won(board, player)

        return e

    def getCanonicalForm(self, board: np.ndarray, player: int):
        # return state if player==1, else return -state if player==-1
        if (player == _BLUE):
            return -np.flipud(np.rot90(board, 1))

        return board
    
    def getActionCanonicalForm(self, action: int, player: int):
        if (player == _BLUE):
            x, y = action // self.n, action % self.n
            return self.n * y + x

        return action

    def getSymmetries(self, board: np.ndarray, pi: int):
        # only one rotational
        pi_board = np.reshape(pi, (self.n, self.n))

        return [(np.rot90(board, 2), np.rot90(pi_board, 2).ravel())]

    def stringRepresentation(self, board: np.ndarray):
        return board.tostring()

    def display(self, board: np.ndarray):
        n = self.n
        print(" " * (n + 1) + "B\n", end="")
        for y in range(n - 1, -1, -1):
            print(" " * (y + 1) + "/", end="")
            for x in range(n):
                print(" " + HexGame.getSquarePiece(board[x, y]), end="")

            print("\n", end="")

        print("O" + "-" * 2 * n + "R\n\n", end="")
