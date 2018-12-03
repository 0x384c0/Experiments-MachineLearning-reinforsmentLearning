import numpy as np
import sys
import traceback
import copy
import random
from collections import namedtuple

from helpers.utils import *

#TODO: remove try and fix
try:
	from .GameClasses import *
except Exception as e:
	pass
try:
	from GameClasses import *
except Exception as e:
	pass

RENDER = is_render()

if RENDER:
	import curses

FIELD_SIZE = Size(40,20) # w,h
START_PLAYER_POSITION = Point(FIELD_SIZE.w/2,0) #x,y
SPEED_MODIFIER = 0.5
EMITTER_RESET_TIME = int(50 / SPEED_MODIFIER)
WIN_TIME = 300 # minimum win time

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
		origin = Point(FIELD_SIZE.w/2, FIELD_SIZE.h * 0.8)
		self._emitters_sets = [[ # start after 23
			CircleWithHoleBulletEmitter	(origin=origin, delay=12.0 / SPEED_MODIFIER, speed=0.5 * SPEED_MODIFIER, num_rays=80, angle_min=PI * -0.80, angle_max=PI * 0.80, angle_generator=AngleGeneratorSine(diff=PI*0.30, period=80.0 / SPEED_MODIFIER)),
		]]
		# self._emitters_sets = [[
		# 	CircleWithHoleBulletEmitter	(origin=origin, delay=12.0 / SPEED_MODIFIER, speed=0.5 * SPEED_MODIFIER, num_rays=80, angle_min=PI * -0.80, angle_max=PI * 0.80, angle_generator=AngleGeneratorSine(diff=PI*0.25, period=80.0 / SPEED_MODIFIER)),
		# ],[
		# 	BulletEmitter				(origin=origin, delay=1.0 / SPEED_MODIFIER,  speed=1.0 * SPEED_MODIFIER, angle=PI * 0., angle_generator=AngleGeneratorLinear(diff=PI * 1.2, period=30.0 / SPEED_MODIFIER, start_offset=True)),
		# 	BulletEmitter				(origin=origin, delay=1.0 / SPEED_MODIFIER,  speed=1.0 * SPEED_MODIFIER, angle=PI * 2.,  angle_generator=AngleGeneratorLinear(diff=PI * -1.2, period=30.0 / SPEED_MODIFIER, start_offset=False)),
		# ],[
		# 	BulletEmitter				(origin=origin, delay=1.0 / SPEED_MODIFIER,  speed=1.0 * SPEED_MODIFIER, angle=PI, angle_generator=AngleGeneratorSine(diff=PI*0.3, period=30.0 / SPEED_MODIFIER))
		# ],[
		# 	CircleBulletEmitter			(origin=origin, delay=10.0 / SPEED_MODIFIER, speed=1.0 * SPEED_MODIFIER, num_rays=20),
		# ]]
		self._emitters = None
		self.win_time_modifier = 0

	def _update_game_state(self):
		self._game_state = np.zeros(FIELD_SIZE.shape()) # empty
		self._game_state[int(self._player_position.x)][int(self._player_position.y)] = vocab[sym_player]
		self._animation_time += 1

		# emit bullets
		for emitter in self._get_emitters():
			emitter.emit(self._animation_time,self._bullets)

		# move or delete bullets
		bullet_for_deleting = []
		for bullet in self._bullets:
			bullet.move(self._animation_time)
			if bullet.origin.x >= 0 and bullet.origin.x < FIELD_SIZE.w and bullet.origin.y >= 0 and bullet.origin.y < FIELD_SIZE.h:
				self._game_state[int(bullet.origin.x)][int(bullet.origin.y)] = vocab[sym_bullet]
			else:
				bullet_for_deleting.append(bullet)
		self._bullets = [x for x in self._bullets if x not in bullet_for_deleting]

	def __del__(self):
		self.stop()

	def _get_emitters(self):
		if self._animation_time % EMITTER_RESET_TIME == 0 or self._emitters == None:
			self._emitters = random.choice(self._emitters_sets)
		return self._emitters

	# public
	def print_controls(self):
		if RENDER:
			self._myscreen.addstr("q - quit, left_key - {}, right_key - {}, up_key - {}, down_key - {}".format(left_key,right_key,up_key,down_key))

	def reset(self):
		self._emitters = None
		self._animation_time = 0
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

		if self._animation_time > WIN_TIME:
			self.reset()
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
