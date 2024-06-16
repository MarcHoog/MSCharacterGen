
import pygame 
import sys
from scripts.nx import NX
from scripts.character import Character
from pygame.math import Vector2

class Game:
    def __init__(self):
        pygame.init()
        
        # Loading nx files
        self.nx = NX('./content/Character.nx')
        
        # Title of the game
        pygame.display.set_caption("PyStory")
        
        # what we show
        self.screen = pygame.display.set_mode((1280, 960))
        
        # What we render on
        self.display = pygame.Surface((640, 480))
        self.clock = pygame.time.Clock()
        
        self.character = Character(self.nx)
        
                
    def run(self):
        
        self.character.calculate_offsets()
        print(self.character.offsets)
        
        while True:
            self.display.fill((14, 219, 248))
            self.display.blit(self.character.sprites['char_body'].load_image(), self.character.offsets['char_body'] + Vector2(100,100))
            self.display.blit(self.character.sprites['char_arm'].load_image(), self.character.offsets['char_arm'] + Vector2(100,100))
            self.display.blit(self.character.sprites['char_head'].load_image(), self.character.offsets['char_head'] + Vector2(100,100))
            
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Quiting the Game.")
                        pygame.quit()
                        sys.exit()
            
            # Return value of this will be the scaled display 
            # and we can just throw it on the screen and that is what we are looking for.
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)
            
Game().run()

