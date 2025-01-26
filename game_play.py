import pygame
import sys
import random

class GamePlay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)  # Larger font for score, etc.
        self.fps_font = pygame.font.SysFont("Arial", 15)  # Smaller font for FPS display
        self.clock = pygame.time.Clock()
        self.running = True
        self.test123 = True
        self.testfrist = True
        # Player settings
        self.player_size = 30
        self.player_x = self.screen.get_width() * 2 // 5  # Starting X position (2/5th of the width)
        self.player_y = self.screen.get_height() // 2  # Start in the middle of the screen vertically
        self.player_velocity = 0  # Starting velocity (no initial speed)
        self.gravity = 0.3  # Gravity pulling downwards
        self.gravity_reversed = -0.3  # Gravity pulling upwards
        self.gravity_state = self.gravity  # Default gravity is pulling downwards
        self.start_flag=1
        self.player_on_object=False

        self.is_falling = True  # Is the player falling?
        #self.ground_y = self.screen.get_height() - self.player_size

        # Platform settings
        self.platforms = []  # List to hold platforms
        self.create_platforms()
        self.platform_speed = 5

        # Countdown settings
        self.countdown_font = pygame.font.SysFont("Arial", 50)
        self.start_time = pygame.time.get_ticks()

    
    def create_platforms(self):
        """Creates a row of platforms at the bottom of the screen."""
        #platform_width = 400
        #platform_height = 20

        # Bottom platform (near the bottom of the screen)
        #bottom_platform_x =  self.screen.get_width() -500 #* 1 // 5  # X position of the bottom platform
        #bottom_platform_y = self.screen.get_height() - platform_height  # Y position at the bottom
        #self.platforms.append(pygame.Rect(bottom_platform_x, bottom_platform_y, platform_width, platform_height))

        # Top platform (near the top of the screen)
        #top_platform_x = self.screen.get_width() -200#* 1 // 5  # X position of the top platform
        #top_platform_y = 0  # Y position near the top
        #self.platforms.append(pygame.Rect(top_platform_x, top_platform_y, platform_width, platform_height))
         # Create a new platform at the right side of the screen
        if self.testfrist:

            platform_width = random.randint(100,200)  # Random width for platforms
            platform_height = 20  # Set a fixed height for the platform
            platform_x = self.screen.get_width()-400  # Start at the right side of the screen
            self.testfrist = False    
        else:

            platform_width = random.randint(100,200)  # Random width for platforms
            platform_height = 20  # Set a fixed height for the platform
            platform_x = self.screen.get_width()  # Start at the right side of the screen
        
        if self.test123: 
            platform_y = 620#random.randint(0, 620)  # Random vertical position for platforms
            self.test123 = False
        else:
            platform_y = random.randint(0, 320)  # Random vertical position for platforms
            self.test123 = True
       
        
        # Create a pygame Rect object for the platform
        platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
        
        # Add platform to the list of platforms
        self.platforms.append(platform_rect)


    def move_platforms(self):
        # Move each platform left by 5 pixels per frame
        for platform in self.platforms:
            platform.x -= self.platform_speed  # Move platform to the left by 5 pixels each frame

    def draw_platforms(self):
        # Draw all platforms on the screen
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), platform)  # Green platforms
    
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
        #if self.gravity_state == self.gravity_reversed:
            # Find the platform that the player is currently colliding with
           # for platform in self.platforms:
             #   if pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size).colliderect(platform):
                    # If the player is above the platform (while moving up), set y position to the bottom of the platform
                #    self.player_y = platform.bottom - self.player_size
                   # break

                
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
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)

        if self.player_velocity > 0:  # Falling
            for platform in self.platforms:
                platform_rect = platform
                if player_rect.bottom  <= platform_rect.top + 10:
                    if player_rect.bottom + 10 >= platform_rect.top:        #300
                        if player_rect.right >= platform_rect.left  and player_rect.left <= platform_rect.right :
                            self.player_y = platform_rect.top - self.player_size  # Align player on top of the platform
                            self.player_velocity = 0  # Stop movement
                            self.player_on_object = True  # Mark as standing on a platform

                             # Calculate how many pixels left on the platform
                            player_land_position = player_rect.left  # Player's left position
                            platform_left = platform_rect.left  # Platform's left position
                            platform_right = platform_rect.right  # Platform's right position
                
                            # Calculate how many pixels player has left on the platform to stand on
                            remaining_space = platform_right - player_land_position  # e.g., 350 - 300 = 50 pixels left

                            # Track platform speed (let's assume the platform moves at a speed of 'platform_speed')
                            #platform_speed = 5  # Example: platform moves 5 pixels per frame to the left
                
                            # Calculate how many frames player can stay on the platform
                            frames_to_fall = remaining_space / self.platform_speed   # 50 pixels / 5 pixels per frame = 10 frames
                
                            # Store this value, so you can use it later to detect when to change velocity to falling
                            self.frames_on_platform = frames_to_fall
                            self.is_falling=True
                            return  # Exit once collision is handled
                
        elif self.player_velocity < 0:  # Moving upwards
            for platform in self.platforms:
                platform_rect = platform
                if player_rect.top >= platform_rect.bottom - 10:
                    if player_rect.top - 10 <= platform_rect.bottom:
                        if player_rect.right >= platform_rect.left  and player_rect.left <= platform_rect.right :
                            self.player_y = platform_rect.bottom  # Align player below the platform
                            self.player_velocity = 0  # Stop movement
                            self.player_on_object = True  # Mark as standing under a platform

                             # Calculate how many pixels left on the platform
                            player_land_position = player_rect.left  # Player's left position
                            platform_left = platform_rect.left  # Platform's left position
                            platform_right = platform_rect.right  # Platform's right position

                            # Calculate how many pixels player has left on the platform to stand on
                            remaining_space = platform_right - player_land_position  # e.g., 350 - 300 = 50 pixels left

                            # Track platform speed (let's assume the platform moves at a speed of 'platform_speed')
                            #platform_speed = 5  # Example: platform moves 5 pixels per frame to the left
                
                            # Calculate how many frames player can stay on the platform
                            frames_to_fall = remaining_space / self.platform_speed   # 50 pixels / 5 pixels per frame = 10 frames
                
                            # Store this value, so you can use it later to detect when to change velocity to falling
                            self.frames_on_platform = frames_to_fall
                            self.is_falling=False
                            return  # Exit once collision is handled

     
    
            
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
                    elif event.key == pygame.K_SPACE: #and not self.is_falling:  # Change gravity when on platform
                        if self.player_on_object:                       
                            self.update_gravity()
                            self.player_on_object=False

            if self.start_flag == 0:
            # Handle player collision with platforms (player stops at platform)
                if not self.player_velocity == 0:
                    self.handle_collisions()
            else:
                self.start_flag = 0
            

            if not  self.player_on_object: 
            # Apply gravity to make the player move up or down
                if self.gravity_state == self.gravity:  # Gravity pulling down
                    self.player_velocity += self.gravity  # Increase velocity by gravity value
                    if self.player_velocity > 8:  # Cap the velocity
                        self.player_velocity = 8
                elif self.gravity_state == self.gravity_reversed:  # Gravity pulling up
                    self.player_velocity -= self.gravity  # Decrease velocity by gravity value
                    if self.player_velocity < -8:  # Cap the velocity (negative for reversed gravity)
                        self.player_velocity = -8
            else:
                self.frames_on_platform -=1

                if self.is_falling:
                    if self.frames_on_platform+8 <= 0:
                        self.player_on_object = False
                        self.player_velocity = 0.3  # Set velocity to falling (positive velocity)
                        self.frames_on_platform = 0  # Reset frames
                else:
                    if self.frames_on_platform+8 <= 0:
                        self.player_on_object = False
                        self.player_velocity = -0.3  # Set velocity to floating (negative velocity)
                        self.frames_on_platform = 0  # Reset frames 
                        

            # Update the player's position based on velocity
            if not self.player_on_object:
                self.player_y += self.player_velocity

            # Update the movement of platforms
            self.move_platforms()

                # Optionally, remove platforms that go off-screen (on the left side)
            self.platforms = [platform for platform in self.platforms if platform.right > 0]

            if len(self.platforms) == 0 or self.platforms[-1].right <= self.screen.get_width():
                self.create_platforms()
            # Draw the game elements
            self.draw()
            pygame.display.update()

            # Cap the frame rate
            self.clock.tick(60)  # 60 FPS limit