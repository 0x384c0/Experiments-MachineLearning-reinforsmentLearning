import numpy as np

class GameHistory():

	
	def __init__(self,size,shape):
		self._size = 4 # history size
		self._shape = shape
		self.shape_with_history = (self._shape[0] * self._size,self._shape[1])
		self.reset()

	def reset(self):
		self._history = np.zeros(shape=self.shape_with_history)

	def put(self,state):
		self._history = np.insert(self._history,0,state,axis=0)
		self._history = np.delete(self._history,range(self._shape[0] * self._size,self._shape[0] * (self._size + 1)),axis=0)


	def get(self):
		return self._history