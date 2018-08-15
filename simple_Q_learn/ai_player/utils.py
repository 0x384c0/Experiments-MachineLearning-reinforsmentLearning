import numpy as np
from helpers.utils import *

def single_batch(data):
	return np.expand_dims(data, axis=0)


def print_batch_data(input_data,target_data,game):
	game_state =  str(token_ids_to_sentence(one_hot_batch_to_array(input_data),game.get_vocab_rev()))
	action = "<" if target_data[0] > target_data[1] else ">"

	OKGREEN = '\033[92m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'

	tmp = one_hot_batch_to_array(input_data)
	if tmp.index(4) >= len(tmp)/2:
		color = OKGREEN if target_data[0] > target_data[1] else FAIL
	else:
		color = OKGREEN if target_data[0] < target_data[1] else FAIL
	print game_state + "   " + color + action + ENDC

def print_train_data(memory_item,game):
	game_state =  str(token_ids_to_sentence(one_hot_batch_to_array(memory_item[0][0]),game.get_vocab_rev()))
	action = "<" if memory_item[0][1] == 0 else ">"
	reward = str(memory_item[0][2])
	next_state =  str(token_ids_to_sentence(one_hot_batch_to_array(memory_item[0][3]),game.get_vocab_rev()))
	print "|" + game_state + "|   " + action + " reward - " + reward + "\t" + next_state