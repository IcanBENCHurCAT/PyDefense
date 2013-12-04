'''
Created on Dec 3, 2013

@author: gparker
'''

import pygame, sys

from pygame.locals import *
import MapLoader

#Need to make this dynamic
screenW = 640
screenH = 480

pygame.init()
pygame.font.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((screenW,screenH))
pygame.display.set_caption("PyDefense 0.1")
#screen = pygame.Surface((screenW, screenH))

drawMap = MapLoader.MapLoader("../assets/Level1.tmx")
drawMap.render(windowSurfaceObj)

f = pygame.font.Font(pygame.font.get_default_font(), 20)
text = "press any key to continue"
i = f.render(text, 1, (180,180,0))
sizeX, sizeY = f.size(text)
x = (screenW / 2) - (sizeX / 2)
y = (screenH / 2) - (sizeY / 2)
windowSurfaceObj.blit(i, (x,y))

red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
towers = [red,green,blue]
selectedTower = -1
run = True
paused = True
while run:
	pygame.display.update()
	fpsClock.tick(30)
	for event in pygame.event.get():
		if (event.type == QUIT): 
			run = False
		#initial clean the screen, can be used for a menu class later
		if paused == True:
			if (event.type == KEYDOWN):
				paused = False
		else:
			drawMap.render(windowSurfaceObj)
			
		#Using this for debugging currently. Shows that certain areas have been marked as 'placeable'
		if (event.type == KEYDOWN ):
			if (event.key == K_TAB):
				drawMap.showPlaceable(windowSurfaceObj)
			if (event.key == K_1):
				selectedTower = 0
			if (event.key == K_2):
				selectedTower = 1
			if (event.key == K_3):
				selectedTower = 2
			if (event.key == K_ESCAPE ):
				selectedTower = -1
		
		if (selectedTower <> -1):
			box = drawMap.getPlaceable(pygame.mouse.get_pos())
			if box: 
				pygame.draw.rect(windowSurfaceObj, towers[selectedTower], box)
				pygame.mouse.set_cursor(*pygame.cursors.arrow)
			else:
				pygame.mouse.set_cursor(*pygame.cursors.broken_x)
		else:
			pygame.mouse.set_cursor(*pygame.cursors.arrow)
