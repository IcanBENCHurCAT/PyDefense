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
	maxLevel = 2
	location = pygame.Rect(0,0,0,0)
	collisionBox = pygame.Rect(0,0,0,0)
	scale = (64,64)
	
	def __init__(self, imagepaths):
		for path in imagepaths:
			self.image.append(pygame.image.load(path))
		self.setName()
			
	def getActiveImage(self, Transparent=False):
		surface = pygame.transform.scale(self.image[self.level -1], self.scale)
		if Transparent:
			surface.set_alpha(128)
		return surface
	
	def upgrade(self):
		self.level += 1
		self.setName()
		
	def setLocation(self, box):
		self.collisionBox = box
		self.location =  pygame.Rect(box.x - (box.width / 2), box.y - (box.height / 2), *self.scale)
		
	def setName(self):
		self.name = "{0} Level {1}".format(self.className, self.level)
			
class FighterTower(Tower):
	image = list()
	name = ""
	className = ""
	def __init__(self):
		paths = ["../assets/fighter.gif","../assets/fighter2.gif"]
		self.damage = 2
		self.delay = 2
		self.className = "Fighter"
		super(FighterTower, self).__init__(paths)
	
	def upgrade(self):
		self.damage += 2
		super(FighterTower, self).upgrade()
		
class ArcherTower(Tower):
	image = list()
	name = ""
	className = ""
	def __init__(self):
		paths = ["../assets/archer.gif","../assets/archer2.gif"]
		self.damage = 1
		self.delay = 1
		self.range = 5
		self.className = "Archer"
		super(ArcherTower, self).__init__(paths)
		
	def upgrade(self):
		self.delay -= 1
		super(ArcherTower, self).upgrade()
		
class MageTower(Tower):
	image = list()
	name = ""
	className = ""
	def __init__(self):
		paths = ["../assets/mage.gif","../assets/mage2.gif"]
		self.damage = 3
		self.delay = 3
		self.range = 3
		self.className = "Mage"
		super(MageTower, self).__init__(paths)
		
	def upgrade(self):
		self.damage += 1
		self.range += 1
		super(MageTower, self).upgrade()