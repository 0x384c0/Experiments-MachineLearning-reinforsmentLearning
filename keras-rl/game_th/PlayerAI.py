import numpy as np

#TODO: fix and remove try
try:
	from .nnet.NNet import NNet
except Exception as e:
	pass
try:
	from nnet.NNet import NNet
except Exception as e:
	pass


WINDOW_LENGTH = 1
env_name = "game_th"
weights_filename				= 'tmp/dqn_{}_weights.h5f'.format(env_name)



class PlayerAI():
	def __init__(self,game):
		self.game_state_shape = (WINDOW_LENGTH,) + game.state_shape()
		self.num_actions = game.get_num_actions()
		nnet = NNet( self.game_state_shape, self.num_actions )
		nnet.load_weights(weights_filename)
		self.nnet = nnet

	def get_input(self,game_state):
		observation = np.reshape(game_state,(1,) + self.game_state_shape)
		actions = self.nnet.get_action(observation)
		action = np.argmax(actions)
		return action
		