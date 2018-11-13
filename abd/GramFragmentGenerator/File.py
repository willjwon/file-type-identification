import unittest
import settings
from FilePathGenerator import file_path_generator


class File:
    def __init__(self, file_type, directory_path, fragment_size):
        self.path_generator = file_path_generator(directory_path)
        _, path = next(self.path_generator)
        self.file = open(path, "rb")
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.file.seek(0)
        self.offset = [-1, 2]
        self.fragment_size = fragment_size
        self.file_type = file_type

    def set_to_next_offset(self):
        if self.offset[1] - self.offset[0] <= 1:
            self.offset[0] = 1
            self.offset[1] *= 2
        else:
            self.offset[0] += 2
        print("Files of type {} exhausted! Rewound with offset {:>0.2}."
              .format(self.file_type, (self.offset[0] / self.offset[1])))

    def set_to_next_file(self):
        rewound_occurred, next_path = next(self.path_generator)
        self.file.close()
        self.file = open(next_path, "rb")
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.file.seek(0)
        if rewound_occurred:
            self.set_to_next_offset()
            offset = int(self.fragment_size * self.offset[0] / self.offset[1])
            self.file.seek(offset)
            self.file_size -= offset

    def read(self, read_size):
        while self.file_size < read_size:
            self.set_to_next_file()

        self.file_size -= read_size
        return self.file.read(read_size)


class FileTest(unittest.TestCase):
    def test_read(self):
        file_type = "mp3"
        file = File(file_type, settings.train_directory_path[file_type], settings.fragment_size_in_bytes)
        for _ in range(1000):
            # print(file.read(4096))
            file.read(4096)

