import pygame
import globals  # Import your global variables and functions

class playerCls:
    def __init__(self,screen,numofplayers):
        self.screen = screen
        self.player_size = 30

        if numofplayers == 2:
            self.player_x = (self.screen.get_width() * 2 // 6 ) -80 # Starting X position (2/5th of the width)
            self.player_y = self.screen.get_height() // 2  # Start in the middle of the screen vertically
            self.player_images = [
            pygame.image.load('assets/characters/blue/BB1.png'),
            pygame.image.load('assets/characters/blue/BB2.png'),
            pygame.image.load('assets/characters/blue/BB3.png'),
            pygame.image.load('assets/characters/blue/BB4.png'),
            pygame.image.load('assets/characters/blue/BB5.png'),
            pygame.image.load('assets/characters/blue/BB6.png'),
            pygame.image.load('assets/characters/blue/BB7.png'),
            ]
            self.player_images_rev = [
            pygame.image.load('assets/characters/blue/RevB1.png'),
            pygame.image.load('assets/characters/blue/RevB2.png'),
            pygame.image.load('assets/characters/blue/RevB3.png'),
            pygame.image.load('assets/characters/blue/RevB4.png'),
            pygame.image.load('assets/characters/blue/RevB5.png'),
            pygame.image.load('assets/characters/blue/RevB6.png'),
            pygame.image.load('assets/characters/blue/RevB7.png'),
        ]
         
        else:
            self.player_x = self.screen.get_width() * 2 // 6  # Starting X position (2/5th of the width)
            self.player_y = self.screen.get_height() // 2  # Start in the middle of the screen vertically
            self.player_images = [
            pygame.image.load('assets/characters/red/RR1.png'),
            pygame.image.load('assets/characters/red/RR2.png'),
            pygame.image.load('assets/characters/red/RR3.png'),
            pygame.image.load('assets/characters/red/RR4.png'),
            pygame.image.load('assets/characters/red/RR5.png'),
            pygame.image.load('assets/characters/red/RR6.png'),
            pygame.image.load('assets/characters/red/RR7.png'),
            ]
            self.player_images_rev = [
            pygame.image.load('assets/characters/red/RevR1.png'),
            pygame.image.load('assets/characters/red/RevR2.png'),
            pygame.image.load('assets/characters/red/RevR3.png'),
            pygame.image.load('assets/characters/red/RevR4.png'),
            pygame.image.load('assets/characters/red/RevR5.png'),
            pygame.image.load('assets/characters/red/RevR6.png'),
            pygame.image.load('assets/characters/red/RevR7.png'),
        ]

        self.player_velocity = 0  # Starting velocity (no initial speed)
        self.frame_counter = 0  # Frame counter to track frames passed
        self.current_frame = 0  # Start with the first frame
        self.gravity = globals.gravity # Gravity pulling downwards
        self.gravity_reversed = - globals.gravity  # Gravity pulling upwards
        self.gravity_state = self.gravity  # Default gravity is pulling downwards
        self.player_on_object= False # check if player is on object so he can jump
        self.is_falling = True  # Is the player falling?
        self.frames_on_platform = 0 #time left on platform so it can calculate the score
        self.total_frames = 0 # we need total and left on platform to calculate the score
        self.totalPoints = 0 #points gather till he finish the game
        self.diseased = False
        self.playerUporDown = 0 #1 is for up images 0 is down images

    def update_movement(self):
        #Update the player's animation frame."""
        self.frame_counter += 1  # Increment the frame counter
            
        if self.frame_counter >= 2:  # Every 2 frames
            self.current_frame = (self.current_frame + 1) % len(self.player_images)
            self.frame_counter = 0  # Reset the frame counter

    def draw(self, screen, color):
        """Draw the player on the screen."""
        self.screen = screen
        player_image = self.player_images[self.current_frame]
        player_image_rev = self.player_images_rev[self.current_frame]

        if self.playerUporDown == 0:
            self.screen.blit(player_image, (self.player_x, self.player_y))
        else:
            self.screen.blit(player_image_rev, (self.player_x, self.player_y))
        #pygame.draw.rect(screen, color, (self.player_x, self.player_y, self.player_size, self.player_size))


    def handle_collisions(self,platforms,platform_speed):
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)

        if self.player_velocity > 0:  # Falling
            for platform in platforms:
                platform_rect = platform
                if player_rect.bottom  <= platform_rect.top + 15:
                    if player_rect.bottom + 15 >= platform_rect.top:        #300
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
                            frames_to_fall = remaining_space / platform_speed   # 50 pixels / 5 pixels per frame = 10 frames
                
                            # Store this value, so you can use it later to detect when to change velocity to falling
                            self.total_frames = frames_to_fall
                            self.frames_on_platform = frames_to_fall + globals.framesextraplat 
                            self.is_falling=True
                            self.playerUporDown = 0
                            return  # Exit once collision is handled
                
        elif self.player_velocity < 0:  # Moving upwards
            for platform in platforms:
                platform_rect = platform
                if player_rect.top >= platform_rect.bottom - 15:
                    if player_rect.top - 15 <= platform_rect.bottom:
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
                            frames_to_fall = remaining_space / platform_speed  # 50 pixels / 5 pixels per frame = 10 frames
                
                            # Store this value, so you can use it later to detect when to change velocity to falling
                            self.frames_on_platform = frames_to_fall + globals.framesextraplat
                            self.is_falling=False
                            self.playerUporDown = 1
                            return  # Exit once collision is handled

    def update_gravity(self):
    #Handles gravity change only when jump is pressed.
        if self.gravity_state == self.gravity:
            self.gravity_state = self.gravity_reversed
        else:
            self.gravity_state = self.gravity

    def calculate_score(self):
      #calculate the score he gather based on how long player stayed on platform
        if self.frames_on_platform < 10:
            self.totalPoints = self.totalPoints + self.total_frames
        else:
            self.totalPoints = self.totalPoints + self.total_frames - self.frames_on_platform
     