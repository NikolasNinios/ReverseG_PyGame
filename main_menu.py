import pygame
import sys
from scoreCls import scoreCls  

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.background = pygame.image.load('assets/images/menuBck.jpg')  # Load background image
        self.font = pygame.font.SysFont("Comic Sans MS", 40)  # Comic font for game title
        self.button_font = pygame.font.SysFont("Arial", 30)  # Regular font for buttons
        self.text_color = (255, 255, 255)  # White text color
        self.running = True
       
         # Initialize JSONManager for handling scores
        self.scoreCls = scoreCls()  # Add this line

        # Colors
        self.title_color = (255, 0, 0)  # Red for "REVERSE G"
        self.box_color = (64, 224, 208)  # Turquoise for the box
        self.diff_box_color = (135, 206, 235)  # Light turquoise for difficulty box

    def draw_background(self):
        # Blit the background image to the screen at the top-left corner (0, 0)
        self.screen.blit(self.background, (0, 0))

    def draw_rounded_box(self, x, y, width, height, radius, color):
        """Draw a box with rounded corners."""
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=radius)

    def draw(self):
        # Draw the background first
        self.draw_background()

        # Draw the game title "REVERSE G"
        title_text = self.font.render("REVERSE G", True, self.title_color)  # Red font for title
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))  # Centered at the top

        # Draw the title in a turquoise box with curved corners
        title_box_width = title_rect.width + 40
        title_box_height = title_rect.height + 20
        self.draw_rounded_box(title_rect.x - 20, title_rect.y - 10, title_box_width, title_box_height, 20, self.box_color)
        
        # Draw title text on top of the box
        self.screen.blit(title_text, title_rect)

       # Box for menu options with fixed width (300) and height (180)
        menu_box_width = 310
        menu_box_height = 180

        # Calculate the x and y coordinates to center the box
        menu_box_x = self.screen.get_width() // 2 - menu_box_width // 2  # Center horizontally
        menu_box_y = 200  # Position it 200 pixels from the top

        # Draw the rounded box with the new position
        self.draw_rounded_box(menu_box_x, menu_box_y, menu_box_width, menu_box_height, 20, self.box_color)

        # Option Text inside the box (1 Player, 2 Players, Scoreboard)
        play_text = self.button_font.render("1 Player (Press 1)", True, (255, 255, 255))
        multiplayer_text = self.button_font.render("2 Players (Press 2)", True, (255, 255, 255))
        scoreboard_text = self.button_font.render("Scoreboard (Press S)", True, (255, 255, 255))

        # Calculate vertical spacing to center text within the box
        vertical_spacing = (menu_box_height - (play_text.get_height() + multiplayer_text.get_height() + scoreboard_text.get_height())) // 4

        # Draw the options inside the menu box (centered horizontally and with equal vertical spacing)
        self.screen.blit(play_text, (menu_box_x + (menu_box_width - play_text.get_width()) // 2, menu_box_y + vertical_spacing))
        self.screen.blit(multiplayer_text, (menu_box_x + (menu_box_width - multiplayer_text.get_width()) // 2, menu_box_y + vertical_spacing + play_text.get_height() + vertical_spacing))
        self.screen.blit(scoreboard_text, (menu_box_x + (menu_box_width - scoreboard_text.get_width()) // 2, menu_box_y + vertical_spacing + play_text.get_height() + multiplayer_text.get_height() + 2 * vertical_spacing))

       # Draw a separate box for difficulty options
        diff_text = self.button_font.render("Mars(M), Earth(E), Jupiter(J)", True, (255, 255, 255))
        diff_box_width = diff_text.get_width() + 40
        diff_box_height = diff_text.get_height() + 20

        # Center the box at the bottom of the screen
        box_x = self.screen.get_width() // 2 - diff_box_width // 2
        box_y = self.screen.get_height() - diff_box_height - 20  # Slight padding from bottom

        # Draw the rounded box
        self.draw_rounded_box(box_x, box_y, diff_box_width, diff_box_height, 30, self.box_color)

        # Center the text inside the box
        text_x = self.screen.get_width() // 2 - diff_text.get_width() // 2
        text_y = box_y + (diff_box_height - diff_text.get_height()) // 2  # Center text vertically in the box

        # Draw difficulty text inside the box
        self.screen.blit(diff_text, (text_x, text_y))

    def show_scores(self):
        """Display the top 20 scores."""
        self.screen.fill((0, 0, 0))  # Clear the screen with black background

        # Load top 20 scores from JSONManager
        top_scores = self.scoreCls.get_top_scores(top_n=20)

        # Display title
        title_text = self.font.render("Top 20 Scores", True, self.text_color)
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Check if there are scores to display
        if not top_scores:
            no_scores_text = self.button_font.render("No scores available", True, (255, 255, 255))
            no_scores_rect = no_scores_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(no_scores_text, no_scores_rect)
        else:
        # Display each score
            y_offset = 120
        for rank, score_entry in enumerate(top_scores, start=1):
            score_text = self.button_font.render(
                f"{rank}. {score_entry['name']} - {score_entry['score']} pts - {score_entry['time_survived']}s",
                True,
                (255, 255, 255),
            )
            self.screen.blit(score_text, (50, y_offset))
            y_offset += 40

         # Display "Press ESC to return" at the bottom
        return_text = self.button_font.render("Press ESC to return", True, (255, 255, 255))
        self.screen.blit(return_text, (self.screen.get_width() // 2 - return_text.get_width() // 2, self.screen.get_height() - 50))

        pygame.display.update()

        # Wait for user to press ESC to return to the menu
        while True:
            for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   pygame.quit()
                   sys.exit()
               if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:  # ESC to return to main menu
                         return

    def run(self):
        self.draw()
        pygame.display.update()

        # Event loop for menu navigation
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # 1 Player selected
                        return 1  # Go to gameplay
                    elif event.key == pygame.K_2:  # 2 Players selected
                        return 1  # Go to multiplayer gameplay (same as 1 Player for now)
                    elif event.key == pygame.K_s:  # Scoreboard selected
                        self.show_scores()  # Show the scores
                    if event.key == pygame.K_ESCAPE:
                        return 0  # Exit game or go back