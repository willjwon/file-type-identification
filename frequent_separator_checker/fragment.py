import os


class Fragment:
    def __init__(self, file_types, directories, fragment_size):
        self.file_paths = dict()
        self.file_indices = dict()
        self.files = dict()
        self.fragment_size = fragment_size
        self.file_types = file_types
        self.file_type_index = 0
        for file_type, directory in zip(file_types, directories):
            self.file_paths[file_type] = \
                [os.path.join(directory, filename) for filename in os.listdir(directory)
                 if ((not filename.startswith(".")) and os.path.isfile(os.path.join(directory, filename)))]
            self.file_indices[file_type] = 0
            self.files[file_type] = open(self.file_paths[file_type][self.file_indices[file_type]], "rb")

    def open_next_file(self):
        file_type = self.file_types[self.file_type_index]

        self.files[file_type].close()

        self.file_indices[file_type] += 1
        if self.file_indices[file_type] >= len(self.file_paths[file_type]):
            self.file_indices[file_type] = 0
            self.files[file_type] = open(self.file_paths[file_type][self.file_indices[file_type]], "rb")

            # open next file type
            self.file_type_index += 1
            if self.file_type_index >= len(self.file_types):
                # whole dataset is read.
                self.file_type_index = 0
                return False, False

            return False, True
        else:
            self.files[file_type] = open(self.file_paths[file_type][self.file_indices[file_type]], "rb")
            return True, True

    def get_fragment(self):
        file_type = self.file_types[self.file_type_index]

        data = self.files[file_type].read(self.fragment_size)
        while len(data) < self.fragment_size:
            open_success = self.open_next_file()
            if not open_success[0]:
                if not open_success[1]:
                    return None
                file_type = self.file_types[self.file_type_index]
                data = self.files[file_type].read(self.fragment_size)
            else:
                data = self.files[file_type].read(self.fragment_size)

        return data, file_type
