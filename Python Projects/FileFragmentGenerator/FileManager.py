import os
import random
import unittest


class FileManager:
    def __init__(self):
        self.file_path = None
        self.file_length = None
        self.fragment_length = None
        self.used_fragment_position = None

    def set_file(self, file_path, fragment_length):
        self.file_path = file_path
        self.file_length = os.path.getsize(file_path)
        self.fragment_length = fragment_length
        self.used_fragment_position = set()

    def random_location(self):
        while True:
            random_number = random.randint(0, self.file_length - self.fragment_length)  # both side inclusive
            if random_number not in self.used_fragment_position:
                break
        self.used_fragment_position.add(random_number)
        return random_number

    def sequential_fragment(self):
        with open(self.file_path, "rb") as file:
            for _ in range(int(self.file_length / self.fragment_length)):
                yield file.read(self.fragment_length)

    def random_fragment(self, count):
        # Check the file can create `count` number of fragments without fragment duplication.
        if count > self.file_length - self.fragment_length + 1:
            print("Random file fragment of file '{}' cannot generate '{}' fragments.".format(self.file_path,
                                                                                             count))
            count = self.file_length - self.fragment_length + 1
            print("Maximum available fragment size '{}' is used.".format(count))

        with open(self.file_path, "rb") as file:
            for _ in range(count):
                location = self.random_location()
                file.seek(location)
                yield file.read(self.fragment_length)


class FileManagerTest(unittest.TestCase):
    def setUp(self):
        self.fileManager = FileManager()
        self.fileManager.set_file("./output_test/output_test", 3)

    def test_set_file(self):
        print("path:", self.fileManager.file_path)
        print("length:", self.fileManager.file_length)

    def test_sequential_fragment(self):
        for fragment in self.fileManager.sequential_fragment():
            print("sequential:", fragment)

    def test_random_fragment(self):
        for fragment in self.fileManager.random_fragment(7):
            print("random:", fragment)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
