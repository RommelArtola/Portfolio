import pygame
import os
import sys
import random
import time



# Class Imports
from Support.Bee_Main import Bee
from Support.Enemy_Fly import Fly
from Support.Static_Environment import Environment
from Support.Frog_Main import Frog
from Support.Score_Keeper import Score
from Support.Crosshair import Crosshair


ROOT_SOUND = os.path.join(os.path.dirname(__file__), 'Assets', 'Sounds')

fly_sound = os.path.join(ROOT_SOUND, 'Flies Sound.mp3')
game_music = os.path.join(ROOT_SOUND, 'BG Music.mp3')
frog_amb = os.path.join(ROOT_SOUND, 'Frog Ambiance.mp3')


class Game():

    def __init__(self, 
                 screen_w:int=800, 
                 screen_h:int=600, 
                 FPS:int=60,
                 num_flies=20,
                 num_bees=10,
                 extra_params=None
                 ) -> None:
        
        # Broad-use variables.
        self.root_path = os.path.dirname(__file__)
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.FPS        = FPS
        self.num_flies  = num_flies
        self.num_bees   = num_bees
        
        
        # Pygame initilizations
        pygame.init() # Initialize game instance
        self.screen     = pygame.display.set_mode((self.screen_w, self.screen_h)) #set screen size
        self.clock      = pygame.time.Clock() #Adjust clock (FPS)
        pygame.display.set_caption('Fly Swatter')

        # Initialize Imported Classes  
        self.flies_group = pygame.sprite.Group() 
        self.flies_group.add([Fly(surface=self.screen, 
                                  due_direction=random.choice(['left', 'right']), 
                                  velocity=random.randint(2,8), 
                                  position=None) for _ in range(self.num_flies)])

        self.bees_group = pygame.sprite.Group() 
        self.bees_group.add([Bee(surface=self.screen, 
                                 due_direction=random.choice(['left', 'right']), 
                                 velocity=random.randint(2,10), 
                                 position=None) for _ in range(self.num_bees)])

        
        self.static_environment = Environment(self.screen, num_clouds=15)
        self.frog = Frog(self.screen, attack_cooldown=500)
        self.score = Score(self.screen)
        self.crosshair = Crosshair(self.screen)
    
    def display_game_over_screen(self):
        # Fill the screen with a background color
        self.screen.fill((0, 0, 0))  # Black background

        # Choose a font and size
        font = pygame.font.Font(None, 74)  # You can use a custom font file

        # Render the "Game Over" text
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        text_rect = game_over_text.get_rect(center=(self.screen_w/2, self.screen_h/2 - 50))
        self.screen.blit(game_over_text, text_rect)

        # Render the score text
        score_text = font.render(f"Score: {self.score.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_w/2, self.screen_h/2 + 50))
        self.screen.blit(score_text, score_rect)
        
    def run(self) -> pygame:
        swarm_sound = pygame.mixer.Sound(fly_sound)
        swarm_sound.play() # Play the flies swarm sound
        swarm_sound.set_volume(.5)

        # background_music = pygame.mixer.Sound(game_music)
        # background_music.play(-1)
        # background_music.set_volume(.05)

        frog_ambiance = pygame.mixer.Sound(frog_amb)
        frog_ambiance.play(-1)
        frog_ambiance.set_volume(.3)

        self.frog.fill_health()
        pygame.mouse.set_visible(False)


        last_attack_time = 0

        game_over = False

        while True:
            mouse_pos = pygame.mouse.get_pos()

            # Call all static environment variables.
            self.static_environment.display()
            self.frog.display()

            self.flies_group.draw(self.screen)
            self.flies_group.update()
            self.bees_group.draw(self.screen)
            self.bees_group.update()
            
            
            self.score.display()
            self.crosshair.draw(mouse_pos)
            


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):

                    # Get the current time
                    current_time = pygame.time.get_ticks()

                    # Check if enough time has passed since the last attack
                    if current_time - last_attack_time >= self.frog.attack_cooldown:
                        # Update the time of the last attack
                        last_attack_time = current_time

                        # Perform the attack
                        self.frog.attack(mouse_pos)

                        # Handle collisions with flies
                        collided_flies = pygame.sprite.spritecollide(
                            self.crosshair, self.flies_group, True)
                        for fly in collided_flies:
                            fly.poof()
                            self.score.update(1)
                            if self.score.score == 15:
                                self.num_bees *= 2
                            if self.score.score == 25:
                                self.num_bees *= 2

                        # Handle collisions with bees
                        collided_bees = pygame.sprite.spritecollide(
                            self.crosshair, self.bees_group, True)
                        for bee in collided_bees:
                            bee.poof()
                            self.frog.take_damage()
                            if self.frog.health_value == 0:
                                print(f"You got a score of: {self.score.score}")
                                game_over = True
                                # pygame.quit()
                                # sys.exit()

                    if len(self.flies_group) < self.num_flies:
                        self.flies_group.add([Fly(surface=self.screen, 
                                  due_direction=random.choice(['left', 'right']), 
                                  velocity=random.randint(2,10), 
                                  position=None) for _ in range(self.num_flies - len(self.flies_group))])
                        
                    if len(self.bees_group) < self.num_bees:
                        self.bees_group.add([Bee(surface=self.screen, 
                                 due_direction=random.choice(['left', 'right']), 
                                 velocity=random.randint(2,10), 
                                 position=None) for _ in range(self.num_bees - len(self.bees_group))])  

            
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                swarm_sound.stop()
                frog_ambiance.stop()
                pygame.mixer_music.stop()
                self.display_game_over_screen()  
                pygame.display.update() #update the sceen at below FPS
                self.clock.tick(self.FPS)
                   

            pygame.display.update() #update the sceen at below FPS
            self.clock.tick(self.FPS)
    
Game().run()