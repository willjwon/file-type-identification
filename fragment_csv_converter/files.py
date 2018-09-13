from print_progress import print_progress
import os
import unittest


class Files:
    def __init__(self, directory="./"):
        file_names = list(filter(lambda name: ("." in name) and (not name.startswith(".")), os.listdir(directory)))
        self.files = list(map(lambda file_name: os.path.join(directory, file_name), file_names))
        self.num_files = len(self.files)

        if self.num_files == 0:
            print("No file in given directory: {}".format(directory))
            exit(-1)

        self.index = 0
        self.opened_file = open(self.files[self.index], "rb")

    def __del__(self):
        if self.opened_file is not None:
            self.opened_file.close()

    def set_next_file(self):
        print_progress(self.index + 1, self.num_files)
        # All files read
        if self.index >= self.num_files - 1:
            self.opened_file.close()
            self.opened_file = None
            return

        self.opened_file.close()
        self.index += 1
        self.opened_file = open(self.files[self.index], "rb")

    def read_fragment(self, size):
        fragment = self.opened_file.read(size)

        while len(fragment) < size:
            self.set_next_file()
            if self.opened_file is None:
                return None

            fragment = self.opened_file.read(size)

        return fragment

    def reset(self):
        self.index = 0
        self.opened_file = open(self.files[self.index], "rb")


class FilesUnitTest(unittest.TestCase):
    def setUp(self):
        self.files = Files()

    def test_read(self):
        size = 4096
        fragment = self.files.read_fragment(size)
        while fragment is not None:
            print(fragment)
            fragment = self.files.read_fragment(size)

        self.files.reset()
        print(self.files.read_fragment(size))
