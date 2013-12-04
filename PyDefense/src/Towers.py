'''
Created on Dec 3, 2013

@author: gparker
'''
import pygame

class Tower(object):
	level = 1
	damage = 1
	delay = 1
	cost = 20
	upgradeCost = 20
	location = pygame.Rect(0,0,0,0)
	name = ""
	
	def __init__(self, imagepaths):
		for path in imagepaths:
			self.image.append(pygame.image.load(path))
			
	def getActiveImage(self):
		return self.image[self.level -1]
	
	def upgrade(self):
		self.level += 1
			
class FighterTower(Tower):
	image = list()
	def __init__(self):
		paths = ["../assets/fighter.gif","../assets/fighter2.gif"]
		super(FighterTower, self).__init__(paths)
		self.damage = 2
		self.delay = 2
		self.name = "Fighter Level 1"
	
	def upgrade(self):
		self.damage += 1
		self.name = "Fighter Level ", self.level
		super(FighterTower, self).upgrade(self)
		
class ArcherTower(Tower):
	image = list()
	def __init__(self):
		paths = ["../assets/archer.gif","../assets/archer2.gif"]
		super(ArcherTower, self).__init__(paths)
		self.damage = 1
		self.delay = 1
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
		self.name = "Mage Level 1"
		
	def upgrade(self):
		self.damage += 1
		self.name = "Mage Level ", self.level
		super(MageTower, self).upgrade(self)