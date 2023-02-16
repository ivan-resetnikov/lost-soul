import pygame as pg

### tiles
from math import dist

### files
from .file import readFromJSON

### location
from .background import LocationTypes

### NPC's
from .npc import NPC

TileSize = 16



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
			# change alpha based on distance from player
			alpha = 255 - (dist(self.pos, player.pos) * 3)
			if alpha < 0 : alpha = 0
			img.set_alpha(alpha)

		frame.blit(img, [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])


class Location :
	def __init__ (self, tiles, name, cam, npc) :
		self.bg = LocationTypes[name](cam)

		self.tiles = tiles

		self.npc = npc


	def update (self, dt, cam) :
		self.bg.update(dt, cam)

		[npc.update(dt) for npc in self.npc]


	def render (self, frame, cam, player) :
		self.bg.render(frame, cam)
		
		[tile.render(frame, cam, player) for tile in self.tiles]

		[npc.render(frame, cam, player) for npc in self.npc]



def loadLocation (player, cam) :
	file = readFromJSON(f'data/world/{player.location}.json')

	### load tiles
	tiles = []

	for y, line in enumerate(file['CONTENT']) :
		for x, char in enumerate(line) :
			if not char in [' '] :
				info = file['CODES'][char]

				tiles.append(Tile(info[0], (info[1], info[2]), (x, y)))

	### load NPC's
	npc = []

	for name in file['NPC'] : npc.append(NPC(name))

	### return data
	return Location(tiles, file['TYPE'], cam, npc)