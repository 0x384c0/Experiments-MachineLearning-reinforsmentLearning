import sys
sys.path.append('..')

from utils.helper_keyboard import getch

class HumanPlayer():
	def get_input(self):
		return getch()

