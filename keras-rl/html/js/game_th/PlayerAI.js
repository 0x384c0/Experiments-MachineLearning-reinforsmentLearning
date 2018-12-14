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

		let 
		max_action_prop = getMaxOfArray(actions),
		min_action_prop = getMinOfArray(actions)

		let action_props = []
		for (let action_prop of actions){
			action_props.push((action_prop - min_action_prop)/(max_action_prop - min_action_prop))
		}
		return {"action":np_argmax(actions),"action_props":action_props}
	}
}

function np_argmax(array){
	return array.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1]
}

function getMaxOfArray(numArray) {
	return Math.max.apply(null, numArray);
}
function getMinOfArray(numArray) {
	return Math.min.apply(null, numArray);
}