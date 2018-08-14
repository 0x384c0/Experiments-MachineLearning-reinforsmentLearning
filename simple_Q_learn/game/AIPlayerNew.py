# -*- coding: utf-8 -*-
BATCH_SIZE = 50
MAX_MEMORY = 500
HIDDEN_SIZE = 100
MAX_ITERATIONS = 5000
TRAIN = True
# TRAIN = False

import sys
sys.path.append('..')

def single_batch(data):
	return np.expand_dims(data, axis=0)

import numpy as np
class ExperienceReplay(object):
	"""
	During gameplay all the experiences < s, a, r, s’ > are stored in a replay memory. 
	In training, batches of randomly drawn experiences are used to generate the input and target for training.
	"""
	def __init__(self, max_memory=MAX_MEMORY, discount=.9):
		"""
		Setup
		max_memory: the maximum number of experiences we want to store
		memory: a list of experiences
		discount: the discount factor for future experience

		In the memory the information whether the game ended at the state is stored seperately in a nested array
		[...
		[experience, game_over]
		[experience, game_over]
		...]
		"""
		self.max_memory = max_memory
		self.memory = list()
		self.discount = discount

	def remember(self, states, game_over):
		#Save a state to memory
		self.memory.append([states, game_over])
		#We don't want to store infinite memories, so if we have too many, we just delete the oldest one
		if len(self.memory) > self.max_memory:
			del self.memory[0]


	def get_batch(self, model, batch_size=BATCH_SIZE):

		#How many experiences do we have?
		len_memory = len(self.memory)

		#Calculate the number of actions that can possibly be taken in the game
		num_actions = model.output_shape[-1]

		#Dimensions of the game field
		env_dim = self.memory[0][0][0].shape[1]

		#We want to return an input and target vector with inputs from an observed state...
		inputs = np.zeros(shape=(batch_size,17,5))

		#...and the target r + gamma * max Q(s’,a’)
		#Note that our target is a matrix, with possible fields not only for the action taken but also
		#for the other possible actions. The actions not take the same value as the prediction to not affect them
		targets = np.zeros(shape=(batch_size,2))

		#We draw states to learn from randomly
		for i, idx in enumerate(np.random.randint(0, len_memory,
			 										size=inputs.shape[0])):

			# idx - id of replay in memeory, i - index of idx in selected replayes
			"""
			Here we load one transition <s, a, r, s’> from memory
			state_t: initial state s
			action_t: action taken a
			reward_t: reward earned r
			state_tp1: the state that followed s’
			"""
			state_t, action_t, reward_t, state_tp1	= self.memory[idx][0] # states
			game_over								= self.memory[idx][1] # We also need to know whether the game ended at this state

			#add the state s to the input
			inputs[i:i+1] = state_t

			# First we fill the target values with the predictions of the model.
			# They will not be affected by training (since the training loss for them is 0)
			targets[i] = model.predict(single_batch(state_t))[0]

			"""
			If the game ended, the expected reward Q(s,a) should be the final reward r.
			Otherwise the target value is r + gamma * max Q(s’,a’)
			"""

			#if the game ended, the reward is the final reward
			if game_over:  # if game_over is True
				targets[i, action_t] = reward_t
			else:
				#  Here Q_sa is max_a'Q(s', a')
				Q_sa = np.max(model.predict(single_batch(state_tp1))[0])
				# r + gamma * max Q(s’,a’)
				targets[i, action_t] = reward_t + self.discount * Q_sa
		return inputs, targets



#Keras is a deep learning libarary
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers.core import Dense, Flatten, Activation
from keras.layers.convolutional import MaxPooling2D, Conv2D
from keras.optimizers import Adam,sgd

class NNet():
	def __init__(self,game):
		self.game = game
		self.hidden_size = HIDDEN_SIZE # Size of the hidden layers
		self.num_actions = game.get_num_actions()
		self.nn_inputs_count = game.get_game_field_width() + game.get_num_actions()


	def baseline_model(self):
		# input - state, output - qValues for each action
		nn_inputs_count,num_actions,hidden_size = self.nn_inputs_count,self.num_actions,self.hidden_size

		#seting up the model with keras
		model = Sequential()
		model.add(Dense(hidden_size, input_shape=self.game.state_shape(), activation='relu', name="INPUTS"))
		model.add(Flatten())
		model.add(Dense(hidden_size, activation='relu'))
		model.add(Dense(num_actions, name="OUTPUTS"))
		model.compile(sgd(lr=.1), "mse")

		return model


def print_batch_data(input_data,target_data,game):
	game_state =  str(token_ids_to_sentence(one_hot_batch_to_array(input_data),game.get_vocab_rev()))
	action = "<" if target_data[0] > target_data[1] else ">"

	OKGREEN = '\033[92m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	tmp = one_hot_batch_to_array(input_data)
	if tmp.index(4) >= len(tmp)/2:
		color = OKGREEN if target_data[0] > target_data[1] else FAIL
	else:
		color = OKGREEN if target_data[0] < target_data[1] else FAIL
	print game_state + "   " + color + action + ENDC

def print_train_data(memory_item,game):
	game_state =  str(token_ids_to_sentence(one_hot_batch_to_array(memory_item[0][0]),game.get_vocab_rev()))
	action = "<" if memory_item[0][1] == 0 else ">"
	reward = str(memory_item[0][2])
	next_state =  str(token_ids_to_sentence(one_hot_batch_to_array(memory_item[0][3]),game.get_vocab_rev()))
	print "|" + game_state + "|   " + action + " reward - " + reward + "\t" + next_state


import glob
from utils.helpers import *
class AIPlayerNew():
	epsilon = .9

	def __init__(self,game):
		self.step = 0
		self.game = game
		self.num_actions = game.get_num_actions()
		self.model = NNet(game).baseline_model()
		self.exp_replay = ExperienceReplay()

	def manage_model_weights(self):
		chenckpoint_file = "tmp/AIPlayer_weights.h5"
		if (self.step == 0):
			if glob.glob(chenckpoint_file + "*"):
				self.model.load_weights(chenckpoint_file)
				print("Model state loaded from file: %s" % chenckpoint_file)

		if (self.step != 0 and self.step % 1000 == 0):
			self.model.save_weights(chenckpoint_file)
			print("Model state saved in file: %s" % chenckpoint_file)

		self.step += 1

	def state_to_onehot(self,state):
		return data_array_to_one_hot(state,self.game.get_num_classes())


	def get_input(self):

		self.manage_model_weights()

		current_state = self.state_to_onehot(self.game.encoded_game_field_state) #input_t is a vector containing representing the game screen
		

		# play olny
		if not TRAIN:
			self.step = 3
			q = self.model.predict(single_batch(current_state)) #q contains the expected rewards for the actions
			action = np.argmax(q[0])
			return self.game.get_actions()[action]


		if np.random.rand() <= self.epsilon:
			action = np.random.randint(0, self.num_actions) #Eat something random from the menu
		else:
			q = self.model.predict(single_batch(current_state)) #q contains the expected rewards for the actions
			action = np.argmax(q[0]) #We pick the action with the highest expected reward

		old_state, action_id, reward, new_state, game_over = self.game.get_train_data(action) # apply action, get rewards and new state
		old_state = self.state_to_onehot(old_state)
		reward = reward.value # enum to reward
		new_state = self.state_to_onehot(new_state)

		# print_train_data([[old_state, action_id, reward, new_state]],self.game)
		self.exp_replay.remember([old_state, action_id, reward, new_state], game_over) # store experience

		inputs, targets = self.exp_replay.get_batch(self.model) # Load batch of experiences

		# # force set train data
		# for i in range(len(inputs)):
		# 	tmp = one_hot_batch_to_array(inputs[i])
		# 	if tmp.index(4) >= len(tmp)/2: # 4    0 1 2 3
		# 		targets[i] = [1,-1] # manual train data
		# 	else:
		# 		targets[i] = [-1,1]

		# #print batch data
		# if self.step > 10:
		# 	for i in range(len(inputs)):
		# 		print_batch_data(inputs[i],targets[i],self.game)
		# 	exit()

		# #print train data
		# if len(self.exp_replay.memory) >= 100:#self.exp_replay.max_memory:
		# 	for memory_item in self.exp_replay.memory:
		# 		print_train_data(memory_item,self.game)
		# 	exit()

		self.model.train_on_batch(inputs, targets) # train model on experiences

		if self.step > MAX_ITERATIONS:
			print "DONE"
			exit()

		return self.game.get_actions()[action]

