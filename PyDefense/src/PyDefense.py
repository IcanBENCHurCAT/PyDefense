import pygame
import pygame.locals
import sys
sys.path.append("../../pytmx")
from Animators import *


from Scenes import *

if __name__ == "__main__":

	pygame.init()
	screen = pygame.display.set_mode((screenW, screenH))
	clock = pygame.time.Clock()

	manager = SceneManager()
	timeScaler = 1.0


	""" start main loop """

	game_over = False
	while not game_over:
		
		clock.tick(60 * timeScaler)
		
		if pygame.event.get(pygame.QUIT):
			game_over = True
		
		keys = pygame.key.get_pressed()
		if(keys[K_SPACE]):
			timeScaler = 3.0
		else:
			timeScaler = 1.0

		manager.scene.handle_events(pygame.event.get())
		manager.scene.update()
		manager.scene.render(screen)


		pygame.display.flip()
