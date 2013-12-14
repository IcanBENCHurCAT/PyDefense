import pygame
import pygame.locals
import sys
sys.path.append("../../pytmx")


from Scenes import *

if __name__ == "__main__":

	pygame.init()
	screen = pygame.display.set_mode((screenW, screenH))
	clock = pygame.time.Clock()

	manager = SceneManager()

	""" start main loop """

	game_over = False
	while not game_over:

		clock.tick(60)

		if pygame.event.get(pygame.QUIT):
			game_over = True
			pass

		manager.scene.handle_events(pygame.event.get())
		manager.scene.update()
		manager.scene.render(screen)

		pygame.display.flip()
