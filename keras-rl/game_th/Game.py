import numpy as np
import sys
import curses
import traceback
import copy
from collections import namedtuple

from helpers.utils import *

from GameClasses import *

RENDER = is_render()

FIELD_SIZE = Size(40,20) # w,h
START_PLAYER_POSITION = Point(FIELD_SIZE.w/2,0) #x,y
WIN_TIME = int(FIELD_SIZE.h * 5)

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
max_vocab_value = 3

# generating vocabs ids
class Game():
	def __init__(self):
		self._myscreen = curses.initscr() if RENDER else None

	def _update_game_state(self):
		self._game_state = np.zeros(FIELD_SIZE.shape()) # empty
		self._game_state[self._player_position.x][self._player_position.y] = vocab[sym_player]
		self._animation_time += 1

		# emit bullets
		for emitter in self._emitters:
			bullet = emitter.emit(self._animation_time,self._bullets)

		# move or delete bullets
		bullet_for_deleting = []
		for bullet in self._bullets:
			bullet.move(self._animation_time)
			if bullet.origin.x >= 0 and bullet.origin.x < FIELD_SIZE.w and bullet.origin.y >= 0 and bullet.origin.y < FIELD_SIZE.h:
				self._game_state[bullet.origin.x][bullet.origin.y] = vocab[sym_bullet]
			else:
				bullet_for_deleting.append(bullet)
		self._bullets = [x for x in self._bullets if x not in bullet_for_deleting]

	def __del__(self):
		self.stop()



	# public
	def print_controls(self):
		if RENDER:
			self._myscreen.addstr("q - quit, left_key - {}, right_key - {}, up_key - {}, down_key - {}".format(left_key,right_key,up_key,down_key))

	def reset(self):
		origin = Point(FIELD_SIZE.w/2, FIELD_SIZE.h * 0.8)
		self._animation_time = 0
		self._emitters = [
		CircleWithHoleBulletEmitter(origin, PI * -0.5, PI * 1.2, 0.5, 12)
		# VarAngleBulletEmitter(origin, PI * 0., PI * 1.2, 30, True, 1, 1),
		# VarAngleBulletEmitter(origin, PI * 2., PI * 0.8, 30, False, 1, 1),
		# CircleBulletEmitter(origin, 10, 1, 6),
		]
		self._bullets = []
		self._player_position = copy.copy(START_PLAYER_POSITION)
		self._update_game_state()

	def render(self):
		print_str = "animation_time: " + str(self._animation_time) + " WIN_TIME: " + str(WIN_TIME) + "  "
		if RENDER:
			y_offset = 2
			self._myscreen.addstr(y_offset - 1,0,print_str)
			for x in range(FIELD_SIZE.w):
				for y in range(FIELD_SIZE.h):
					sym = vocab_rev[int(self._game_state[x][y])]
					y_rev = FIELD_SIZE.h - 1 - y
					self._myscreen.addstr(y_rev + y_offset,x,sym)
				self._myscreen.addstr("\n")
			self._myscreen.refresh()
		else:
			print(print_str)

	def send_key(self,action_id):
		pressed_key = actions[action_id]

		if pressed_key == up_key:
			self._player_position.y += 1

		if pressed_key == down_key:
			self._player_position.y -= 1

		if pressed_key == left_key:
			self._player_position.x -= 1

		if pressed_key == right_key:
			self._player_position.x += 1

		self._player_position.x = clamp(self._player_position.x,0,FIELD_SIZE.w - 1)
		self._player_position.y = clamp(self._player_position.y,0,FIELD_SIZE.h - 1)

		self._update_game_state()

		for bullet in self._bullets:
			if self._player_position == bullet.origin:
				self.reset()
				return GameResult.los

		if self._animation_time % WIN_TIME == 0:
			return GameResult.win

		return GameResult.none

	# play requirements
	def action_id_for_action(self,action):
		if action in actions:
			return actions.index(action)
		else:
			return actions.index(none_key)

	def stop(self):
		if RENDER:
			curses.endwin() #stty sane

	# aiplayer requirements
	def get_num_actions(self):
		return len(actions)

	def state_shape(self):
		return FIELD_SIZE.shape()

	def max_state_value(self):
		return max_vocab_value

	def get_state(self):
		return self._game_state





def state_with_channels(data):
	return np.expand_dims(data, axis=0)
