'''
Created on Dec 14, 2013

@author: gparker
'''
'''
Created on Dec 3, 2013

@author: gparker
'''

import pygame
import sys
sys.path.append("../../pytmx")
from pygame.locals import *
import MapLoader
import Towers

#Need to make this dynamic
screenW = 1024
screenH = 768
pygame.display.set_caption("PyDefense 0.1")

pygame.init()

fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((screenW,screenH))




#TODO: Move to Scenes
drawMap = MapLoader.MapLoader("../assets/Level2.tmx")
drawMap.render(windowSurfaceObj)
GUI = MapLoader.MapGUI(screenW, screenH)
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
	if paused == False:
		drawMap.update()
		GUI.health -= drawMap.damage
		GUI.money += drawMap.money
	fpsClock.tick(30)
	if paused == False:
		drawMap.render(windowSurfaceObj)
		GUI.render(windowSurfaceObj)
	for event in pygame.event.get():
		if (event.type == QUIT): 
			run = False
		
		#Using this for debugging currently. Shows that certain areas have been marked as 'placeable'
		if (event.type == KEYDOWN ):
			if (event.key == K_TAB):
				drawMap.addEnemy()
			if (event.key == K_1):
				selectedTower = 0
			if (event.key == K_2):
				selectedTower = 1
			if (event.key == K_3):
				selectedTower = 2
			if (event.key == K_ESCAPE ):
				selectedTower = -1
				GUI.closeTowerMenu()
				hoverTower = None
			
			if selectedTower <> -1:
				towerInHand = None
				GUI.closeTowerMenu()
		
		if (event.type == MOUSEBUTTONDOWN):
			if towerInHand and GUI.money >= towerInHand.cost:
				drawMap.placeTower(towerInHand)
				GUI.money -= towerInHand.cost
				towerInHand.showRadius = False
				selectedTower = -1
			elif hoverTower:
				if GUI.openTower:
					GUI.closeTowerMenu()
				GUI.openTowerMenu(hoverTower)
			x,y = pygame.mouse.get_pos()
			GUI.click(x, y, drawMap)
		
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
				towerInHand.showRadius = True
			
			tower.setLocation(box)
			tower.render(windowSurfaceObj, Transparent=True)
			#windowSurfaceObj.blit(tower.getActiveImage(Transparent=True), (tower.location.x,tower.location.y))
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
