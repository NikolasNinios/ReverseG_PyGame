import pygame
import sys

class GamePlay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)  # Larger font for score, etc.
        self.fps_font = pygame.font.SysFont("Arial", 15)  # Smaller font for FPS display
        self.clock = pygame.time.Clock()
        self.running = True
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        # Your game elements go here (player, obstacles, etc.)
        score_text = self.font.render("Score: 0", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
          # Display FPS in the top-right corner with smaller font
        fps_text = self.fps_font.render(f"FPS: {self.clock.get_fps():.2f}", True, (255, 255, 255))
        fps_rect = fps_text.get_rect(topright=(self.screen.get_width() - 20, 20))  # Positioning to top-right
        self.screen.blit(fps_text, fps_rect)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to pause
                        return 2  # Switch to Pause menu
                    elif event.key == pygame.K_ESCAPE:
                        return 0  # Exit game and go back to main menu

            # Call the draw function to display game elements
            self.draw()
            pygame.display.update()

            # Cap the frame rate (you can adjust this FPS value)
            self.clock.tick(60)  # 60 FPS limit