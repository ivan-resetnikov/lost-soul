import pygame as pg

from math import sin, dist

from .file import readFromJSON

from random import randint


Font = pg.font.Font('assets/font/pixel.ttf', 5)



class Text :
	def __init__ (self, text, color, effects, speed, pos, i) :
		self.img = Font.render(text, 0, color)
		self.effects = {'wave': effects['wave'], 'shake': effects['shake'], 'shake speed': effects['shake speed']}

		self.speed = speed

		self.pos = pos

		self.i = i

		self.shakeCooldown = 0

		self.constantOffset = [0, 0]


	def render (self, frame, cam, time, boxSize, parentPos, parentImage) :
		offset = [0, 0]

		offset[1] += sin((time + self.i)) * self.effects['wave']

		self.shakeCooldown += 1

		if self.shakeCooldown == self.effects['shake speed']:
			self.constantOffset[0] = randint(-self.effects['shake'], self.effects['shake'])
			self.constantOffset[1] = randint(-self.effects['shake'], self.effects['shake'])
			self.shakeCooldown = 0

		frame.blit(self.img, (
			(self.pos[0] + offset[0] + self.constantOffset[0]) - cam.pos[0] + parentPos[0] - (boxSize[0] * 0.35) - (parentImage.get_width() * 0.5),
			(self.pos[1] + offset[1] + self.constantOffset[1]) - cam.pos[1] + parentPos[0] - 7))



class NPC :
	def __init__ (self, name) :
		content = readFromJSON(f'data/npc/{name}.json')

		### stats
		self.name = content['name']

		### position
		self.pos      = content['location']['pos']
		self.location = content['location']['location']

		### dialogue
		self.dialogue = list(content['dialogue'].values())[0]
		self.updateDialogue()

		### visuals
		self.img = {}
		for name in list(content['img'].keys())[1::] :
			images = []
			for file in content['img'][name] :
				path = 'assets/npc/' + content['img']['img path'] + '/' + file

				images.append(pg.image.load(path).convert_alpha())

				self.img[name] = images

		self.anim = {'idle': 0}

		self.time = 0


	def update (self, dt) :
		self.time += 0.1


	def render (self, frame, cam, player) :
		img = self.animate()

		if dist(self.pos, player.pos) < 75 :
			if self.pos[0] < player.pos[0] : img = pg.transform.flip(img, True, False)

		frame.blit(img, [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])

		pos = [
				self.pos[0] - cam.pos[0] - (self.dialogueBoxSize[0] * 0.35) - (self.img['idle'][0].get_width() * 0.5),
				self.pos[1] - cam.pos[1] - 5 - 10]

		pg.draw.rect(frame, (34, 32, 52), (pos[0]-3, pos[1]-4, self.dialogueBoxSize[0]+2, self.dialogueBoxSize[1]))
		pg.draw.rect(frame, (255, 255, 255), (pos[0]-4, pos[1]-5, self.dialogueBoxSize[0]+4, self.dialogueBoxSize[1]+2), 1)

		x, y = 0, 0
		for letter in self.letters :
			letter.render(frame, cam, self.time, self.dialogueBoxSize, self.pos, self.img['idle'][0])

			x += letter.img.get_width() + 5


	def updateDialogue (self) :
		text = self.dialogue['text']

		stats = {
			'speed'   : 5,
			'color'   : (255, 255, 255),
			'effects' : {'wave': 0, 'shake': 0, 'shake speed': 6},
		}

		self.letters = []

		i = 0

		x, y = 0, -10

		for element in text :
			type_ = str(type(element))[8:-2:]

			if type_ == 'dict' :
				if 'speed'   in element : stats['speed']   = element['speed']
				if 'color'   in element : stats['color']   = element['color']
				if 'effects' in element :
					if 'wave'  in element['effects'] : stats['effects']['wave']  = element['effects']['wave']
					if 'shake' in element['effects'] : stats['effects']['shake'] = element['effects']['shake']
					if 'shake speed' in element['effects'] : stats['effects']['shake speed'] = element['effects']['shake speed']

			elif type_ == 'str' :
				for letter in element :
					self.letters.append(Text(
						letter,
						stats['color'],
						stats['effects'],
						stats['speed'],
						[x, y], i))

					i += 1

					x += 6

				x += 5

		self.dialogueBoxSize = [x-3, y+10+7+8]


	def animate (self) :
		self.anim['idle'] += 1

		if self.anim['idle'] >= 60 : self.anim['idle'] = 0

		if self.anim['idle'] >= 0  and self.anim['idle'] <  30 : img = self.img['idle'][0]
		if self.anim['idle'] >= 30 and self.anim['idle'] <= 60 : img = self.img['idle'][1]

		return img