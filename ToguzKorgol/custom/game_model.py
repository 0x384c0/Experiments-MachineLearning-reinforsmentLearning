# https://github.com/Hvass-Labs/TensorFlow-Tutorials/blob/master/16_Reinforcement_Learning.ipynb

import tensorflow as tf
import numpy as np

board_size = 18
num_actions = 18


game_state = tf.placeholder(dtype=tf.float32, shape=[board_size], name="game_state")
next_action_probabilities = tf.placeholder(dtype=tf.float32, shape=[num_actions], name="next_action_probabilities")

padding = 'same'
init = tf.truncated_normal_initializer(mean=0.0, stddev=2e-2)
activation = tf.nn.relu


inputs = tf.reshape( tensor=game_state, shape=[1,1,1,board_size]) # convert for 2d conv layer [batch_size,width,height,channels]

# First convolutional layer.
net = tf.layers.conv2d(inputs=inputs, name='layer_conv1',
                       filters=board_size, kernel_size=3, strides=1,
                       padding=padding,
                       kernel_initializer=init, activation=activation)

# Second convolutional layer.
net = tf.layers.conv2d(inputs=net, name='layer_conv2',
                       filters=board_size, kernel_size=3, strides=1,
                       padding=padding,
                       kernel_initializer=init, activation=activation)

# Third convolutional layer.
net = tf.layers.conv2d(inputs=net, name='layer_conv3',
                       filters=board_size, kernel_size=3, strides=1,
                       padding=padding,
                       kernel_initializer=init, activation=activation)

# Final fully-connected layer.
net = tf.layers.dense(inputs=net, name='layer_fc_out', units=num_actions,
                      kernel_initializer=init, activation=None)


#TODO: calculate loss

#TODO: train


#test
with tf.Session() as sess:
	sess.run(tf.global_variables_initializer())
	initial_game_state = [9,9,9,9,9,9,9,9,9, 9,9,9,9,9,9,9,9,9]

	game_state_for_print = sess.run(game_state,feed_dict={game_state:initial_game_state})
	print "game_state_for_print"
	print game_state_for_print

	inputs_for_print = sess.run(inputs,feed_dict={game_state:initial_game_state})
	print "inputs_for_print"
	print inputs_for_print

	# exit()

	action_prediction = sess.run(net,feed_dict={game_state:initial_game_state})

	action_prediction = np.reshape(action_prediction,(board_size))
	print "action_prediction"
	print action_prediction
	print "\nnp.argmax(action_prediction)"
	print np.argmax(action_prediction)
