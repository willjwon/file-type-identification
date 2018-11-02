import pickle


class GramClassifier:
    def __init__(self, fragment_size, filtered_separators_file_path="./filtered_separators.pickle"):
        with open(filtered_separators_file_path, "rb") as file:
            self.separators = pickle.load(file)
        self.fragment_size = fragment_size
        self.gram_sizes = sorted(self.separators.keys(), reverse=True)

    def classify(self, fragment):
        for gram_size in self.gram_sizes:
            for i in range(0, self.fragment_size - gram_size + 1):
                gram = fragment[i:i + gram_size]
                if gram in self.separators[gram_size].keys():
                    return self.separators[gram_size][gram]

        return None
