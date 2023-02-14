import pygame as pg

import core



class Game :
	def __init__ (self) :
		### settings
		self.windowSize = (1000, 800)
		self.renderSize = (250, 200)
		self.title = 'Lost Soul | V 1.0'

		self.fps = 60
		self.dt  = 1

		### window
		self.window = pg.display.set_mode(self.windowSize)
		self.frame  = pg.Surface(self.renderSize)
		self.clock  = pg.time.Clock()
		pg.display.set_caption(self.title)


	def update (self) :
		self.player.update(self.dt, self.location)
		self.camera.update()


	def render (self) :
		self.frame.fill((34, 32, 52))
		### render
		[tile.render(self.frame, self.camera) for tile in self.location]

		self.player.render(self.frame, self.camera)

		### update screen
		self.window.blit(pg.transform.scale(self.frame, self.windowSize), (0, 0))
		self.clock.tick(self.fps)
		pg.display.flip()


	def run (self) :
		self.onStart()

		self.running = True
		while self.running :
			for event in pg.event.get() :
				if event.type == pg.QUIT :
					self.running = False


			self.update()
			self.render()

		pg.quit()
		pg.font.quit()
		pg.mixer.quit()


	def onStart (self) : # 132, 16, 28
		self.player = core.Player()
		self.camera = core.Camera(self.player, self.renderSize)

		self.location = core.loadLocation(self.player)



if __name__ == '__main__' :
	Game().run()