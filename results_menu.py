import pygame
import sys

class ResultsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("Paused", True, (255, 255, 255))
        self.screen.blit(title, (350, 100))
        
        resume_text = self.font.render("Press 'R' to Resume", True, (255, 255, 255))
        self.screen.blit(resume_text, (300, 200))
        
        quit_text = self.font.render("Press 'Q' to Quit to Main Menu", True, (255, 255, 255))
        self.screen.blit(quit_text, (200, 250))
    
    def run(self):
        self.draw()
        pygame.display.update()
        
        # Event loop for pause menu
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Resume game
                        return 1  # Back to gameplay
                    elif event.key == pygame.K_q:  # Quit to main menu
                        return 0  # Back to main menu