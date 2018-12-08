import os  

import numpy as np
from keras.optimizers import Adam
from rl.agents.dqn import DQNAgent
from rl.policy import LinearAnnealedPolicy, BoltzmannQPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor
from rl.callbacks import FileLogger, ModelIntervalCheckpoint, TrainIntervalLogger

WINDOW_LENGTH = 1

NB_STEPS				= 150000#1000000
MEMORY_LIMIT			= NB_STEPS
NB_STEPS_WARMUP			= NB_STEPS * 0.1# NB_STEPS * 0.05
TARGET_MODEL_UPDATE		= NB_STEPS * 0.01

INTERVAL_CALLBACK		= NB_STEPS * 0.25
FILE_LOGGER_INTERVAL	= 100

EPS_GREEDY_NB_STEPS		= NB_STEPS * 0.3
FIT_LOG_INTERVAL		= NB_STEPS * 0.01

env_name = "game_th"
weights_filename				= 'tmp/dqn_{}_weights.h5f'.format(env_name)
checkpoint_weights_filename		= 'tmp/dqn_' + env_name + '_weights_{step}.h5f'
log_filename					= 'tmp/dqn_{}_log.json'.format(env_name)
model_filename					= 'tmp/model.h5'


class AgentProcessor(Processor):
	def process_reward(self, reward):
		# print("reward " + str(reward))
		return np.clip(reward, -1., 1.)


class AgentWrapper():
	def __init__(self,env,nnet,nb_actions):
		model = nnet.model

		# keras-rl
		memory = SequentialMemory(limit=MEMORY_LIMIT, window_length=WINDOW_LENGTH)
		policy = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=1., value_min=.1, value_test=.05,
		                              nb_steps=EPS_GREEDY_NB_STEPS)
		dqn = DQNAgent(model=model, nb_actions=nb_actions, policy=policy, memory=memory,
		               nb_steps_warmup=NB_STEPS_WARMUP, target_model_update=TARGET_MODEL_UPDATE)# gamma=.99, train_interval=4, delta_clip=1.
		dqn.compile(Adam(lr=.00025), metrics=['mae'])

		self.processor = AgentProcessor()
		dqn.processor = self.processor

		#for training

		self.env = env
		self.dqn = dqn

	def save_weights(self):
		self.dqn.save_weights(weights_filename, overwrite=True)

	def save_model(self):
		self.dqn.model.save(model_filename)

	def load_weights(self):
		if os.path.exists(weights_filename):
			print("Loading from " + weights_filename)
			self.dqn.load_weights(weights_filename)
		else:
			print(weights_filename + " not found")

	def train(self):
		callbacks = [
			ModelIntervalCheckpoint(checkpoint_weights_filename, interval=INTERVAL_CALLBACK),
			FileLogger(log_filename, interval=FILE_LOGGER_INTERVAL)
		]
		self.dqn.fit(self.env, callbacks=callbacks, nb_steps=NB_STEPS, log_interval=FIT_LOG_INTERVAL)

	def test(self):
		self.dqn.test(env, nb_episodes=10, visualize=True)
