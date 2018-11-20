import numpy as np

#TODO: fix and remove try
try:
	from .GameHistory import GameHistory
	from .nnet.NNet import NNet
except Exception as e:
	pass
try:
	from GameHistory import GameHistory
	from nnet.NNet import NNet
except Exception as e:
	pass


env_name = "game_th"
weights_filename				= 'tmp/dqn_{}_weights.h5f'.format(env_name)



class PlayerAI():
	def __init__(self,game):
		self._game_history = GameHistory(game.state_shape())
		self.game_state_shape = (1,) + self._game_history.shape_with_history
		self.num_actions = game.get_num_actions()
		nnet = NNet( self.game_state_shape, self.num_actions )
		nnet.load_weights(weights_filename)
		self.nnet = nnet

	def get_input(self,game_state):
		self._game_history.put(game_state)
		game_state_with_history = self._game_history.get()
		observation = np.reshape(game_state_with_history,(1,) + self.game_state_shape)
		actions = self.nnet.get_action(observation)
		action = np.argmax(actions)
		return action
		