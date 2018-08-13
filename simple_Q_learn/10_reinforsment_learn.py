import tensorflow as tf
import numpy as np
import time


from game.Game import *
from game.AIPlayer import *
from game.HumanPlayer import *

quit_key = "q"


# main
print "Controls - left: " + left_key + " right: " + right_key + " quit: " + quit_key
game = Game()
# player = HumanPlayer()
player = AIPlayer(game)

game.reset()

while True:
	game.render()

	pressed_key = player.get_input()
	if pressed_key == quit_key:
		break

	game.send_key(pressed_key)