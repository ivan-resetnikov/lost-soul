import pygame as pg

from  math import dist
from .file import readFromJSON

from RPGtext import Text



class NPC :
	def __init__ (self, name) :
		content = readFromJSON(f'data/npc/{name}.json')

		### stats
		self.name = content['name']

		### position
		self.pos      = content['location']['pos']
		self.location = content['location']['location']

		### dialogue
		self.dialogue = Text(r'<"effects": {"shake":1}, "font": {"color": [255, 0, 0]}>Hey! <"effects":{"shake":0}, "font": {"color": [255, 255, 255]}>What are you doing here!', 'assets/font/pixel.ttf', 5, 1, False)

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


	def render (self, frame, cam, player) :
		img = self.animate()

		if dist(self.pos, player.pos) < 75 :
			if self.pos[0] < player.pos[0] :img = pg.transform.flip(img, True, False)

		frame.blit(img, [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])

		self.dialogue.render(frame, [
			self.pos[0] - cam.pos[0] + 8,
			self.pos[1] - cam.pos[1] - 10], centered=True)


	def animate (self) :
		self.anim['idle'] += 1

		if self.anim['idle'] >= 60 : self.anim['idle'] = 0

		if self.anim['idle'] >= 0  and self.anim['idle'] <  30 : img = self.img['idle'][0]
		if self.anim['idle'] >= 30 and self.anim['idle'] <= 60 : img = self.img['idle'][1]

		return img