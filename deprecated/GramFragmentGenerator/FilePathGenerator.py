import os
import unittest


def file_path_generator(directory_path):
    if not directory_path.endswith("/"):
        directory_path += "/"

    while True:
        rewound = True
        for file_name in os.listdir(directory_path):
            if not file_name.startswith("."):
                yield (rewound, directory_path + file_name)
                rewound = False


class FilePathGeneratorTest(unittest.TestCase):
    def test_file_path_generator(self):
        file_path = file_path_generator("./")
        for _ in range(30):
            print(next(file_path))

