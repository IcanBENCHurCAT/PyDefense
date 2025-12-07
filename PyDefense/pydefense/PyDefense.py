import pygame
import pygame.locals
import sys
import os

def initSave():
	import sqlite3
	# Ensure game.db is created in the same directory as the script or a user data dir.
	# For simplicity, we keep it relative to this file.
	db_path = os.path.join(os.path.dirname(__file__), 'game.db')
	conn = sqlite3.connect(db_path)
	db = conn.cursor()
	db.execute('''CREATE TABLE IF NOT EXISTS save_set (id INTEGER PRIMARY KEY,
		title TEXT, date DATETIME)''')
	conn.commit()

def main():
	initSave()
	pygame.init()
	pygame.font.init()
	from .Scenes import SceneManager, screenW, screenH
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

if __name__ == "__main__":
	main()
