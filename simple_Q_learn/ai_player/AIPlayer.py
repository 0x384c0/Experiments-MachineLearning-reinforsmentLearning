from .utils import *
from ExperienceReplay import ExperienceReplay


MAX_ITERATIONS = 10000
MIN_EPSILON = .1
MAX_EPSILON = .95



class AIPlayer():

	def __init__(self,game,nnet):
		self.iterations = 0
		self.game = game
		self.num_actions = self.game.get_num_actions()
		self.model = nnet( self.game.state_shape(), self.num_actions )
		self.exp_replay = ExperienceReplay(self.game.state_shape(), self.num_actions)

	def manage_model_weights(self):
		if (self.iterations == 0):
			self.model.load()
		if (self.iterations != 0 and self.iterations % 1000 == 0):
			self.model.save()
		self.iterations += 1

	def train_and_get_input(self):

		self.manage_model_weights()

		current_state = self.game.get_state() #input_t is a vector containing representing the game screen

		if np.random.rand() <= self.epsilon:
			action = np.random.randint(0, self.num_actions) #Eat something random from the menu
		else:
			q = self.model.predict(single_batch(current_state)) #q contains the expected rewards for the actions
			action = np.argmax(q[0]) #We pick the action with the highest expected reward

		old_state, action_id, reward, new_state, game_over = self.game.get_train_data(action) # apply action, get rewards and new state
		reward = reward.value # enum to reward

		self.exp_replay.remember([old_state, action_id, reward, new_state], game_over) # store experience

		inputs, targets = self.exp_replay.get_batch(self.model) # Load batch of experiences

		# print_train_data([[old_state, action_id, reward, new_state]],self.game)

		# # force set train data
		# for i in range(len(inputs)):
		# 	tmp = one_hot_batch_to_array(inputs[i])
		# 	if tmp.index(4) >= len(tmp)/2: # 4    0 1 2 3
		# 		targets[i] = [1,-1] # manual train data
		# 	else:
		# 		targets[i] = [-1,1]

		# #print batch data
		# if self.iterations > 10:
		# 	for i in range(len(inputs)):
		# 		print_batch_data(inputs[i],targets[i],self.game)
		# 	exit()

		# #print train data
		# if len(self.exp_replay.memory) >= 100:#self.exp_replay.max_memory:
		# 	for memory_item in self.exp_replay.memory:
		# 		print_train_data(memory_item,self.game)
		# 	exit()

		self.model.train_on_batch(inputs, targets) # train model on experiences

		if self.iterations > MAX_ITERATIONS:
			if callable(self.game.stop):
				self.game.stop()
			print "DONE"
			exit()

		return self.game.get_actions()[action]

	def get_input(self):

		if (self.iterations == 0):
			self.model.load()
		self.iterations = -1

		current_state = self.game.get_state() #input_t is a vector containing representing the game screen
		q = self.model.predict(single_batch(current_state)) #q contains the expected rewards for the actions
		action = np.argmax(q[0])
		return self.game.get_actions()[action]

	@property
	def epsilon(self):
		result = MAX_EPSILON - (MAX_EPSILON - MIN_EPSILON) * self.iterations/(MAX_ITERATIONS * 0.6)
		return clamp(result,MIN_EPSILON,MAX_EPSILON)