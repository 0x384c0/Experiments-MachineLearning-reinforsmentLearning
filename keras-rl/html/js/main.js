//UI
let
loadingIndicator,
gameElement,
pixiGameElement,
progresses

//others
let
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
	progresses = [
		document.getElementById("pr_left"),
		document.getElementById("pr_right"),
		document.getElementById("pr_up"),
		document.getElementById("pr_down"),
		document.getElementById("pr_stay"),
	]
	showLoading()
	initNNet()
	.then(() => {
		initPixiJs()
		hideLoading()
		// document.addEventListener('keydown', refresh)
		timerId = setInterval(refresh, 40)
	})
}

//UI Others
function initPixiJs(){
	pixiJsRenderer = new PixiJSRenderer(game,pixiGameElement)
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
	let 
	result = player
	.get_input(game.get_state())

	let 
	pressed_key_id = result.action,
	action_props = result.action_props

	for (let [i, progress] of progresses.entries()){
		progress.value = 100 * action_props[i]
		if (i == pressed_key_id){
			progress.className = "selected_action"
		} else {
			progress.className = "not_seleted_action"
		}
	}

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