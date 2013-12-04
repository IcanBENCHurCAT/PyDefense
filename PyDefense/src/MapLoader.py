'''
Created on Dec 3, 2013

@author: gparker
'''
import pygame
class MapLoader(object):
	'''
	classdocs
	'''
	placeable = [] #list of placeable boxes

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

	def showPlaceable(self, surface):
		for box in self.placeable:
			pygame.draw.rect(surface, pygame.Color(255,0,0), box)
	
	def getPlaceable(self, coords):
		'''
		returns the box that intersects with the coordinates given
		'''
		for box in self.placeable:
			if box.collidepoint(coords):
				return box
