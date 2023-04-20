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

g = HexGame()

# all players
dp = DirectPlayer(g).play
rp = RandomPlayer(g).play


# nnet players
n1 = NNet(g)
n1.load_checkpoint("./temp/", "best.pth.tar")
args1 = dotdict({'numMCTSSims': 50, 'cpuct': 20})
mcts1 = MCTS(g, n1, args1)
def n1p(x): return np.argmax(mcts1.getActionProb(x, temp=0))

n2 = NNet(g, dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10, # Original: 10
    'batch_size': 64,
    'cuda': False,
    'num_channels': 64,
}))
n2.load_checkpoint("./temp/", "best-64-channels.pth.tar")
args2 = dotdict({'numMCTSSims': 50, 'cpuct': 20})
mcts2 = MCTS(g, n2, args2)
def n2p(x): return np.argmax(mcts2.getActionProb(x, temp=0))


arena = Arena.Arena(n1p, dp, g, display=HexGame.display)

print(arena.playGames(6, verbose=True))
