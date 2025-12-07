'''
Created on Dec 5, 2013

@author: gparker
'''
import pygame
from .Animators import *
import math
import os

# Calculate path to assets relative to this file
base_path = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(base_path, '..', 'assets') + os.sep

class Enemy(SpriteAnimate):
	collideBox = pygame.Rect(0,0,0,0)
	position = (0,0)
	floatPosition = (0.0,0.0)
	health = 0
	max_health = 0
	value = 0
	armor = 0
	speed = 0 #how many updates before moving one pixel 
	damage = 0
	pathRemaining = 0
	target = (0,0)
	path = list()
	def __init__(self, path, full_animation):
		self.path = path
		self.position = self.path[0]
		x,y = self.position
		self.floatPosition = (float(x),float(y))
		self.target = self.path[1]
		self.distanceCounter = 0.0
		self.pathRemaining = self.getLengthRemaining()
		super(Enemy,self).__init__(full_animation)
		self.collideBox = pygame.Rect(x,y,*(self.current_frame.size))
		self.update_delay = 25
		self.healthBar = pygame.Rect((self.collideBox.bottomleft), (self.collideBox.width / 2, 5))
		self.healthBar.centerx = self.collideBox.centerx
		self.max_health = self.health

	def getNextTarget(self):
		currNode = self.path.index(self.target)
		if currNode != (len(self.path) - 1):
			currNode += 1
		return self.path[currNode]
	
	def getLengthRemaining(self):
		index = self.path.index(self.target)
		x,y = self.path[index]
		dist = math.hypot(x-self.position[0], y-self.position[1])
		lastNode = (x,y)
		while index != (len(self.path) - 1):
			index += 1
			x,y = self.path[index]
			dist += math.hypot(x-lastNode[0], y-lastNode[1])
			lastNode = (x,y)
		
		return dist
	
	def attack(self, amount):
		self.health -= amount
	
	def update(self):
		'''
		updates the current location and attributes of the enemy
		
		returns True if the path has been completed
		returns integer if the enemy has been destroyed
		'''
		if self.path[(len(self.path) - 1)] == self.position:
				return True
			
		if self.health <= 0:
			return self.value
			
		self.distanceCounter += 1.0 / self.speed
		currSpeed = 0
		while self.distanceCounter > 1.0:
			currSpeed += 1
			self.distanceCounter -= 1
		#if we should move at least one 'unit'
		if currSpeed > 0:
			#Calculate a triangle with a hyp of 1
			#Angle1 can be determined from inverse tan of the difference from self.position to self.target
			#angle is in radians
			sides = (self.target[0] - self.position[0], self.target[1] - self.position[1])
			a,b = sides
			angle1 = math.atan2(b, a)

			rise = math.sin(angle1) * currSpeed
			run = math.cos(angle1) * currSpeed
			self.floatPosition = (self.floatPosition[0] + run, self.floatPosition[1] + rise)
			self.position = (int(self.floatPosition[0]),int(self.floatPosition[1]))
			
			if self.target == self.position:
				self.target = self.getNextTarget()
				
			if(abs(rise) > abs(run)):
				#up-down
				if(rise < 0):
					self.setAnimation('up')
				else:
					self.setAnimation('down')
			else:
				#left-right
				if(run < 0):
					self.setAnimation('left')
				else:
					self.setAnimation('right')
			
			self.pathRemaining = self.getLengthRemaining()
			
		width,height = self.current_frame.size
		x,y = self.position
		self.collideBox = pygame.Rect((x - width / 2, y - height / 2), 
									(width,height))
		self.healthBar.centerx = self.collideBox.centerx
		self.healthBar.y = self.collideBox.bottom
		super(Enemy,self).update()
		return False
	
	def render(self,surface, position):
		super(Enemy, self).render(surface, position)
		pygame.draw.rect(surface, (255,0,0), self.healthBar)
		hp = pygame.Rect(self.healthBar.topleft, (int(self.healthBar.width * (float(self.health) / float(self.max_health))), self.healthBar.height))
		pygame.draw.rect(surface, (0,255,0), hp)
		
	def applyBonuses(self, bonuses):
		if 'health' in bonuses:
			self.health += bonuses['health']
			self.max_health = self.health
		if 'armor' in bonuses:
			self.armor += bonuses['armor'] #TODO: implement
		if 'resist' in bonuses:
			pass #TODO: implement
		if 'speed' in bonuses:
			self.speed -= bonuses['speed'] #TODO: also affect update rate?
		if 'value' in bonuses:
			self.value += bonuses['value']

class Skeleton(Enemy):
	image_path = assets_path + 'zombie_n_skeleton2.png'
	# Lazy loading of image to avoid pygame init issues if imported early,
	# but since we init pygame in main, this might be fine if instantiated later.
	# However, class attributes are evaluated at import time.
	# We should probably load images in __init__ or use a resource manager.
	# For now, I'll keep it as is but assuming pygame.display.set_mode hasn't been called yet might be an issue for convert() if used.
	# But pygame.image.load works without set_mode.
	
	def __init__(self, path):
		self.image = pygame.image.load(self.image_path)
		self.health = 10
		self.speed = 5
		self.damage = 10
		self.value = 15
		helper = SpriteSheetHelper(self.image, 4, 9 )
		self.animations = {'down' : helper.getRow(0,(3,5)), 
					'left' : helper.getRow(1,(3,5)),
					'right' : helper.getRow(2, (3,5)),
					'up' : helper.getRow(3,(3,5))}
		super(Skeleton, self).__init__(path, self.animations)
		
	def render(self, surface):
		super(Skeleton, self).render(surface, self.collideBox.topleft)
		
class Zombie(Enemy):
	image_path = assets_path + 'zombie_n_skeleton2.png'
	
	def __init__(self, path):
		self.image = pygame.image.load(self.image_path)
		self.health = 10
		self.speed = 5
		self.damage = 10
		self.value = 15
		helper = SpriteSheetHelper(self.image, 4, 9 )
		self.animations = {'down' : helper.getRow(0,(0,2)), 
					'left' : helper.getRow(1,(0,2)),
					'right' : helper.getRow(2, (0,2)),
					'up' : helper.getRow(3,(0,2))}
		super(Zombie, self).__init__(path=path, full_animation=self.animations)
		
	def render(self, surface):
		super(Zombie, self).render(surface, self.collideBox.topleft)

class Spider(Enemy):
	image_path = assets_path + 'spider_4.png'
	
	def __init__(self, path):
		self.image = pygame.image.load(self.image_path)
		self.health = 10
		self.speed = 5
		self.damage = 10
		self.value = 15
		helper = SpriteSheetHelper(self.image, 4, 7)
		self.animations = {'down' : helper.getRow(0,(0,5)), 
					'left' : helper.getRow(1,(0,5)),
					'right' : helper.getRow(2,(0,5)),
					'up' : helper.getRow(3,(0,5))}
		super(Spider, self).__init__(path=path, full_animation=self.animations)
		
	def render(self, surface):
		super(Spider, self).render(surface, self.collideBox.topleft)

class Wolf(Enemy):
	image_path = assets_path + 'wolfsheet.png'
	
	def __init__(self, path):
		self.image = pygame.image.load(self.image_path)
		self.health = 10
		self.speed = 5
		self.damage = 10
		self.value = 15
		helper = SpriteSheetHelper(self.image, 4, 5 )
		self.animations = {'down' : helper.getRow(0), 
					'left' : helper.getRow(1),
					'right' : helper.getRow(2),
					'up' : helper.getRow(3)}
		super(Wolf, self).__init__(path=path, full_animation=self.animations)
		self.update_delay = 15
	def render(self, surface):
		super(Wolf, self).render(surface, self.collideBox.topleft)
		
class Crow(Enemy):
	image_path = assets_path + 'crow.png'
	
	def __init__(self, path):
		self.image = pygame.image.load(self.image_path)
		self.health = 10
		self.speed = 5
		self.damage = 10
		self.value = 15
		self.flying = True
		self.last_x = 0
		helper = SpriteSheetHelper(self.image, 2, 5 )
		self.animations = {'right' : helper.getRow(0), 
					'left' : helper.getRow(1)}
		super(Crow, self).__init__(path=path, full_animation=self.animations)
		self.update_delay = 15
	def render(self, surface):
		super(Crow, self).render(surface, self.collideBox.topleft)
		
	def update(self):
		ret = super(Crow, self).update()
		if self.last_x != self.collideBox.x:
			if self.last_x < self.collideBox.x:
				self.setAnimation('right')
			else:
				self.setAnimation('left')
			self.last_x = self.collideBox.x
		return ret
