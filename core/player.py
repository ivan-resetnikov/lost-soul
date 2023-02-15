from .sound import Sounds

import pygame as pg

Controller = {
	'speed': 0.8,

	'run_friction': 0.6,
	'brake_friction': 0.4,

	'jump_force': -3.5,
	'coyote_jump_time': 11,

	'jump_gravity' : 0.1,
	'glide_gravity': 0.07,
	'fall_gravity' : 0.2
}




def colliding (obj0, colliders) :
	colliding = False

	for obj1 in colliders :
		if pg.Rect((obj0.pos[0], obj0.pos[1], 16, 16)).colliderect((obj1.pos[0], obj1.pos[1], 16, 16)) :
			colliding = True

	return colliding


class Player :
	def __init__ (self) :
		### visuals & animation
		self.img = [
			pg.image.load('assets/player/idle.0.png').convert_alpha(),
			pg.image.load('assets/player/idle.1.png').convert_alpha(),
			pg.image.load('assets/player/walk.0.png').convert_alpha(),
			pg.image.load('assets/player/walk.1.png').convert_alpha(),
			pg.image.load('assets/player/walk.2.png').convert_alpha(),
			pg.image.load('assets/player/jump.png').convert_alpha(),
			pg.image.load('assets/player/fall.png').convert_alpha(),
			pg.image.load('assets/player/glide.png').convert_alpha()]


		self.anim = {'idle': 0, 'walk': 0}

		### state
		self.pos = [0, 0]
		self.vel = [0, 0]

		self.location = 0

		### physics
		self.holding_space = False
		self.time_since_landed = 0
		self.last_pressed = 'd'


	def update (self, dt, colliders) :
		self.dt = dt

		keys = pg.key.get_pressed()

		### horizontal movement
		if keys[pg.K_a] :
			self.vel[0] -= Controller['speed']
			self.last_pressed = 'a'
		if keys[pg.K_d] :
			self.vel[0] += Controller['speed']
			self.last_pressed = 'd'

		self.pos[0] += self.vel[0]

		# wall colliding
		if colliding(self, colliders) : self.pos[0] -= self.vel[0]

		# friction
		if keys[pg.K_a] or keys[pg.K_d] :
			self.vel[0] *= Controller['run_friction'] * self.dt
		if not keys[pg.K_a] and not keys[pg.K_d] :
			self.vel[0] *= Controller['brake_friction'] * self.dt

		### gravity
		self.pos[1] += self.vel[1]

		self.pos[1] += 1

		# landing
		if colliding(self, colliders) :
			self.pos[1] -= self.vel[1]
			self.vel[1] = 0

			self.time_since_landed = Controller['coyote_jump_time']

		else :
			# gravity
			if self.vel[1] > 0 : self.vel[1] += Controller['fall_gravity'] * self.dt
			if self.vel[1] < 0 : self.vel[1] += Controller['jump_gravity'] * self.dt
			if self.vel[1] < 1 and self.vel[1] > -1 : self.vel[1] += Controller['glide_gravity'] * self.dt

		self.pos[1] += 1

		if colliding(self, colliders) :
			if not self.isLanded :
				Sounds['player']['land'].play()
			self.isLanded = True

		else : self.isLanded = False

		self.pos[1] -= 2

		### jumping

		# coyote jump timer
		if self.time_since_landed > 0 : self.time_since_landed -= 1

		# jump
		if keys[pg.K_SPACE] and self.time_since_landed > 0 and not self.holding_space :
			self.vel[1] = Controller['jump_force']
			self.holding_space = True

			self.pos[1] += self.vel[1]

			Sounds['player']['jump'].play()

		# cut jump height
		self.pos[1] += 3

		if (self.holding_space and not keys[pg.K_SPACE]) or (self.holding_space and colliding(self, colliders)) :
			self.vel[1] /= 3
			self.holding_space = False

		self.pos[1] -= 3


	def render (self, frame, cam) :
		frame.blit(self.animate(), [
			self.pos[0] - cam.pos[0],
			self.pos[1] - cam.pos[1]])


	def animate (self) :
		img = self.img[0]

		if self.anim['idle'] > 30 : self.anim['idle'] = 0
		if self.anim['walk'] > 30 : self.anim['walk'] = 0

		keys = pg.key.get_pressed()

		if self.isLanded and not keys[pg.K_a] and not keys[pg.K_d] :
			if self.anim['idle'] >= 0  and self.anim['idle'] < 15 : img = self.img[0]
			if self.anim['idle'] >= 15 and self.anim['idle'] < 30 : img = self.img[1]

			self.anim['idle'] += 1 * self.dt

		elif self.isLanded and (keys[pg.K_a] or keys[pg.K_d]) :
			if self.anim['walk'] >= 0  and self.anim['walk'] < 5  : img = self.img[2]
			if self.anim['walk'] >= 5  and self.anim['walk'] < 10 : img = self.img[3]
			if self.anim['walk'] >= 10 and self.anim['walk'] < 20 : img = self.img[4]

			if self.anim['walk'] in [5, 10, 20] : Sounds['player']['walk'].play()

			self.anim['walk'] += 1 * self.dt

		elif not self.isLanded :
			if self.vel[1] > 0 : img = self.img[6]
			if self.vel[1] < 0 : img = self.img[5]
			if self.vel[1] < 1 and self.vel[1] > -1 : img = self.img[7]

		if self.last_pressed == 'd' : img = pg.transform.flip(img, True, False)

		return img