import unittest
import sys
import os

# Add the package to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Mock SDL for headless
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
pygame.init()

from pydefense.Enemies import Enemy, Skeleton
from pydefense.Towers import Tower, FighterTower
from pydefense import Animators

class TestEnemies(unittest.TestCase):
    def test_enemy_initialization(self):
        path = [(0,0), (10,0)]
        # Use a mock animation dict for base Enemy if needed, but easier to test concrete classes
        # However, concrete classes load images.
        # We need to make sure assets are found.

        # Test Skeleton
        skel = Skeleton(path)
        self.assertEqual(skel.health, 10)
        self.assertEqual(skel.position, (0,0))
        self.assertEqual(skel.target, (10,0))

    def test_enemy_movement(self):
        path = [(0,0), (10,0)]
        skel = Skeleton(path)
        skel.speed = 1 # fast for testing

        # Update
        skel.update()
        # Should have moved towards (10,0)
        self.assertNotEqual(skel.position, (0,0))

    def test_enemy_take_damage(self):
        path = [(0,0), (10,0)]
        skel = Skeleton(path)
        initial_health = skel.health
        skel.attack(5)
        self.assertEqual(skel.health, initial_health - 5)

class TestTowers(unittest.TestCase):
    def test_tower_initialization(self):
        # FighterTower loads images
        tower = FighterTower()
        self.assertEqual(tower.damage, 6)
        self.assertEqual(tower.level, 1)

    def test_tower_upgrade(self):
        tower = FighterTower()
        initial_damage = tower.damage
        tower.upgrade()
        self.assertEqual(tower.level, 2)
        self.assertGreater(tower.damage, initial_damage)

    def test_tower_targeting(self):
        tower = FighterTower()
        # Mock enemy
        path = [(100,100), (110,100)]
        enemy = Skeleton(path)
        enemy.collideBox.center = (100, 100)

        # Set tower location near enemy
        tower.collideBox = pygame.Rect(90, 90, 32, 32)
        tower.location = pygame.Rect(90, 90, 64, 64) # simplified

        # Update tower with enemy list
        tower.update([enemy])

        # Should target the enemy
        self.assertEqual(tower.target, enemy)

if __name__ == '__main__':
    unittest.main()
