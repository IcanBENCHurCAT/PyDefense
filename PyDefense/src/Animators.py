'''
Created on Dec 22, 2013

@author: gparker
'''
import pygame
import math
import tkSimpleDialog
import os
from Tkinter import *

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
		f = self.current_frame
		s = pygame.Surface((f.width, f.height),pygame.SRCALPHA, 32)
		s.blit(self.image, (0,0), f)
		if(hasattr(self,'rotation')):
			loc = s.get_rect().center
			s = pygame.transform.rotate(s, math.degrees(-1 *self.rotation))
			s.get_rect().center = loc
			
		surface.blit(s, position)
		
	def setRotation(self, radians):
		self.rotation = radians

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
		
	def getRow(self,row, subset=None):
		if(subset):
			return self.images[row][subset[0]:subset[1]]
		return self.images[row]
	
	def getColumn(self,column):
		img_list = list()
		for i in range(0,self.rows):
			img_list.append(self.images[i][column])
		return img_list
	
class Arrow(SpriteAnimate):
	image = pygame.image.load('../assets/arrow.png')
	def __init__(self):
		helper = SpriteSheetHelper(self.image, 8, 1)
# 		self.animations = {'left' : helper.getRow(0), 
# 					'up-left' : helper.getRow(1),
# 					'up' : helper.getRow(2),
# 					'up-right' : helper.getRow(3),
# 					'right' : helper.getRow(4),
# 					'down-right' : helper.getRow(5),
# 					'down' : helper.getRow(6),
# 					'down-left' : helper.getRow(7)}
		self.animations = {'attack' : helper.getRow(4)}
		super(Arrow, self).__init__(self.animations)
	
class Fireball(SpriteAnimate):
	''''
	0 = left
	1 = up-left
	2 = up
	3 = up-right
	4 = right
	5 = down-right
	6 = down
	7 = down-left
	'''
	image = pygame.image.load('../assets/fireball.png')
	def __init__(self):
		helper = SpriteSheetHelper(self.image, 8, 8)
# 		self.animations = {'left' : helper.getRow(0), 
# 					'up-left' : helper.getRow(1),
# 					'up' : helper.getRow(2),
# 					'up-right' : helper.getRow(3),
# 					'right' : helper.getRow(4),
# 					'down-right' : helper.getRow(5),
# 					'down' : helper.getRow(6),
# 					'down-left' : helper.getRow(7)}
		self.animations = {'attack' : helper.getRow(4)}
		super(Fireball, self).__init__(self.animations)
	
class ProjectilePhysics(object):
	
	directions = {'left':math.pi, 
				'up-left':(5.0 * math.pi / 4.0),
				'up':(3.0 * math.pi / 2.0),
				'up-right':(7.0 * math.pi / 4.0),
				'right':0,
				'down-right':(math.pi / 4.0),
				'down':(math.pi / 2.0),
				'down-left':(3.0 * math.pi / 4.0)}
	
	def __init__(self, start, target):
		self.current_position = start
		self.float_position = (float(start[0]),float(start[1]))
		self.destination = target
		self.is_done = False
		self.current_direction = 0
	
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
				self.current_direction = angle1
				
		
		dist = (abs(self.current_position[0] - self.destination.position[0]), abs(self.current_position[1] - self.destination.position[1]))
		if dist[0] <= self.speed * 5 and dist[1] <= self.speed * 5:
			self.is_done = True
			
		self.animation.setAnimation(direction)
		
		self.animation.update()
	
	def render(self, surface):
		draw_position = (self.current_position[0] - self.animation.current_frame.width / 2,
						self.current_position[1] - self.animation.current_frame.height / 2)
		self.animation.render(surface, draw_position)
	
class FireballPhysics(ProjectilePhysics):
	
	speed = 3
	
	def __init__(self, start, target):
		self.animation = Fireball()
		self.animation.setAnimation('attack')
		super(FireballPhysics, self).__init__(start, target)
		
	def update(self):
		super(FireballPhysics, self).update()
		self.animation.setRotation(self.current_direction)
		
class ArrowPhysics(ProjectilePhysics):
	speed = 5
	
	def __init__(self, start, target):
		self.animation = Arrow()
		self.animation.setAnimation('attack')
		super(ArrowPhysics, self).__init__(start, target)
		
	def update(self):
		super(ArrowPhysics, self).update()
		self.animation.setRotation(self.current_direction)
		
class Sword(SpriteAnimate):
	image = pygame.image.load('../assets/fighterAttack.png')
	
	def __init__(self):
		helper = SpriteSheetHelper(self.image, 1, 5)
		self.animations = {'attack':helper.getRow(0)}
		super(Sword, self).__init__(self.animations)

class SwordPhysics(ProjectilePhysics):
	speed = 3
	
	def __init__(self, start, target):
		self.animation = Sword()
		self.animation.setAnimation('attack')
		super(SwordPhysics,self).__init__(start, target)
		
	def update(self):
		super(SwordPhysics, self).update()
		self.animation.setRotation(self.current_direction)

class ButtonType(object):
	green = 0
	blue = 1
	red = 2

class ButtonAlignment(object):
	left = 0
	center = 1
	right = 2
	
class ButtonAnimate(object):
	button_image = pygame.image.load('../assets/UI3Buttons.png')
	text_image = pygame.image.load('../assets/UITextBox.png')
	font = pygame.font.SysFont('quartzms', 20)
	bold = False
	color = (200, 200, 200)
	
	def __init__(self, style, text, position, alignment = ButtonAlignment.left):
		helper = SpriteSheetHelper(self.button_image, 1, 3)
		self.action = None
		self.params = None
		self.button_rec = None
		if style == ButtonType.green:
			self.button_rec = helper.getColumn(0)[0]
		elif style == ButtonType.blue:
			self.button_rec = helper.getColumn(1)[0]
		elif style == ButtonType.red:
			self.button_rec = helper.getColumn(2)[0]
		else:
			raise NotImplementedError
		
		self.text = text
		self.position = position
		self.alignment = alignment
		
		self.is_aligned = False
		self.makeImage()
		
	def render(self, surface):
		surface.blit(self.full_button, self.position)
		
	def cursorUpdate(self, position):
		if self.collide_rect.collidepoint(position):
			if self.bold == False:
				self.bold = True
				self.color = (255,255,255)
				self.makeImage()
		else:
			self.bold = False
			self.color = (200,200,200)
			self.makeImage()
		
	def makeImage(self):
		button_surface = pygame.Surface(self.button_rec.size,pygame.SRCALPHA, 32)
		button_surface.blit(self.button_image, (0,0), self.button_rec)
		
		text_rec = pygame.Rect((0,0), self.font.size(self.text))
		text_rec.width *= 1.5
		text_rec.height *= 3
		text_surface = pygame.Surface(self.text_image.get_size(),pygame.SRCALPHA, 32)
		text_surface.blit(self.text_image, (0,0))
		text_surface = pygame.transform.scale(text_surface, text_rec.size)
		
		scale = float(text_rec.height) / float(self.button_rec.height)
		btn_rec = pygame.Rect((0,0),(int(self.button_rec.width * scale), int(self.button_rec.height * scale)))
		right, top = btn_rec.topright
		text_rec.topleft = (right - text_rec.width * .1, top)
		button_surface = pygame.transform.scale(button_surface,btn_rec.size)
		
		self.full_button = pygame.Surface((int(btn_rec.width + text_rec.width), int(btn_rec.height)),pygame.SRCALPHA, 32)
		self.full_button.blit(text_surface, text_rec.topleft)
		self.full_button.blit(button_surface, btn_rec.topleft)
		
		if self.is_aligned == False:
			if self.alignment == ButtonAlignment.left:
				pass
			elif self.alignment == ButtonAlignment.right:
				x,y = self.position
				x -= self.full_button.get_width()
				self.position = (x,y)
			elif self.alignment == ButtonAlignment.center:
				x,y = self.position
				x -= (self.full_button.get_width() / 2)
				y -= (self.full_button.get_height() / 2)
				self.position = (x,y)
			else:
				raise NotImplementedError
			self.is_aligned = True
		
		button_text = self.font.render(self.text, True, self.color)
		txt_rec = pygame.Rect((0,0), self.font.size(self.text))
		txt_rec.center = text_rec.center
		self.full_button.blit(button_text, txt_rec.topleft)
		self.collide_rect = self.full_button.get_rect()
		self.collide_rect.topleft = self.position
		
	def doAction(self):
		if self.action:
			if self.params:
				self.action(*self.params)
			else:
				self.action()
		
class Menu(object):
	
	def __init__(self, size, color, position=(0,0), center=None, alpha=255):
		self.buttons = list()
		self.background = pygame.Rect(position, size)
		if center is not None:
			self.background.center = center
		self.color = color
		self.alpha = alpha
	
	def cursorUpdate(self, position):
		for btn in self.buttons:
			btn.cursorUpdate(position)
	
	def render(self, screen):
		s = pygame.Surface(self.background.size, pygame.SRCALPHA, 32)
		r,g,b = self.color
		s.fill((r,g,b,self.alpha))
		screen.blit(s, self.background.topleft)
		for btn in self.buttons:
			btn.render(screen)
			
	def click(self, position):
		for btn in self.buttons:
			if btn.collide_rect.collidepoint(position):
				btn.doAction()
	
class StartMenu(Menu):
	
	start = 0
	load = 1
	options = 2
	exit = 3
	
	def __init__(self, size, color, position=(0,0), center=None):
		super(StartMenu,self).__init__(size, color, position, center)
		spacing = 80
		x,y = self.background.center
		x -= spacing
		y -= spacing
		self.buttons.append(ButtonAnimate(ButtonType.green, "    Start    ",(x,y)))
		y += spacing
		self.buttons.append(ButtonAnimate(ButtonType.green, "    Load     ", (x,y)))
		y += spacing
		self.buttons.append(ButtonAnimate(ButtonType.blue, "    Options  ", (x,y)))
		y += spacing
		self.buttons.append(ButtonAnimate(ButtonType.red, "     Exit     ", (x,y)))
	
	def initStart(self, action):
		self.buttons[self.start].action = action
	
	def initOptions(self, action):
		self.buttons[self.options].action = action
	
	def initLoad(self, action):
		self.buttons[self.load].action = action
	
	def initExit(self, action):
		self.buttons[self.exit].action = action

class PauseMenu(Menu):
	save = 0
	load = 1
	options = 2
	exit = 3
	
	def __init__(self, size, color, position=(0,0), center=None, alpha=255):
		super(PauseMenu,self).__init__(size, color, position, center, alpha)
		spacing = 80
		x,y = self.background.center
		x -= spacing
		y -= spacing
		self.buttons.append(ButtonAnimate(ButtonType.green, "    Save    ",(x,y)))
		y += spacing
		self.buttons.append(ButtonAnimate(ButtonType.green, "    Load     ", (x,y)))
		y += spacing
		self.buttons.append(ButtonAnimate(ButtonType.blue, "    Options  ", (x,y)))
		y += spacing
		self.buttons.append(ButtonAnimate(ButtonType.red, "Exit to Main Menu", (x,y)))
	
	def initSave(self, action):
		self.buttons[self.save].action = action
	
	def initOptions(self, action):
		self.buttons[self.options].action = action
	
	def initLoad(self, action):
		self.buttons[self.load].action = action
	
	def initExit(self, action):
		self.buttons[self.exit].action = action
	
class SaveMenu(Menu):
	
	ok = 0
	cancel = 1
	slot = [2, 3, 4]
	default_text = 'Open Slot'
	
	def __init__(self, size, color, position=(0,0), center=None, alpha=255):
		super(SaveMenu,self).__init__(size, color, position, center, alpha)
		padding = 10
		x,y = self.background.bottomleft
		btn = ButtonAnimate(ButtonType.green, "    OK    ",(x,y))
		w,h = btn.collide_rect.size
		y -= (h + padding)
		x += padding
		btn.position = (x,y)
		self.buttons.append(btn)
		
		x = self.background.right
		btn = ButtonAnimate(ButtonType.red, "Cancel", (x,y), 
			alignment=ButtonAlignment.right)
		x,y = btn.collide_rect.topleft
		x -= padding
		btn.position = (x,y)
		self.buttons.append(btn)
		
		slots = 3
		for i in range(0, slots):
			self.buttons.append(None)
		x,y = self.background.center
		padding = h*2
		y -= 100
		import sqlite3
		conn = sqlite3.connect('game.db')
		conn.row_factory = sqlite3.Row
		db = conn.cursor()
		db.execute('SELECT * FROM save_set ORDER BY date DESC')
		self.date_text = {1 : ["", (0,0)],
						2 : ["", (0,0)],
						3 : ["", (0,0)]}
		for row in db.fetchall():
			text = str.format("{0}", row['title'])
			slot = int(row['id'])
			self.buttons[slot + 1] = ButtonAnimate(ButtonType.blue, text, 
				(x,y), alignment=ButtonAlignment.center)
			self.date_text[slot][0] = row['date']
			w,h = self.buttons[slot + 1].font.size(row['date'])

			x2, y2 = (x,y)
			x2 -= w / 2
			y2 -= padding / 2 - h / 2
			self.date_text[slot][1] = (x2,y2)
			
			y += padding
		

		for i in range(0, slots):
			if self.buttons[2 + i] is None:
				self.buttons[2 + i] = ButtonAnimate(ButtonType.blue, self.default_text,
					(x,y), alignment=ButtonAlignment.center)
				y += padding
		
		self.selected_slot = 1
		self.selected_title = ""
		
	def initOK(self, action):
		self.buttons[self.ok].action = action
	
	def initCancel(self, action):
		self.buttons[self.cancel].action = action
		
	def initSelectSlot(self, action):
		for slot in self.slot:
			self.buttons[slot].action = self.make_action(slot, action)
	
	def make_action(self, slot, action):
		return lambda : action(slot)
	
	def input(self, event):
		if event.key == pygame.K_BACKSPACE:
			if len(self.selected_title):
				self.selected_title = self.selected_title[:-1]
		else:
			try:
				a = unichr(event.key) 
				self.selected_title += str(a)
			except:
				print 'Unhandled keyboard input' #Likely a shift?
				
	def setTitle(self):
		if(self.default_text == self.buttons[self.selected_slot].text):
			self.selected_title = ''
		else:
			self.selected_title = self.buttons[self.selected_slot].text
		 
	def render(self, screen):
		super(SaveMenu, self).render(screen)
		for index, data in self.date_text.items():
			word_text = self.buttons[index + 1].font.render(data[0], False, 
										(255,255,255))
			screen.blit(word_text, data[1])
		
		