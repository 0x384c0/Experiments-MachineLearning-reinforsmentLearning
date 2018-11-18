from math import pi as PI
from math import sin, cos, floor
from enum import Enum

#utils
def fract(x):
	return x - floor(x)


#classes
class GameResult(Enum):
	win = 1
	los = 0
	none = 1e-3

class Point():
	def __init__(self, x, y):
		self.x, self.y = x, y

	def __eq__(self, other):
		return int(other.x) == int(self.x) and int(other.y) == int(self.y)

class Size(Point):
	@property
	def w(self):
		return self.x

	@property
	def h(self):
		return self.y

	def shape(self):
		return (self.w,self.h)

class Bullet():
	def __init__(self, origin, velocity, time):
		self.__origin, self.velocity, self._prev_time = origin, velocity, time

	@property
	def origin(self):
		return Point(int(self.__origin.x),int(self.__origin.y))

	def move(self,time):
		time_diff = float(time - self._prev_time)
		self._prev_time = time
		self.__origin = Point(self.__origin.x + time_diff * self.velocity.x, self.__origin.y + time_diff * self.velocity.y)

# single emitters	
class BulletEmitter():
	def __init__(self, origin, speed, delay, angle, angle_generator=None):
		self.origin, self.speed, self.delay, self.angle, self.angle_generator = origin, float(speed), float(delay), float(angle), angle_generator

	def emit(self,time, bullets):
		if time % self.delay == 0:
			angle = self.angle
			if self.angle_generator is not None:
				diff = self.angle_generator.get_angle(time)
				if diff is not None:
					angle += diff
				else:
					return
			bullets.append( Bullet(self.origin, Point(sin(angle) * self.speed, cos(angle) * self.speed), time))




# circle emitters
class CircleBulletEmitter():
	def __init__(self, origin, delay, speed, num_rays):
		self.__emitters = []
		for n in range(num_rays):
			self.__emitters.append(BulletEmitter(origin, speed, delay, PI * 2. * (float(n)/float(num_rays))))

	def emit(self,time, bullets):
		for emitter in self.__emitters:
			emitter.emit(time,bullets)

class CircleWithHoleBulletEmitter():
	def __init__(self, origin, delay, speed, num_rays, angle_min, angle_max, angle_generator=None):
		self.__emitters = []
		for n in range(num_rays):
			angleDiff = angle_max - angle_min
			andgle = angle_min + angleDiff * (float(n)/float(num_rays))
			self.__emitters.append(BulletEmitter(origin, speed, delay, andgle, angle_generator))

	def emit(self,time, bullets):
		for emitter in self.__emitters:
			emitter.emit(time,bullets)




#var angle
class AngleGeneratorLinear():
	def __init__(self, diff, period, start_offset):
		self.diff, self.period, self.start_offset = diff, float(period), start_offset

	def get_angle(self,time):
		time = float(time)


		f2time = self.period*2. * fract(time/(self.period*2.))
		if self.start_offset and f2time >= self.period:
			return None

		if not self.start_offset and f2time < self.period:
			return None

		return self.diff * fract(time/self.period) 


class AngleGeneratorSine():
	def __init__(self, diff, period):
		self.diff, self.period = diff, float(period)

	def get_angle(self,time):
		return self.diff * sin(fract(time/self.period) * PI * 2  )
