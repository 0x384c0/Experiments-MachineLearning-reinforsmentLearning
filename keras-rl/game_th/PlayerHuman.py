from helpers.helper_keyboard import getch

class PlayerHuman():

	def __init__(self,game):
		self.game = game 


	def get_input(self,game_state):
		pressed_key = getch()

		if pressed_key == "q":
			self.game.stop() # stty sane
			exit()

		action_id = self.game.action_id_for_action(pressed_key)
		return action_id

