class PlayerAI{
	constructor(state_shape,num_actions,nnet){
		this._game_history = new GameHistory(state_shape)
		this.game_state_shape = [1].concat(this._game_history.shape_with_history)
		this.num_actions = num_actions
		this.nnet = nnet
	}
	get_input(game_state){
		this._game_history.put(game_state)
		let observation = this._game_history.get()

		let actions = this.nnet.get_action(observation,this.game_state_shape)
		return np_argmax(actions)
	}
}

function np_argmax(array){
	return array.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1]
}