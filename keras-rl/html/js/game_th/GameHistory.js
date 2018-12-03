class GameHistory{
	constructor(shape){
		this._size = 4 // history size
		this._shape = shape
		this.shape_with_history = [this._shape[0] * this._size, this._shape[1]]
		this.reset()
	}
	reset(){
		this._history = np.zeros(this.shape_with_history).tolist()
	}
	put(state){
		this._history = np_insert(this._history,0,state.tolist(),0)
		this._history = np_delete(this._history,this._shape[0] * this._size,0)
	}
	get(){
		return this._history
	}
}

function np_insert(arr,obj,values,axis){
	return values.concat(arr)
}

function np_delete(arr,obj,axis){
	arr.length = obj
	return arr
}