'''
Created on Dec 3, 2013

@author: gparker
'''

import pygame, sys

from pygame.locals import *
import MapLoader
import Towers

#Need to make this dynamic
screenW = 640
screenH = 480

pygame.init()
pygame.font.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((screenW,screenH))
pygame.display.set_caption("PyDefense 0.1")
backgroundColor = (255,255,255)
#screen = pygame.Surface((screenW, screenH))

drawMap = MapLoader.MapLoader("../assets/Level1.tmx")
drawMap.render(windowSurfaceObj)

f = pygame.font.Font(pygame.font.get_default_font(), 20)
GUI = MapLoader.MapGUI(screenW, screenH, f)


text = "press any key to continue"
i = f.render(text, 1, (180,180,0))
sizeX, sizeY = f.size(text)
x = (screenW / 2) - (sizeX / 2)
y = (screenH / 2) - (sizeY / 2)
windowSurfaceObj.blit(i, (x,y))



fighter = Towers.FighterTower
archer = Towers.ArcherTower
mage = Towers.MageTower
towers = [fighter, archer, mage]
towerInHand = None
hoverTower = None
selectedTower = -1



run = True
paused = True
while run:
	pygame.display.update()
	fpsClock.tick(30)
	if paused == False:
		windowSurfaceObj.fill(backgroundColor)
		drawMap.render(windowSurfaceObj)
		GUI.render(windowSurfaceObj)
	for event in pygame.event.get():
		if (event.type == QUIT): 
			run = False
		#initial clean the screen, can be used for a menu class later
		if paused == True:
			if (event.type == KEYDOWN):
				paused = False
# 		else:
# 			drawMap.render(windowSurfaceObj)
# 			GUI.render(windowSurfaceObj)
		
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
				GUI.closeTowerMenu()
			
			if selectedTower <> -1:
				towerInHand = None
		
		if (event.type == MOUSEBUTTONDOWN):
			if towerInHand and GUI.money >= towerInHand.cost:
				drawMap.placeTower(towerInHand)
				GUI.money -= towerInHand.cost
				selectedTower = -1
			elif hoverTower:
				GUI.openTowerMenu(hoverTower)
		
		#Capture the item hovering over
		if(event.type == MOUSEMOTION):
			if towerInHand is None:
				hoverTower = drawMap.getTower(*pygame.mouse.get_pos())
				
	#End Events loop
	
	if (selectedTower <> -1):
		box = drawMap.getPlaceable(pygame.mouse.get_pos())
		if box: 
			
			if towerInHand:
				tower = towerInHand
			else:
				tower = towers[selectedTower]()
				towerInHand = tower
			
			tower.setLocation(box)
			windowSurfaceObj.blit(tower.getActiveImage(Transparent=True), (tower.location.x,tower.location.y))
			pygame.mouse.set_cursor(*pygame.cursors.arrow)
		else:
			pygame.mouse.set_cursor(*pygame.cursors.broken_x)
			towerInHand = None
	else:
		pygame.mouse.set_cursor(*pygame.cursors.arrow)
		towerInHand = None
	
	if towerInHand:
		GUI.setSelectedText(towerInHand)
		hoverTower = None
	elif hoverTower:
		GUI.setSelectedText(hoverTower)
	else:
		GUI.selectedItem = "" 
