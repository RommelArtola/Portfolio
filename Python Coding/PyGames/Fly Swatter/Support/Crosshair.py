import pygame
import os
import random


game_directory = os.path.dirname(os.path.dirname(__file__))

ROOT_IMG = os.path.join(game_directory,  'Assets', 'Images')
ROOT_SOUND = os.path.join(game_directory, 'Assets', 'Sounds')

crosshair_img = os.path.join(ROOT_IMG, 'Crosshair.png')


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, surface, position:list=None) -> None:
        super().__init__()
        self.surface    = surface
        self.screen_w   = self.surface.get_width()
        self.screen_h   = self.surface.get_height()

    

        self.image =  pygame.image.load(crosshair_img, 'Fly Enemy').convert() #Converts for optimization
        self.image    = pygame.transform.scale(self.image, size=(self.image.get_width()/3, self.image.get_height()/3)) #size== (w,h) #scale

        self.rect = self.image.get_rect()
        self.image.set_colorkey((0,0,255))

    def draw(self, position):
        self.surface.blit(self.image, position)
        self.rect.center = position
    
