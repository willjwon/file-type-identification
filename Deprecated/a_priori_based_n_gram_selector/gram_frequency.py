from files import *
from gram_filter import *
import unittest


class GramFrequency:
    def __init__(self, gram_size, candidate):
        self.gram_size = gram_size
        self.frequency = candidate

    def count_fragment(self, fragment, fragment_size):
        for i in range(fragment_size - self.gram_size + 1):
            gram = fragment[i:i + self.gram_size]

            if gram in self.frequency.keys():
                self.frequency[gram] += 1

    def get_frequent_gram_by_frequency(self, threshold):
        self.frequency = {k: v for (k, v) in self.frequency.items() if v >= threshold}

    def get_frequent_gram_by_max_ratio(self, threshold):
        total_frequency = max(self.frequency.values())
        self.frequency = {k: v for (k, v) in self.frequency.items() if (v / total_frequency) >= threshold}

    def generate_next_candidate(self):
        frequent_grams = self.frequency.keys()
        next_candidate = dict()
        for forward_gram in frequent_grams:
            backward_gram_prefix = forward_gram[1:self.gram_size]

            for suffix in range(0, 256):
                backward_gram = backward_gram_prefix + bytes([suffix])
                if backward_gram in frequent_grams:
                    next_candidate[forward_gram + bytes([suffix])] = 0

        return next_candidate


class GramFrequencyTest(unittest.TestCase):
    def setUp(self):
        self.files = Files("/Users/barber/tests")

        one_gram_candidate = dict()
        for suffix in range(0, 256):
            one_gram_candidate[bytes([suffix])] = 0

        self.gram_frequency = GramFrequency(1, one_gram_candidate)
        self.gram_filter = GramFilter()

    def test_count_one_gram(self):
        size = 4096

        fragment = self.files.read_fragment(size)
        while fragment is not None:
            self.gram_frequency.count_fragment(fragment, size)
            fragment = self.files.read_fragment(size)
        self.files.reset()

        next_candidate = self.gram_frequency.generate_next_candidate()

        two_gram_frequency = GramFrequency(2, next_candidate)
        fragment = self.files.read_fragment(size)
        while fragment is not None:
            two_gram_frequency.count_fragment(fragment, size)
            fragment = self.files.read_fragment(size)
        self.files.reset()

        print("Two Gram: {}".format(two_gram_frequency.frequency))
        two_gram_frequency.get_frequent_gram_by_max_ratio(0.1)
        print("Two_Gram: {}".format(len(two_gram_frequency.frequency)))
        print("Selected: {}".format(two_gram_frequency.frequency))

        next_candidate = two_gram_frequency.generate_next_candidate()

        three_gram_frequency = GramFrequency(3, next_candidate)
        fragment = self.files.read_fragment(size)
        while fragment is not None:
            three_gram_frequency.count_fragment(fragment, size)
            fragment = self.files.read_fragment(size)
        self.files.reset()

        print(three_gram_frequency.frequency)
        three_gram_frequency.get_frequent_gram_by_max_ratio(0.1)
        print("Three_Gram: {}".format(len(three_gram_frequency.frequency)))
        print("Selected: {}".format(three_gram_frequency.frequency))

    def test_max_gram(self):
        size = 4096
        gram = 1

        fragment = self.files.read_fragment(size)
        while fragment is not None:
            self.gram_frequency.count_fragment(fragment, size)
            fragment = self.files.read_fragment(size)
        self.files.reset()

        self.gram_filter.add_frequent_grams(self.gram_frequency.frequency)
        next_candidate = self.gram_frequency.generate_next_candidate()
        gram += 1
        testing_gram_frequency = GramFrequency(gram, next_candidate)
        previous_frequent_gram_len = 0

        while previous_frequent_gram_len != len(testing_gram_frequency.frequency):
            previous_frequent_gram_len = len(testing_gram_frequency.frequency)
            fragment = self.files.read_fragment(size)
            while fragment is not None:
                testing_gram_frequency.count_fragment(fragment, size)
                fragment = self.files.read_fragment(size)
            self.files.reset()

            testing_gram_frequency.get_frequent_gram_by_max_ratio(0.05)
            print("At gram {}, Selected {} Separators".format(gram, len(testing_gram_frequency.frequency)))
            print("\t{}".format(testing_gram_frequency.frequency))
            next_candidate = testing_gram_frequency.generate_next_candidate()
            gram += 1
            self.gram_filter.add_frequent_grams(testing_gram_frequency.frequency)
            testing_gram_frequency = GramFrequency(gram, next_candidate)

        top_grams = self.gram_filter.filter_top_n_grams(512)
        total_picked = 0
        print(top_grams)
        for k, v in top_grams.items():
            print("At Gram {}, picked {} separators.".format(k, len(v)))
            total_picked += len(v)
        print("Total: {} separators".format(total_picked))
