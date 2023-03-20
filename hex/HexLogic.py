import numpy as np
from queue import Queue

_RED = 1
_BLUE = -1
_EMPTY = 0

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

_HEX_ADJACENT = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (1, -1),
    (-1, 1)
]


def add(p1: tuple, p2: tuple):
    return (p1[0]+p2[0], p1[1]+p2[1])


class Board():
    pieces: np.ndarray

    def __init__(self, n: int = 11):
        """Set up initial board configuration.

        n: Size of the board
        """

        self.n = n

        # Create the empty board array.
        self.pieces = np.zeros((n, n))

    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self, color: int):
        """Returns all the legal moves for the given color.
        """

        return np.where(self.pieces == _EMPTY, 1, 0)

    def execute_move(self, move: tuple(int, int), color: int):
        """Perform the given move on the board
        """

        self.pieces[move] = color

    def _out_of_map(self, p: tuple):
        return tuple[0] < 0 or tuple[0] >= self.n or tuple[1] < 0 or tuple[1] >= self.n

    def _red_player_won(self) -> int:
        # Red won?
        red_queue = Queue()

        for y in range(self.n):
            if self.pieces[0, y] == _RED:
                red_queue.put((0, y))

        red_visited = np.zeros((11, 11))

        while len(red_queue) != 0:
            red_point = red_queue.pop()

            if (red_point[0] == self.n - 1):
                return 1

            red_visited[red_point] = 1

            for adjacent in _HEX_ADJACENT:
                p = add(red_point, adjacent)
                if (self._out_of_map(p) or red_visited[p]):
                    continue

                if (self.pieces[p] == _RED):
                    red_queue.put(p)

        # Blue won?
        blue_queue = Queue()

        for x in range(self.n):
            if self.pieces[x, 0] == _BLUE:
                blue_queue.put((x, 0))

        blue_visited = np.zeros((11, 11))

        while len(blue_queue) != 0:
            blue_point = blue_queue.pop()

            if (blue_point[1] == self.n - 1):
                return -1

            blue_visited[blue_point] = 1

            for adjacent in _HEX_ADJACENT:
                p = add(blue_point, adjacent)
                if (self._out_of_map(p) or blue_visited[p]):
                    continue

                if (self.pieces[p] == _BLUE):
                    blue_queue.put(p)

        return 0

    def player_won(self, color: int) -> int:
        # return 0 if not ended, 1 if player won, -1 if player lost
        return color * self._red_player_won()
