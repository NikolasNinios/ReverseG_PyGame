import pygame
import sys
import globals
from scoreCls import scoreCls 

class ResultsMenu:
    def __init__(self, screen, result_data):
        self.screen = screen
        self.result_data = result_data
        self.font = pygame.font.Font(None, 40)
        self.running = True
        self.updateresults = True
        self.scoreCls = scoreCls()

    def run(self):

        # Format the scores with two decimal places
        player1_score =  round(self.result_data['player1_score'],2)
        if globals.multiplayer == 2 :
            player2_score =  round(self.result_data['player2_score'],2)

        if self.updateresults:
            if globals.multiplayer == 2 :
               self.scoreCls.save_score("RED",player1_score,globals.diffistats)
               self.scoreCls.save_score("BLUE",player2_score,globals.diffistats)
               self.updateresults =False
            else:
               self.scoreCls.save_score("RED",self.result_data['player1_score'],globals.diffistats)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Restart game
                        return 1  # Return to gameplay state
                    elif event.key == pygame.K_ESCAPE:  # Go back to main menu
                        return 0 # Return to main menu state

            # Draw results screen
            self.screen.fill((0, 0, 0))  # Clear screen

            if globals.multiplayer == 2 :
                # Display scores
                self.draw_text(f"Red Score: {player1_score}", 200, 100, (255, 255, 255))
                self.draw_text(f"Blue Score: {player2_score}", 200, 150, (255, 255, 255))
                 # Display instructions
                self.draw_text("Press R to play again", 200, 250, (255, 255, 255))
                self.draw_text("Press ESC to return to main menu", 200, 300, (255, 255, 255))
            else:
                self.draw_text(f"Red Score: {player1_score}", 200, 100, (255, 255, 255))
                 # Display instructions
                self.draw_text("Press R to play again", 200, 200, (255, 255, 255))
                self.draw_text("Press ESC to return to main menu", 200, 250, (255, 255, 255))
        
            pygame.display.flip()

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))