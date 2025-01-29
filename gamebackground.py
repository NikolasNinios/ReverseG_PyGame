import pygame

class Background:
    def __init__(self, screen, image_path, speed):
        self.screen = screen
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (screen.get_width(), screen.get_height()))
        self.bg_width, self.bg_height = self.image.get_width(), self.image.get_height()
        self.x = 0  # Starting position
        self.y = 0
        self.speed = speed  # Speed at which the background moves
    
    def update(self):
        # Move the background
        self.x -= self.speed
        if self.x <= -self.bg_width:
            self.x = 0  # Reset the position to create a seamless loop
    
    def draw(self):
        # Draw the background twice to cover the entire screen width
        self.screen.blit(self.image, (self.x, self.y))
        self.screen.blit(self.image, (self.x + self.bg_width, self.y))