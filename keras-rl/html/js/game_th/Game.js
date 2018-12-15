const
FIELD_SIZE = new Size(40,20), // w,h
START_PLAYER_POSITION = new Point(FIELD_SIZE.w/2,0), //x,y
SPEED_MODIFIER = 0.5,
EMITTER_RESET_TIME = int(50 / SPEED_MODIFIER),
WIN_TIME = 3000, // minimum win time

//game objects
sym_player = "P",
sym_bullet = "*",
sym_bonus = "+",
sym_empty = "&nbsp;",

//keys
left_key = "a",
right_key = "d",
up_key = "w",
down_key = "s",
none_key = "*",
actions = [left_key,right_key,up_key,down_key,none_key],

vocab = {
	[sym_empty]:0, 
	[sym_player]:1,
	[sym_bullet]:2,
	[sym_bonus]:3,
},
vocab_rev = {
	0:sym_empty, 
	1:sym_player,
	2:sym_bullet,
	3:sym_bonus,
},
max_vocab_value = 3

class Game{
	constructor(){
		
		origin = new Point(FIELD_SIZE.w/2, FIELD_SIZE.h * 0.8)
		this._emitters_sets = [[ 
			new CircleBulletEmitter(origin, 3.0 / SPEED_MODIFIER, 1.0 * SPEED_MODIFIER, 10, new AngleGeneratorLinear(PI * 1.2, 100.0 / SPEED_MODIFIER, null, 0.9681745822599894)),
		]]
		// this._emitters_sets = [[ // start after 26
		// 	new CircleWithHoleBulletEmitter	(origin, 12.0 / SPEED_MODIFIER, 0.5 * SPEED_MODIFIER, 80, PI * -0.80, PI * 0.80, new AngleGeneratorSine(PI*0.30, 80.0 / SPEED_MODIFIER)),
		// ]]
		this._emitters = null
		this.win_time_modifier = 0
		this.is_first_round = true
	}
	_update_game_state(){
		this._game_state = np.zeros(FIELD_SIZE.shape()) // empty
		this._game_state.set(int(this._player_position.x), int(this._player_position.y), vocab[sym_player]) 
		this._animation_time += 1

		// emit bullets
		for (let emitter of this._get_emitters())
			emitter.emit(this._animation_time,this._bullets)

		// move or delete bullets
		let bullet_for_deleting = []
		for (let bullet of this._bullets){
			bullet.move(this._animation_time)
			if (bullet.origin.x >= 0 && bullet.origin.x < FIELD_SIZE.w && bullet.origin.y >= 0 && bullet.origin.y < FIELD_SIZE.h)
				this._game_state.set(int(bullet.origin.x),int(bullet.origin.y),vocab[sym_bullet])
			else
				bullet_for_deleting.push(bullet)
		}
		
		this._bullets = this._bullets.filter(function(value, index, arr){
			return !bullet_for_deleting.includes(value)
		});

	}
	_get_emitters(){
		if (this._animation_time % EMITTER_RESET_TIME == 0 || this._emitters == null)
			this._emitters = random.choice(this._emitters_sets)
		return this._emitters

	}
	print_controls(){
		return "q - quit, left_key - "+left_key+", right_key - "+right_key+", up_key - "+right_key+", down_key - "+down_key

	}
	reset(){

		if (!this.is_first_round){
			origin = new Point(FIELD_SIZE.w/2, FIELD_SIZE.h * 0.8)
			this._emitters_sets = [[ 
				new CircleBulletEmitter(origin, 3.0 / SPEED_MODIFIER, 1.0 * SPEED_MODIFIER, 10, new AngleGeneratorLinear(PI * 1.2, 100.0 / SPEED_MODIFIER, null, Math.random())),
			]]
		} else {
			this.is_first_round = false
		}


		this._emitters = null
		this._animation_time = 0
		this._bullets = []
		this._player_position = copy(START_PLAYER_POSITION)
		this._update_game_state()

	}
	render(){
		// print( "animation_time: " + str(this._animation_time) + " WIN_TIME: " + str(WIN_TIME) + "  ")
		let result = ""
		for (let y of range(FIELD_SIZE.h)){
			for (let x of range(FIELD_SIZE.w)){
				let sym = vocab_rev[int(this._game_state.get(x, (FIELD_SIZE.h - 1) - y))]
				// y_rev = FIELD_SIZE.h - 1 - y
				result += sym
			}
			result += "<br>"
		}
		return result
	}
	send_key(action_id){
		let pressed_key = actions[action_id]

		if (pressed_key == up_key)
			this._player_position.y += 1

		if (pressed_key == down_key)
			this._player_position.y -= 1

		if (pressed_key == left_key)
			this._player_position.x -= 1

		if (pressed_key == right_key)
			this._player_position.x += 1

		this._player_position.x = clamp(this._player_position.x,0,FIELD_SIZE.w - 1)
		this._player_position.y = clamp(this._player_position.y,0,FIELD_SIZE.h - 1)

		this._update_game_state()

		for (let bullet of this._bullets){
			if (this._player_position.equals(bullet.origin)){
				this.reset()
				return GameResult.los
			}
		}

		if (this._animation_time > WIN_TIME){
			this.reset()
			return GameResult.win
		}

		return GameResult.none

	}
	action_id_for_action(action){
		if (actions.includes(action))
			return actions.indexOf(action)
		else
			return actions.indexOf(none_key)

	}
	stop(){

	}
	get_num_actions(){
		return len(actions)

	}
	state_shape(){
		return FIELD_SIZE.shape()

	}
	max_state_value(){
		return max_vocab_value

	}
	get_state(){
		return this._game_state

	}

	get_player_position(w,h,gameFildSize){
		return new Point(
			(this._player_position.x / gameFildSize.w) * w,
			h - (this._player_position.y / gameFildSize.h) * h
			)
	}

	get_bullets(){
		return this._bullets
	}
}


function state_with_channels(data){
	return np.expand_dims(data, axis=0)
}