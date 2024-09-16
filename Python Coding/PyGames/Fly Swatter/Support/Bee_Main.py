import pygame
import os
import random

game_directory = os.path.dirname(os.path.dirname(__file__))

ROOT_IMG = os.path.join(game_directory,  'Assets', 'Images')
ROOT_SOUND = os.path.join(game_directory, 'Assets', 'Sounds')


bee_img = os.path.join(ROOT_IMG, 'Bee.png') 
poof_img_raw = os.path.join(ROOT_IMG, 'Poof.png')
poof_file = os.path.join(ROOT_SOUND, 'Poof Sound.wav')


class Bee(pygame.sprite.Sprite):
    def __init__(self, surface, due_direction:str, velocity=5, position:list=None) -> None:
        super().__init__()
        self.surface    = surface
        self.screen_w   = self.surface.get_width()
        self.screen_h   = self.surface.get_height()
        self.direction = due_direction
        
        
        self.velocity   = velocity #(self.screen_w / (3.5 * FPS)) #Velocity formula (adapted)
        self.max_y_height = int(self.screen_h - (self.screen_h*.30))        
        self.max_x_pos = int(self.screen_w * 1.50) + 1
        self.min_x_pos = -(self.max_x_pos - self.screen_w)

        if position is None:
            self.position = [random.randint(0, self.max_x_pos),
                            random.randint(0, self.max_y_height)] #to be updated later.
        else:
            self.position = position
        

        self.image =  pygame.image.load(bee_img, 'Fly Enemy').convert() #Converts for optimization
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.image    = pygame.transform.scale(self.image, size=(self.image.get_width()/3, self.image.get_height()/3)) #size== (w,h) #scale

        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.image.set_colorkey((0,0,255))

        
        self.mask = pygame.mask.from_surface(self.image)


        # Load poof image and sound
        self.poof_img = pygame.image.load(poof_img_raw).convert()
        self.poof_img.set_colorkey((0, 0, 255))
        self.poof_img = pygame.transform.scale(self.poof_img, [coord // 2 for coord in self.poof_img.get_size()])
        self.poof_sound = pygame.mixer.Sound(poof_file)

    def update(self):
        if self.direction == 'left':
            self.rect.x -= self.velocity
            if self.rect.right < 0:
                self.rect.left, self.rect.top = [int(self.screen_w*1.10),
                                                    random.randint(0, self.max_y_height)]
                #self.kill()
                #self.poof()

        elif self.direction == 'right':
            self.rect.x += self.velocity
            if self.rect.left > self.screen_w:
                self.rect.right, self.rect.top = [int(0 - self.screen_w*.10),
                                                    random.randint(0, self.max_y_height)]
                #self.kill()
                #self.poof()


    def poof(self):
        self.poof_sound.play()
        self.surface.blit(self.poof_img, self.rect)
