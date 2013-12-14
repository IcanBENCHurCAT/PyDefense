'''
Created on Dec 3, 2013

@author: gparker
'''
import pygame
import locale
import Enemies

class MapGUI(object):
	screenW = 0
	screenH = 0
	selectedItem = ""
	openTower = None
	font = None
	btnUpgrade = None
	btnSell = None
	
	def __init__(self, width, height):
		locale.setlocale( locale.LC_ALL, '' )
		self.money = 200
		self.health = 100
		self.screenW = width
		self.screenH = height
		pygame.font.init()
		self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
		self.btnUpgrade = MapButton("Upgrade", self.font)
		self.btnSell = MapButton("Sell", self.font)
	
	def setSelectedText(self, tower):
		self.selectedItem = tower.name
		
	def openTowerMenu(self, tower):
		self.openTower = tower
		self.setSelectedText(tower)
		self.openTower.showRadius = True
	
	def closeTowerMenu(self):
		if self.openTower:
			self.openTower.showRadius = False
			self.openTower = None
	
	def click(self, x, y, theMap):
		if self.openTower:
			rec = self.sellLoc()
			if rec.collidepoint(x,y):
				theMap.money += (self.openTower.cost * .80) #Needs 'upgrade cost' added in
				theMap.removeTower(self.openTower)
				self.closeTowerMenu()
			rec = self.upgradeLoc()
			if rec.collidepoint(x,y) and self.openTower.level < self.openTower.maxLevel and self.money >= self.openTower.upgradeCost:
				theMap.money -= self.openTower.upgradeCost
				self.openTower.upgrade()
				self.closeTowerMenu()
	
	def render(self, surface):
		#Print Money top-left
		text = locale.currency( self.money, grouping=True )
		i = self.font.render(text, 1, (180,180,0))
		
		sizeX, sizeY = self.font.size(text)
		x = self.screenW - sizeX - 15
		y = 15
		surface.blit(i, (x,y))
		
		text = "HP: {0}".format(self.health)
		i = self.font.render(text, 1, (180, 180, 0))
		x,y = (15,15)
		surface.blit(i, (x,y))
		
		text = self.selectedItem
		i = self.font.render(text, 1, (180, 180, 0))
		sizeX, sizeY = self.font.size(text)
		x = 15
		y = self.screenH - sizeY - 15
		surface.blit(i, (x,y))
		
		if self.openTower:
			rec = self.sellLoc()
			self.btnSell.render(surface, (rec.x,rec.y))
			
			rec = self.upgradeLoc()
			self.btnUpgrade.render(surface, (rec.x,rec.y))
			
	def upgradeLoc(self):
		rec = self.sellLoc()
		rec.x -= self.btnUpgrade.width + 10
		rec.width = self.btnUpgrade.width
		rec.height = self.btnUpgrade.height
		return rec
	
	def sellLoc(self):
		x = self.screenW - self.btnSell.width - 15
		y = self.screenH - self.btnSell.height - 15
		rec = pygame.Rect(x, y, 
						self.btnSell.width, 
						self.btnSell.height)
		return rec
	
class MapButton(object):
	width = 0
	height = 0
	text = ""
	font = None
	surface = None
	borderColor = (0,0,0)
	borderWidth = 1
	buttonScale = 1.5
	buttonColor = (0,0,255)
	buttonRect = None
	transparency = 100
	
	def __init__(self, text, font):
		self.font = font
		self.text = text
		width, height = self.font.size(text)
		self.width = int(width * self.buttonScale)
		self.height = int(height * self.buttonScale)
		self.buttonRect = pygame.Rect(self.borderWidth,
									self.borderWidth, 
									self.width - (2 * self.borderWidth), 
									self.height - (2 * self.borderWidth))
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(self.borderColor)
		buttonSurface = pygame.Surface((self.buttonRect.width, self.buttonRect.height))
		buttonSurface.fill(self.buttonColor)
		self.surface.blit(buttonSurface, (self.borderWidth, self.borderWidth))
		image = self.font.render(text, 1, (180,180,0))
		x = (self.width / 2) - (width / 2)
		y = (self.height / 2) - (height / 2)
		self.surface.blit(image, (x,y))
		self.surface.set_alpha(self.transparency)
		
	def render(self, surface, *coords):
		surface.blit(self.surface, coords)
		
		
class MapLoader(object):
	'''
	classdocs
	'''
	placeable = [] #list of placeable boxes
	towers = []
	enemyQueue = []
	activeEnemies = []
	enemyPath = []
	entrance = None
	exit = None
	money = 200
	health = 100

	def __init__(self, filename):
		import tmxloader
		self.tiledmap = tmxloader.load_pygame(filename, pixelalpha=True)
		for group in self.tiledmap.objectgroups:
			for obj in group:
				if obj.type == "Entrance":
					self.entrance = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
				elif obj.type == "Exit":
					self.exit = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
				elif obj.type == "Path":
					points = obj.points
					x = obj.x
					y = obj.y
					for pt in points:
						newX,newY = pt
						newX += x
						newY += y
						self.enemyPath.append((newX,newY))
						
		tw = self.tiledmap.tilewidth
		th = self.tiledmap.tileheight
		gt = self.tiledmap.getTileImage
		layers = self.tiledmap.tilelayers
		for l in xrange(0, len(self.tiledmap.tilelayers)):
			for y in xrange(0, self.tiledmap.height):
				for x in xrange(0, self.tiledmap.width):
					if hasattr(layers[l],"placeable"):
						if layers[l].placeable == "true":
							tile = gt(x, y, l)
							if tile: 
								self.placeable.append(pygame.Rect(x*tw,y*th,tw,th))
				
		
		#TODO: append some enemies to the queue
		self.enemyQueue.append(Enemies.Sphere(self.enemyPath))

	def update(self):
		#Need to determine when to add new enemies
		for enemy in self.enemyQueue:
			ret = enemy.update()
			if(type(ret) == int):
				self.money += ret
				self.enemyQueue.remove(enemy)
			elif ret == True:
				self.health -= enemy.damage
				self.enemyQueue.remove(enemy)
		
		for tower in self.towers:
			tower.update(self.enemyQueue)
			
	def render(self, surface):
		tw = self.tiledmap.tilewidth
		th = self.tiledmap.tileheight
		gt = self.tiledmap.getTileImage

		for l in xrange(0, len(self.tiledmap.tilelayers)):
			for y in xrange(0, self.tiledmap.height):
				for x in xrange(0, self.tiledmap.width):
					tile = gt(x, y, l)
					if tile: 
						surface.blit(tile, (x*tw, y*th)) #add the tile to the image to be drawn
		
		#Need to order items from lowest Y to highest Y and call render() on each of them
		for enemy in self.enemyQueue:
			enemy.render(surface)
			
		for tower in self.towers:
			tower.render(surface)
	
	def getPlaceable(self, coords):
		'''
		returns the box that intersects with the coordinates given
		'''
		for box in self.placeable:
			if box.collidepoint(coords):
				if self.hasTower(box) == False:
					return box
			
	def hasTower(self, box):
		for tower in self.towers:
			if box.colliderect(tower.collideBox):
				return True
		return False
	
	def getTower(self, x, y):
		for tower in self.towers:
			if tower.collideBox.collidepoint(x,y):
				return tower
			
	def placeTower(self, tower):
		self.towers.append(tower)
		
	def removeTower(self, tower):
		self.towers.remove(tower)
		
	def addEnemy(self):
		self.enemyQueue.append(Enemies.Sphere(self.enemyPath))
		
		