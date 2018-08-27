from keras.models import Sequential
from keras.layers import Dense, Flatten, Activation, Permute, Conv2D

HIDDEN_SIZE = 512

class NNet():
	def __init__(self,input_shape,nb_actions): # self.game.state_shape() , game.get_num_ actions()

		model = Sequential()
		# (channels, width, height)
		model.add(Conv2D(filters=32, kernel_size=(8, 8), strides=(4, 4) , input_shape=input_shape, data_format='channels_first', name="INPUTS"))
		model.add(Activation('relu'))
		model.add(Conv2D(filters=64, kernel_size=(4, 4), strides=(2, 2)))
		model.add(Activation('relu'))
		model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1)))
		model.add(Activation('relu'))
		model.add(Flatten())
		model.add(Dense(HIDDEN_SIZE))
		model.add(Activation('relu'))
		model.add(Dense(nb_actions, name="OUTPUTS"))
		model.add(Activation('linear'))

		self.model = model

	def load_weights(self,file_name):
		self.model.load_weights(file_name)

	def get_action(self,observation):
		return self.model.predict(observation)
