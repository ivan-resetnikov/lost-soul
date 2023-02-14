import pygame as pg

from .file import readFromJSON

TileSize = 16



def loadLocation (player) :
	file = readFromJSON(f'data/world/{player.location}.json')
	location = []

	for y, line in enumerate(file['CONTENT']) :
		for x, char in enumerate(line) :
			if not char in [' '] :
				info = file['CODES'][char] # [<file name>, <flip x>, <flip y>]

				location.append(Tile(info[0], (info[1], info[2]), (x, y)))

	return location



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