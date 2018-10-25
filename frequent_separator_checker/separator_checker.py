import operator


class SeparatorChecker:
    def __init__(self):
        self.frequency_dict = None
        self.gram_size = 0
        self.total_grams = 0

    @staticmethod
    def obvious_separators():
        return set([bytes([i]) for i in range(256)]), 1

    @staticmethod
    def init_candidate():
        init_candidates = set()
        for i in range(256):
            for j in range(256):
                init_candidates.add(bytes([i, j]))
        return set(init_candidates), 2

    def set_candidate_separators(self, candidate_separators, gram_size):
        self.frequency_dict = dict()
        for separator in candidate_separators:
            self.frequency_dict[separator] = 0
        self.gram_size = gram_size
        self.total_grams = 0

    def count_fragment(self, fragment):
        for i in range(len(fragment) - self.gram_size + 1):
            gram = fragment[i:i + self.gram_size]
            if gram in self.frequency_dict.keys():
                self.frequency_dict[gram] += 1
            self.total_grams += 1

    def get_frequent_separators(self, proportion):
        frequent_separators = set()
        frequency_dict_sorted = sorted(self.frequency_dict.items(), key=operator.itemgetter(1), reverse=True)
        print("top-5 frequent: {} (of {})".format(frequency_dict_sorted[:5], self.total_grams))

        num_frequent_separators = int(len(frequency_dict_sorted) * proportion)
        for i in range(num_frequent_separators):
            frequent_separators.add(frequency_dict_sorted[i][0])

        return frequent_separators

    @staticmethod
    def make_candidate_separators(frequent_separators):
        candidate_separators = set()

        for separator in frequent_separators:
            for i in range(256):
                if bytes([i]) + separator[:-1] in frequent_separators:
                    candidate_separators.add(bytes([i]) + separator)
                if separator[1:] + bytes([i]) in frequent_separators:
                    candidate_separators.add(separator + bytes([i]))

        return candidate_separators
