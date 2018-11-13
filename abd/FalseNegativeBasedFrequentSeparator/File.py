from FilePathGenerator import file_path_generator


class File:
    def __init__(self, directory_path):
        self.path_generator = file_path_generator(directory_path)
        _, path = next(self.path_generator)
        self.file = open(path, "rb")
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.file.seek(0)

    def set_to_next_file(self):
        rewound_occurred, next_path = next(self.path_generator)
        self.file.close()
        self.file = open(next_path, "rb")
        self.file.seek(0, 2)
        self.file_size = self.file.tell()
        self.file.seek(0)
        if rewound_occurred:
            return False
        return True

    def read(self, read_size):
        while self.file_size < read_size:
            success = self.set_to_next_file()
            if not success:
                return None

        self.file_size -= read_size
        return self.file.read(read_size)
