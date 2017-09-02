import os
import unittest


class FragmentManager:
    def __init__(self):
        self.fragment_path = None
        self.bit_frequency_data = None
        self.fragment_length = None
        self.gram = None

    def set_fragment(self, fragment_path, gram):
        self.fragment_path = fragment_path
        self.bit_frequency_data = dict()
        self.fragment_length = os.path.getsize(fragment_path)
        self.gram = gram

    def compute_bit_frequency_data(self, output_csv_file, file_type_number):
        location = 0
        with open(self.fragment_path, "rb") as file:
            while True:
                file.seek(location)
                read_byte = file.read(self.gram)  # read byte number of grams
                if not read_byte:
                    break
                read_byte_in_int = int.from_bytes(read_byte, byteorder="big")
                if read_byte_in_int in self.bit_frequency_data:
                    self.bit_frequency_data[read_byte_in_int] += 1
                else:
                    self.bit_frequency_data[read_byte_in_int] = 1
                location += 1
                if location > self.fragment_length - self.gram:
                    break

        with open(output_csv_file, "a") as file:
            for gram in range(2 ** (8 * self.gram)):
                if gram in self.bit_frequency_data:
                    file.write(str(self.bit_frequency_data[gram]))
                else:
                    file.write("0")
                file.write(",")

            file.write("{}\n".format(file_type_number))


class FragmentManagerTest(unittest.TestCase):
    def setUp(self):
        self.fragment_manager = FragmentManager()
        self.fragment_manager.set_fragment("./test/test", 2)

    def test_compute_bit_frequency_data(self):
        # print(self.fragment_manager.compute_bit_frequency_data())
        pass
