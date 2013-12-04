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
	font = None
	
	def __init__(self, width, height, font):
		locale.setlocale( locale.LC_ALL, '' )
		self.money = 200
		self.screenW = width
		self.screenH = height
		self.font = font
	
	def setSelectedText(self, tower):
		self.selectedItem = tower.name
	
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
		
		