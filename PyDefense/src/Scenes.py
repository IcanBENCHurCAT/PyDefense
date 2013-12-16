import pygame
from pygame.locals import *
import yaml
import MapLoader
import Towers


""" base Scene object """
screenW = 1024
screenH = 768

class Scene(object):
	
	
	def __init__(self):
		pass

	def render(self, screen):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def handle_events(self, events):
		raise NotImplementedError


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
		
		self.GUI = MapLoader.MapGUI(screenW, screenH)
		
	def render(self, screen):
		screen.fill((255,255,255))
		self.drawMap.render(screen)
		self.GUI.render(screen)
		
		if self.towerInHand:
			self.towerInHand.render(screen, Transparent=True)
			self.GUI.setSelectedText(self.towerInHand)
			self.hoverTower = None
		elif self.hoverTower:
			self.GUI.setSelectedText(self.hoverTower)
		else:
			self.GUI.selectedItem = ""

	def update(self):
		
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
			box = self.drawMap.getPlaceable(pygame.mouse.get_pos())
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
				x,y = pygame.mouse.get_pos()
				self.GUI.click(x, y, self.drawMap)
			
			#Capture the item hovering over
			if(event.type == MOUSEMOTION):
				if self.towerInHand is None:
					self.hoverTower = self.drawMap.getTower(*pygame.mouse.get_pos())
				


""" Title Screen Scene object """


class TitleScene(Scene):

	def __init__(self):
		super(TitleScene, self).__init__()
		self.title_font = pygame.font.SysFont('Open Sans', 60)
		self.sub_font = pygame.font.SysFont('Open Sans', 20)

	def render(self, screen):
		screen.fill((108, 192, 78))
		title_text = self.title_font.render('PyDefense', True,
											(255, 255, 255))
		sub_text = self.sub_font.render('press [space] to start', True,
										(255, 255, 255))
		
		w,h = self.title_font.size('PyDefense')
		screen.blit(title_text, (screenW / 2 - w / 2, 
								screenH / 2 - h /2))
		w,h = self.sub_font.size('press [space] to start')
		screen.blit(sub_text, (screenW / 2 - w /2, 
							(screenH / 2 + h / 2) + 100))

	def update(self):
		pass

	def handle_events(self, events):
		for e in events:
			if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
				self.manager.go_to(LevelScene('1'))
