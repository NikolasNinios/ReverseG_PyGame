import pygame
import sys
import random
import math
from playerCls import playerCls 
from platformCls import platformCls 
import globals  # Import your global variables and functions

class GamePlay:
    def __init__(self, screen,numofplayers):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)  # Larger font for score, etc.
        self.fps_font = pygame.font.SysFont("Arial", 15)  # Smaller font for FPS display
        self.clock = pygame.time.Clock()
        self.start_flag = 1 # for the start only cause the player always start with 0 velocity in the first frame
        self.paused = False #for pause menu
        self.running = True # for loop to start

        #initialize 1 player
        self.player1 = playerCls(self.screen,1)

        #initialize 2 player
        if numofplayers == 2:
            self.SecondPlayer = True
            self.player2 = playerCls(self.screen,2)
        else:
            self.SecondPlayer = False

    
        # init first platform
        self.platforms = []  # List to hold platforms 
        self.initplatform = platformCls(self.screen,self.platforms,globals.platform_width,True)
        self.platforms.append(self.initplatform.platform_rect)
     
    def draw(self):
        self.screen.fill((0, 0, 0))
        # Your game elements go here (player, obstacles, etc.)
        score_text = self.font.render(f"Red Score: {self.player1.totalPoints:.2f}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 20))
        
        if self.SecondPlayer:
            score_text = self.font.render(f"Blue Score: {self.player2.totalPoints:.2f}", True, (255, 255, 255))
            self.screen.blit(score_text, (200, 20))
            
        # Display FPS in the top-right corner with smaller font
        fps_text = self.fps_font.render(f"FPS: {self.clock.get_fps():.2f}", True, (255, 255, 255))
        fps_rect = fps_text.get_rect(topright=(self.screen.get_width() - 20, 20))  # Positioning to top-right
        self.screen.blit(fps_text, fps_rect)
     
        # Draw players
        self.player1.draw(self.screen,(255, 0, 0))

        if self.SecondPlayer:
            self.player2.draw(self.screen,(0, 0, 255))

        # Draw the platforms (as blue boxes)
        for platform in self.platforms:           
            pygame.draw.rect(self.screen, (0, 0, 255), platform)
    
    def move_platforms(self,platformsList):
        # Move each platform left by 5 pixels per frame
        for platform in platformsList:
            platform.x -= globals.platformVelocity # Move platform to the left 

    def draw_platforms(self):
        # Draw all platforms on the screen
            pygame.draw.rect(self.screen, (0, 255, 0), self.platform_rect)  # Green platforms

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
                           self.player1.calculate_score()
                    elif event.key == pygame.K_b and self.SecondPlayer:
                        if self.player2.player_on_object:                       
                           self.player2.update_gravity()
                           self.player2.player_on_object=False
                           self.player2.calculate_score()

           
            if not self.paused:  

                if self.start_flag == 0:
                # Handle player collision with platforms (player stops at platform)
                    if not self.player1.player_velocity == 0:
                        self.player1.handle_collisions(self.platforms,globals.platformVelocity)
                    if self.SecondPlayer:
                        if not self.player2.player_velocity == 0:
                            self.player2.handle_collisions(self.platforms,globals.platformVelocity)
                else:
                    self.start_flag = 0  

                if self.SecondPlayer:
                    if not  self.player2.player_on_object: 
                # Apply gravity to make the player move up or down
                        if self.player2.gravity_state == self.player2.gravity:  # Gravity pulling down
                           self.player2.player_velocity += self.player2.gravity  # Increase velocity by gravity value
                           if self.player2.player_velocity > globals.playerVelocity:  # Cap the velocity
                              self.player2.player_velocity = globals.playerVelocity - globals.gravity
                        elif self.player2.gravity_state == self.player2.gravity_reversed:  # Gravity pulling up
                             self.player2.player_velocity -= self.player2.gravity  # Decrease velocity by gravity value
                             if self.player2.player_velocity < - globals.playerVelocity:  # Cap the velocity (negative for reversed gravity)
                                self.player2.player_velocity = - globals.playerVelocity + globals.gravity
                    else:
                        self.player2.frames_on_platform -= 1

                        if self.player2.is_falling:
                            if self.player2.frames_on_platform <= 0:
                                self.player2.player_on_object = False
                                self.player2.player_velocity = globals.gravity  # Set velocity to falling (positive velocity)
                                #self.player2.calculate_score()
                                self.player2.frames_on_platform = 0  # Reset frames
                        else:
                            if self.player2.frames_on_platform <= 0:
                                self.player2.player_on_object = False
                                self.player2.player_velocity = -globals.gravity  # Set velocity to floating (negative velocity)
                                #self.player2.calculate_score()
                                self.player2.frames_on_platform = 0  # Reset frames 
                        
                    # Update the player's position based on velocity
                    if not self.player2.player_on_object:
                        self.player2.player_y += self.player2.player_velocity
           
                           

                if not  self.player1.player_on_object: 
                # Apply gravity to make the player move up or down
                    if self.player1.gravity_state == self.player1.gravity:  # Gravity pulling down
                        self.player1.player_velocity += self.player1.gravity  # Increase velocity by gravity value
                        if self.player1.player_velocity > globals.playerVelocity:  # Cap the velocity
                            self.player1.player_velocity = globals.playerVelocity - globals.gravity
                    elif self.player1.gravity_state == self.player1.gravity_reversed:  # Gravity pulling up
                        self.player1.player_velocity -= self.player1.gravity  # Decrease velocity by gravity value
                        if self.player1.player_velocity < - globals.playerVelocity:  # Cap the velocity (negative for reversed gravity)
                            self.player1.player_velocity = - globals.playerVelocity + globals.gravity
                else:
                    self.player1.frames_on_platform -=1

                    if self.player1.is_falling:
                        if self.player1.frames_on_platform <= 0:
                            self.player1.player_on_object = False
                            self.player1.player_velocity = globals.gravity  # Set velocity to falling (positive velocity)
                            #self.player1.calculate_score()
                            self.player1.frames_on_platform = 0  # Reset frames
                    else:
                        if self.player1.frames_on_platform <= 0:
                            self.player1.player_on_object = False
                            self.player1.player_velocity = - globals.gravity # Set velocity to floating (negative velocity)
                            #self.player1.calculate_score()
                            self.player1.frames_on_platform = 0  # Reset frames 
                        
                # Update the player's position based on velocity
                if not self.player1.player_on_object:
                    self.player1.player_y += self.player1.player_velocity

            # Update the movement of platforms
            self.move_platforms(self.platforms)

            # Optionally, remove platforms that go off-screen (on the left side)
            self.platforms = [platform for platform in self.platforms if platform.right > 0]

            if len(self.platforms) == 0 or self.platforms[-1].right <= self.screen.get_width():
                self.initplatform = platformCls(self.screen,self.platforms,globals.platform_width)
                self.platforms.append(self.initplatform.platform_rect)

            if self.SecondPlayer:
                if self.player2.player_y <=0 or self.player2.player_y >= 640:
                    self.player2.diseased =True
                if self.player1.player_y <=0 or self.player1.player_y >= 640:
                    self.player1.diseased =True

                if self.player1.diseased and self.player2.diseased:
                    self.running = False
                    return {"player1_score": self.player1.totalPoints, 
                            "player2_score": self.player2.totalPoints}
            else:
                if self.player1.player_y <=0 or self.player1.player_y >= 640:
                    self.player1.diseased =True
                if self.player1.diseased:
                    self.running = False
                    return {"player1_score": self.player1.totalPoints}

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
        self.draw_text('RED changes gravity with "R"', self.screen.get_height() // 2 - 50)
        if self.SecondPlayer:
            self.draw_text('BLUE changes gravity with "B"', self.screen.get_height() // 2)
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