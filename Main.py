import pygame
import sys
from main_menu import MainMenu
from game_play import GamePlay
from pause_menu import PauseMenu

# Initialize Pygame
pygame.init()
#test edw
# Set screen dimensions and title
screen = pygame.display.set_mode((1024, 640))
pygame.display.set_caption("Reverse G")

# Game states
MENU = 0
PLAY = 1
PAUSE = 2

current_state = MENU

# Set the FPS limit (e.g., 60 frames per second)
#fps = 60
#clock = pygame.time.Clock()

# Game Loop
def game_loop():
    global current_state
    
    # Main menu
    if current_state == MENU:
        main_menu = MainMenu(screen)
        current_state = main_menu.run()
    
    # Gameplay
    elif current_state == PLAY:
        game_play = GamePlay(screen)
        current_state = game_play.run()
    
    # Pause menu
    elif current_state == PAUSE:
        pause_menu = PauseMenu(screen)
        current_state = pause_menu.run()

         # Cap the frame rate
    #clock.tick(fps)

# Run the game loop
if __name__ == "__main__":
    while True:
        game_loop()