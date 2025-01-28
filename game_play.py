import pygame
import sys
import random
import math
from playerCls import playerCls 

class GamePlay:
    def __init__(self, screen,numofplayers):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)  # Larger font for score, etc.
        self.fps_font = pygame.font.SysFont("Arial", 15)  # Smaller font for FPS display
        self.clock = pygame.time.Clock()
        self.start_flag = 1 # for the start only cause the player always start with 0 velocity in the first frame
        self.paused = False #for pause menu

        self.running = True
        self.test123 = True
        self.testfrist = True

        #initialize 1 player
        self.player1 = playerCls(self.screen,1)

        #initialize 2 player
        if numofplayers == 2:
            self.SecondPlayer = True
            self.player2 = playerCls(self.screen,2)
        else:
            self.SecondPlayer = False

        

        # Platform settings
        self.platforms = []  # List to hold platforms
        self.create_platforms()
        self.platform_speed = 5

 
    def create_platforms(self):
        """Creates a row of platforms at the bottom of the screen."""
        #platform_width = 400
        platform_height = 20
        platform_width = random.randint(150,300)
    
        if self.testfrist:

            platform_width = 1024  # Random width for platforms
            #platform_height = 20  # Set a fixed height for the platform
            platform_x = self.screen.get_width()-1024  # Start at the right side of the screen
            platform_y = 620
            self.testfrist = False    
        else:

            
           
            last_platform = self.platforms[-1]  # Get the most recently created platform
            last_platform_end_x = last_platform.x + last_platform.width
            last_platform_y = last_platform.y

            platform_x = last_platform_end_x + platform_width

            if platform_x > 1024:
                return
            

            #f platform_x = min(platform_x, self.screen.get_width())

            # Calculate vertical difference (Δy) to determine the fall distance
            if not self.test123: 
                platform_y = random.randint(340, 600)  # Random vertical position for platforms
                self.test123 = True
            else:
               platform_y = random.randint(20, 300)  # Random vertical position for platforms
               self.test123 = False


            #platform_y = random.randint(0, 620)  # Randomize the next platform's vertical position
            delta_y = last_platform_y - platform_y

            # Ensure there’s enough distance vertically (for jump/fall mechanics)
            if abs(delta_y) < 100:
                platform_y = last_platform_y - 100 if delta_y > 0 else last_platform_y + 100


            # Use gravity to calculate the fall time (t)
            gravity = 0.3  # Gravity per frame

            if delta_y > 0:  # Platform is above the current platform (jumping up)
            # Use player velocity and jump mechanics to calculate jump time
                jump_time = math.sqrt((2 * delta_y) / gravity)  # t = sqrt(2 * Δy / a)
                fall_time = 0  # No fall time needed
            elif delta_y < 0:  # Platform is below the current platform (falling)
            # Use gravity to calculate fall time
                fall_time = math.sqrt((-2 * delta_y) / gravity)  # t = sqrt(2 * Δy / a)
                jump_time = 0  # No jump time needed
            else:
                fall_time = 0  # No fall time if the platforms are at the same height
                jump_time = 0  # No jump time if no height difference

            #fall_time = math.sqrt((2 * delta_y) / gravity)  # t = sqrt(2 * Δy / a)

            # Calculate the maximum horizontal distance the player can cover in fall_time
            player_velocity = 8  # Max player horizontal velocity
            platform_velocity = 5  # Platforms move left at 5 pixels/frame
            relative_velocity = player_velocity - platform_velocity  # Net horizontal velocity

            # Calculate the max horizontal distance based on the jump or fall time
            max_horizontal_distance = relative_velocity * max(fall_time, jump_time)  # Pixels the player can cover horizontally

            # Calculate where the next platform should be placed
            platform_x = last_platform_end_x + max_horizontal_distance +40  # Add the max horizontal distance


            # Calculate the next platform's x-coordinate
            # Calculate the next platform's x-coordinate
            # Ensure the platform_x is far enough from the last platform's end position
            #horizontal_gap = max(200, max_horizontal_distance)  # Minimum gap of 200 pixels between platforms
            #platform_x = min(last_platform_end_x + horizontal_gap, self.screen.get_width())  # Ensure it’s within screen bounds
            #gap = 100  # Fixed gap between platforms
            
            #platform_x = last_platform_end_x + gap  # Add 50 pixels gap
            #platform_x = min(platform_x, self.screen.get_width())

            #platform_x = last_platform_end_x + horizontal_gap  # Ensure platform is placed at least 200 pixels away from the last one
        
        # Ensure that the new platform doesn't overlap with the previous platform horizontally
            #while platform_x < last_platform_end_x + horizontal_gap:
                #platform_x = last_platform_end_x + horizontal_gap  # Add gap if necessary
                #platform_x = min(platform_x, self.screen.get_width())  # Ensure it’s within screen bounds



            #platform_width = random.randint(100,200)  # Random width for platforms
            #platform_height = 20  # Set a fixed height for the platform
            #platform_x = self.screen.get_width()  # Start at the right side of the screen
        
        #if self.test123: 
            #platform_y = 620#random.randint(0, 620)  # Random vertical position for platforms
            #self.test123 = False
       # else:
        #    platform_y = random.randint(0, 320)  # Random vertical position for platforms
        #    self.test123 = True
       
        
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

                
        # Draw player (as a red box)
        #pygame.draw.rect(self.screen, (255, 0, 0), (self.player_x, self.player_y, self.player_size, self.player_size))
        #pygame.draw.rect(self.screen, (255, 0, 0), (self.player.player_x, self.player.player_y, self.player.player_size, self.player.player_size))
         # Draw player2 (as a green box)
        #pygame.draw.rect(self.screen, (0, 0, 255), (self.player_x2, self.player_y2, self.player_size2, self.player_size2))
        self.player1.draw(self.screen,(255, 0, 0))

        if self.SecondPlayer:
            self.player2.draw(self.screen,(0, 0, 255))

        # Draw the platforms (as blue boxes)
        for platform in self.platforms:
            pygame.draw.rect(self.screen, (0, 0, 255), platform)
    

    #Main game logic loop
    def run(self):
        
        self.show_instructions()  # Show instructions before starting the game
        self.wait_for_keypress()  # Wait for key press to continue with the game


        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to pause
                        #return 2  # Switch to Pause menu
                        self.paused = not self.paused 
                        if self.paused:
                            self.mainmenu=0
                            self.pause_game() 
                            if self.mainmenu == 1:
                                return 0          
                    elif event.key == pygame.K_ESCAPE:  # Press 'Escape' to go to main menu
                        return 0  # Exit game and go back to main menu
                    elif event.key == pygame.K_r: #and not self.is_falling:  # Change gravity when on platform
                        if self.player1.player_on_object:                       
                           self.player1.update_gravity()
                           self.player1.player_on_object=False
                    elif event.key == pygame.K_b and self.SecondPlayer:
                        if self.player2.player_on_object:                       
                           self.player2.update_gravity()
                           self.player2.player_on_object=False

           
            if not self.paused:  

                if self.start_flag == 0:
                # Handle player collision with platforms (player stops at platform)
                    if not self.player1.player_velocity == 0:
                        self.player1.handle_collisions(self.platforms,5)
                    if self.SecondPlayer:
                        if not self.player2.player_velocity == 0:
                            self.player2.handle_collisions(self.platforms,5)
                else:
                    self.start_flag = 0  

                if self.SecondPlayer:
                    if not  self.player2.player_on_object: 
                # Apply gravity to make the player move up or down
                        if self.player2.gravity_state == self.player2.gravity:  # Gravity pulling down
                           self.player2.player_velocity += self.player2.gravity  # Increase velocity by gravity value
                           if self.player2.player_velocity > 8:  # Cap the velocity
                              self.player2.player_velocity = 7.7
                        elif self.player2.gravity_state == self.player2.gravity_reversed:  # Gravity pulling up
                             self.player2.player_velocity -= self.player2.gravity  # Decrease velocity by gravity value
                             if self.player2.player_velocity < -8:  # Cap the velocity (negative for reversed gravity)
                                self.player2.player_velocity = -7.7
                    else:
                        self.player2.frames_on_platform -=1

                        if self.player2.is_falling:
                            if self.player2.frames_on_platform+10 <= 0:
                                self.player2.player_on_object = False
                                self.player2.player_velocity = 0.3  # Set velocity to falling (positive velocity)
                                self.player2.frames_on_platform = 0  # Reset frames
                        else:
                            if self.player2.frames_on_platform+10 <= 0:
                                self.player2.player_on_object = False
                                self.player2.player_velocity = -0.3  # Set velocity to floating (negative velocity)
                                self.player2.frames_on_platform = 0  # Reset frames 
                        
                    # Update the player's position based on velocity
                    if not self.player2.player_on_object:
                        self.player2.player_y += self.player2.player_velocity
           
                
                
            

                if not  self.player1.player_on_object: 
                # Apply gravity to make the player move up or down
                    if self.player1.gravity_state == self.player1.gravity:  # Gravity pulling down
                        self.player1.player_velocity += self.player1.gravity  # Increase velocity by gravity value
                        if self.player1.player_velocity > 8:  # Cap the velocity
                            self.player1.player_velocity = 7.7
                    elif self.player1.gravity_state == self.player1.gravity_reversed:  # Gravity pulling up
                        self.player1.player_velocity -= self.player1.gravity  # Decrease velocity by gravity value
                        if self.player1.player_velocity < -8:  # Cap the velocity (negative for reversed gravity)
                            self.player1.player_velocity = -7.7
                else:
                    self.player1.frames_on_platform -=1

                    if self.player1.is_falling:
                        if self.player1.frames_on_platform+10 <= 0:
                            self.player1.player_on_object = False
                            self.player1.player_velocity = 0.3  # Set velocity to falling (positive velocity)
                            self.player1.frames_on_platform = 0  # Reset frames
                    else:
                        if self.player1.frames_on_platform+10 <= 0:
                            self.player1.player_on_object = False
                            self.player1.player_velocity = -0.3  # Set velocity to floating (negative velocity)
                            self.player1.frames_on_platform = 0  # Reset frames 
                        

            # Update the player's position based on velocity
                if not self.player1.player_on_object:
                    self.player1.player_y += self.player1.player_velocity

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



    #--------------------------------------------------------------------------------------------------------------------
    #Game instructions Start ---------------
    def draw_text(self, text, y, font_size=32, color=(255, 255, 255)):
        font = pygame.font.SysFont('Arial', font_size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        # Center the text horizontally and vertically
        text_rect.centerx = self.screen.get_width() // 2
        text_rect.y = y

        self.screen.blit(text_surface, text_rect)

    def show_instructions(self):
        # Display instructions to the players
        self.screen.fill((0, 0, 0))  # Fill the screen with black background
        self.draw_text('Player 1 changes gravity with "R"', self.screen.get_height() // 2 - 50)
        if self.SecondPlayer:
            self.draw_text('Player 2 changes gravity with "B"', self.screen.get_height() // 2)
            self.draw_text('"P" Pause The Game', self.screen.get_height() // 2+50)
            self.draw_text('Press any key to start', self.screen.get_height() // 2 + 100)
        else:
            self.draw_text('"P" Pause The Game', self.screen.get_height() // 2)
            self.draw_text('Press any key to start', self.screen.get_height() // 2 + 50)

        pygame.display.update()

    def wait_for_keypress(self):
        # Wait for any key to be pressed to continue
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Any key press will proceed
                    waiting_for_key = False
    #Game instructions End ---------------

    #--------------------------------------------------------------------------------------------------------------------
    # PAUSE MENU FUNCTIONS START------------ 
    def draw_pause_screen(self):
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, (255, 0, 0))
        self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 3))

        resume_text = font.render("Press 'P' to Resume", True, (255, 255, 255))
        self.screen.blit(resume_text, (self.screen.get_width() // 2 - resume_text.get_width() // 2, self.screen.get_height() // 2))

        exit_text = font.render("Press 'ESC' to Exit", True, (255, 255, 255))
        self.screen.blit(exit_text, (self.screen.get_width() // 2 - exit_text.get_width() // 2, self.screen.get_height() // 1.5))

    def draw_game_with_pause_overlay(self):
        # Draw the game as usual (background, player, platforms, etc.)
        self.draw()

        # Create a semi-transparent overlay for the frozen effect
        overlay_surface = pygame.Surface(self.screen.get_size())  # Full screen overlay
        overlay_surface.set_alpha(128)  # Set transparency (0-255 range)
        overlay_surface.fill((0, 0, 0))  # Black color with transparency
        self.screen.blit(overlay_surface, (0, 0))  # Draw the overlay on top of the game
        # Draw the pause screen (on top of the overlay)
        self.draw_pause_screen()
    
    def pause_game(self):
        #Handles the pause state.
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' again to resume
                        self.paused = False
                    elif event.key == pygame.K_ESCAPE:  # Press 'Escape' to go to main menu
                        self.paused = False
                        self.mainmenu = 1
                        return 0  # Exit game

            self.draw_game_with_pause_overlay()           
            pygame.display.update()
            self.clock.tick(60)  
     # PAUSE MENU FUNCTIONS END------------   