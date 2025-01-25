# Global Variables

# Difficulty settings (default to False)
difficulty = "Mars(M)"  # Can be "Easy", "Medium", or "Hard"

def set_difficulty(level):
    #Set the difficulty level based on user input.
    #Mars is Easy
    #Earth is Medium
    #Jupiter is Hard

    global difficulty
    difficulty = level
    print(f"Difficulty set to {difficulty}")

