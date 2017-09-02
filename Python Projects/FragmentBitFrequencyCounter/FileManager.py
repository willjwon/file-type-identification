import os
import unittest


class FileManager:
    def __init__(self, input_directory_path):
        self.input_directory_path = input_directory_path
        # MARK: Deprecated
        # self.output_directory_path = output_directory_path

    def fragment_list(self):
        if os.path.exists(self.input_directory_path):
            return os.listdir(self.input_directory_path)
        else:
            print("Directory '{}' doesn't exist!\n".format(self.input_directory_path))
            return []

    def fragment_path(self, filename):
        if self.input_directory_path.endswith("/"):
            return self.input_directory_path + filename
        else:
            return self.input_directory_path + "/" + filename

    # MARK: deprecated
    # def output_path(self, filename):
    #     if not os.path.exists(self.output_directory_path):
    #         os.makedirs(self.output_directory_path)
    #     if self.output_directory_path.endswith("/"):
    #         return self.output_directory_path  + filename + ".csv"
    #     else:
    #         return self.output_directory_path + "/" + filename + ".csv"


class FileManagerTest(unittest.TestCase):
    def setUp(self):
        self.file_manager = FileManager("./")

    def test_fragment_list(self):
        print(self.file_manager.fragment_list())

    def test_fragment_path(self):
        self.assertEqual(self.file_manager.fragment_path("test"), "./test")


def main():
    unittest.main()


if __name__ == "__main__":
    main()
