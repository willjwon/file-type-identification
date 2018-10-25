import os
import json
import unittest


class Settings:
    def __init__(self, directory, filename):
        settings_file_path = os.path.join(directory, filename)
        with open(settings_file_path, "r") as file:
            self.settings = json.load(file)

    def read(self, *args):
        settings_read = self.settings
        try:
            for arg in args:
                settings_read = settings_read[arg]
        except KeyError:
            return None
        except TypeError:
            return None
        return settings_read


class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings(directory="../", filename="settings.json")

    def test_print_argumetn(self):
        print(self.settings.read("fragment", "size"))