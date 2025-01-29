# Global Variables
import pygame
import random


# Difficulty settings (default to False)
difficulty = "Mars(A)"  # Can be "Easy", "Medium", or "Hard"
music_muted = False # Global variable to track whether the music is muted or not
multiplayer = 1 # Global variable to track multiplayer mode
gravity = 0.3 # Global gravity based on difficulty
playerVelocity = 8 #Global max speed based on difficulty
platformVelocity = 5 #Global max speed based on difficulty
platform_width = random.randint(150,300) # Global platofrom width based on diff
upordownobject = "down"
framesextraplat = 5
diffistats = "Mars"


def playersmode(multi):
    global multiplayer
    multiplayer = multi
    print(f"Difficulty set to {multiplayer}")

def upordown(obj):
    global upordownobject 
    upordownobject = obj

def set_difficulty(level):
    #Set the difficulty level based on user input.
    #Mars(A) is Easy
    #Earth(E) is Medium
    #Jupiter(J) is Hard

    global difficulty
    global gravity  
    global playerVelocity 
    global platformVelocity 
    global platform_width
    global framesextraplat
    global diffistats

    difficulty = level

    if difficulty == "Mars(A)":
        gravity = 0.3 
        playerVelocity = 8 
        platformVelocity = 5 
        platform_width = random.randint(200,300)
        framesextraplat = 5 
        diffistats = "Mars"
    elif difficulty == "Earth(E)":
        gravity = 0.3 * 1.2
        playerVelocity = 8 * 1.2 
        platformVelocity = 5 * 1.2 
        platform_width = random.randint(150,300)
        framesextraplat = 5 * 1.2
        diffistats = "Earth"
    elif difficulty == "Jupiter(J)":
        gravity = 0.3 * 1.8
        playerVelocity = 8 * 1.8
        platformVelocity = 5  * 1.8
        platform_width = random.randint(150,250)
        framesextraplat = 5 
        diffistats = "Jupiter"
    else:
        gravity = 0.3 
        playerVelocity = 8 
        platformVelocity = 5 
        platform_width = random.randint(200,300)

    print(f"Difficulty set to {difficulty}")


def toggle_music():
    # Function to toggle music (mute/unmute)
    global music_muted
    if music_muted:
        pygame.mixer.music.unpause()  # Unpause the music
        music_muted = False       
    else:
        pygame.mixer.music.pause()  # Pause the music
        music_muted = True


def draw_mute_icon(screen, is_muted):
    if music_muted:
        mute_icon = pygame.image.load('assets/images/mute.png')  # Muted icon
    else:
        mute_icon = pygame.image.load('assets/images/audio.png')  # Unmuted icon

    # Resize the icon to 20x20
    mute_icon = pygame.transform.scale(mute_icon, (20, 20))  # Resize the icon to 20x20 pixels

    # Position the icon (bottom-right corner of the screen, adjust as needed)
    icon_x = screen.get_width() - mute_icon.get_width() - 30  # 30px padding from right (more space for text)
    icon_y = screen.get_height() - mute_icon.get_height() - 10  # 30px padding from bottom

    screen.blit(mute_icon, (icon_x, icon_y))

    # Draw the text 'M' next to the icon
    text_font = pygame.font.SysFont("Arial", 24)  # You can adjust the font size as needed
    mute_text = text_font.render("M", True, (255, 255, 255))  # White color text
    screen.blit(mute_text, (icon_x + mute_icon.get_width() + 5, icon_y))  # Position text next to the icon
