# Global Variables
import pygame


# Difficulty settings (default to False)
difficulty = "Mars(A)"  # Can be "Easy", "Medium", or "Hard"
music_muted = False # Global variable to track whether the music is muted or not
multiplayer = 1 # Global variable to track multiplayer mode



def playersmode(multi):
    global multiplayer
    multiplayer = multi
    print(f"Difficulty set to {multiplayer}")


def set_difficulty(level):
    #Set the difficulty level based on user input.
    #Mars is Easy
    #Earth is Medium
    #Jupiter is Hard

    global difficulty
    difficulty = level
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
