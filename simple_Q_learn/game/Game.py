import sys
sys.path.append('..')
from enum import Enum
import copy

from helpers.utils import *


#game objects
player = "P"
bullet = "*"
bonus = "+"
empty = " "
#field
initial_game_field = "*       +P      *"

#keys
left_key = "a"
right_key = "d"
actions = [left_key,right_key]
num_actions = len(actions)

# generating vocabs ids
vocab, vocab_rev, num_classes = create_vocabulary(initial_game_field)

player_id = vocab[player]
bullet_id = vocab[bullet]
bonus_id = vocab[bonus]
empty_id = vocab[empty]

game_field_width = len(initial_game_field)

class GameResult(Enum):
	win = 1
	los = -1
	none = -0.000000000000000000001

class Game():


	last_los_position = None
	last_win_position = None

	score = 0
	__encoded_game_field_state = None


	steps_from_game_begins_for_max_inactivity_penalty = game_field_width * 5
	steps_from_game_begins = 0


	def __getPlayerPosition(self):
		return self.__encoded_game_field_state.index(player_id)

	# public
	def print_controls(self):
		print "Controls - left: " + left_key + " right: " + right_key

	def reset(self):
		self.steps_from_game_begins = 0
		self.__encoded_game_field_state = sentence_to_token_ids(initial_game_field,vocab)


		empty_indexes = []
		for idx,field_id in enumerate(self.__encoded_game_field_state):

			if field_id == player_id:
				self.__encoded_game_field_state[idx] = empty_id

			if field_id == bonus_id:
				self.__encoded_game_field_state[idx] = empty_id

			if field_id == empty_id:
				empty_indexes.append(idx)


		random_bonus_position = random.choice(empty_indexes)
		self.__encoded_game_field_state[random_bonus_position] = bonus_id
		empty_indexes.remove(random_bonus_position)

		random_player_position = random.choice(empty_indexes)
		self.__encoded_game_field_state[random_player_position] = player_id

	def render(self):
		OKGREEN = '\033[92m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		field_str = token_ids_to_sentence(self.__encoded_game_field_state, vocab_rev)
		if self.last_win_position != None:
			field_str = field_str[:self.last_win_position + 1] + ENDC + field_str[self.last_win_position + 1:]
			field_str = field_str[:self.last_win_position] + OKGREEN + field_str[self.last_win_position:]
			self.last_win_position = None

		if self.last_los_position != None:
			field_str = field_str[:self.last_los_position + 1] + ENDC + field_str[self.last_los_position + 1:]
			field_str = field_str[:self.last_los_position] + FAIL + field_str[self.last_los_position:]
			self.last_los_position = None


		print "|" + field_str + "| score: " + str(self.score)



	def send_key(self,pressed_key):
		player_position = self.__getPlayerPosition()

		old_player_position = player_position

		if pressed_key == left_key:
			player_position -= 1
		elif pressed_key == right_key:
			player_position += 1
		else:
			print "Wrong Key"
			exit()


		#game rules

		#inactivity
		if self.steps_from_game_begins > self.steps_from_game_begins_for_max_inactivity_penalty:
			self.score -= 1
			self.reset()
			return GameResult.los
		self.steps_from_game_begins += 1

		#out of bounds
		if player_position < 0 or player_position > len(self.__encoded_game_field_state) - 1:
			self.score -= 1
			self.reset()
			self.last_los_position = player_position
			return GameResult.los
		#win
		if self.__encoded_game_field_state[player_position] == bonus_id:
			self.score += 1
			self.reset()
			self.last_win_position = player_position
			return GameResult.win
		#los
		if self.__encoded_game_field_state[player_position] == bullet_id:
			self.score -= 1
			self.reset()
			self.last_los_position = player_position
			return GameResult.los
		#continue

		self.__encoded_game_field_state[old_player_position] = empty_id
		self.__encoded_game_field_state[player_position] = player_id
		return GameResult.none


	#nn utils
	def state_to_onehot(self,state):
		return data_array_to_one_hot(state,num_classes)

	# aiplayer requirements
	def get_actions(self):
		return actions

	def get_num_actions(self):
		return num_actions

	def state_shape(self):
		return (game_field_width,num_classes)


	def get_state(self):
		return self.state_to_onehot(self.__encoded_game_field_state)



	def get_train_data(self,action_id):
		old_score = self.score
		old_state = copy.copy( self.__encoded_game_field_state)

		reward = self.send_key(actions[action_id])
		new_state = copy.copy( self.__encoded_game_field_state)
		game_over = reward != GameResult.none

		self.score = old_score
		self.__encoded_game_field_state = old_state

		old_state = self.state_to_onehot(old_state)
		new_state = self.state_to_onehot(new_state)

		return old_state, action_id, reward, new_state, game_over