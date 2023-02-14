import pygame as pg

from random import randint

from .file import readFromJSON

TileSize = 16




class VoidBG :
	def __init__ (self) :
		self.rects = []
		self.rectSpawnCooldown = 0


	def update (self, dt, cam) :
		if self.rectSpawnCooldown > 0 : self.rectSpawnCooldown -= 1

		if self.rectSpawnCooldown == 0 :
			size = randint(8, 32)
			img = pg.Surface((size, size))
			darken = randint(0, 30)
			pg.draw.rect(img, (172 - darken, 50 - darken, 50 - darken), (0, 0, size, size), 3)
			img.set_colorkey((0, 0, 0))
			img.set_alpha(randint(70, 200))
			z = randint(2, 7)
			self.rects.append([img, [randint(round(0 - (cam.pos[0] / z)), round(250 - (cam.pos[0] / z))), 200 + 32], img, 0, z])

			self.rectSpawnCooldown = 60


	def render (self, frame, cam) :
		for rect in self.rects :
			frame.blit(rect[0], (
				rect[1][0] - (rect[0].get_width()  * 0.5) - (cam.pos[0] / rect[4]),
				rect[1][1] - (rect[0].get_height() * 0.5) - (cam.pos[1] / (rect[4] * 2))))
			rect[3] += 0.5
			rect[0] = pg.transform.rotate(rect[2], rect[3])
			rect[1][1] -= 0.25


LocationTypes = {
	'void': VoidBG
}


class Location :
	def __init__ (self, tiles, name) :
		self.tiles = tiles
		self.bg = LocationTypes[name]()


	def update (self, dt, cam) :
		self.bg.update(dt, cam)


	def render (self, frame, cam) :
		self.bg.render(frame, cam)
		[tile.render(frame, cam) for tile in self.tiles]



def loadLocation (player) :
	file = readFromJSON(f'data/world/{player.location}.json')

	tiles = []
	for y, line in enumerate(file['CONTENT']) :
		for x, char in enumerate(line) :
			if not char in [' '] :
				info = file['CODES'][char] # [<file name>, <flip x>, <flip y>]

				tiles.append(Tile(info[0], (info[1], info[2]), (x, y)))

	return Location(tiles, file['TYPE'])



class Tile :
	def __init__ (self, name, flip, pos) :
		### visuals
		self.img = pg.transform.flip(pg.image.load(f'assets/tiles/{name}'), flip[0], flip[1]).convert_alpha()

		### stats
		self.pos = ((pos[0] - 5) * TileSize, (pos[1] - 5) * TileSize)
		self.name = name[:-4:]


	def render (self, frame, cam) :
		frame.blit(self.img, [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])