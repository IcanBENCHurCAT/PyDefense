'''
Created on Dec 5, 2013

@author: gparker
'''
import pygame
import math

class Enemy(object):
	position = (0,0)
	health = 0
	armor = 0
	speed = 0
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
	
	def update(self):
		if self.path[(len(self.path) - 1)] == self.position:
				return True
		#Need to pass in deltaTime to correctly calculate movement rate
		newCoords = [self.position[0],self.position[1]]
		for i in range(0,2):
			if self.target[i] != newCoords[i]:
				diff = self.target[i] - newCoords[i]
				sign = 1
				if diff < 0:
					sign = -1

				if math.fabs(diff) < self.speed:
					newCoords[i] += sign * diff
				else:
					newCoords[i] += sign * self.speed 
		self.position = (newCoords[0],newCoords[1])
		if self.target == self.position:
			self.target = self.getNextTarget()
		
		self.pathRemaining = self.getLengthRemaining()
		return False
	
	def render(self, surface):
		x,y = self.position
		surface.blit(self.currentFrame, (x - 16, y - 16))
		
class Sphere(Enemy):
	
	def __init__(self, path):
		self.health = 20
		self.speed = 1
		self.damage = 10
		alpha = pygame.Surface((32,32))
		#alpha.set_alpha(0)
		surface = pygame.Surface((32,32))
		pygame.draw.circle(surface, (0,0,255), (16,16), 16)
		alpha.blit(surface, (0,0))
		self.currentFrame = alpha
		sprites = list()
		sprites.append(alpha)
		super(Sphere, self).__init__(sprites, path)
	
	def render(self, surface):
		currentFrame = self.animation[0]
		super(Sphere, self).render(surface)
		