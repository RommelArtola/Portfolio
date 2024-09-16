import pygame
import os
import random

game_directory = os.path.dirname(os.path.dirname(__file__))

ROOT_IMG = os.path.join(game_directory,  'Assets', 'Images')
ROOT_SOUND = os.path.join(game_directory, 'Assets', 'Sounds')

class Score():
    def __init__(self, surface) -> None:
        self.surface = surface

        self.screen_w = self.surface.get_width()
        self.screen_h = self.surface.get_height()

        self.score = 0


    def display(self):
        myFont = pygame.font.SysFont(None, size=30)
        self.textSurface = myFont.render(f'Score = {self.score}', True, (0,0,0))
        self.surface.blit(self.textSurface, (self.screen_w-200,10))

    def update(self, update_amount):
        self.score += update_amount

