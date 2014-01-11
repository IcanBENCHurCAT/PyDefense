'''
Created on Dec 5, 2013

@author: gparker
'''
import pygame
import math
from Animators import *

class Enemy(SpriteAnimate):
	collideBox = pygame.Rect(0,0,0,0)
	position = (0,0)
	floatPosition = (0.0,0.0)
	health = 0
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

	def getNextTarget(self):
		currNode = self.path.index(self.target)
		if currNode <> (len(self.path) - 1):
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
		super(Enemy,self).update()
		return False
	
# 	def render(self, surface):
# 		x,y = self.position
# 		surface.blit(self.currentFrame, (x - self.collideBox.width / 2, 
# 										y - self.collideBox.width / 2))
		
	def applyBonuses(self, bonuses):
		if 'health' in bonuses:
			self.health += bonuses['health']
		if 'armor' in bonuses:
			self.armor += bonuses['armor'] #TODO: implement
		if 'resist' in bonuses:
			pass #TODO: implement
		if 'speed' in bonuses:
			self.speed /= bonuses['speed']
		if 'value' in bonuses:
			self.value += bonuses['value']
# class Sphere(Enemy):
# 	
# 	def __init__(self, path):
# 		self.health = 10
# 		self.speed = 5
# 		self.damage = 10
# 		self.value = 15
# 		surface = pygame.Surface((32,32))
# 		pygame.draw.circle(surface, (0,0,255), (16,16), 16) #these 16's need to be pulled from the surface object
# 		self.currentFrame = surface
# 		super(Sphere, self).__init__(path)
# 	
# 	def render(self, surface):
# 		x,y = self.position
# 		surface.blit(self.currentFrame, (x - self.collideBox.width / 2, 
# 										y - self.collideBox.width / 2))
		
class Skeleton(Enemy):
	image = pygame.image.load('../assets/zombie_n_skeleton2.png')
	
	def __init__(self, path):
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
		
class Zombie(Enemy, SpriteAnimate):
	image = pygame.image.load('../assets/zombie_n_skeleton2.png')
	
	def __init__(self, path):
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
		