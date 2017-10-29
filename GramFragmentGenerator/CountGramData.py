import unittest
import pickle
import os


def generate_one_hot_group_csv_string(group_index, num_groups):
    gram_string_list = ["0"] * num_groups
    gram_string_list[group_index] = "1"
    return ','.join(gram_string_list)


class CountGramData:
    frequent_separators = None

    @classmethod
    def load_frequent_separators(cls):
        if not os.path.exists("./frequent_separators.pickle"):
            print("ERROR: './frequent_separators.pickle' not found.")
            print("Please place './frequent_separators.pickle' properly and try again.")
            exit(-1)
        with open("frequent_separators.pickle", "rb") as file:
            cls.frequent_separators = pickle.load(file)

        # get gram information
        grams = list(sorted(cls.frequent_separators.keys()))
        cls.min_gram = grams[0]
        cls.max_gram = grams[-1]

    @classmethod
    def count_gram_data_and_get_result_csv_string(cls, data):
        count_result = []

        # count 1 ~ 5 gram.
        for gram in range(cls.min_gram, cls.max_gram + 1):
            partial_count_result = [0] * len(cls.frequent_separators[gram])
            for index in range(len(data) - gram + 1):
                gram_value = int.from_bytes(data[index:(index + gram)], byteorder="big")
                if gram_value in cls.frequent_separators[gram]:
                    partial_count_result[cls.frequent_separators[gram][gram_value]] += 1
            count_result += partial_count_result

        # compute the gram string and return.
        return ','.join(str(i) for i in count_result)


class CountGramDataTest(unittest.TestCase):
    def test_generate_one_hot_group_csv_string(self):
        self.assertEqual(generate_one_hot_group_csv_string(1, 3), "0,1,0")
