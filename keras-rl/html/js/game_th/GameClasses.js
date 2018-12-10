
var GameResult = Object.freeze({
	"win":1.0, 
	"los":-1.0, 
	"none":0.005
})

class Point{
	constructor(x,y){
		this.x = x
		this.y = y
	}
	equals(other){
		return int(other.x) == int(this.x) && int(other.y) == int(this.y)
	}
}

class Size extends Point{
	get w(){
		return this.x
	}

	get h(){
		return this.y
	}

	shape(){
		return [this.w,this.h]
	}
}

class Bullet{

	constructor(origin, velocity, time){
		this._origin = origin
		this.velocity = velocity
		this._prev_time = time
	}

	get origin(){
		return new Point(int(this._origin.x),int(this._origin.y))
	}

	move(time){
		let time_diff = float(time - this._prev_time)
		this._prev_time = time
		this._origin = new Point(this._origin.x + time_diff * this.velocity.x, this._origin.y + time_diff * this.velocity.y)
	}

	originFloat(w,h,gameFildSize){
		return new Point(
			(this._origin.x / gameFildSize.w) * w,
			h - (this._origin.y / gameFildSize.h) * h
			)
		// return  new Point(this._origin.x,this._origin.y)
	}
}

// single emitters	
class BulletEmitter{
	constructor(origin, speed, delay, angle, angle_generator=null){
		this.origin = origin
		this.speed = speed
		this.delay = delay
		this.angle = angle
		this.angle_generator = angle_generator
	}

	emit(time, bullets){
		if (time % this.delay == 0){
			let angle = this.angle
			if (this.angle_generator != null){
				let diff = this.angle_generator.get_angle(time)
				if (diff != null)
					angle += diff
				else
					return
			}
			bullets.push( new Bullet(this.origin, new Point(sin(angle) * this.speed, cos(angle) * this.speed), time))
		}
	}
}

// circle emitters
class CircleBulletEmitter{
	constructor(origin, delay, speed, num_rays, angle_generator=null){

		this.__emitters = []
		for (let n of range(num_rays)){
			this.__emitters.push(new BulletEmitter(origin, speed, delay, PI * 2. * (float(n)/float(num_rays)),angle_generator))
		}
	}

	emit(time, bullets){
		for (let emitter of this.__emitters){
			emitter.emit(time,bullets)
		}
	}
}

class CircleWithHoleBulletEmitter{
	constructor(origin, delay, speed, num_rays, angle_min, angle_max, angle_generator=null){
		this.__emitters = []
		for (let n of range(num_rays)){
			let angleDiff = angle_max - angle_min
			let andgle = angle_min + angleDiff * (float(n)/float(num_rays))
			this.__emitters.push(new BulletEmitter(origin, speed, delay, andgle, angle_generator))
		}
	}

	emit(time, bullets){
		for (let emitter of this.__emitters){
			emitter.emit(time,bullets)
		}
	}
}

// var angle
class AngleGeneratorLinear{

	constructor( diff, period, start_offset){
		this.diff = diff
		this.period = float(period)
		this.start_offset = start_offset
	}

	get_angle(i_time){
		let time = float(i_time)


		let f2time = this.period*2. * fract(time/(this.period*2.))

		if (this.start_offset != null){

			if (this.start_offset && f2time >= this.period){
				return null
			}

			if (!this.start_offset && f2time < this.period){
				return null
			}
		}

		return this.diff * fract(time/this.period) 
	}
}

class AngleGeneratorSine{
	
	constructor( diff, period){
		this.diff = diff
		this.period = float(period)
	}

	get_angle(time){
		return this.diff * sin(fract(time/this.period) * PI * 2  )
	}
}