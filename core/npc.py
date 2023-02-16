import pygame as pg

from .file import readFromJSON



class NPC :
	def __init__ (self, name) :
		content = readFromJSON(f'data/npc/{name}.json')

		### stats
		self.name = content['name']

		### position
		self.pos      = content['location']['pos']
		self.location = content['location']['location']

		### visuals
		self.img = {}
		for name in list(content['img'].keys())[1::] :
			images = []
			for file in content['img'][name] :
				path = 'assets/npc/' + content['img']['img path'] + '/' + file

				images.append(pg.image.load(path).convert_alpha())

				self.img[name] = images

		self.anim = {'idle': 0}


	def update (self, dt) :
		pass


	def render (self, frame, cam) :
		frame.blit(self.animate(), [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])


	def animate (self) :
		self.anim['idle'] += 1

		if self.anim['idle'] >= 60 : self.anim['idle'] = 0

		if self.anim['idle'] >= 0  and self.anim['idle'] <  30 : img = self.img['idle'][0]
		if self.anim['idle'] >= 30 and self.anim['idle'] <= 60 : img = self.img['idle'][1]

		return img