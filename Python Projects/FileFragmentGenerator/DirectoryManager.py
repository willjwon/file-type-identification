import os
import unittest


class DirectoryManager:
    def __init__(self, input_directory_path, output_directory_path):
        self.input_directory_path = input_directory_path
        self.output_directory_path = output_directory_path

    def change_input_directory_path(self, new_input_directory_path):
        self.input_directory_path = new_input_directory_path

    def change_output_directory_path(self, new_output_directory_path):
        self.output_directory_path = new_output_directory_path

    def file_list(self):
        if os.path.exists(self.input_directory_path):
            return os.listdir(self.input_directory_path)
        else:
            print("Path '{}' doesn't exist! --- it is therefore skipped.\n".format(self.input_directory_path))
            return []

    def get_input_path(self, filename):
        if self.input_directory_path.endswith("/"):
            return self.input_directory_path + filename
        else:
            return self.input_directory_path + "/" + filename

    def get_output_path(self, filename):
        if self.output_directory_path.endswith("/"):
            return self.output_directory_path + filename
        else:
            return self.output_directory_path + "/" + filename

    def write_into_file(self, filename, data):
        if not os.path.exists(self.output_directory_path):
            os.makedirs(self.output_directory_path)
        with open(self.get_output_path(filename), "wb") as file:
            file.write(data)


class DirectoryManagerTest(unittest.TestCase):
    def setUp(self):
        self.directoryManager = DirectoryManager("./", "./output_test")

    def test_change_input_directory_path(self):
        self.directoryManager.change_input_directory_path("changed_input_dir")
        print(self.directoryManager.input_directory_path)

    def test_change_output_directory_path(self):
        self.directoryManager.change_output_directory_path("changed_output_dir")
        print(self.directoryManager.output_directory_path)

    def test_fileList(self):
        print(self.directoryManager.file_list())

    def test_get_output_path(self):
        self.assertEqual(self.directoryManager.get_output_path("hello"), "./output_test/hello")

    def test_write_into_file(self):
        self.directoryManager.write_into_file("output_test", "abcdef".encode())
        print("Writing complete!")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
