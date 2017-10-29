import unittest
import pickle
import settings


def generate_one_hot_group_csv_string(group_index, num_groups):
    gram_string_list = ["0"] * num_groups
    gram_string_list[group_index] = "1"
    return ','.join(gram_string_list)


class CountGramData:
    frequent_separators = None

    @classmethod
    def load_frequent_separators(cls):
        with open("frequent_separators.pickle", "rb") as file:
            cls.frequent_separators = pickle.load(file)

    @classmethod
    def count_gram_data_and_get_result_csv_string(cls, data):
        count_result = []

        # count 2 ~ 5 gram.
        for gram in range(settings.max_grams):
            partial_count_result = [0] * len(cls.frequent_separators[gram])
            for index in range(len(data) - gram + 1):
                # Computes 1 gram when gram = 0, therefore should use gram + 1 for actual gram size
                gram_value = int.from_bytes(data[index:(index + (gram + 1))], byteorder="big")
                if gram_value in cls.frequent_separators[gram]:
                    partial_count_result[cls.frequent_separators[gram][gram_value]] += 1
            count_result += partial_count_result

        # compute the gram string and return.
        return ','.join(str(i) for i in count_result)


class CountGramDataTest(unittest.TestCase):
    def test_generate_one_hot_group_csv_string(self):
        self.assertEqual(generate_one_hot_group_csv_string(1, 3), "0,1,0")
