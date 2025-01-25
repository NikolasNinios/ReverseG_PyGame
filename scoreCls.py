import os
import json

class scoreCls:
    def __init__(self, file_path="data/scores.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the JSON file and its directory exist."""
        if not os.path.exists(os.path.dirname(self.file_path)):
            os.makedirs(os.path.dirname(self.file_path))  # Create directory if it doesn't exist

        if not os.path.isfile(self.file_path):
            with open(self.file_path, "w") as file:
                json.dump([], file)  # Create an empty JSON array
            print(f"Created a new JSON file at {self.file_path}")

    def save_score(self, player_name, score, time_survived):
        """Save a player's score to the JSON file."""
        data = self.load_scores()  # Load existing data
        data.append({"name": player_name, "score": score, "time_survived": time_survived})

        # Save updated data back to the JSON file
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Saved {player_name}'s score to {self.file_path}")

    def load_scores(self):
        """Load all scores from the JSON file."""
        if os.path.getsize(self.file_path) == 0:  # Check if the file is empty
            return []  # Return an empty list if the file is empty
        with open(self.file_path, "r") as file:
            return json.load(file)

    def get_top_scores(self, top_n=5):
        """Retrieve the top N scores."""
        data = self.load_scores()
        sorted_scores = sorted(data, key=lambda x: x['score'], reverse=True)  # Sort by score descending
        return sorted_scores[:top_n]

    def reset_scores(self):
        """Reset the JSON file to an empty state."""
        with open(self.file_path, "w") as file:
            json.dump([], file)
        print(f"All scores have been reset in {self.file_path}")