from math import pi as PI
from math import sin, cos, floor
from enum import Enum

#utils
def fract(x):
	return x - floor(x)


#classes
class GameResult(Enum):
	win = 1
	los = -1
	none = 1e-10

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

		
class BulletEmitter():
	def __init__(self, origin, angle, speed, delay):
		self.origin, self.angle, self.speed, self.delay = origin, float(angle), float(speed), float(delay)

	def emit(self,time, bullets):
		if time % self.delay == 0:
			bullets.append( Bullet(self.origin, Point(sin(self.angle) * self.speed, cos(self.angle) * self.speed), time))

class CircleBulletEmitter():
	def __init__(self, origin, num_rays, speed, delay):
		self.__emitters = []
		for n in range(num_rays):
			self.__emitters.append(BulletEmitter(origin, PI * 2. * (float(n)/float(num_rays)), speed, delay))

	def emit(self,time, bullets):
		for emitter in self.__emitters:
			emitter.emit(time,bullets)

class CircleWithHoleBulletEmitter():
	def __init__(self, origin, angleMin, angleMax, speed, delay):
		num_rays = 80
		self.__emitters = []
		for n in range(num_rays):
			angleDiff = angleMax - angleMin
			andgle = angleMin + angleDiff * (float(n)/float(num_rays))
			self.__emitters.append(BulletEmitter(origin, andgle, speed, delay))

	def emit(self,time, bullets):
		for emitter in self.__emitters:
			emitter.emit(time,bullets)


class VarAngleBulletEmitter():
	def __init__(self, origin, angleMin, angleMax, angleTime, startOffset, speed, delay):
		self.origin, self.angleMin, self.angleMax, self.angleTime, self.startOffset ,self.speed, self.delay = origin, angleMin, angleMax, float(angleTime), startOffset, speed, delay

	def emit(self,time, bullets):
		time = float(time)

		f2time = self.angleTime*2. * fract(time/(self.angleTime*2.))
		if self.startOffset and f2time >= self.angleTime:
			return

		if not self.startOffset and f2time < self.angleTime:
			return

		if time % self.delay == 0:
			angle = self.angleMin + (self.angleMax - self.angleMin) * fract(time/self.angleTime) 
			bullets.append( Bullet(self.origin, Point(sin(angle) * self.speed, cos(angle) * self.speed), time))