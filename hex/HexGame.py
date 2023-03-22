from __future__ import print_function
import numpy as np
from Game import Game
import sys
from collections import deque
sys.path.append('..')

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


class HexGame(Game):
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return HexGame.square_content[piece]

    def __init__(self, n: int = 11):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        return np.zeros((self.n, self.n), dtype=np.int8)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board: np.ndarray, player: int, action: int):
        new_board: np.ndarray = np.copy(board)
        new_board[int(action/self.n), action % self.n] = player
        return (new_board, -player)

    def getValidMoves(self, board: np.ndarray, player: int):
        return np.where(board == _EMPTY, 1, 0).ravel()

    def _out_of_map(self, p: tuple):
        return p[0] < 0 or p[0] >= self.n or p[1] < 0 or p[1] >= self.n

    def _red_player_won(self, board: np.ndarray) -> int:
        # Red won?
        red_queue = deque([(0, y) for y in range(self.n) if board[0, y] == _RED])

        red_visited = np.zeros((11, 11), dtype=np.int8)

        while len(red_queue) > 0:
            r_x, r_y = red_queue.popleft()

            if (r_x == self.n - 1):
                return 1

            red_visited[r_x, r_y] = 1

            for a_x, a_y in _HEX_ADJACENT:
                p = (r_x + a_x, r_y + a_y)
                if (self._out_of_map(p) or red_visited[p]):
                    continue

                if (board[p] == _RED):
                    red_queue.append(p)

        # Blue won?
        blue_queue = deque([(x, 0) for x in range(self.n) if board[x, 0] == _BLUE])

        blue_visited = np.zeros((11, 11), dtype=np.int8)

        while len(blue_queue) > 0:
            b_x, b_y = blue_queue.popleft()

            if (b_y == self.n - 1):
                return -1

            blue_visited[b_x, b_y] = 1

            for a_x, a_y in _HEX_ADJACENT:
                p = (b_x + a_x, b_y + a_y)
                if (self._out_of_map(p) or blue_visited[p]):
                    continue

                if (board[p] == _BLUE):
                    blue_queue.append(p)

        return 0

    def player_won(self, board: np.ndarray, color: int) -> int:
        # return 0 if not ended, 1 if player won, -1 if player lost
        return color * self._red_player_won(board)

    def getGameEnded(self, board: np.ndarray, player: int):
        # return 0 if not ended, 1 if player won, -1 if player lost
        return self.player_won(board, player)

    def getCanonicalForm(self, board: np.ndarray, player: int):
        # return state if player==1, else return -state if player==-1
        if (player == _BLUE):
            return -1 * np.rot90(np.flipud(board), 1)

        return board

    def getSymmetries(self, board: np.ndarray, pi: int):
        # mirror, rotational
        pi_board = np.reshape(pi, (self.n, self.n))

        rotated_board = np.rot90(board, 1)
        rotated_pi = np.rot90(pi_board, 1)

        return [
            (np.rot90(board, 2), np.rot90(pi_board, 2).ravel()),
            (np.fliplr(rotated_board), np.fliplr(rotated_pi).ravel()),
            (np.flipud(rotated_board), np.flipud(rotated_pi).ravel())
        ]

    def stringRepresentation(self, board: np.ndarray):
        return board.tostring()