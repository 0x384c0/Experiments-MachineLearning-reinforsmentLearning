import tensorflow as tf
import numpy as np
import time

from helpers.utils import *
from ai_player.AIPlayer import AIPlayer

# from game.Game import Game
# from game.nnet.NNet import NNet
# from game.HumanPlayer import HumanPlayer

from game_th.Game import Game
from game_th.nnet.NNet import NNet
from game.HumanPlayer import HumanPlayer


# TRAIN = True
TRAIN = is_train_mode()
HUMAN_PLAYER = is_human_player_mode()

game = Game()
player = HumanPlayer() if HUMAN_PLAYER else AIPlayer(game,NNet)

game.print_controls()
game.reset()

while True:
	game.render()
	if TRAIN:
		pressed_key = player.train_and_get_input()
	else:
		pressed_key = player.get_input()
	game.send_key(pressed_key)
