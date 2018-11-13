import random
from files import Files


class Directories:
    def __init__(self, directories):
        self.files = []
        for index, directory in directories.items():
            self.files.append((int(index), Files(directory=directory)))

    def random_directory(self):
        if len(self.files) == 0:
            return None, None
        return self.files[random.randrange(len(self.files))]

    def sequential_directory(self):
        if len(self.files) == 0:
            return None, None
        return self.files[0]

    def remove_directory(self, index):
        for i in range(len(self.files)):
            if self.files[i][0] == index:
                del self.files[i]
                break
