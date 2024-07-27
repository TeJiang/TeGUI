import os
import json

DEFAULT_SETTINGS = {
    "layout": "default",
    "theme": "light",
    "x_axes_variable": "wavelength",
    # Add any other default settings here...
}


class Settings:
    def __init__(self):
        # Check if the preferences.json file exists, if not, use the default values
        if os.path.exists("preferences.json"):
            with open("preferences.json", "r") as f:
                self.preferences = json.load(f)
        else:
            self.preferences = DEFAULT_SETTINGS
            self.save_preferences()

    def get_preference(self, key):
        return self.preferences.get(key)

    def set_preference(self, key, value):
        self.preferences[key] = value
        self.save_preferences()

    def save_preferences(self):
        with open("preferences.json", "w") as f:
            json.dump(self.preferences, f)


# Usage:
settings = Settings()
theme = settings.get_preference("theme")  # Read a setting
settings.set_preference("theme", "dark")  # Change a setting