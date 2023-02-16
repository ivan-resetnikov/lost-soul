import pygame as pg

from random import randint



class VoidBG :
	def __init__ (self, cam) :
		# rects
		self.rects = []
		self.rectSpawnCooldown = 0

		# leaves
		self.leaves = []
		self.leafSpawnCooldown = 0

		# rects
		for _ in range(15) :
			size = randint(8, 32)
			img = pg.Surface((size, size))
			darken = randint(0, 30)
			pg.draw.rect(img, (172 - darken, 50 - darken, 50 - darken), (0, 0, size, size), 3)
			img.set_colorkey((0, 0, 0))
			img.set_alpha(randint(70, 100))
			z = randint(2, 7)
			self.rects.append([img, [randint(round(0 + (cam.pos[0] / z)), round(250 + (cam.pos[0] / z))), randint(0, (200 + 32))], img, randint(0, 360), z])

		# leaves
		self.leafImg = pg.image.load('assets/objects/leaf.png').convert_alpha()
		self.leafImg.set_alpha(255)


	def update (self, dt, cam) :
		self.dt = dt

		if self.rectSpawnCooldown > 0 : self.rectSpawnCooldown -= 1 * self.dt
		if self.leafSpawnCooldown > 0 : self.leafSpawnCooldown -= 1 * self.dt

		### spawn rect
		if self.rectSpawnCooldown == 0 :
			# random size
			size = randint(8, 32)

			# image
			img = pg.Surface((size, size))
			darken = randint(0, 30)
			pg.draw.rect(img, (172 - darken, 50 - darken, 50 - darken), (0, 0, size, size), 3)
			img.set_colorkey((0, 0, 0))
			img.set_alpha(randint(70, 175))

			# depth for parallax effect
			z = randint(2, 9)

			pos = [
				randint(round(0 + (cam.pos[0] / z)),
				round(250 + (cam.pos[1] / z))), 200 + 32
			]

			self.rects.append([img, pos, img, 0, z])

			self.rectSpawnCooldown = 60

		### spawn leaf
		if self.leafSpawnCooldown == 0 :
			pos = [
				250 + 4 + cam.pos[0],
				randint(round(-100 - cam.pos[1]), round(200 - cam.pos[1]))
			]

			self.leaves.append([self.leafImg, pos, self.leafImg.copy(), 0, [-1, 0.25]])
			
			self.leafSpawnCooldown = 10


	def render (self, frame, cam) :
		### rects

		toRemove = []
		for rect in self.rects :
			# render rect
			frame.blit(rect[0], (
				rect[1][0] - (rect[0].get_width()  * 0.5) - (cam.pos[0] / rect[4]),
				rect[1][1] - (rect[0].get_height() * 0.5) - (cam.pos[1] / (rect[4] * 2))))

			# rotate rect
			rect[3] += 0.25 * self.dt
			rect[0] = pg.transform.rotate(rect[2], rect[3])

			# move rect
			rect[1][1] -= 0.125  * self.dt

			# remove useless rects
			if rect[1][1] < (-32 - (cam.pos[1] / rect[4]) ) : toRemove.append(rect)

		for rect in toRemove : self.rects.remove(rect)

		### leaves

		toRemove = []
		for leaf in self.leaves :
			# render leaf
			frame.blit(leaf[0], (
				leaf[1][0] - (leaf[0].get_width()  * 0.5) - cam.pos[0],
				leaf[1][1] - (leaf[0].get_height() * 0.5) - cam.pos[1]))

			# rotate image
			leaf[0] = pg.transform.rotate(leaf[2], leaf[3])
			leaf[3] += 1.5 * self.dt

			# move by its velocity
			leaf[1][0] += leaf[4][0] * self.dt
			leaf[1][1] += leaf[4][1] * self.dt

			# remove useless leaves
			if leaf[1][0] < -8 + cam.pos[0] : toRemove.append(leaf)

		for leaf in toRemove : self.leaves.remove(leaf)


LocationTypes = {
	'void': VoidBG
}