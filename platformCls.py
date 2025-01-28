import pygame

class platformCls:
    def __init__(self,screen,numofplayers):
        self.screen = screen
        self.player_size = 30

        if numofplayers == 2:
            self.player_x = (self.screen.get_width() * 2 // 6 ) -40 # Starting X position (2/5th of the width)
            self.player_y = self.screen.get_height() // 2  # Start in the middle of the screen vertically
        else:
            self.player_x = self.screen.get_width() * 2 // 6  # Starting X position (2/5th of the width)
            self.player_y = self.screen.get_height() // 2  # Start in the middle of the screen vertically
            
        self.player_velocity = 0  # Starting velocity (no initial speed)
        self.gravity = 0.3  # Gravity pulling downwards
        self.gravity_reversed = -0.3  # Gravity pulling upwards
        self.gravity_state = self.gravity  # Default gravity is pulling downwards
        self.player_on_object= False # check if player is on object so he can jump
        self.is_falling = True  # Is the player falling?
        self.frames_on_platform = 0 #time left on platform so it can calculate the score