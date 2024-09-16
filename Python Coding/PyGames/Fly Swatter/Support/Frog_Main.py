import pygame
import os
import random

game_directory = os.path.dirname(os.path.dirname(__file__))

ROOT_IMG = os.path.join(game_directory,  'Assets', 'Images')
ROOT_SOUND = os.path.join(game_directory, 'Assets', 'Sounds')


frog_img = os.path.join(ROOT_IMG, 'Frog.png')
heart_full_img = os.path.join(ROOT_IMG, 'Heart Full.png')
heart_broken_img = os.path.join(ROOT_IMG, 'Heart Broken.png')
lick_file = os.path.join(ROOT_SOUND, 'Lick Sound.wav')
damage_sound = os.path.join(ROOT_SOUND, 'Take Damage.mp3')

class Frog():
    def __init__(self, surface, attack_cooldown=500) -> None:
        self.surface = surface
        self.attack_cooldown = attack_cooldown
        self.screen_w = self.surface.get_width()
        self.screen_h = self.surface.get_height()

        self.center = [0,0] 

        self.mask = None

        self.heart_bar = {} # {Tuple Location: Heart Img}
        self.health_value = None #changes to 3 later
        self.take_dmg_sound=pygame.mixer.Sound(damage_sound)

    def load_image(self, color_key=(0,0,255)):
        
        # Frog Details
        self.img    = pygame.image.load(frog_img, 'Frog Player').convert() #Converts for optimization

        self.img.set_colorkey(color_key) #Removes the color_key color background
        img_w       = self.img.get_width()
        img_h       = self.img.get_height()
        self.img    = pygame.transform.scale(self.img, size=(img_w, img_h)) #size== (w,h)
        img_size = self.img.get_size()

        self.center = [ int(self.screen_w/2) - img_size[0]/2, self.screen_h*.85] #Done this to place the frog in the center of the screen.

        return self.img #returns frog

    def fill_health(self):
        # Heart Details
        self.heart_full = pygame.image.load(heart_full_img, 'Full Heart').convert()
        self.heart_full.set_colorkey((0,0,0))
        self.heart_broken = pygame.image.load(heart_broken_img, 'Broken Heart').convert()
        self.heart_broken.set_colorkey((0,0,0))

        
        self.heart_bar = {    (0,0): self.heart_full,
                              (self.screen_w*.10, 0): self.heart_full,
                              (self.screen_w*.20, 0): self.heart_full
                        }
        self.health_value = sum( [self.heart_full == i for i in self.heart_bar.values()])

    def attack(self, mouse_pos):
        pygame.draw.line(self.surface, color=(255,0,0), start_pos=(self.screen_w/2, self.screen_h - (self.screen_h*.05)), end_pos=mouse_pos, width=15)
        pygame.mixer.Sound(lick_file).play()
        #pygame.draw.circle(self.surface, color=(255,0,0), center = mouse_pos, radius=10)

    def take_damage(self):
        self.take_dmg_sound.play()
        self.take_dmg_sound.set_volume(.5)
        self.heart_bar[list(self.heart_bar.keys())[self.health_value -1]] = self.heart_broken
        self.health_value -= 1

    def display(self):
        self.load_image()
        self.surface.blit(self.img, self.center)
        self.surface.blits( (heart, pos) for pos, heart in self.heart_bar.items())

    