import pygame
import math
import random
import globals  # Import your global variables and functions

class platformCls:
    def __init__(self,screen,platformsList,Gplatform_width,firstplatform=False):
            
        self.screen = screen
        platform_height = 20
        platform_width = Gplatform_width
    
        if firstplatform:

            platform_width = 1024  # first platform for players to start          
            platform_x = self.screen.get_width()-1024  # Start at the right side of the screen
            platform_y = 620
            globals.upordown("up")
        else:
            last_platform = platformsList[-1]  # Get the most recently created platform
            last_platform_end_x = last_platform.x + last_platform.width
            last_platform_y = last_platform.y

            platform_x = last_platform_end_x + platform_width

            # Calculate vertical difference (Δy) to determine the fall distance
            if globals.upordownobject == "down": 
                platform_y = random.randint(350, 600)  # Random vertical position for platforms
                globals.upordown("up")
            elif globals.upordownobject == "up" :
               platform_y = random.randint(40, 290)  
               globals.upordown("down")
            else:
               platform_y = random.randint(20, 600)  

            delta_y = last_platform_y - platform_y

            # Ensure there’s enough distance vertically (for jump/fall mechanics)
            if abs(delta_y) < 100:
                platform_y = last_platform_y - 100 if delta_y > 0 else last_platform_y + 100

            # Use gravity to calculate the fall time (t)
            gravity = globals.gravity  # Gravity per frame

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


            # Calculate the maximum horizontal distance the player can cover in fall_time
            player_velocity = globals.playerVelocity  # Max player horizontal velocity
            platform_velocity = globals.platformVelocity  # Platforms move left speed
            relative_velocity = player_velocity - platform_velocity  # Net horizontal velocity

            # Calculate the max horizontal distance based on the jump or fall time
            max_horizontal_distance = relative_velocity * max(fall_time, jump_time)  # Pixels the player can cover horizontally

            # Calculate where the next platform should be placed
            platform_x = last_platform_end_x + max_horizontal_distance +40  # Add the max horizontal distance 
       
        # Create a pygame Rect object for the platform
        self.platform_rect = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
        

    def should_create_platform(self, platformsList,platform_width):
        #Determines whether a new platform should be created based on the last platform's position.
        last_platform = platformsList[-1]  # Get the most recently created platform
        last_platform_end_x = last_platform.x + last_platform.width

        platform_x = last_platform_end_x + platform_width
        # If platform_x exceeds the screen width (1024), return False
        if platform_x > 1024:
            return False
        else:
            return True
        
   