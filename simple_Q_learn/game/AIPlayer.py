import sys
sys.path.append('..')

import glob
import random

from collections import namedtuple
from utils.tensorboard_logging import *

class AIPlayer():

	ReplayItem = namedtuple("ReplayItem", "reward old_input_state input_state")
	logger = Logger('tmp/basic')

	game = None
	old_score = 0
	old_input_state = None


	discount = 0.9
	epsilon = 0.1
	max_epsilon = 0.9
	epsilon_increase_factor = 20.0 #800

	runs = 0
	epoch = 0

	learning_rate = 0.2
	max_epoch = 3000
	replay_memory_size = 200
	replay_memory = []
	replay_batch_size = int(replay_memory_size * 0.8)
	nn_outputs_count = 1
	chenckpoint_file = "tmp/LSTM_Model.ckpt"
	net = None
	loss = None
	sess = None
	saver = None
	predictions = None
	optimize = None
	tf_game_state = None

	def __init__(self,game):
		self.num_actions = game.get_num_actions()
		self.nn_inputs_count = game.get_game_field_width() + game.get_num_actions()
		self.game_field_width = game.get_game_field_width()

		self.game = game
		self.init_nn_graph()
		self.sess = tf.Session()
		self.sess.run(tf.global_variables_initializer())
		self.saver = tf.train.Saver()
		self.load_state()

	def init_nn_graph(self):
		padding = 'same'
		init = tf.truncated_normal_initializer(mean=0.0, stddev=2e-2)
		activation = tf.sigmoid

		self.tf_game_state = tf.placeholder(dtype=tf.float32, shape=[None,1,self.nn_inputs_count,1], name="game_state") #[batch, in_height, in_width, in_channels]
		# Convolutional layer.
		net = tf.layers.conv2d(inputs=self.tf_game_state,	name='layer_conv1',
													filters=1, kernel_size=3, strides=1,
													padding=padding, kernel_initializer=init, activation=activation)
		# Pooling Layer #1	
		net = tf.layers.max_pooling2d(inputs=net, pool_size=[1, 2], strides=2)

		# Dense Layer
		net = tf.reshape(net, [-1, (self.nn_inputs_count)/2 ])
		net = tf.layers.dense(inputs=net, units=256, activation=tf.nn.relu)

		# Final fully-connected layer.
		net = tf.layers.dense(inputs=net,	name='layer_fc_out',
								units=self.nn_outputs_count, kernel_initializer=init, activation=None)

		predictions = tf.placeholder(dtype=tf.float32,shape=[None,self.nn_outputs_count])

		loss = tf.losses.mean_squared_error(
			net,
			predictions,
		)

		

		optimize = tf.train.GradientDescentOptimizer(learning_rate=self.learning_rate).minimize(loss)


		self.total_epoches = tf.Variable(0, name="total_epoches",trainable=False)
		self.increment_total_epoches = tf.assign_add(self.total_epoches,1,name="increment_total_epoches")

		self.net,self.loss,self.predictions,self.optimize = net,loss,predictions,optimize

	def run_model(self,input_state_action):
		tf_game_state = np.reshape(input_state_action,(1,1,self.nn_inputs_count,1))
		q_value = self.sess.run(self.net, feed_dict={self.tf_game_state:tf_game_state})
		return np.asscalar( q_value)



	def train(self,training_x_data,training_y_data):
		# print "training_x_data\t\t\t" + "".join(map(str,training_x_data))
		training_x_data = np.reshape(training_x_data,(len(training_x_data), 1, self.nn_inputs_count, 1))
		self.sess.run(self.optimize, feed_dict={self.tf_game_state:training_x_data, self.predictions:training_y_data})
		if self.need_log_loss():
			loss = self.sess.run(self.loss, feed_dict={self.tf_game_state:training_x_data, self.predictions:training_y_data})
			self.log_loss(loss)


	def get_input(self):
		# Capture current state
		input_state = [0]*(self.game.getFieldSize() + self.num_actions)
		input_state[self.game.getPlayerPosition()] = 1
		# print "input_state\t\t\t" + "".join(map(str,input_state))

		if self.runs != 0:
			# If this is not the first
			# Evaluate what happened on last action and calculate reward
			reward = self.get_reward()

			self.replay_memory.append(self.ReplayItem(reward=reward,old_input_state=self.old_input_state,input_state=input_state))
			if len(self.replay_memory) > self.replay_memory_size + 1:
				self.replay_memory.pop(0)


		# If replay memory is full train network on a batch of states from the memory
		if len(self.replay_memory) > self.replay_memory_size:
			# Randomly samply a batch of actions from the memory and train network with these actions

			aa_milne_arr = [self.replay_memory[0], self.replay_memory[3],self.replay_memory[2],self.replay_memory[1]]

			batch = []
			for a in range(self.replay_batch_size):
				batch.append(random.choice(self.replay_memory))

			training_x_data = []
			training_y_data = []

			# For each batch calculate new q_value based on current network and reward
			for m in batch:
				# To get entire q table row of the current state run the network once for every posible action
				q_table_row = []
				for a in range(self.num_actions):
					# Create neural network input vector for this action
					input_state_action = list(input_state)
					# Set a 1 in the action location of the input vector
					input_state_action[self.game_field_width + a] = 1
					# Run the network for this action and get q table row entry
					q_table_row.append(self.run_model(input_state_action))

				# Update the q value
				updated_q_value = m.reward + self.discount * max(q_table_row)

				# Add to training set
				training_x_data.append(m.old_input_state)
				training_y_data.append([updated_q_value])

			# Train network with batch
			self.train(training_x_data,training_y_data)
			self.increment_epoch()




		# Chose action based on Q value estimates for state
		# If a random number is higher than epsilon we take a random action
		# We will slowly increase @epsilon based on runs to a maximum of @max_epsilon - this encourages early exploration
		epsilon_run_factor = (self.max_epsilon-self.epsilon) if (self.runs/self.epsilon_increase_factor) > (self.max_epsilon-self.epsilon) else (self.runs/self.epsilon_increase_factor)
		action_taken_index = None
		if random.random() > (self.epsilon + epsilon_run_factor):
			action_taken_index = random.randint(0,self.num_actions - 1)
			# Select random action
		else:
			# To get the entire q table row of the current state run the network once for every posible action
			q_table_row = []
			for a in range(self.num_actions):
				# Create neural network input vector for this action
				input_state_action = list(input_state)
				# Set a 1 in the action location of the input vector
				input_state_action[self.game_field_width + a] = 1
				# print "input_state_action\t\t\t" + "".join(map(str,input_state_action))
				# Run the network for this action and get q table row entry

				model_result = self.run_model(input_state_action)

				q_table_row.append(model_result)
			

			action_taken_index = np.argmax(q_table_row)


		# Set action taken in input state before storing it
		input_state[self.game_field_width + action_taken_index] = 1
		self.old_input_state = input_state

		# Save score and current state
		self.old_score = self.game.score
		self.runs += 1

		# time.sleep(0.01)


		#test
		if self.need_save_state():
			self.save_state()

		if self.epoch > self.max_epoch:
			print "\n".join(map(str,self.replay_memory))
			self.save_state()
			return quit_key

		return self.game.get_actions()[action_taken_index]



	# helpers
	min_inactivity_penalty = -0.0000001

	def get_reward(self):
		if self.runs != 0:
			reward = self.min_inactivity_penalty # self.min_inactivity_penalty - (abs(self.max_inactivity_penalty) - abs(self.min_inactivity_penalty)) * (self.steps_from_game_begins/self.steps_from_game_begins_for_max_inactivity_penalty)
			
			
			if self.game.score > self.old_score:
				reward = 1 # reward is 1 if our score increased
			elif self.game.score < self.old_score:
				reward = -1 # reward is -1 if our score decreased
			return reward
		else:
			return None


	def increment_epoch(self):
		self.epoch += 1
		self.sess.run(self.increment_total_epoches)


	def need_log_loss(self):
		return self.epoch != 0 and self.epoch % (self.max_epoch/1000.0) == 0

	def log_loss(self,loss):
		total_epoches = self.sess.run(self.total_epoches)
		self.logger.log_scalar("loss",np.asscalar(loss),total_epoches)



	def need_save_state(self):
		return self.epoch != 0 and self.epoch % (self.max_epoch/50.0) == 0

	def save_state(self):
		sess = self.sess
		saver = self.saver
		save_path = saver.save(sess, self.chenckpoint_file)
		print("Model saved in file: %s" % save_path)

	def load_state(self):
		sess = self.sess
		saver = self.saver
		chenckpoint_file = self.chenckpoint_file
		if glob.glob(chenckpoint_file + "*"):
			modelPath = saver.restore(sess, chenckpoint_file)
			print "\n----------------- Loaded state from: " + chenckpoint_file

