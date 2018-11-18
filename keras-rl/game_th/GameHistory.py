import numpy as np

class GameHistory():
	
	def __init__(self,size,shape):
		self._size = size
		self._shape = shape
		self.reset()

	def reset(self):
		self._history = np.zeros(shape=(self._size,) + self._shape)

	def put(self,state):
		self._history = np.roll(self._history,1,0)
		self._history = np.insert(self._history,0,state,axis=0)
		self._history = np.delete(self._history,self._size - 1,axis=0)

	def get(self):
		return self._history