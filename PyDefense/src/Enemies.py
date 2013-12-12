'''
Created on Dec 5, 2013

@author: gparker
'''
import pygame
import math

class Enemy(object):
	collideBox = pygame.Rect(0,0,0,0)
	position = (0,0)
	health = 0
	value = 0
	armor = 0
	speed = 0 #how many updates before moving one pixel 
	distanceCounter = 0.0
	damage = 0
	pathRemaining = 0
	target = (0,0)
	animation = None
	currentFrame = None
	path = list()
	def __init__(self, sprites, path):
		self.animation = sprites
		self.path = path
		self.position = self.path[0]
		self.target = self.path[1]
		
		self.pathRemaining = self.getLengthRemaining()
		self.collideBox = pygame.Rect(self.position, self.currentFrame.get_size())

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
		if currSpeed > 0:
			newCoords = [self.position[0],self.position[1]]
			for i in range(0,2):
				if self.target[i] != newCoords[i]:
					diff = self.target[i] - newCoords[i]
					sign = 1
					if diff < 0:
						sign = -1
	
					if math.fabs(diff) < currSpeed:
						newCoords[i] += sign * diff
					else:
						newCoords[i] += sign * currSpeed 
			self.position = (newCoords[0],newCoords[1])
			if self.target == self.position:
				self.target = self.getNextTarget()
			
			self.pathRemaining = self.getLengthRemaining()
		width,height = self.currentFrame.get_size()
		x,y = self.position
		self.collideBox = pygame.Rect((x - width / 2, y - height / 2), 
									(width,height))
		return False
	
	def render(self, surface):
		x,y = self.position
		surface.blit(self.currentFrame, (x - self.collideBox.width / 2, 
										y - self.collideBox.width / 2))
		
class Sphere(Enemy):
	
	def __init__(self, path):
		self.health = 20
		self.speed = 5
		self.damage = 10
		self.value = 20
		alpha = pygame.Surface((32,32))
		#alpha.set_alpha(0)
		surface = pygame.Surface((32,32))
		pygame.draw.circle(surface, (0,0,255), (16,16), 16) #these 16's need to be pulled from the surface object
		alpha.blit(surface, (0,0))
		self.currentFrame = surface
		sprites = list()
		sprites.append(alpha)
		super(Sphere, self).__init__(sprites, path)
	
	def render(self, surface):
		super(Sphere, self).render(surface)
		