import numpy as np
import sys
import curses
import traceback
import copy
from collections import namedtuple

from helpers.utils import *

from GameClasses import *

RENDER = True# not is_train_mode()

FIELD_SIZE = Size(40,20) # w,h
START_PLAYER_POSITION = Point(FIELD_SIZE.w/2,0) #x,y
WIN_TIME = int(FIELD_SIZE.h * 3)

#game objects
sym_player = "P"
sym_bullet = "*"
sym_bonus = "+"
sym_empty = " "

#keys
left_key = "a"
right_key = "d"
up_key = "w"
down_key = "s"
none_key = "*"
actions = [left_key,right_key,up_key,down_key,none_key]

vocab = {
	sym_empty:0, 
	sym_player:1,
	sym_bullet:2,
	sym_bonus:3,
}
vocab_rev = {v: k for k, v in vocab.items()}

# generating vocabs ids
class Game():
	__myscreen = curses.initscr() if RENDER else None

	def __update_game_state(self):
		self.__game_state = np.zeros(FIELD_SIZE.shape()) # empty
		self.__game_state[self.__player_position.x][self.__player_position.y] = vocab[sym_player]
		self.__animation_time += 1

		# emit bullets
		for emitter in self.__emitters:
			bullet = emitter.emit(self.__animation_time,self.__bullets)

		# move or delete bullets
		bullet_for_deleting = []
		for bullet in self.__bullets:
			bullet.move(self.__animation_time)
			if bullet.origin.x >= 0 and bullet.origin.x < FIELD_SIZE.w and bullet.origin.y >= 0 and bullet.origin.y < FIELD_SIZE.h:
				self.__game_state[bullet.origin.x][bullet.origin.y] = vocab[sym_bullet]
			else:
				bullet_for_deleting.append(bullet)
		self.__bullets = [x for x in self.__bullets if x not in bullet_for_deleting]

	def __del__(self):
		self.stop()



	# public
	def print_controls(self):
		if RENDER:
			self.__myscreen.addstr("q - quit, left_key - {}, right_key - {}, up_key - {}, down_key - {}".format(left_key,right_key,up_key,down_key))

	def reset(self):
		origin = Point(FIELD_SIZE.w/2, FIELD_SIZE.h * 0.8)
		self.__animation_time = 0
		self.__emitters = [
		CircleWithHoleBulletEmitter(origin, PI * -0.5, PI * 1.2, 0.5, 12)
		# VarAngleBulletEmitter(origin, PI * 0., PI * 1.2, 30, True, 1, 1),
		# VarAngleBulletEmitter(origin, PI * 2., PI * 0.8, 30, False, 1, 1),
		# CircleBulletEmitter(origin, 10, 1, 6),
		]
		self.__bullets = []
		self.__player_position = copy.copy(START_PLAYER_POSITION)
		self.__update_game_state()

	def render(self):
		if RENDER:
			y_offset = 2
			self.__myscreen.addstr(y_offset - 1,0,"animation_time: " + str(self.__animation_time) + " WIN_TIME: " + str(WIN_TIME) + "  ")
			for x in range(FIELD_SIZE.w):
				for y in range(FIELD_SIZE.h):
					sym = vocab_rev[int(self.__game_state[x][y])]
					y_rev = FIELD_SIZE.h - 1 - y
					self.__myscreen.addstr(y_rev + y_offset,x,sym)
				self.__myscreen.addstr("\n")
			self.__myscreen.refresh()

	def send_key(self,pressed_key):
		if pressed_key == "q":
			if RENDER:
				curses.endwin() # stty sane
			exit()

		if pressed_key == up_key:
			self.__player_position.y += 1

		if pressed_key == down_key:
			self.__player_position.y -= 1

		if pressed_key == left_key:
			self.__player_position.x -= 1

		if pressed_key == right_key:
			self.__player_position.x += 1

		self.__player_position.x = clamp(self.__player_position.x,0,FIELD_SIZE.w - 1)
		self.__player_position.y = clamp(self.__player_position.y,0,FIELD_SIZE.h - 1)

		self.__update_game_state()

		for bullet in self.__bullets:
			if self.__player_position == bullet.origin:
				self.reset()
				return GameResult.los

		if self.__animation_time % WIN_TIME == 0:
			return GameResult.win

		return GameResult.none

	# aiplayer requirements
	def get_actions(self):
		return actions

	def get_num_actions(self):
		return len(actions)

	def state_shape(self):
		NUM_OF_IMAGE_CHANNELS = 1
		return (NUM_OF_IMAGE_CHANNELS,) + FIELD_SIZE.shape()

	def get_state(self):
		return state_with_channels(self.__game_state)

	def get_train_data(self,action_id):
		animation_time = self.__animation_time
		emitters = copy.deepcopy(self.__emitters)
		bullets = copy.deepcopy(self.__bullets)
		player_position = copy.copy(self.__player_position)

		old_state = np.copy(self.__game_state)
		reward = self.send_key(actions[action_id])
		new_state = np.copy(self.__game_state)
		game_over = reward != GameResult.none

		self.__animation_time = animation_time
		self.__emitters = emitters
		self.__bullets = bullets
		self.__player_position = player_position
		self.__game_state = np.copy(old_state)

		return state_with_channels(old_state), action_id, reward, state_with_channels(new_state), game_over

	def stop(self):
		if RENDER:
			curses.endwin()



def state_with_channels(data):
	return np.expand_dims(data, axis=0)
