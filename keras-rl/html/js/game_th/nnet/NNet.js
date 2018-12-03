var _model = null
var _loading = false

class NNet{
	load(){
		if (_model == null && !_loading){
			_loading = true
			console.log("Loading model ... ")
			return tf
			.loadModel('model/model.json')
			.then((i_model) => {
				_model = i_model
				_loading = false
				return Promise.resolve()
			})
		} else{
			return Promise.resolve()
		}
	}

	get_action(observation,shape){// image - element
		if (!this.modelLoaded){ return null }


		tf.nextFrame()
		let promise = tf.tidy(() => {

			const xs = tf.tensor4d(
				[[observation]],
				[1,].concat(shape)
			)
			const predictions = _model.predict(xs)
			let actions = Array.from(predictions.dataSync())
			return actions
		})
		return promise
	}

	get modelLoaded(){
		return _model != null
	}
}