import pygame
import pygame.locals
import sys
sys.path.append("../../pytmx")

def initSave():
	import sqlite3
	conn = sqlite3.connect('game.db')
	db = conn.cursor()
	db.execute('''CREATE TABLE IF NOT EXISTS save_set (id INTEGER PRIMARY KEY,
		title TEXT, date DATETIME)''')
	conn.commit()

if __name__ == "__main__":
	initSave()
	pygame.init()
	pygame.font.init()
	from Scenes import SceneManager,screenW,screenH
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
		if(keys[pygame.K_SPACE]):
			timeScaler = 3.0
		else:
			timeScaler = 1.0

		manager.scene.handle_events(pygame.event.get())
		manager.scene.update()
		manager.scene.render(screen)


		pygame.display.flip()
