import pygame
import sys

class GamePlay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)  # Larger font for score, etc.
        self.fps_font = pygame.font.SysFont("Arial", 15)  # Smaller font for FPS display
        self.clock = pygame.time.Clock()
        self.running = True

        # Player settings
        self.player_size = 30
        self.player_x = self.screen.get_width() * 2 // 5  # Starting X position (2/5th of the width)
        self.player_y = self.screen.get_height() // 2  # Start in the middle of the screen vertically
        self.player_velocity = 0  # Starting velocity (no initial speed)
        self.gravity = 0.3  # Gravity pulling downwards
        self.gravity_reversed = -0.3  # Gravity pulling upwards
        self.gravity_state = self.gravity  # Default gravity is pulling downwards

        self.is_falling = False  # Is the player falling?
        #self.ground_y = self.screen.get_height() - self.player_size

        # Platform settings
        self.platforms = []  # List to hold platforms
        self.create_platforms()

        # Countdown settings
        self.countdown_font = pygame.font.SysFont("Arial", 50)
        self.start_time = pygame.time.get_ticks()

    
    def create_platforms(self):
        """Creates a row of platforms at the bottom of the screen."""
        platform_width = 500
        platform_height = 20

        # Bottom platform (near the bottom of the screen)
        bottom_platform_x = self.screen.get_width() * 1 // 5  # X position of the bottom platform
        bottom_platform_y = self.screen.get_height() - platform_height  # Y position at the bottom
        self.platforms.append(pygame.Rect(bottom_platform_x, bottom_platform_y, platform_width, platform_height))

        # Top platform (near the top of the screen)
        top_platform_x = self.screen.get_width() * 1 // 5  # X position of the top platform
        top_platform_y = 0  # Y position near the top
        self.platforms.append(pygame.Rect(top_platform_x, top_platform_y, platform_width, platform_height))

    
    def draw(self):
        self.screen.fill((0, 0, 0))
        # Your game elements go here (player, obstacles, etc.)
        score_text = self.font.render("Score: 0", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))
        
        # Display FPS in the top-right corner with smaller font
        fps_text = self.fps_font.render(f"FPS: {self.clock.get_fps():.2f}", True, (255, 255, 255))
        fps_rect = fps_text.get_rect(topright=(self.screen.get_width() - 20, 20))  # Positioning to top-right
        self.screen.blit(fps_text, fps_rect)

        # If gravity is reversed, adjust the player's y-position so they appear on the platform's bottom
        if self.gravity_state == self.gravity_reversed:
            # Find the platform that the player is currently colliding with
            for platform in self.platforms:
                if pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size).colliderect(platform):
                    # If the player is above the platform (while moving up), set y position to the bottom of the platform
                    self.player_y = platform.bottom - self.player_size
                    break

                
        # Draw player (as a red box)
        pygame.draw.rect(self.screen, (255, 0, 0), (self.player_x, self.player_y, self.player_size, self.player_size))

        # Draw the platforms (as blue boxes)
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 0, 255), platform)

    def display_countdown(self):
        # Countdown from 3 to 1
        time_left = (pygame.time.get_ticks() - self.start_time) // 1000  # Time in seconds
        if time_left < 3:
            countdown_text = self.countdown_font.render(str(3 - time_left), True, (255, 255, 255))
            self.screen.blit(countdown_text, (self.screen.get_width() // 2 - countdown_text.get_width() // 2, self.screen.get_height() // 3))

        # Show "GO!" after countdown is finished
        elif time_left == 3:
            go_text = self.countdown_font.render("GO!", True, (255, 255, 255))
            self.screen.blit(go_text, (self.screen.get_width() // 2 - go_text.get_width() // 2, self.screen.get_height() // 3))

        return time_left
    
    def handle_collisions(self):
        """Handles collisions between the player and platforms."""
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
        self.is_falling = True  # Assume falling unless proven otherwise


        # Check for collisions with platforms
        # Assume the player is falling until proven otherwise
        #self.is_falling = True  
        for platform in self.platforms:
            if player_rect.colliderect(platform):
                if self.is_falling and self.gravity_state == self.gravity:  # Falling down to the platform
                    # Stop at the platform's top if gravity is normal
                    self.player_y = platform.top - self.player_size
                    self.player_velocity = 0  # Stop the falling velocity
                    self.is_falling = False  # Player is no longer falling
                    break  # Exit after the first collision with a platform
                elif self.is_falling and self.gravity_state == self.gravity_reversed:  # Falling up (gravity reversed)
                    # Stop at the platform's bottom if gravity is reversed
                    self.player_y = platform.bottom
                    self.player_velocity = 0  # Stop the rising velocity
                    self.is_falling = True  # Player is no longer falling
                    break  # Exit after the first collision with a platform
            else:
                # If no collision, the player is falling
                self.is_falling = True

        # After checking collisions, apply gravity only if not on a platform
        #if self.is_falling:
         # Apply gravity when in the air (either falling down or rising up)
         #   if self.gravity_state == self.gravity:
          #     self.player_velocity += self.gravity  # Falling down
           # elif self.gravity_state == self.gravity_reversed:
            #   self.player_velocity -= self.gravity  # Moving upwards
            
    def update_gravity(self):
        """Handles gravity change only when spacebar is pressed."""
        if self.gravity_state == self.gravity:
            self.gravity_state = self.gravity_reversed
        else:
            self.gravity_state = self.gravity

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to pause
                        return 2  # Switch to Pause menu
                    elif event.key == pygame.K_ESCAPE:  # Press 'Escape' to go to main menu
                        return 0  # Exit game and go back to main menu
                    elif event.key == pygame.K_SPACE and not self.is_falling:  # Change gravity when on platform
                        if not self.is_falling:
                            self.update_gravity()

            # Handle player collision with platforms (player stops at platform)
            self.handle_collisions()

            # Apply gravity to make the player move up or down
            if self.gravity_state == self.gravity:  # Gravity pulling down
                self.player_velocity += self.gravity  # Increase velocity by gravity value
                if self.player_velocity > 10:  # Cap the velocity
                    self.player_velocity = 10
            elif self.gravity_state == self.gravity_reversed:  # Gravity pulling up
                 self.player_velocity -= self.gravity  # Decrease velocity by gravity value
                 if self.player_velocity < -10:  # Cap the velocity (negative for reversed gravity)
                    self.player_velocity = -10

            # Update the player's position based on velocity
            self.player_y += self.player_velocity

            # Draw the game elements
            self.draw()
            pygame.display.update()

            # Cap the frame rate
            self.clock.tick(60)  # 60 FPS limit