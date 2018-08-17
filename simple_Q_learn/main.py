import tensorflow as tf
import numpy as np
import time

from helpers.utils import *
from game_th.Game import Game
# from game.Game import Game
from ai_player.AIPlayer import AIPlayer
from game.HumanPlayer import HumanPlayer


# TRAIN = True
TRAIN = is_train_mode()

game = Game()
player = HumanPlayer() if is_human_player_mode() else AIPlayer(game)

game.print_controls()
game.reset()

while True:
	game.render()
	if TRAIN:
		pressed_key = player.train_and_get_input()
	else:
		pressed_key = player.get_input()
	game.send_key(pressed_key)
