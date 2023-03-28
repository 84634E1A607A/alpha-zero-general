import Arena
from MCTS import MCTS
from hex.HexGame import HexGame
from hex.HexPlayers import *
from hex.pytorch.NNet import NNetWrapper as NNet


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = HexGame(7)

# all players
rp = DirectPlayer(g).play


# nnet players
n1 = NNet(g)
n1.load_checkpoint("./temp/", "best.pth.tar")
args1 = dotdict({'numMCTSSims': 50, 'cpuct': 20})
mcts1 = MCTS(g, n1, args1)
def n1p(x): return np.argmax(mcts1.getActionProb(x, temp=0))


arena = Arena.Arena(n1p, rp, g, display=HexGame.display)

print(arena.playGames(2, verbose=True))
