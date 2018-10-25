import pickle


class SeparatorCounter:
    def __init__(self, separator_path):
        with open(separator_path, "rb") as file:
            separators = pickle.load(file)

        max_gram_len = max(separators.keys())
        self.index = 0

        self.grams_to_count = []
        self.separators_index = dict()

        for gram_len in range(1, max_gram_len + 1):
            if gram_len in separators:
                self.grams_to_count.append(gram_len)
                self.separators_index[gram_len] = dict()

                for separator in separators[gram_len]:
                    self.separators_index[gram_len][separator] = self.index
                    self.index += 1

    def count_frequency(self, fragment):
        frequency_result = [0 for _ in range(self.index)]
        for gram_len in self.grams_to_count:
            for index in range(len(fragment) - gram_len + 1):
                gram = fragment[index:index + gram_len]
                if gram in self.separators_index[gram_len]:
                    frequency_result[self.separators_index[gram_len][gram]] += 1
        return frequency_result
