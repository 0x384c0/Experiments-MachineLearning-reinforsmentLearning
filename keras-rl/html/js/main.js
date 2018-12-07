let
//UI
loadingIndicator,
gameElement,
pixiGameElement,
//others
nnet,
game,
player,
timerId,
pixiJsRenderer


//LifeCycle
window.addEventListener("DOMContentLoaded", domContentLoaded);
function domContentLoaded() {
	loadingIndicator = document.getElementById("loadingIndicator")
	gameElement = document.getElementById("game_element")
	pixiGameElement = document.getElementById("pixi_game_element")
	showLoading()
	initNNet()
	.then(() => {
		initPixiJs()
		hideLoading()
		document.addEventListener('keydown', refresh)
		// timerId = setInterval(refresh, 100)
	})
}

//UI Others
function initPixiJs(){
	pixiJsRenderer = new PixiJSRenderer(game,document.body)
}
function initNNet(){
	nnet = new NNet()
	return nnet
	.load()
	.then(() => {
		console.log("Model loaded")
		game = new Game()
		game.reset()

		const
		state_shape = game.state_shape(),
		num_actions = game.get_num_actions()
		player = new PlayerAI(state_shape,num_actions,nnet)
	})
}
function refresh(){
	pressed_key_id = player
	.get_input(game.get_state())
	game.send_key(pressed_key_id)
	// gameElement.innerHTML = game.render()
	game.render()
	pixiJsRenderer.nextFrame()
	// if (event.keyCode == 65){
	// 	game.send_key(0)
	// 	gameElement.innerHTML = game.render()
	// } else if (event.keyCode == 68){
	// 	game.send_key(1)
	// 	gameElement.innerHTML = game.render()
	// } else if (event.keyCode == 87){
	// 	game.send_key(2)
	// 	gameElement.innerHTML = game.render()
	// } else if (event.keyCode == 83){
	// 	game.send_key(3)
	// 	gameElement.innerHTML = game.render()
	// } else {
	// 	game.send_key(4)
	// 	gameElement.innerHTML = game.render()
	// }
}


//loading
function showLoading(){
	loadingIndicator.className = "loader"
}
function hideLoading(){
	loadingIndicator.className = 'hidden'
}