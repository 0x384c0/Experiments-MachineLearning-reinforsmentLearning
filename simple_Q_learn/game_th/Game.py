import numpy as np
import sys
import curses
import traceback
import copy
from collections import namedtuple

from helpers.utils import *

from GameClasses import *


FIELD_SIZE = Size(40,20) # w,h
START_PLAYER_POSITION = Point(FIELD_SIZE.w/2,0) #x,y

#game objects
sym_player = "P"
sym_bullet = "*"
sym_bonus = "+"
sym_empty = " "

vocab = {
	sym_empty:0, 
	sym_player:1,
	sym_bullet:2,
	sym_bonus:3,
}
vocab_rev = {v: k for k, v in vocab.items()}

# generating vocabs ids
class Game():
	__myscreen = curses.initscr()

	def __update_game_state(self):
		try: 
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


		except Exception as e:
			self.handleException(e)

	# public
	def print_controls(self):
		self.__myscreen.addstr("q - quit")

	def reset(self):
		try: 
			origin = Point(FIELD_SIZE.w/2, FIELD_SIZE.h * 0.8)
			self.__animation_time = 0
			self.__emitters = [
			CircleWithHoleBulletEmitter(origin, PI * -0.5, PI * 1.2, 1, 6)
			# VarAngleBulletEmitter(origin, PI * 0., PI * 1.2, 30, True, 1, 1),
			# VarAngleBulletEmitter(origin, PI * 2., PI * 0.8, 30, False, 1, 1),
			# CircleBulletEmitter(origin, 10, 1, 6),
			]
			self.__bullets = []
			self.__player_position = copy.copy(START_PLAYER_POSITION)
			self.__update_game_state()
		except Exception as e:
			self.handleException(e)

	def render(self):
		y_offset = 2
		try: 
			for x in range(FIELD_SIZE.w):
				for y in range(FIELD_SIZE.h):
					sym = vocab_rev[int(self.__game_state[x][y])]
					y_rev = FIELD_SIZE.h - 1 - y
					self.__myscreen.addstr(y_rev + y_offset,x,sym)
				self.__myscreen.addstr("\n")
			self.__myscreen.refresh()
		except Exception as e:
			self.handleException(e)

	def send_key(self,pressed_key):
		try: 
			if pressed_key == "q":
				curses.endwin()
				exit()

			if pressed_key == "w":
				self.__player_position.y += 1

			if pressed_key == "s":
				self.__player_position.y -= 1

			if pressed_key == "a":
				self.__player_position.x -= 1

			if pressed_key == "d":
				self.__player_position.x += 1

			self.__player_position.x = clamp(self.__player_position.x,0,FIELD_SIZE.w - 1)
			self.__player_position.y = clamp(self.__player_position.y,0,FIELD_SIZE.h - 1)

			self.__update_game_state()

			for bullet in self.__bullets:
				if self.__player_position == bullet.origin:
					self.reset()
					return GameResult.los

			return GameResult.none

		except Exception as e:
			self.handleException(e)

	def handleException(self,e):
		curses.endwin()
		print(traceback.format_exc())
		print(e)
		exit()
