from __future__ import print_function
import numpy as np
from .HexLogic import Board
from Game import Game
import sys
sys.path.append('..')

_RED = 1
_BLUE = -1
_EMPTY = 0


class HexGame(Game):
    square_content = {
        -1: "X",
        +0: "-",
        +1: "O"
    }

    @staticmethod
    def getSquarePiece(piece):
        return HexGame.square_content[piece]

    def __init__(self, n: int):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        return self.n*self.n

    def getNextState(self, board: Board, player: int, action: int):
        b = Board(self.n)
        b.pieces: np.ndarray = np.copy(board)
        move = (int(action/self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    def getValidMoves(self, board: Board, player: int):
        return board.get_legal_moves(player)

    def getGameEnded(self, board: Board, player: int):
        # return 0 if not ended, 1 if player won, -1 if player lost
        return board.player_won(player)

    def getCanonicalForm(self, board: Board, player: int):
        # return state if player==1, else return -state if player==-1
        return player*board

    def getSymmetries(self, board: Board, pi: int):
        # mirror, rotational
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        board: np.ndarray = board.pieces

        rotated_board = np.rot90(board, 1)
        rotated_pi = np.rot90(pi_board, 1)

        return [
            (np.rot90(board, 2), np.rot90(pi_board, 2).ravel()),
            (np.fliplr(rotated_board), np.fliplr(rotated_pi).ravel()),
            (np.flipud(rotated_board), np.flipud(rotated_pi).ravel())
        ]

    def stringRepresentation(self, board):
        return board.tostring()
