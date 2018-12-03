//UI
let 
loadingIndicator,
gameView,
//nnet
nnet,
game,
player,
timerId


//LifeCycle
window.addEventListener("DOMContentLoaded", domContentLoaded);
function domContentLoaded() {
	loadingIndicator = document.getElementById("loadingIndicator")
	gameView = document.getElementById("game_view")
	
	document.addEventListener('keydown', refresh)
 

	showLoading()
	nnet = new NNet()
	nnet
	.load()
	.then(() => {
		console.log("Model loaded")
		game = new Game()
		game.reset()

		const
		state_shape = game.state_shape(),
		num_actions = game.get_num_actions()
		player = new PlayerAI(state_shape,num_actions,nnet)
		hideLoading()

		// timerId = setInterval(refresh, 100)
	})
}

//UI Actions
function refresh(){
	pressed_key_id = player
	.get_input(game.get_state())
	

	game.send_key(pressed_key_id)
	gameView.innerHTML = game.render()
	// if (event.keyCode == 65){
	// 	game.send_key(0)
	// 	gameView.innerHTML = game.render()
	// } else if (event.keyCode == 68){
	// 	game.send_key(1)
	// 	gameView.innerHTML = game.render()
	// } else if (event.keyCode == 87){
	// 	game.send_key(2)
	// 	gameView.innerHTML = game.render()
	// } else if (event.keyCode == 83){
	// 	game.send_key(3)
	// 	gameView.innerHTML = game.render()
	// } else {
	// 	game.send_key(4)
	// 	gameView.innerHTML = game.render()
	// }
}


//loading
function showLoading(){
	loadingIndicator.className = "loader"
}
function hideLoading(){
	loadingIndicator.className = 'hidden'
}