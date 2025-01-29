import pygame
import sys
from main_menu import MainMenu
from game_play import GamePlay
from results_menu import ResultsMenu
import globals  # Import your global variables and functions

# Initialize Pygame
pygame.init()

# Initialize the mixer for background music
pygame.mixer.init()

try:
    # Load and play the background music (loop it indefinitely)
    pygame.mixer.music.load('assets/music/spacemusic.wav')  # Make sure to provide correct path
    pygame.mixer.music.play(-1, 0.0)  # Loop music indefinitely
except pygame.error as e:
    print(f"Error loading music: {e}")
    #pygame.quit()
    #sys.exit()


# Set screen dimensions and title
screen = pygame.display.set_mode((1024, 640))
pygame.display.set_caption("Reverse G")

# Game states
MENU = 0
PLAY = 1
RESULTS = 2

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
        game_play = GamePlay(screen, globals.multiplayer)
        result_data = game_play.run()
        if result_data != 0:  # If gameplay returns result data, move to RESULTS
            current_state = RESULTS
            results_menu = ResultsMenu(screen, result_data)  # Pass scores to results menu
            current_state = results_menu.run()
        else:
            current_state=0
   
    # Results menu
    elif current_state == RESULTS:
        results_menu = ResultsMenu(screen)
        current_state = results_menu.run()


# Run the game loop
if __name__ == "__main__":
    while True:
        game_loop()