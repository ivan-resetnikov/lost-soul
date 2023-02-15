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
		self.location.update(self.dt, self.camera)

		self.player.update(self.dt, self.location.tiles)
		self.camera.update(self.dt)


	def render (self) :
		pg.display.set_caption('{title} | FPS: {fps}'.format(title=self.title, fps=round(self.clock.get_fps())))
		self.frame.fill((34, 32, 52))

		### render
		self.location.render(self.frame, self.camera, self.player)
		self.player  .render(self.frame, self.camera)

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


	def onStart (self) :
		self.player = core.Player()
		self.camera = core.Camera(self.player, self.renderSize)

		self.location = core.loadLocation(self.player, self.camera)



if __name__ == '__main__' :
	Game().run()