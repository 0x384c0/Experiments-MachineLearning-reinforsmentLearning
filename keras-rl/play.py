import time
from helpers.utils import *

from game_th.Game import Game
from game_th.PlayerHuman import PlayerHuman
from game_th.PlayerAI import PlayerAI


HUMAN_PLAYER = is_human_player_mode()

game = Game()
player = PlayerHuman(game) if HUMAN_PLAYER else PlayerAI(game)

game.print_controls()
game.reset()

while True:
	time.sleep(0.01)
	game.render()
	pressed_key_id = player.get_input(game.get_state())
	game.send_key(pressed_key_id)