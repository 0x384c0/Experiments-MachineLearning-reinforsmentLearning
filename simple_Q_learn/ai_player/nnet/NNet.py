import glob
import os
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Conv2D
from keras.optimizers import Adam,sgd

HIDDEN_SIZE = 100
chenckpoint_file = "tmp/AIPlayer_weights.h5"

class NNet():
	def __init__(self,input_shape,num_actions): # self.game.state_shape() , game.get_num_ actions()
		self.input_shape = input_shape
		self.num_actions = num_actions

		model = Sequential()
		model.add(Dense(HIDDEN_SIZE, input_shape=self.input_shape, activation='relu', name="INPUTS"))
		model.add(Flatten())
		model.add(Dense(HIDDEN_SIZE, activation='relu'))
		model.add(Dense(self.num_actions, name="OUTPUTS"))
		model.compile(sgd(lr=.1), "mse")

		self.model = model

	def predict(self,batch):
		return self.model.predict(batch)

	def train_on_batch(self, inputs, targets):
		self.model.train_on_batch(inputs, targets)

	def load(self):
		if not os.path.exists("tmp"):
			os.makedirs("tmp")
		if glob.glob(chenckpoint_file + "*"):
			self.model.load_weights(chenckpoint_file)
			print("Model state loaded from file: %s" % chenckpoint_file)

	def save(self):
		self.model.save_weights(chenckpoint_file)
		print("Model state saved in file: %s" % chenckpoint_file)
