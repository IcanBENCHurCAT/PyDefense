'''
Created on Dec 22, 2013

@author: gparker
'''
import pygame
import math

class SpriteAnimate(object):
	
	full_animation = dict()
	current_animation = list()
	current_frame = None
	update_delay = 5
	update_counter = 0
	image = None
	
	def __init__(self, full_animation):
		self.full_animation = full_animation
		key,value = self.full_animation.items()[0]
		self.current_animation = value
		self.current_frame = self.current_animation[0]
	
	def nextFrame(self):
		index = self.current_animation.index(self.current_frame)
		if index == (len(self.current_animation) - 1):
			index = 0
		else:
			index += 1
		
		self.current_frame = self.current_animation[index]
	
	def update(self):
		self.update_counter += 1
		if self.update_counter >= self.update_delay:
			self.update_counter -= self.update_delay
			self.nextFrame()
			
	def setAnimation(self, key):
		if key in self.full_animation:
			if self.current_animation <> self.full_animation[key]:
				self.current_animation = self.full_animation[key]
				self.current_frame = self.current_animation[0]
	
	def render(self,surface, position):
		surface.blit(self.image, position, self.current_frame)

class SpriteSheetHelper(object):
	
	images = None #images[row][column]
	rows = 0
	columns = 0
	def __init__(self, image, rows, columns):
		self.rows = rows
		self.columns = columns
		self.images = [[0 for x in range(columns)] for x in range(rows)] 
		width = image.get_width() / columns
		height = image.get_height() / rows
		for i in range(0,rows):
			for j in range(0,columns):
# 				crop = pygame.Surface((width, height))
# 				crop.blit(image, (0,0), area = (j*width,i*height,width,height))
				self.images[i][j] = pygame.Rect((j*width,i*height,width,height))
		
	def getRow(self,row):
		return self.images[row]
	
	def getColumn(self,column):
		img_list = list()
		for i in range(0,self.rows):
			img_list.append(self.images[i][column])
		return img_list
	
class Fireball(SpriteAnimate):
	''''
	0 = left 		PI
	1 = up-left 	3PI/4
	2 = up 			PI/2
	3 = up-right 	PI/4
	4 = right 		0PI
	5 = down-right	7PI/4
	6 = down 		3PI/2
	7 = down-left 	5PI/4
	''' 
	animations = dict()
	image = pygame.image.load('../assets/fireball.png')
	def __init__(self):
		helper = SpriteSheetHelper(self.image, 8, 8)
		self.animations = {'left' : helper.getRow(0), 
					'up-left' : helper.getRow(1),
					'up' : helper.getRow(2),
					'up-right' : helper.getRow(3),
					'right' : helper.getRow(4),
					'down-right' : helper.getRow(5),
					'down' : helper.getRow(6),
					'down-left' : helper.getRow(7)}
		super(Fireball, self).__init__(self.animations)
	
class FireballPhysics(object):
	
	speed = 3
	directions = {'left':math.pi, 
				'up-left':(5.0 * math.pi / 4.0),
				'up':(3.0 * math.pi / 2.0),
				'up-right':(7.0 * math.pi / 4.0),
				'right':0,
				'down-right':(math.pi / 4.0),
				'down':(math.pi / 2.0),
				'down-left':(3.0 * math.pi / 4.0)}
	
	def __init__(self, start, target):
		self.fireball = Fireball()
		self.fireball.setAnimation('left')
		self.current_position = start
		self.float_position = (float(start[0]),float(start[1]))
		self.destination = target
		self.is_done = False

	
	def update(self):
		if self.is_done == True:
			return
		
		if self.destination.position == self.current_position:
			self.is_done = True
		
		direction = ''
		
		sides = (self.destination.position[0] - self.current_position[0], self.destination.position[1] - self.current_position[1])
		a,b = sides
		angle1 = math.atan2(b, a)

		rise = math.sin(angle1) * self.speed
		run = math.cos(angle1) * self.speed
		
		self.float_position = (self.float_position[0] + run, self.float_position[1] + rise)
		self.current_position = (int(self.float_position[0]),int(self.float_position[1]))
		
		dist = float("inf")
		
		if angle1 < 0:
			angle1 = (2.0 * math.pi) + angle1
			
		for item in self.directions.items():
			new_dist = abs(angle1 - item[1])
			if new_dist < dist:
				dist = new_dist
				direction = item[0]
				
		
		dist = (abs(self.current_position[0] - self.destination.position[0]), abs(self.current_position[1] - self.destination.position[1]))
		if dist[0] <= self.speed and dist[1] <= self.speed:
			self.current_position = self.destination.position
			
		self.fireball.setAnimation(direction)
		
		self.fireball.update()
	
	def render(self, surface):
		draw_position = (self.current_position[0] - self.fireball.current_frame.width / 2,
						self.current_position[1] - self.fireball.current_frame.height / 2)
		self.fireball.render(surface, draw_position)
	