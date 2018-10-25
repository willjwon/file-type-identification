import os


class Fragment:
    def __init__(self, directory, fragment_size):
        self.file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory)
                           if ((not filename.startswith(".")) and os.path.isfile(os.path.join(directory, filename)))]
        self.file_index = 0
        self.file = open(self.file_paths[self.file_index], "rb")
        self.fragment_size = fragment_size

    def open_next_file(self):
        self.file.close()

        self.file_index += 1
        if self.file_index >= len(self.file_paths):
            self.file_index = 0
            self.file = open(self.file_paths[self.file_index], "rb")
            return False
        else:
            self.file = open(self.file_paths[self.file_index], "rb")
            return True

    def get_fragment(self):
        data = self.file.read(self.fragment_size)
        while len(data) < self.fragment_size:
            open_success = self.open_next_file()
            if not open_success:
                return None
            else:
                data = self.file.read(self.fragment_size)
        return data
