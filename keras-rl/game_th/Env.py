import gym
from gym import spaces
import numpy as np

from Game import Game,GameResult



class Env():
	def __init__(self,game):
		self._game = game
		self.action_space = spaces.Discrete(self._game.get_num_actions())
		self.observation_space = spaces.Box(low=0, high=self._game.max_state_value(), dtype=np.uint8, shape=self._game.state_shape())

	def step(self, action):
		reward_enum = self._game.send_key(action)
		
		reward = reward_enum.value
		observation = self._game.get_state()
		done = reward_enum != GameResult.none
		info = {"action": action}

		return observation, reward, done, info

	def reset(self):
		self._game.reset()
		observation = self._game.get_state()
		return observation

	def render(self):
		self._game.render()