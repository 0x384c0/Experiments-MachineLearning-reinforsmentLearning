const CANVAS_WIDTH = 512

class PlayerObject{}

class PixiJSRenderer{
	constructor(game,element){
		this.playerObject = new PlayerObject()
		this.game = game
		this.element = element
		this.app = new PIXI.Application(CANVAS_WIDTH, CANVAS_WIDTH * (FIELD_SIZE.h / FIELD_SIZE.w), {backgroundColor : 0x000000})
		this._objects = []

		element.appendChild(this.app.view)
		this.app.view.className = element.className 
		this._createBackground()

		// let app = this.app
		// var bunny = PIXI.Sprite.fromImage('img/bunny.png')
		// bunny.anchor.set(0.5);
		// bunny.x = app.screen.width / 2;
		// bunny.y = app.screen.height / 2;
		// app.stage.addChild(bunny);
	}

	nextFrame(){
		let newObjects = [new GameObject(this.game.get_player_position(this.app.screen.width, this.app.screen.height, FIELD_SIZE),this.playerObject)]
		for (let bullet of this.game.get_bullets()){
			newObjects.push(new GameObject(bullet.originFloat(this.app.screen.width, this.app.screen.height, FIELD_SIZE),bullet))
		}

		let added =  newObjects.filter(x => !this._includes(this._objects,x))
		let intersection = this._objects.filter(x => this._includes(newObjects,x))
		let removed = this._objects.filter(x => !this._includes(newObjects,x))

		for (let object of added){
			if (object.object == this.playerObject){
				let charcterImages = [
					'img/player/reimu.png',
					'img/player/marisa.png',
					'img/player/cirno.png',
				]
				let image = random.choice(charcterImages)
				object.createSprite(this._createAnimatedSprite(image))
			} else{
				object.createSprite(this._createSprite('img/bullet.png'))
			}
			this.app.stage.addChild(object.sprite)
		}
		
		for (let object of intersection){
			let origin = newObjects.find((newObject) => {return newObject.object == object.object }).origin
			object.update(origin)
		}

		for (let object of removed){
			this.app.stage.removeChild(object.sprite)
		}

		this._objects = added.concat(intersection)
	}

	_includes(array,otherGameObject){
		for (let gameObject of array){
			if (gameObject.object == otherGameObject.object){
				return true
			}
		}
		return false
	}

	_createBackground(){
		let container = new PIXI.Container()
		let stg3bg1 = new PIXI.extras.TilingSprite( PIXI.Texture.fromImage('img/stage03/stg3bg1.png'), this.app.screen.width, this.app.screen.height )
		
		let stg3bg3l = new PIXI.extras.TilingSprite( PIXI.Texture.fromImage('img/stage03/stg3bg3.png'), this.app.screen.width, this.app.screen.height * 2 )
		stg3bg3l.scale.x = 0.5
		stg3bg3l.scale.y = 0.5
		let stg3bg2r = new PIXI.extras.TilingSprite( PIXI.Texture.fromImage('img/stage03/stg3bg3.png'), this.app.screen.width, this.app.screen.height * 2 )
		stg3bg2r.scale.x = 0.5
		stg3bg2r.scale.y = 0.5
		stg3bg2r.rotation = PI
		stg3bg2r.x = this.app.screen.width
		stg3bg2r.y = this.app.screen.height

		let stg3bg4l = new PIXI.extras.TilingSprite( PIXI.Texture.fromImage('img/stage03/stg3bg4.png'), this.app.screen.width, this.app.screen.height * 4 )
		stg3bg4l.scale.x = 0.25
		stg3bg4l.scale.y = 0.25
		let stg3bg4r = new PIXI.extras.TilingSprite( PIXI.Texture.fromImage('img/stage03/stg3bg4.png'), this.app.screen.width, this.app.screen.height * 4 )
		stg3bg4r.scale.x = 0.25
		stg3bg4r.scale.y = 0.25
		stg3bg4r.rotation = PI
		stg3bg4r.x = this.app.screen.width
		stg3bg4r.y = this.app.screen.height

		container.addChild(stg3bg1)
		container.addChild(stg3bg3l)
		container.addChild(stg3bg2r)
		container.addChild(stg3bg4l)
		container.addChild(stg3bg4r)
		container.alpha = 0.5
		this.app.stage.addChild(container)
		this.app.ticker.add(function() {
			stg3bg1.tilePosition.y += 0.25
			stg3bg3l.tilePosition.y += 1
			stg3bg2r.tilePosition.y -= 1
			stg3bg4l.tilePosition.y += 4
			stg3bg4r.tilePosition.y -= 4
		})
	}
	_createSprite(image){
		return PIXI.Sprite.fromImage(image)
	}
	_createAnimatedSprite(image){
		let 
		frameW = 256 / 8,
		frameH = 50
		let baseTex = PIXI.Texture.fromImage(image);
		let frames = [];
		for (let i of range(8)){
			frames.push(new PIXI.Rectangle( i * frameW, 0, frameW, frameH))
		}
		let textures = frames.map(function(frame) { return new PIXI.Texture(baseTex, frame); });
		let sprite = new PIXI.extras.AnimatedSprite(textures)
		sprite.animationSpeed = 0.1
		sprite.play()
		return sprite
	}
}


class GameObject{
	constructor(origin,object){
		this.origin = origin
		this.object = object
		this.sprite = null
	}
	createSprite(sprite){
		this.sprite = sprite
		this.sprite.anchor.set(0.5)
		this.update(origin)
	}
	update(origin){
		this.origin = origin
		this.sprite.x = this.origin.x
		this.sprite.y = this.origin.y
	}
}
