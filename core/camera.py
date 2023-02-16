class Camera :
	def __init__ (self, target, screenSize) :
		self.screenOffset = [screenSize[0] * 0.5, screenSize[1] * 0.5]

		self.pos = [target.pos[0] - self.screenOffset[0], target.pos[1] - self.screenOffset[1]]
		self.target = target

		self.focusSpeed = 0.1


	def update (self, dt) :
		### move towards target
		self.pos[0] += (self.target.pos[0] - self.screenOffset[0] - self.pos[0]) * self.focusSpeed * dt
		self.pos[1] += (self.target.pos[1] - self.screenOffset[1] - self.pos[1]) * self.focusSpeed * dt