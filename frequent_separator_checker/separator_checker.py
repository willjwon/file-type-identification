import operator


class SeparatorChecker:
    def __init__(self):
        self.frequency_dict = None
        self.gram_size = 0
        self.total_fragments_count = 0

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
        self.total_fragments_count = 0

    def count_fragment(self, fragment):
        gram_set = set()
        for i in range(len(fragment) - self.gram_size + 1):
            gram_set.add(fragment[i:i + self.gram_size])
        for gram in gram_set:
            if gram in self.frequency_dict.keys():
                self.frequency_dict[gram] += 1
        self.total_fragments_count += 1

    @staticmethod
    def separators_into_set_form(frequent_separators_list):
        frequent_separators_set = set()
        for separator in frequent_separators_list:
            frequent_separators_set.add(separator[0])
        return frequent_separators_set

    def get_frequent_separators_relative(self, proportion):
        frequency_dict_sorted = sorted(self.frequency_dict.items(), key=operator.itemgetter(1), reverse=True)
        frequency_dict_sorted = list(map(lambda gram: (gram[0], gram[1] / self.total_fragments_count),
                                         frequency_dict_sorted))

        num_frequent_separators = int(len(frequency_dict_sorted) * proportion)
        return frequency_dict_sorted[:num_frequent_separators]

    def get_frequent_separators_absolute(self, top_n):
        frequency_dict_sorted = sorted(self.frequency_dict.items(), key=operator.itemgetter(1), reverse=True)
        frequency_dict_sorted = list(map(lambda gram: (gram[0], gram[1] / self.total_fragments_count),
                                         frequency_dict_sorted))

        if len(frequency_dict_sorted) <= top_n:
            return frequency_dict_sorted

        return frequency_dict_sorted[:top_n]

    def get_frequent_separators_frequency(self, threshold):
        frequency_dict_sorted = sorted(self.frequency_dict.items(), key=operator.itemgetter(1), reverse=True)
        frequency_dict_sorted = list(map(lambda gram: (gram[0], gram[1] / self.total_fragments_count),
                                         frequency_dict_sorted))

        i = 0
        for i in range(len(frequency_dict_sorted)):
            if frequency_dict_sorted[i][1] < threshold:
                break

        return frequency_dict_sorted[:i]

    @staticmethod
    def print_top_5(frequent_separators_list):
        print_string = []
        counts = min(5, len(frequent_separators_list))
        for i in range(counts):
            print_string.append("{}({:.2f}%)".format(frequent_separators_list[i][0],
                                                     frequent_separators_list[i][1] * 100))
        print("\tTop {}: {}".format(counts, ", ".join(print_string)))

    @staticmethod
    def print_bottom_5(frequent_separators_list):
        print_string = []
        counts = min(5, len(frequent_separators_list))
        for i in range(-1, (-1 * counts) - 1, -1):
            print_string.append("{}({:.2f}%)".format(frequent_separators_list[i][0],
                                                     frequent_separators_list[i][1] * 100))
        print("\tBottom {}: {}".format(counts, ", ".join(print_string)))

    @staticmethod
    def filter_by_frequency(frequent_separators_list, threshold):
        return list(filter(lambda gram: gram[1] >= threshold, frequent_separators_list))

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
