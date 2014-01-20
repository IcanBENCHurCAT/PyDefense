import pygame
from pygame.locals import *
import yaml
import MapLoader
import Towers


""" base Scene object """

#TODO: These values need to be determined via options and a configuration manager
baseScreenW = 1024
baseScreenH = 768
#screenW = 1280
#screenH = 960
screenW = 1024
screenH = 768
wRatio = float(baseScreenW) / float(screenW)
hRatio = float(baseScreenH) / float(screenH)

class Scene(object):
	
	
	def __init__(self):
		pass

	def render(self, screen):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def handle_events(self, events):
		raise NotImplementedError
	
	def getCursorXY(self):
		x,y = pygame.mouse.get_pos()
		x = x * wRatio
		y = y * hRatio
		return (x,y)


""" SceneManager object """


class SceneManager(object):

	def __init__(self):
		self.go_to(TitleScene())

	def go_to(self, scene):
		self.scene = scene
		self.scene.manager = self


""" Level Scene object """


class LevelScene(Scene):
	drawMap = None
	GUI = None 
	fighter = Towers.FighterTower
	archer = Towers.ArcherTower
	mage = Towers.MageTower
	towers = [fighter, archer, mage]

	towerInHand = None
	hoverTower = None
	selectedTower = -1
	currentLevel = 0
	save_id = None
	
	
	def __init__(self, level_name):
		super(LevelScene, self).__init__()
		assets_path = '../assets/'
		yaml_file = open(assets_path + level_name + '.lvl.yaml')
		level_data = yaml.safe_load(yaml_file)
		yaml_file.close()
		self.currentLevel = int(level_name)

		map_data = level_data.get('level')
		enemy_list = level_data.get('enemies')
		
		self.drawMap = MapLoader.MapLoader(assets_path + map_data['map'])
		if enemy_list:
			self.drawMap.buildEnemyQueue(enemy_list)
		
		self.GUI = MapLoader.MapGUI(baseScreenW, baseScreenH)
		from Animators import PauseMenu
		self.pause_menu = PauseMenu((screenW * .8, screenH * .8),(200,200,200),center=pygame.display.get_surface().get_rect().center, alpha=128)
		self.is_paused = False
		self.pause_menu.initExit(self.exitToMain)
		self.pause_menu.initSave(self.saveGame)
		
		
		
	def exitToMain(self):
		self.manager.go_to(TitleScene())
		
	def saveGame(self):
		self.manager.go_to(SaveScene(self))
	def render(self, screen):
		screen.fill((255,255,255))
		surface = pygame.Surface((baseScreenW, baseScreenH))
		
		self.drawMap.render(surface)
		self.GUI.render(surface)
		
		if self.towerInHand:
			self.towerInHand.render(surface, Transparent=True)
			self.GUI.setSelectedText(self.towerInHand)
			self.hoverTower = None
		elif self.hoverTower:
			self.GUI.setSelectedText(self.hoverTower)
		else:
			self.GUI.selectedItem = ""
			
		surface = pygame.transform.scale(surface, (screenW, screenH))
		screen.blit(surface, (0,0))
		if self.is_paused:
			self.pause_menu.render(screen)
	
	def update(self):
		if self.is_paused:
			return self.pause_menu.cursorUpdate(pygame.mouse.get_pos())
		if self.drawMap.winning:
			self.GUI.winning = True
			return
		if self.drawMap.losing:
			self.GUI.losing = True
			return
	
		self.drawMap.update()
		self.GUI.money = self.drawMap.money
		self.GUI.health = self.drawMap.health
		if (self.selectedTower <> -1):
			box = self.drawMap.getPlaceable(self.getCursorXY())
			if box: 
				if self.towerInHand is None:
					self.towerInHand = self.towers[self.selectedTower]()
					self.towerInHand.showRadius = True
				
				self.towerInHand.setLocation(box)
				
				pygame.mouse.set_cursor(*pygame.cursors.arrow)
			else:
				pygame.mouse.set_cursor(*pygame.cursors.broken_x)
				self.towerInHand = None
		else:
			pygame.mouse.set_cursor(*pygame.cursors.arrow)
			self.towerInHand = None
			
	def handle_events(self, events):
		for event in events:
			if self.is_paused:
				if event.type == MOUSEBUTTONUP:
					self.pause_menu.click(pygame.mouse.get_pos())
				if event.type == KEYUP:
					if event.key == K_ESCAPE:
						self.is_paused = False
				continue
			if (event.type == KEYDOWN ):
				if self.drawMap.winning:
					self.manager.go_to(LevelScene(str(self.currentLevel + 1)))
				if self.drawMap.losing:
					self.manager.go_to(LevelScene(str(self.currentLevel)))
				if (event.key == K_TAB):
					self.drawMap.sendNextWave()
				if (event.key == K_1):
					self.selectedTower = 0
				if (event.key == K_2):
					self.selectedTower = 1
				if (event.key == K_3):
					self.selectedTower = 2
				if (event.key == K_ESCAPE ):
					self.selectedTower = -1
					self.GUI.closeTowerMenu()
					self.hoverTower = None
				
				if self.selectedTower <> -1:
					self.towerInHand = None
					self.GUI.closeTowerMenu()
			
			if (event.type == MOUSEBUTTONDOWN):
				if self.towerInHand and self.drawMap.money >= self.towerInHand.cost:
					self.drawMap.placeTower(self.towerInHand)
					self.drawMap.money -= self.towerInHand.cost
					self.towerInHand.showRadius = False
					self.selectedTower = -1
				elif self.hoverTower:
					if self.GUI.openTower:
						self.GUI.closeTowerMenu()
					self.GUI.openTowerMenu(self.hoverTower)
				x,y = self.getCursorXY()
				self.GUI.click(x, y, self.drawMap)
			
			#Capture the item hovering over
			if(event.type == MOUSEMOTION):
				if self.towerInHand is None:
					self.hoverTower = self.drawMap.getTower(*self.getCursorXY())
				
			if event.type == KEYUP:
					if event.key == K_ESCAPE:
						self.is_paused = True

""" Title Screen Scene object """


class TitleScene(Scene):

	def __init__(self):
		super(TitleScene, self).__init__()
		self.title_font = pygame.font.SysFont('Open Sans', 60)
		self.sub_font = pygame.font.SysFont('Open Sans', 20)
		from Animators import StartMenu
		self.menu = StartMenu((screenW,screenH), (10,10,10))
		self.menu.initStart(self.newGame)
		self.menu.initExit(self.exitGame)

	def render(self, screen):
		self.menu.render(screen)
		title_text = self.title_font.render('PyDefense', True,
											(255, 255, 255))
# 		
		w,h = self.title_font.size('PyDefense')
		screen.blit(title_text, (screenW / 2 - w / 2, 
								100))

	def update(self):
		self.menu.cursorUpdate(pygame.mouse.get_pos())
		
	def newGame(self):
		self.manager.go_to(LevelScene('1'))
		
	def exitGame(self):
		exit()

	def handle_events(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				self.menu.click(pygame.mouse.get_pos())
				
class SaveScene(Scene):
	
	def __init__(self, last_scene):
		super(SaveScene, self).__init__()
		self.title_font = pygame.font.SysFont('Open Sans', 60)
		#self.sub_font = pygame.font.SysFont('Open Sans', 20)
		from Animators import SaveMenu
		self.menu = SaveMenu((screenW,screenH), (10,10,10))
		self.menu.initOK(self.saveOK)
		self.menu.initCancel(self.saveCancel)
		self.menu.initSelectSlot(self.selectSlot)
		self.last_scene = last_scene
		label = 'Save Your Game'
		self.title_text = self.title_font.render(label, True,
											(255, 255, 255))
		w,h = self.title_font.size(label)
		self.position = (screenW / 2 - w / 2, 100)
		
		self.save_slot = 1
		self.save_title = "Random Name"
		
	def render(self, screen):
		self.menu.render(screen)
		screen.blit(self.title_text, self.position)

	def update(self):
		self.menu.cursorUpdate(pygame.mouse.get_pos())

	def handle_events(self, events):
		for e in events:
			if e.type == pygame.MOUSEBUTTONDOWN:
				self.menu.click(pygame.mouse.get_pos())
				
	def selectSlot(self, slot, title):
		self.save_slot = slot
		self.save_title = title
		
	def saveOK(self, overwrite=False):
		import sqlite3
		import time
		conn = sqlite3.connect('game.db')
		db = conn.cursor()
		db.execute("SELECT * FROM save_set WHERE id=?", [self.save_slot])
		reply = db.fetchone()
		if reply:
			if overwrite == False:
				return False
		current_time = time.strftime("%Y-%m-%d  %H:%M:%S" ) 
		db.execute("INSERT INTO save_set VALUES(?, ?, ?)", [self.save_slot, self.save_title, current_time])
		conn.commit()
		self.manager.go_to(self.last_scene)
	
	def saveCancel(self):
		self.manager.go_to(self.last_scene)