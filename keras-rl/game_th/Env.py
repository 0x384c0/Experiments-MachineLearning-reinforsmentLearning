import gym
from gym import spaces
import numpy as np

from Game import Game,GameResult
from GameHistory import GameHistory



class Env():

	def __init__(self,game):
		self._game = game
		self.action_space = spaces.Discrete(self._game.get_num_actions())
		self._game_history = GameHistory(self._game.state_shape())
		# self.observation_space = spaces.Box(low=0, high=self._game.max_state_value(), dtype=np.uint8, shape=(self.STATE_HISTORY_SIZE,) + self._game.state_shape()) # TODO: remove if not used

	def step(self, action):
		reward_enum = self._game.send_key(action)
		self._game_history.put(self._game.get_state())
		
		reward = reward_enum.value
		observation = self._game_history.get()
		done = reward_enum != GameResult.none
		info = {"action": action}


		return observation, reward, done, info

	def reset(self):
		self._game.reset()
		self._game_history.reset()
		self._game_history.put(self._game.get_state())

		observation = self._game_history.get()

		return observation

	def render(self):
		self._game.render()

	def get_shape_with_history(self):
		return self._game_history.shape_with_history