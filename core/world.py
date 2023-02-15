import pygame as pg

from math        import sqrt

from .file       import readFromJSON
from .background import LocationTypes

TileSize = 16



def distance (pos0, pos1) :
	return sqrt(
		(pos0[0] - pos1[0]) ** 2 +
		(pos0[1] - pos1[1]) ** 2)



class Tile :
	def __init__ (self, name, flip, pos) :
		### visuals
		self.img = pg.transform.flip(pg.image.load(f'assets/tiles/{name}'), flip[0], flip[1]).convert_alpha()

		### stats
		self.pos = ((pos[0] - 5) * TileSize, (pos[1] - 5) * TileSize)
		self.name = name[:-4:]


	def render (self, frame, cam, player) :
		img = self.img.copy()

		if 'void' in self.name :
			alpha = 255 - (distance(self.pos, player.pos) * 3)
			if alpha < 0 : alpha = 0
			img.set_alpha(alpha)

		frame.blit(img, [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])


class Location :
	def __init__ (self, tiles, name, cam) :
		self.tiles = tiles
		self.bg = LocationTypes[name](cam)


	def update (self, dt, cam) :
		self.bg.update(dt, cam)


	def render (self, frame, cam, player) :
		self.bg.render(frame, cam)
		[tile.render(frame, cam, player) for tile in self.tiles]


def loadLocation (player, cam) :
	file = readFromJSON(f'data/world/{player.location}.json')

	tiles = []
	for y, line in enumerate(file['CONTENT']) :
		for x, char in enumerate(line) :
			if not char in [' '] :
				info = file['CODES'][char] # [<file name>, <flip x>, <flip y>]

				tiles.append(Tile(info[0], (info[1], info[2]), (x, y)))

	return Location(tiles, file['TYPE'], cam)