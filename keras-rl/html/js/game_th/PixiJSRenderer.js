class PlayerObject{}

class PixiJSRenderer{
	constructor(game,element){
		this.playerObject = new PlayerObject()
		this.game = game
		this.element = element
		this.app = new PIXI.Application(800, 600, {backgroundColor : 0x000000})
		this._objects = []

		element.appendChild(this.app.view)


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
			if (object.object == this.playerObject)
				object.createSprite('img/cirno.png')
			else
				object.createSprite('img/bullet.png')
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
}


class GameObject{
	constructor(origin,object){
		this.origin = origin
		this.object = object
		this.sprite = null
	}
	createSprite(image){
		this.sprite = PIXI.Sprite.fromImage(image)
		this.sprite.anchor.set(0.5)
		this.update(origin)
	}
	update(origin){
		this.origin = origin
		this.sprite.x = this.origin.x
		this.sprite.y = this.origin.y
	}
}
