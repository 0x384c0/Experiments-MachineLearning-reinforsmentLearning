import sys
sys.path.append('..')

from helpers.helper_keyboard import getch

class HumanPlayer():
	def get_input(self):
		return getch()

