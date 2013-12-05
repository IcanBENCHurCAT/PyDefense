'''
Created on Dec 3, 2013

@author: gparker
'''
import pygame
import locale

class MapGUI(object):
	screenW = 0
	screenH = 0
	money = 0
	selectedItem = ""
	openTower = None
	font = None
	btnUpgrade = None
	btnSell = None
	
	def __init__(self, width, height, font):
		locale.setlocale( locale.LC_ALL, '' )
		self.money = 200
		self.screenW = width
		self.screenH = height
		self.font = font
		self.btnUpgrade = MapButton("Upgrade", font)
		self.btnSell = MapButton("Sell", font)
	
	def setSelectedText(self, tower):
		if self.openTower is None:
			self.selectedItem = tower.name
		
	def openTowerMenu(self, tower):
		self.openTower = tower
		self.setSelectedText(tower)
	
	def closeTowerMenu(self):
		self.openTower = None
	
	def render(self, surface):
		#Print Money top-left
		text = locale.currency( self.money, grouping=True )
		i = self.font.render(text, 1, (180,180,0))
		
		sizeX, sizeY = self.font.size(text)
		x = self.screenW - sizeX - 15
		y = 15
				
		surface.blit(i, (x,y))
		
		text = self.selectedItem
		i = self.font.render(text, 1, (180, 180, 0))
		sizeX, sizeY = self.font.size(text)
		x = 15
		y = self.screenH - sizeY - 15
		surface.blit(i, (x,y))
		
		if self.openTower:
			x = self.screenW - self.btnSell.width - 15
			y = self.screenH - self.btnSell.height - 15
			self.btnSell.render(surface, (x,y))
			
			x -= self.btnUpgrade.width + 10
			self.btnUpgrade.render(surface, (x,y))
			
	
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

	def __init__(self, filename):
		import tmxloader
		self.tiledmap = tmxloader.load_pygame(filename, pixelalpha=True)
	
	
	def render(self, surface):
		tw = self.tiledmap.tilewidth
		th = self.tiledmap.tileheight
		gt = self.tiledmap.getTileImage

		layers = self.tiledmap.tilelayers
		for l in xrange(0, len(self.tiledmap.tilelayers)):
			for y in xrange(0, self.tiledmap.height):
				for x in xrange(0, self.tiledmap.width):
					tile = gt(x, y, l)
					if tile: 
						surface.blit(tile, (x*tw, y*th)) #add the tile to the image to be drawn
						
						#check for special attributes on the layer, tile, etc...
						if hasattr(layers[l],"placeable"):
							if layers[l].placeable == "true":
								self.placeable.append(pygame.Rect(x*tw,y*th,tw,th))
		
		for tower in self.towers:
			surface.blit(tower.getActiveImage(), tower.location)

	
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
			if box.colliderect(tower.collisionBox):
				return True
		return False
	
	def getTower(self, x, y):
		for tower in self.towers:
			if tower.collisionBox.collidepoint(x,y):
				return tower
			
	def placeTower(self, tower):
		self.towers.append(tower)
		
		