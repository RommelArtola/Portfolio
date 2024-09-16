import pygame
import os
import random

game_directory = os.path.dirname(os.path.dirname(__file__))

ROOT_IMG = os.path.join(game_directory,  'Assets', 'Images')
ROOT_SOUND = os.path.join(game_directory, 'Assets', 'Sounds')

cloud_img = os.path.join(ROOT_IMG, 'Cloud.png')
bg_img = os.path.join(ROOT_IMG, 'background.png')



class Environment():

    def __init__(self, surface, num_clouds=12) -> None:
        self.surface = surface
        
        self.screen_w = self.surface.get_width()
        self.screen_h = self.surface.get_height()

        self.clouds_positions = [ [random.randint(-20, self.screen_w), 
                                   random.randint(-20, 250)]
                                   for _ in range(num_clouds)] #left, top


    def sky_env2(self):
        self.sky    = self.surface.fill(color=(14, 219, 248))

        cloud = pygame.image.load(cloud_img, 'Clouds').convert()
        cloud.set_colorkey((0,0,255))


        self.surface.blits( [(cloud, pos) for pos in self.clouds_positions] ) #blitsequence of (img, (x,y)) passed into the blits.

    def sky_env(self):
        self.sky    = pygame.image.load(bg_img).convert()
        self.sky = pygame.transform.scale(self.sky, (self.screen_w, self.screen_h))


        cloud = pygame.image.load(cloud_img, 'Clouds').convert()
        cloud.set_colorkey((0,0,255))

        self.surface.blit(self.sky, (0,0))
        self.surface.blits( [(cloud, pos) for pos in self.clouds_positions] ) #blitsequence of (img, (x,y)) passed into the blits.
    

    def grass_env(self):
        """ Grass, road, and dirt elements"""
        grass_rect = pygame.Rect(0, #left 
                                 self.screen_h - (self.screen_h//3), #1/3 way down (top)
                                 self.screen_w, #width
                                 self.screen_h) #height
        
        self.grass  = pygame.draw.rect(surface=self.surface, color=(45, 185, 100), rect=grass_rect)


        dirt_rect = pygame.Rect(0, 
                                grass_rect.top + (grass_rect.top//4),
                                self.screen_w,
                                self.screen_h)
        
        self.road = pygame.draw.rect(surface=self.surface, color=(142, 87, 47), rect=dirt_rect)

    def display(self):
        self.sky_env()
        self.grass_env()

