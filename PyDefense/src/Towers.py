'''
Created on Dec 3, 2013

@author: gparker
'''
import pygame

class Tower(object):
	level = 1
	damage = 1
	delay = 1
	cost = 100
	range = 1
	upgradeCost = 20
	location = pygame.Rect(0,0,0,0)
	collisionBox = pygame.Rect(0,0,0,0)
	name = ""
	scale = (64,64)
	
	def __init__(self, imagepaths):
		for path in imagepaths:
			self.image.append(pygame.image.load(path))
			
	def getActiveImage(self, Transparent=False):
		surface = pygame.transform.scale(self.image[self.level -1], self.scale)
		if Transparent:
			surface.set_alpha(128)
		return surface
	
	def upgrade(self):
		self.level += 1
		
	def setLocation(self, box):
		self.collisionBox = box
		self.location =  pygame.Rect(box.x - (box.width / 2), box.y - (box.height / 2), *self.scale)
			
class FighterTower(Tower):
	image = list()
	def __init__(self):
		paths = ["../assets/fighter.gif","../assets/fighter2.gif"]
		super(FighterTower, self).__init__(paths)
		self.damage = 2
		self.delay = 2
		self.name = "Fighter Level 1"
	
	def upgrade(self):
		self.damage += 2
		self.name = "Fighter Level ", self.level
		super(FighterTower, self).upgrade(self)
		
class ArcherTower(Tower):
	image = list()
	def __init__(self):
		paths = ["../assets/archer.gif","../assets/archer2.gif"]
		super(ArcherTower, self).__init__(paths)
		self.damage = 1
		self.delay = 1
		self.range = 5
		self.name = "Archer Level 1"
		
	def upgrade(self):
		self.delay -= 1
		self.name = "Archer Level ", self.level
		super(ArcherTower, self).upgrade(self)
		
class MageTower(Tower):
	image = list()
	def __init__(self):
		paths = ["../assets/mage.gif","../assets/mage2.gif"]
		super(MageTower, self).__init__(paths)
		self.damage = 3
		self.delay = 3
		self.range = 3
		self.name = "Mage Level 1"
		
	def upgrade(self):
		self.damage += 1
		self.range += 1
		self.name = "Mage Level ", self.level
		super(MageTower, self).upgrade(self)