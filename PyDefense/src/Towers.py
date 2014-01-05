'''
Created on Dec 3, 2013

@author: gparker
'''
import pygame
import math
from Animators import *

class Tower(object):
	level = 1
	damage = 1
	delay = 1 #how many ticks it take before the tower can fire again
	delayTimer = 0 #used in counting ticks
	cost = 100
	range = 1 #multiplier for the distBase
	distBase = 50 #base number of pixels for the range of the tower
	upgradeCost = 50
	maxLevel = 2
	location = pygame.Rect(0,0,0,0) #where the tower appears to be
	collideBox = pygame.Rect(0,0,0,0) #a 32x32 block of space the tower 'exists' in
	scale = (64,64) #scale the image of the tower up to this point
	target = None #enemy to attack
	showRadius = False #whether to draw the radius or not
	
	def __init__(self, imagepaths):
		for path in imagepaths:
			self.image.append(pygame.image.load(path))
		self.setName()
			
	def getActiveImage(self, Transparent=False):
		surface = pygame.transform.scale(self.image[self.level -1], self.scale)
		if Transparent:
			surface.set_alpha(128)
		return surface
	
	def drawRadius(self, surface):
		pygame.draw.circle(surface, (0,255,255), (self.location.x + self.location.width / 2, 
			self.location.y + self.location.height / 2), int(self.distBase * self.range), 2)
	
	def upgrade(self):
		self.level += 1
		self.setName()
		
	def setLocation(self, box):
		self.collideBox = box
		self.location =  pygame.Rect(box.x - (box.width / 2), box.y - (box.height / 2), *self.scale)
		
	def setName(self):
		self.name = "{0} Level {1}".format(self.className, self.level)
		
	def setTarget(self, enemies):
		self.target = None
		x,y = (self.collideBox.x + self.collideBox.width / 2, 
			self.collideBox.y + self.collideBox.height / 2)
		for enemy in enemies:
			xEnemy = enemy.collideBox.centerx
			yEnemy = enemy.collideBox.centery
			dist = math.hypot(x-xEnemy,y-yEnemy) - enemy.collideBox.width / 2
			if dist <= (self.range * self.distBase):
				self.target = enemy
				break
	
	def attack(self):
		#todo: overload each subclass to add projectiles, animations etc...
		self.target.attack(self.damage)
	
	def update(self, enemies):
		self.setTarget(enemies)
		if self.target:
			self.delayTimer += 1
			if self.delayTimer >= self.delay:
				self.delayTimer -= self.delay
				self.attack()
	
	def render(self, surface, Transparent=False):
		surface.blit(self.getActiveImage(Transparent), self.location)
		if self.showRadius:
			self.drawRadius(surface)
	
		
class FighterTower(Tower):
	image = list()
	name = ""
	className = ""
	animateAttack = False
	def __init__(self):
		paths = ["../assets/fighter.gif","../assets/fighter2.gif"]
		self.damage = 6
		self.delay = 60
		self.range = 1.5
		self.className = "Fighter"
		super(FighterTower, self).__init__(paths)
	
	def upgrade(self):
		self.damage += 2
		self.range = 1.69
		super(FighterTower, self).upgrade()
		
	def attack(self):
		self.animateAttack = True
		super(FighterTower, self).attack()
		
	def render(self, surface, Transparent=False):
		if self.animateAttack:
			self.animateAttack = False
			pygame.draw.ellipse(surface, (255,0,0), 
							(self.target.collideBox.x, self.target.collideBox.y,
							self.target.collideBox.width, self.collideBox.height), 
							2)
		super(FighterTower, self).render(surface, Transparent=Transparent)
		
class ArcherTower(Tower):
	image = list()
	name = ""
	className = ""
	def __init__(self):
		paths = ["../assets/archer.gif","../assets/archer2.gif"]
		self.damage = 1
		self.delay = 30
		self.range = 4
		self.className = "Archer"
		self.animateAttack = list()
		super(ArcherTower, self).__init__(paths)
		
	def upgrade(self):
		self.delay -= 10
		super(ArcherTower, self).upgrade()
		
	def attack(self):
		animation = ArrowPhysics(self.collideBox.center, self.target)
		self.animateAttack.append(animation)
		super(ArcherTower, self).attack()
		
	def update(self, enemies):
		for attack in self.animateAttack:
			attack.update()
			if attack.is_done:
				self.animateAttack.remove(attack)
		super(ArcherTower, self).update(enemies)
		
	def render(self, surface, Transparent=False):
		super(ArcherTower, self).render(surface, Transparent=Transparent)
		for attack in self.animateAttack:
			attack.render(surface)
		
class MageTower(Tower):
	image = list()
	name = ""
	className = ""
	def __init__(self):
		paths = ["../assets/mage.gif","../assets/mage2.gif"]
		self.damage = 2
		self.delay = 150
		self.range = 3
		self.className = "Mage"
		self.animateAttack = list()
		super(MageTower, self).__init__(paths)
		
	def upgrade(self):
		self.damage += 1
		super(MageTower, self).upgrade()
		
	def attack(self):
		#self.animateAttack = True
		animation = FireballPhysics(self.collideBox.center, self.target)
		self.animateAttack.append(animation)
		super(MageTower, self).attack()
		
	def update(self, enemies):
		for attack in self.animateAttack:
			attack.update()
			if attack.is_done:
				self.animateAttack.remove(attack)
		super(MageTower, self).update(enemies)
			
	def render(self, surface, Transparent=False):
		super(MageTower, self).render(surface, Transparent=Transparent)
		
		for attack in self.animateAttack:
			attack.render(surface)
		
